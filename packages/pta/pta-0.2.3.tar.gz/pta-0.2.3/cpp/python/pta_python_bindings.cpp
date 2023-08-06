// Copyright (c) 2021 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#include <chord_samplers/mvn_pdf_sampler.h>
#include <hit_and_run_sampler.h>
#include <loggers/eigen_state_logger.h>
#include <loggers/multi_logger.h>
#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>

#include "loggers/directions_logger.h"
#include "python_helper.h"
#include "settings/free_energy_sampling_settings.h"
#include "steady_state_free_energies_descriptor.h"

using namespace hyperflux;
using namespace samply;

namespace py = pybind11;

typedef double Scalar;

template <typename ChainState, typename DurationFormat>
using Loggers =
    MultiLogger<ChainState, DurationFormat, EigenStateLogger, DirectionsLogger>;
using Sampler =
    HitAndRunSampler<Scalar, SteadyStateFreeEnergiesDescriptor, MvnPdfSampler, Loggers>;

struct TFSResult {
    py::array_t<double> chains;
    py::array_t<uint8_t> directions;
    py::array_t<uint32_t> direction_counts;
};

TFSResult sample_free_energies(
    const py::EigenDRef<Eigen::MatrixXd> E,
    const py::EigenDRef<Eigen::MatrixXd> f,
    const py::EigenDRef<Eigen::MatrixXd> S,
    const py::EigenDRef<Eigen::MatrixXd> lb,
    const py::EigenDRef<Eigen::MatrixXd> ub,
    const py::EigenDRef<Eigen::Matrix<uint32_t, -1, 1>> constrained_rxns_ids,
    const py::EigenDRef<Eigen::MatrixXd> initial_state,
    const FreeEnergySamplingSettings& settings,
    const py::EigenDRef<Eigen::MatrixXd> vars_to_drg_T,
    const py::EigenDRef<Eigen::MatrixXd> vars_to_drg_shift,
    const py::EigenDRef<Eigen::MatrixXd> direction_transform_T)
{
    // Redirect stdout to the Python output.
    py::scoped_ostream_redirect stream(std::cout,
                                       py::module_::import("sys").attr("stdout"));

    AffineTransform<double> vars_to_drg(vars_to_drg_T, vars_to_drg_shift);
    AffineTransform<double> directions_transform(
        direction_transform_T, Vector<double>::Zero(direction_transform_T.rows()));

    Ellipsoid<Scalar> vars_constraints(E * settings.truncation_multiplier, f);
    FluxConstraints flux_constraints{S, lb, ub};
    ThermodynamicConstraints thermo_constraints{
        constrained_rxns_ids.cast<Eigen::Index>(), vars_to_drg};

    SteadyStateFreeEnergiesDescriptor<Scalar> descriptor(
        vars_constraints, flux_constraints, thermo_constraints, directions_transform,
        settings);
    MvnPdfSampler<Scalar> chord_sampler(AffineTransform<double>(E, f));

    const size_t preallocated_states =
        (settings.num_steps - settings.num_skipped_steps) / settings.steps_thinning;

    Sampler::LoggerType loggers(
        Sampler::LoggerType::Logger<0>(settings.worker_id, settings.steps_thinning,
                                       settings.num_skipped_steps, preallocated_states),
        Sampler::LoggerType::Logger<1>(settings.worker_id,
                                       settings.steps_thinning_directions,
                                       settings.num_skipped_steps));

    Sampler sampler(descriptor, chord_sampler, loggers);
    sampler.get_logger().get<1>().set_descriptor(sampler.get_space_descriptor());
    sampler.get_logger().get<1>().set_sampler(sampler.get_chord_sampler());
    sampler.set_state(initial_state);
    sampler.simulate(settings.num_steps);

    // Copy back resulting samples.
    TFSResult result;
    result.chains = python_helper::vector_of_eigen_matrices_to_numpy_3d_array(
        sampler.get_logger().get<0>().get_states()),
    std::tie(result.directions, result.direction_counts) =
        python_helper::direction_counts_to_python(
            sampler.get_logger().get<1>().get_directions_counts());
    return result;
}

void add_pta_python_bindings(py::module& m)
{
    py::class_<FreeEnergySamplingSettings, Settings>(m, "FreeEnergySamplerSettings")
        .def(py::init<>())
        .def_readwrite("truncation_multiplier",
                       &FreeEnergySamplingSettings::truncation_multiplier)
        .def_readwrite("feasibility_cache_size",
                       &FreeEnergySamplingSettings::feasibility_cache_size)
        .def_readwrite("drg_epsilon", &FreeEnergySamplingSettings::drg_epsilon)
        .def_readwrite("flux_epsilon", &FreeEnergySamplingSettings::flux_epsilon)
        .def_readwrite("min_rel_region_length",
                       &FreeEnergySamplingSettings::min_rel_region_length)
        .def_readwrite("steps_thinning_directions",
                       &FreeEnergySamplingSettings::steps_thinning_directions);

    py::class_<TFSResult>(m, "TFSResult")
        .def(py::init<>())
        .def_readwrite("chains", &TFSResult::chains)
        .def_readwrite("directions", &TFSResult::directions)
        .def_readwrite("direction_counts", &TFSResult::direction_counts);

    m.def("sample_free_energies", &sample_free_energies);
}