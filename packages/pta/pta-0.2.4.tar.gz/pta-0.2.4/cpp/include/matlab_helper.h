// Copyright (c) 2020 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef HYPERFLUX_MATLAB_HELPER_H
#define HYPERFLUX_MATLAB_HELPER_H

#include <Eigen/Dense>
#include <Eigen/StdVector>
#include <unordered_map>
#include <vector>

#ifdef MEX_BUILD
#include <mex.hpp>
#include <mexAdapter.hpp>
#else
#include <MatlabDataArray.hpp>
#include <MatlabEngine.hpp>
#endif

#include <settings.h>

#include "eigen-hash.h"
#include "settings/free_energy_sampling_settings.h"
#include "settings/uniform_flux_sampling_settings.h"

namespace hyperflux {
namespace matlab_helper {

template <typename Scalar = double>
samply::Matrix<Scalar> matlab_matrix_to_eigen(
    matlab::data::TypedArray<Scalar>&& matlab_matrix)
{
    // The construction of a matrix from a pointer triggers a copy constructor,
    // thus the pointer is safely released when it goes out of scope.
    const auto matlab_matrix_ptr = matlab_matrix.release();
    return Eigen::Map<samply::Matrix<Scalar>>(matlab_matrix_ptr.get(),
                                              matlab_matrix.getDimensions()[0],
                                              matlab_matrix.getDimensions()[1]);
}

template <typename Matrix, typename Allocator>
matlab::data::TypedArray<typename Matrix::Scalar> vector_of_eigen_matrices_to_matlab(
    const std::vector<Matrix, Allocator>& data)
{
    // Allocate space for the MATLAB array.
    assert(!data.empty());
    matlab::data::ArrayFactory factory;
    auto samples = factory.createArray<typename Matrix::Scalar>(
        {static_cast<size_t>(data[0].rows()), static_cast<size_t>(data[0].cols()),
         data.size()});

    // Copy the data.
    for (size_t matrix_idx = 0u; matrix_idx < data.size(); ++matrix_idx) {
        memcpy(&*(samples.begin() + data[0].rows() * data[0].cols() * matrix_idx),
               data[matrix_idx].template cast<typename Matrix::Scalar>().data(),
               data[matrix_idx].size() * sizeof(typename Matrix::Scalar));
    }

    return samples;
}

template <typename T>
matlab::data::TypedArray<T> vector_of_vectors_to_matlab(
    const std::vector<std::vector<T>>& data)
{
    // Allocate space for the MATLAB array.
    assert(!data.empty());
    matlab::data::ArrayFactory factory;
    auto result = factory.createArray<T>({data[0].size(), data.size()});

    // Copy the data.
    for (size_t vector_idx = 0u; vector_idx < data.size(); ++vector_idx) {
        memcpy(&*(result.begin() + data[0].size() * vector_idx),
               data[vector_idx].data(), data[vector_idx].size() * sizeof(T));
    }

    return result;
}

template <typename Matrix>
matlab::data::TypedArray<typename Matrix::Scalar> eigen_matrix_to_matlab(
    const Matrix& data)
{
    // Allocate space for the MATLAB array.
    matlab::data::ArrayFactory factory;
    auto samples = factory.createArray<typename Matrix::Scalar>(
        {static_cast<size_t>(data.rows()), static_cast<size_t>(data.cols())});

    // Copy the data.
    memcpy(&*(samples.begin()),
           data.template cast<typename Matrix::Scalar>().eval().data(),
           data.size() * sizeof(typename Matrix::Scalar));
    return samples;
}

template <typename Variable>
Variable get_scalar_field(matlab::data::StructArray& matlab_struct,
                          const std::string& field_name)
{
    try {
        matlab::data::TypedArrayRef<double> field = matlab_struct[0][field_name];
        return Variable(field[0]);
    } catch (...) {
        throw std::runtime_error(std::string("Value for setting '") + field_name +
                                 std::string("' must be specified"));
    }
}

template <typename Variable>
Variable get_scalar_field_or_default(matlab::data::StructArray& matlab_struct,
                                     const std::string& field_name,
                                     const Variable& default_value)
{
    try {
        matlab::data::TypedArrayRef<double> field = matlab_struct[0][field_name];
        return Variable(field[0]);
    } catch (...) {
        return default_value;
    }
}

std::string get_string_field_or_default(matlab::data::StructArray& matlab_struct,
                                        const std::string& field_name,
                                        const std::string& default_value)
{
    try {
        matlab::data::TypedArrayRef<matlab::data::MATLABString> field =
            matlab_struct[0][field_name];
        return matlab::engine::convertUTF16StringToUTF8String(field[0]);
    } catch (std::exception&) {
        return default_value;
    }
}

samply::Settings create_samply_settings(matlab::data::StructArray& matlab_struct)
{
    samply::Settings settings;

    settings.worker_id =
        get_scalar_field<size_t>(matlab_struct, std::string("workerId"));

    settings.num_steps = get_scalar_field<size_t>(matlab_struct, std::string("nSteps"));
    settings.steps_thinning = get_scalar_field_or_default<size_t>(
        matlab_struct, std::string("stepsThinning"), 1u);
    settings.num_skipped_steps = get_scalar_field_or_default<size_t>(
        matlab_struct, std::string("nWarmupSteps"), 0u);

    settings.console_logging_interval_ms =
        get_scalar_field_or_default<std::chrono::milliseconds>(
            matlab_struct, std::string("consoleLoggingIntervalMs"),
            std::chrono::milliseconds(1'000));
    settings.log_directory = get_string_field_or_default(
        matlab_struct, std::string("logsDir"), std::string(""));

    return settings;
}

UniformFluxSamplingSettings create_uniform_flux_sampling_settings(
    matlab::data::StructArray& matlab_struct)
{
    return UniformFluxSamplingSettings(create_samply_settings(matlab_struct));
}

FreeEnergySamplingSettings create_free_energy_sampling_settings(
    matlab::data::StructArray& matlab_struct)
{
    FreeEnergySamplingSettings settings(create_samply_settings(matlab_struct));

    settings.truncation_multiplier =
        get_scalar_field<double>(matlab_struct, std::string("truncationMultiplier"));
    settings.feasibility_cache_size = get_scalar_field_or_default<size_t>(
        matlab_struct, std::string("feasibilityCacheSize"), 10'000u);

    settings.drg_epsilon = get_scalar_field_or_default<double>(
        matlab_struct, std::string("drgEpsilon"), 1e-3);
    settings.flux_epsilon = get_scalar_field_or_default<double>(
        matlab_struct, std::string("fluxEpsilon"), 1e-4);
    settings.min_rel_region_length = get_scalar_field_or_default<double>(
        matlab_struct, std::string("minRelativeRegionLength"), 1e-6);

    settings.steps_thinning_directions = get_scalar_field_or_default<size_t>(
        matlab_struct, std::string("stepsThinningDirections"), 1u);

    return settings;
}

template <typename Matrix1, typename Matrix2, typename Matrix3>
matlab::data::StructArray create_sampling_result_object(
    const Matrix1& initial_states,
    const Matrix2& final_states,
    const std::vector<Matrix3, Eigen::aligned_allocator<Matrix3>>& chains)
{
    matlab::data::ArrayFactory factory;
    matlab::data::StructArray result =
        factory.createStructArray({1, 1}, {"initialStates", "finalStates", "chains"});

    result[0]["initialStates"] =
        eigen_matrix_to_matlab(initial_states.template cast<double>());
    result[0]["finalStates"] =
        eigen_matrix_to_matlab(final_states.template cast<double>());
    result[0]["chains"] = vector_of_eigen_matrices_to_matlab(chains);
    return result;
}

template <typename Matrix1, typename Matrix2, typename Matrix3, typename Hasher>
matlab::data::StructArray create_sampling_result_object(
    const Matrix1& initial_states,
    const Matrix2& final_states,
    const std::vector<Matrix3, Eigen::aligned_allocator<Matrix3>>& chains,
    const std::unordered_map<std::vector<uint8_t>, uint32_t, Hasher>& directions_counts)
{
    matlab::data::ArrayFactory factory;
    matlab::data::StructArray result = factory.createStructArray(
        {1, 1}, {"initialStates", "finalStates", "chains", "directions", "counts"});

    samply::Vector<uint32_t> counts(directions_counts.size());
    std::vector<std::vector<uint8_t>> directions(directions_counts.size());

    size_t direction_idx = 0u;
    for (const auto& it : directions_counts) {
        directions[direction_idx] = it.first;
        counts[direction_idx] = it.second;
        direction_idx++;
    }

    result[0]["initialStates"] =
        eigen_matrix_to_matlab(initial_states.template cast<double>());
    result[0]["finalStates"] =
        eigen_matrix_to_matlab(final_states.template cast<double>());
    result[0]["chains"] = vector_of_eigen_matrices_to_matlab(chains);
    result[0]["directions"] = vector_of_vectors_to_matlab(directions);
    result[0]["counts"] = eigen_matrix_to_matlab(counts);

    return result;
}

/**
 * @brief Notifies the MATLAB execution that an error occurred and the execution
 * of the MEX function must be terminated. This throws an error in the MATLAB
 * session with the given error message.
 *
 * @param error_message String containing the error message to display in the
 * MATLAB console.
 * @param matlab_engine Pointer to the current MATLAB engine.
 */
void throw_error(const std::string& error_message,
                 std::shared_ptr<matlab::engine::MATLABEngine>&& matlab_engine)
{
    matlab::data::ArrayFactory factory;
    matlab_engine->feval(
        matlab::engine::convertUTF8StringToUTF16String("error"), 0,
        std::vector<matlab::data::Array>({factory.createScalar(error_message)}));
}

}  // namespace matlab_helper
}  // namespace hyperflux

#endif
