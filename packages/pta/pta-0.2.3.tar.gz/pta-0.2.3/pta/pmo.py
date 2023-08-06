"""Construction and solution of Probabilistic Metabolic Optimization (PMO)
problems.
"""

from __future__ import annotations

import logging
import multiprocessing
import os
import pickle
import tempfile
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import cvxpy as cp
import numpy as np
import numpy.linalg as la
from scipy.stats.distributions import chi2

import cobra

from .constants import default_confidence_level, default_max_drg, default_min_drg
from .flux_space import FluxSpace
from .thermodynamic_space import ThermodynamicSpace, ThermodynamicSpaceBasis

logger = logging.getLogger(__name__)
_pmo_problem: PmoProblem


class PmoProblemPool:
    """Creation of a process pool for solving multiple PMO problems on the same model."""

    def __init__(self, num_processes: Optional[int], *argv):
        """Initialize a process pool for solving multiple PMO problems.

        Parameters
        ----------
        num_processes : Optional[int]
            Number of workers in the pool.
        argv
            Arguments to be passed to the constructor of :code:`PmoProblem`
        """
        # Pick the number of processes based on the number of available CPUs.
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()
            if num_processes is None:
                logger.warning(
                    "Cannot determine the number of processors available. Assuming 1."
                )
                num_processes = 1
        assert num_processes >= 1, "At least one process is needed."

        # Create a temporary file to copy the initialization arguments to the worker
        # processes. Helps performance on Windows.
        with tempfile.NamedTemporaryFile(delete=False) as args_file:
            pickle.dump(argv, open(args_file.name, "wb"))
            self._args_filename = args_file.name

        # Create the process pool, initializing a PmoProblem on each worker.
        self._pool = multiprocessing.Pool(
            num_processes,
            initializer=PmoProblemPool._init_process,
            initargs=[self._args_filename],
        )

    def map(
        self, fn: Callable[[PmoProblem, Any], Any], inputs: Iterable[Any]
    ) -> List[Any]:
        """Executes a function on each input element. This is the same as the regular
        :code:`map` function, except that it executes in parallel on the available
        workers.

        Parameters
        ----------
        fn : Callable[[PmoProblem, Any], Any]
            Function to be applied to each element.
        inputs : Iterable[Any]
            An iterable containing the input elements.

        Returns
        -------
        List[Any]
            A list containing the result of applying the function to each input element.
        """
        inputs_with_fn = [(fn, i) for i in inputs]
        return self._pool.map(PmoProblemPool._pool_task, inputs_with_fn)

    def close(self):
        """Waits for all jobs to be done and closes the pool."""
        self._pool.close()
        self._pool.join()
        if os.path.isfile(self._args_filename):
            os.remove(self._args_filename)

    @staticmethod
    def _init_process(args_filename):
        global _pmo_problem
        argv = pickle.load(open(args_filename, "rb"))
        _pmo_problem = PmoProblem(*argv)

    @staticmethod
    def _pool_task(v: Tuple[Callable[[PmoProblem, Any], Any], Any]):
        global _pmo_problem
        return v[0](_pmo_problem, v[1])


