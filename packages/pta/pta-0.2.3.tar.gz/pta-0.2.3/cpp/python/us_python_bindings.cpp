// Copyright (c) 2021 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#include <chord_samplers/uniform_pdf_sampler.h>
#include <coordinate_hit_and_run_sampler.h>
#include <descriptors/polytope.h>
#include <loggers/console_progress_logger.h>
#include <loggers/eigen_state_logger.h>
#include <loggers/multi_logger.h>
#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>

#include "python_helper.h"
#include "settings/uniform_flux_sampling_settings.h"

using namespace hyperflux;
using namespace samply;

namespace py = pybind11;

typedef double Scalar;

template <typename ChainState, typename DurationFormat>
using UniformLoggers =
    MultiLogger<ChainState, DurationFormat, EigenStateLogger, ConsoleProgressLogger>;
using UniformSampler =
    CoordinateHitAndRunSampler<Scalar, Polytope, UniformPdfSampler, UniformLoggers>;

py::array_t<double> sample_flux_space_uniform(
    const py::EigenDRef<Eigen::MatrixXd> G,
    const py::EigenDRef<Eigen::MatrixXd> h,
    const py::EigenDRef<Eigen::MatrixXd> from_Fd_T,
    const py::EigenDRef<Eigen::MatrixXd> initial_state,
    const UniformFluxSamplingSettings& settings)
{
    // Redirect stdout to the Python output.
    py::scoped_ostream_redirect stream(std::cout,
                                       py::module_::import("sys").attr("stdout"));

    AffineTransform<double> from_Fd(from_Fd_T, Vector<double>::Zero(G.cols()));

    Polytope<Scalar> descriptor(G, h, from_Fd);
    UniformPdfSampler<Scalar> chord_sampler(G.cols());

    const size_t preallocated_states =
        (settings.num_steps - settings.num_skipped_steps) / settings.steps_thinning;
    UniformSampler::LoggerType loggers(
        UniformSampler::LoggerType::Logger<0>(
            settings.worker_id, settings.steps_thinning, settings.num_skipped_steps,
            preallocated_states),
        UniformSampler::LoggerType::Logger<1>(settings.worker_id,
                                              settings.console_logging_interval_ms));

    UniformSampler sampler(descriptor, chord_sampler, loggers);
    sampler.set_state(initial_state);
    sampler.simulate(settings.num_steps);

    // Copy back resulting samples.
    return python_helper::vector_of_eigen_matrices_to_numpy_3d_array(
        sampler.get_logger().get<0>().get_states());
}

void add_us_python_bindings(py::module& m)
{
    py::class_<UniformFluxSamplingSettings, Settings>(m, "UniformSamplerSettings")
        .def(py::init<>());

    m.def("sample_flux_space_uniform", &sample_flux_space_uniform);
}