class PmoProblem(object):
    """Construction and solution of a Probabilistic Metabolic Optimization (PMO)
    problem.

    Parameters
    ----------
    network : Union[cobra.Model, FluxSpace]
        Cobra model or `FluxSpace` object describing the flux space of the metabolic
        network.
    thermodynamic_space : ThermodynamicSpace
        Description of the thermodynamic space of the metabolic network.
    thermodynamic_space_basis : ThermodynamicSpaceBasis, optional
        A basis for the thermodynamic space. If specified, `m` will be defined in this
        basis.
    objective : Callable[ [PmoProblem], cp.problems.objective.Objective], optional
        A function used to set the optimization objective. By default the probability of
        in thermodynamic space is maximized.
    confidence_level : float, optional
        Confidence level (in the range :math:`[0.0, 1.0[`) on the joint of the
        thermodynamic variables, by default 0.95.
    min_drg : float, optional
        Minimum magnitude for the reaction energy of each reaction, by default 1e-1.
    max_drg : float, optional
        Maximum magnitude for the reaction energy of each reaction, by default 1000.
    solver : Optional[str], optional
        Name of the solver to use, this can be any of the solvers supported by CVXPY, by
        default None.
    solver_options : dict, optional
        Dictionary specifying additional options for the solver.
    """

    _MAX_COEFFICIENT_RANGE = 5e8
    _DEFAULT_SOLVER_OPTIONS = {cp.GUROBI: {"IntFeasTol": 1e-9, "FeasibilityTol": 1e-9}}

    def __init__(
        self,
        network: Union[cobra.Model, FluxSpace],
        thermodynamic_space: ThermodynamicSpace,
        thermodynamic_space_basis: ThermodynamicSpaceBasis = None,
        objective: Callable[[PmoProblem], cp.problems.objective.Objective] = None,
        confidence_level: float = default_confidence_level,
        min_drg: float = default_min_drg,
        max_drg: float = default_max_drg,
        solver: Optional[str] = None,
        solver_options: dict = {},
    ):
        if isinstance(network, FluxSpace):
            self._F = network.copy()
        else:
            self._F = FluxSpace.from_cobrapy_model(network)
        self._T = thermodynamic_space
        if thermodynamic_space_basis is not None:
            self._B = thermodynamic_space_basis
        else:
            self._B = ThermodynamicSpaceBasis(thermodynamic_space)
        assert self.B.to_drg is not None, (
            "The thermodynamic space basis "
            "must have explicit reaction energies for PMO."
        )

        # Find mapping from reactions in F to reactions in T (T only covers a subset of
        # the reactions in F).
        self._rxn_idxs_F_to_T = [
            self.F.reaction_ids.index(id) for id in self.T.reaction_ids
        ]

        # Scale the flux space to make the problem numerically nicer.
        self._flux_scale = PmoProblem._scale_flux_space(self.F)

        # Store numerical settings.
        self._confidence_level = confidence_level
        self._min_drg = min_drg
        self._max_drg = max_drg

        # Initialize solver settings.
        self.solver = solver
        self.solver_options = solver_options

        # Flux, thermodynamic and direction variables.
        self._vs = cp.Variable((self.F.n_reactions, 1), "fluxes")
        self._m = cp.Variable((self.B.dimensionality, 1), "m")
        if np.all(
            np.logical_or(
                self.F.lb[self._rxn_idxs_F_to_T] >= 0,
                self.F.ub[self._rxn_idxs_F_to_T] <= 0,
            )
        ):
            # If flux bounds already fix all the directions we do not need integer
            # variables.
            self._fixed_directions = True
            self._d = cp.Variable((len(self.T.reaction_ids), 1), "directions")
        else:
            self._fixed_directions = False
            self._d = cp.Variable(
                (len(self.T.reaction_ids), 1), "directions", boolean=True
            )

        # If no objective is specified, maximize the probability of the
        # thermodynamic variables.
        self._objective = objective or (
            lambda p: cp.Minimize(
                cp.atoms.quad_form(p.m, np.identity(p.B.dimensionality))
            )
        )

        self._make_big_M_coefficients()
        self._make_constraints()
        self._rebuild_cvxpy_problem()

    @property
    def confidence_level(self):
        """Gets the confidence level on the thermodynamic space."""
        return self._confidence_level

    @property
    def min_drg(self) -> float:
        """Gets the minimum absolute value of DrG allowed in the model."""
        return self._min_drg

    @property
    def max_drg(self) -> float:
        """Gets the maximum absolute value of DrG in the model."""
        return self._max_drg

    @property
    def flux_scale(self) -> np.array:
        """Gets the vector of scaling factors for the scaled fluxes."""
        return self._flux_scale

    @property
    def objective(
        self,
    ) -> Optional[Callable[[PmoProblem], cp.problems.objective.Objective]]:
        """Gets the function that constructs the PMO objective."""
        return self._objective

    @objective.setter
    def objective(self, value: Callable[[PmoProblem], cp.problems.objective.Objective]):
        """Sets the function that constructs the PMO objective."""
        self._objective = value
        self._rebuild_cvxpy_problem()

    @property
    def vs(self) -> cp.Variable:
        """Gets the CVXPY variable representing scaled reaction fluxes."""
        return self._vs

    @property
    def m(self) -> cp.Variable:
        """Gets the CVXPY variable representing the thermodynamic space in the
        minimal basis."""
        return self._m

    @property
    def d(self) -> cp.Variable:
        """Gets the CVXPY variable representing reaction directions."""
        return self._d

    @property
    def v(self) -> np.array:
        """Gets the predicted reaction fluxes."""
        return self._vs.value / self.flux_scale

    @property
    def log_c(self) -> np.array:
        """Gets the predicted log-concentrations. Can be none if concentrations are not
        represented explicitely.
        """
        return self.B.to_log_conc(self.m.value)

    @property
    def drg0(self) -> np.array:
        """Gets the predicted standard reaction energies. Can be none if standard
        reaction energies are not represented explicitely.
        """
        return self.B.to_drg0(self.m.value)

    @property
    def drg(self) -> np.array:
        """Gets the predicted reaction energies. Can be none if reaction energies are
        not represented explicitely.
        """
        return self.B.to_drg(self.m.value)

    @property
    def solver(self) -> Optional[str]:
        """Gets the selected solver."""
        return self._solver

    @solver.setter
    def solver(self, value: Optional[str]):
        """Sets the selected solver."""
        self._solver = value

    @property
    def solver_options(self) -> Dict[str, Any]:
        """Gets the solver options."""
        return self._solver_options

    @solver_options.setter
    def solver_options(self, value: Dict[str, Any]):
        """Sets the solver options."""
        self._solver_options = value

    @property
    def F(self) -> FluxSpace:
        """Gets the flux space associated with the PMO problem."""
        return self._F

    @property
    def T(self) -> ThermodynamicSpace:
        """Gets the thermodynamic space associated with the PMO problem."""
        return self._T

    @property
    def B(self) -> ThermodynamicSpaceBasis:
        """Gets the thermodynamic space basis associated with the PMO problem."""
        return self._B

    @property
    def flux_lb_constraint(self) -> cp.constraints.constraint.Constraint:
        """Gets the lower bound constraint for fluxes."""
        return (self._flux_lb_constraint,)

    @property
    def flux_ub_constraint(self) -> cp.constraints.constraint.Constraint:
        """Gets the upper bound constraint for fluxes."""
        return (self._flux_ub_constraint,)

    @property
    def steady_state_constraint(self) -> cp.constraints.constraint.Constraint:
        """Gets the steady state constraint."""
        return (self._steady_state_constraint,)

    @property
    def confidence_constraint(self) -> cp.constraints.constraint.Constraint:
        """Gets the constraint for the selected confidence level."""
        return self._m_constraint

    @property
    def sign_constraints(self) -> cp.constraints.constraint.Constraint:
        """Gets the reaction direction constraints. The constraints at indices
        0 and 1 are constraints on the reaction energies, while 2 and 3 are
        constraints on the fluxes."""
        return self._sign_constraints

    def solve(self, verbose=False) -> str:
        """Solves the PMO problem. The result of the optimization is stored inside the
        class.

        Parameters
        ----------
        verbose : bool, optional
            True is the solver log should be printed to the console, false otherwise. By
            default False.

        Returns
        -------
        str
            The CVXPY result of the optimization.
        """
        # Get the default solver-specific options and add the user options.
        options = self._DEFAULT_SOLVER_OPTIONS.get(self.solver, {})
        options = {**options, **self.solver_options}

        # Solve the optimization problem.
        self._problem.solve(solver=self.solver, verbose=verbose, **options)
        return self._problem.status

    def rebuild_for_directions(self, directions: np.array) -> PmoProblem:
        """Construct a copy of this PMO problem constrained to the given reaction
        directions.

        Parameters
        ----------
        directions : np.array
            Vector containing the directions (0: backward, 1: forward) of the reactions
            in T.

        Returns
        -------
        PmoProblem
            A copy of this problem, constrained to the given directions.
        """
        reaction_idxs = [self.F.reaction_ids.index(id) for id in self.T.reaction_ids]

        new_lb = self.F.lb[
            reaction_idxs,
        ]
        new_ub = self.F.ub[
            reaction_idxs,
        ]
        new_lb[directions > 0.5,] = np.maximum(
            new_lb[
                directions > 0.5,
            ],
            0,
        )
        new_ub[directions < 0.5,] = np.minimum(
            new_ub[
                directions < 0.5,
            ],
            0,
        )

        constrained_F = self.F.copy()
        constrained_F.lb[reaction_idxs] = new_lb
        constrained_F.ub[reaction_idxs] = new_ub

        return PmoProblem(
            constrained_F,
            self.T,
            self.B,
            self.objective,
            self.confidence_level,
            self.min_drg,
            self.max_drg,
            self.solver,
            self.solver_options,
        )

    @staticmethod
    def _scale_flux_space(F: FluxSpace) -> np.array:
        """Rescale the flux space in order to reduce the range of coefficients in S, lb
        and ub.
        """
        reference = np.maximum(np.max(np.abs(F.lb)), np.max(np.abs(F.ub)))
        max_absolute_flux = np.maximum(np.abs(F.lb), np.abs(F.ub))

        # Limit the maximum scaling factor, otherwise we may obtain bad range of
        # coefficients in S. This is a heuristic, and we should pick the value
        # with a better method.
        col_scale = np.minimum(reference / max_absolute_flux, 100)
        F.lb = F.lb * col_scale
        F.ub = F.ub * col_scale
        F.S = F.S @ np.diag(1 / col_scale.ravel())

        row_scale = np.max(np.abs(F.S), axis=1)
        if any(row_scale == 0):
            zero_row_mets = [
                F.metabolite_ids[i] for i in np.where(row_scale == 0)[0].tolist()
            ]
            raise Exception(
                "One row of the stoichiometric matrix is zero, "
                "Please make sure that the model does not contain orphan "
                "metabolites. The metabolites corresponding to zero rows are "
                f"{','.join(zero_row_mets)}."
            )
        F.S = np.diag(reference / row_scale) @ F.S

        return col_scale

    def _make_big_M_coefficients(self):
        """Creates the Big-M coefficients for flux and reaction energies based. We must
        pick those such that they allow a reasonably large range of coefficients but
        without creating numerical challenges for the solver.
        """
        ones = np.ones((len(self.T.reaction_ids), 1))

        self._big_M_r = self.max_drg * ones
        self._big_M_f = (
            1.01
            * np.maximum(np.abs(self.F.lb), np.abs(self.F.ub))[self._rxn_idxs_F_to_T, :]
        )
        self._epsilon_r = self.min_drg * ones
        self._epsilon_f = np.maximum(
            self._big_M_f / self._MAX_COEFFICIENT_RANGE,
            np.max(self._big_M_f) / self._MAX_COEFFICIENT_RANGE,
        )

        all_bounds = np.abs(np.vstack((self.F.lb, self.F.ub)))
        min_flux_bound = np.min(all_bounds[np.nonzero(all_bounds)])

        if min_flux_bound < np.max(self._big_M_f) / self._MAX_COEFFICIENT_RANGE * 10:
            logger.warning(
                "The coefficient range of the flux bounds "
                f"({np.max(self._big_M_f) / min_flux_bound}) is close or "
                f"larger than {self.MAX_COEFFICIENT_RANGE} "
                "and may lead to numerical errors. It is recommended to "
                "simplify the model to reduce the range."
            )

    def _make_constraints(self):
        """Create the CVXPY constraints of the problem."""
        # Flux constraints.
        self._flux_lb_constraint = self.vs >= self.F.lb
        self._flux_ub_constraint = self.vs <= self.F.ub
        self._steady_state_constraint = self.F.S @ self.vs == np.zeros(
            (self.F.n_metabolites, 1)
        )

        # Thermodynamic space constraints.
        CI_square = chi2.ppf(self._confidence_level, self.B.dimensionality)
        self._m_constraint = (
            cp.atoms.quad_form(self.m, np.identity(self.B.dimensionality)) <= CI_square
        )

        # Mappings between fluxes and constrained fluxes.
        v_to_v_con = np.identity(self.F.n_reactions)[self._rxn_idxs_F_to_T, :]

        # Sign relations.
        assert self.B.to_drg_transform is not None
        (T, s) = self.B.to_drg_transform

        self._sign_constraints = [
            cp.multiply(self._big_M_r, self.d) + T @ self.m + s
            <= self._big_M_r - self._epsilon_r,
            cp.multiply(self._big_M_r, self.d) + T @ self.m + s >= self._epsilon_r,
            cp.multiply(self._big_M_f, self.d) - v_to_v_con @ self.vs
            <= self._big_M_f - self._epsilon_f,
            cp.multiply(self._big_M_f, self.d) - v_to_v_con @ self.vs
            >= self._epsilon_f,
        ]

        if self._fixed_directions:
            directions = np.zeros((len(self.T.reaction_ids), 1))
            directions[
                self.F.lb[
                    self._rxn_idxs_F_to_T,
                ]
                >= 0
            ] = 1
            self._sign_constraints += [self.d == directions]

        # Assemble in a single set of constraints.
        self._constraints = [
            self._flux_lb_constraint,
            self._flux_ub_constraint,
            self._steady_state_constraint,
            self._m_constraint,
        ] + self._sign_constraints

    def _rebuild_cvxpy_problem(self):
        """Rebuild the CVXPY representation of the PMO problem."""
        self._problem = cp.Problem(self.objective(self), self._constraints)
