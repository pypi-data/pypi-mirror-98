// Copyright (c) 2020 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_MVN_PDF_SAMPLER_H
#define SAMPLY_MVN_PDF_SAMPLER_H

#include "axis_rays_packet.h"
#include "helpers/sampling_helper.h"
#include "intersections_packet_with_weights.h"
#include "rays_packet.h"
#include "reparametrized_object.h"

namespace samply {

/**
 * @brief Class for sampling along a ray crossing a Multivariate Normal
 * Distribution (MVN).
 *
 * @tparam ScalarType Scalar type for sampling operations.
 */
template <typename ScalarType>
class MvnPdfSampler {
public:
    /**
     * @brief Scalar type used for sampling operations.
     */
    typedef ScalarType Scalar;

    /**
     * @brief Construct a new instance of the MvnPdfSampler class with zero mean
     * and identity convariance.
     *
     * @param num_variables Number of variables in the MVN.
     */
    MvnPdfSampler(size_t num_variables)
        : is_standard_(true),
          samples_transform_(Matrix<double>::Identity(num_variables, num_variables),
                             Vector<double>::Zero(num_variables))
    {
    }

    /**
     * @brief Construct a new instance of the MvnPdfSampler class.
     *
     * @param samples_transform Transform from the unit MVN to desired MVN.
     */
    MvnPdfSampler(const AffineTransform<double>& samples_transform)
        : samples_transform_(samples_transform), is_standard_(false)
    {
    }

    /**
     * @brief Samples a point along each of the specified rays.
     *
     * @param rays Rays along which points must be sampled.
     * @param intersections Intersection points defining the sections on each
     * ray from which the points can be sampled.
     * @param sampling_helper Helper object for generating random numbers.
     * @return Vector containing the sampled points on each ray.
     */
    Vector<Scalar> sample1d(const RaysPacket<Scalar>& rays,
                            const IntersectionsPacket<Scalar>& intersections,
                            SamplingHelper& sampling_helper);

    /**
     * @brief Samples a point along each of the specified rays.
     *
     * @param rays Rays along which points must be sampled.
     * @param intersections Intersection points defining the sections on each
     * ray from which the points can be sampled.
     * @param sampling_helper Helper object for generating random numbers.
     * @return Vector containing the sampled points on each ray.
     */
    Vector<Scalar> sample1d(const RaysPacket<Scalar>& rays,
                            const IntersectionsPacketWithWeights<Scalar>& intersections,
                            SamplingHelper& sampling_helper);

    /**
     * @brief Samples a point along each of the specified rays.
     *
     * @param rays Rays along which points must be sampled.
     * @param intersections Intersection points defining the sections on each
     * ray from which the points can be sampled.
     * @param sampling_helper Helper object for generating random numbers.
     * @return Vector containing the sampled points on each ray.
     */
    Vector<Scalar> sample1d(const AxisRaysPacket<Scalar>& rays,
                            const IntersectionsPacket<Scalar>& intersections,
                            SamplingHelper& sampling_helper);

    /**
     * @brief Get a reparametrized version of this object such that sampling
     * operations are easy.
     *
     * @return Reparametrized version of this object, containing the
     * transforms mapping between the two parametrizations.
     */
    ReparametrizedObject<MvnPdfSampler<Scalar>> get_optimally_reparametrized_sampler()
        const;

    const Vector<Scalar>& get_last_sampled_ts() const
    {
        return last_sampled_ts_;
    }

protected:
    /**
     * @brief Reparametrize the rays such that their intersection with the MVN
     * is a standard normal distribution (i.e. with mean = 0 and std = 1).
     */
    template <template <typename> typename IntersectionsPacketType>
    std::tuple<RaysPacket<Scalar>,
               IntersectionsPacketType<Scalar>,
               Vector<Scalar>,
               Vector<ScalarType>>
    reparametrize_rays_(const RaysPacket<Scalar>& rays,
                        const IntersectionsPacketType<Scalar>& intersections);

    AffineTransform<double> samples_transform_;

    bool is_standard_;

    Vector<Scalar> last_sampled_ts_;
};

//==============================================================================
//	MvnPdfSampler public methods implementation.
//==============================================================================

template <typename ScalarType>
inline Vector<ScalarType> MvnPdfSampler<ScalarType>::sample1d(
    const RaysPacket<Scalar>& in_rays,
    const IntersectionsPacket<Scalar>& in_intersections,
    SamplingHelper& sampling_helper)
{
    if (!is_standard_)
        throw std::runtime_error("MvnPdfSampler must be reparametrized");

    RaysPacket<Scalar> rays;
    IntersectionsPacket<Scalar> intersections(in_intersections);
    Vector<Scalar> ray_t_scale_factors;
    Vector<Scalar> ray_t_offsets;
    std::tie(rays, intersections, ray_t_scale_factors, ray_t_offsets) =
        reparametrize_rays_(in_rays, in_intersections);

    Vector<Scalar> t;
    if (intersections.one_ray_one_intersection) {
        t = Vector<Scalar>(ray_t_offsets.size());
        for (Eigen::Index i = 0; i < ray_t_offsets.size(); i++) {
            if (in_rays.directions.col(i).isZero()) {
                t(i) = sampling_helper.get_random_uniform_scalar(
                    in_intersections.segment_starts(i),
                    in_intersections.segment_ends(i));
            } else {
                t(i) = sampling_helper.get_random_truncated_normal(
                    Scalar(0), Scalar(1), intersections.segment_starts(i),
                    intersections.segment_ends(i));
            }
        }
    } else {
        // Otherwise we need to first sample a segment from all the segments
        // belonging to each ray and then sample a point from it.
        auto sample_on_segments_union = [&](const auto& segment_starts,
                                            const auto& segment_ends,
                                            const Eigen::Index ray_index) -> Scalar {
            // Choose the segment from which the next point must be sampled.
            Vector<Scalar> segment_weights =
                sampling_helper.get_normal_cdf_interval<Scalar>(segment_starts,
                                                                segment_ends);

            if (!(segment_weights.array() > 0).any()) {
                return -ray_t_offsets(ray_index);
            } else {
                const Eigen::Index sampled_segment_idx =
                    sampling_helper.sample_index_with_weights(segment_weights);

                // Sample the next point uniformly on the chosen segment.
                return sampling_helper.get_random_truncated_normal(
                    Scalar(0.0), Scalar(1.0), segment_starts(sampled_segment_idx),
                    segment_ends(sampled_segment_idx));
            }
        };

        // For each ray, identify the segments belonging to it and sample from
        // union.
        t = intersections.for_each_ray(sample_on_segments_union);
    }

    Vector<Scalar> sampled_ts = (t + ray_t_offsets).cwiseQuotient(ray_t_scale_factors);
    last_sampled_ts_ = sampled_ts;
    return sampled_ts;
}

template <typename ScalarType>
inline Vector<ScalarType> MvnPdfSampler<ScalarType>::sample1d(
    const RaysPacket<Scalar>& in_rays,
    const IntersectionsPacketWithWeights<Scalar>& in_intersections,
    SamplingHelper& sampling_helper)
{
    if (!is_standard_)
        throw std::runtime_error("MvnPdfSampler must be reparametrized");

    RaysPacket<Scalar> rays;
    IntersectionsPacketWithWeights<Scalar> intersections(in_intersections);
    Vector<Scalar> ray_t_scale_factors;
    Vector<Scalar> ray_t_offsets;
    std::tie(rays, intersections, ray_t_scale_factors, ray_t_offsets) =
        reparametrize_rays_(in_rays, in_intersections);

    Vector<Scalar> t;
    if (intersections.one_ray_one_intersection) {
        t = Vector<Scalar>(ray_t_offsets.size());
        for (Eigen::Index i = 0; i < ray_t_offsets.size(); i++) {
            if (in_rays.directions.col(i).isZero()) {
                t(i) = sampling_helper.get_random_uniform_scalar(
                    in_intersections.segment_starts(i),
                    in_intersections.segment_ends(i));
            } else {
                t(i) = sampling_helper.get_random_truncated_normal(
                    Scalar(0), Scalar(1), intersections.segment_starts(i),
                    intersections.segment_ends(i));
            }
        }
    } else {
        // Otherwise we need to first sample a segment from all the segments
        // belonging to each ray and then sample a point from it.
        auto sample_on_segments_union =
            [&](const auto& segment_starts, const auto& segment_ends,
                const auto& weights, const Eigen::Index ray_index) -> Scalar {
            // Choose the segment from which the next point must be sampled.
            Vector<Scalar> segment_weights =
                weights.cwiseProduct(sampling_helper.get_normal_cdf_interval<Scalar>(
                    segment_starts, segment_ends));

            if (!(segment_weights.array() > 0).any()) {
                return -ray_t_offsets(ray_index);
            } else {
                Eigen::Index sampled_segment_idx =
                    sampling_helper.sample_index_with_weights(segment_weights);

                // Sample the next point uniformly on the chosen segment.
                return sampling_helper.get_random_truncated_normal(
                    Scalar(0.0), Scalar(1.0), segment_starts(sampled_segment_idx),
                    segment_ends(sampled_segment_idx));
            }
        };

        // For each ray, identify the segments belonging to it and sample from
        // union.
        t = intersections.for_each_ray(sample_on_segments_union);
    }
    return (t + ray_t_offsets).cwiseQuotient(ray_t_scale_factors);
}

template <typename ScalarType>
inline Vector<ScalarType> MvnPdfSampler<ScalarType>::sample1d(
    const AxisRaysPacket<Scalar>& in_rays,
    const IntersectionsPacket<Scalar>& in_intersections,
    SamplingHelper& sampling_helper)
{
    return sample1d(AffineTransform<Scalar>::identity(in_rays.origins.rows()) * in_rays,
                    in_intersections, sampling_helper);
}

template <typename ScalarType>
ReparametrizedObject<MvnPdfSampler<ScalarType>>
MvnPdfSampler<ScalarType>::get_optimally_reparametrized_sampler() const
{
    return ReparametrizedObject<MvnPdfSampler<Scalar>>(
        MvnPdfSampler<Scalar>(samples_transform_.get_shift().size()),
        samples_transform_, samples_transform_.inverse());
}

//==============================================================================
//	MvnPdfSampler protected methods implementation.
//==============================================================================

template <typename ScalarType>
template <template <typename> typename IntersectionsPacketType>
inline std::tuple<RaysPacket<ScalarType>,
                  IntersectionsPacketType<ScalarType>,
                  Vector<ScalarType>,
                  Vector<ScalarType>>
MvnPdfSampler<ScalarType>::reparametrize_rays_(
    const RaysPacket<ScalarType>& rays,
    const IntersectionsPacketType<ScalarType>& in_intersections)
{
    // 1) Rescale the direction and segment bounds of each ray such that
    //    directions are unitary vectors.
    IntersectionsPacketType<Scalar> intersections(in_intersections);
    Vector<Scalar> ray_t_scale_factors = rays.directions.colwise().norm();
    Matrix<Scalar> directions =
        rays.directions * ray_t_scale_factors.cwiseInverse().asDiagonal();

    if (intersections.one_ray_one_intersection) {
        intersections.segment_starts =
            in_intersections.segment_starts.cwiseProduct(ray_t_scale_factors);
        intersections.segment_ends =
            in_intersections.segment_ends.cwiseProduct(ray_t_scale_factors);
    } else {
        intersections.segment_starts = in_intersections.segment_starts.cwiseProduct(
            ray_t_scale_factors(in_intersections.ray_indices));
        intersections.segment_ends = in_intersections.segment_ends.cwiseProduct(
            ray_t_scale_factors(in_intersections.ray_indices));
    }

    // 2) Reparametrize the lines such that the origins are the projections of
    //    the mean of the MVN on the rays.
    Vector<Scalar> ray_t_offsets =
        (-rays.origins.cwiseProduct(directions)).colwise().sum();
    Matrix<Scalar> origins = rays.origins + directions * ray_t_offsets.asDiagonal();

    if (intersections.one_ray_one_intersection) {
        intersections.segment_starts = intersections.segment_starts - ray_t_offsets;
        intersections.segment_ends = intersections.segment_ends - ray_t_offsets;
    } else {
        intersections.segment_starts =
            intersections.segment_starts - ray_t_offsets(in_intersections.ray_indices);
        intersections.segment_ends =
            intersections.segment_ends - ray_t_offsets(in_intersections.ray_indices);
    }

    return std::tuple<RaysPacket<Scalar>, IntersectionsPacketType<Scalar>,
                      Vector<Scalar>, Vector<Scalar>>(
        RaysPacket<Scalar>{origins, directions}, intersections, ray_t_scale_factors,
        ray_t_offsets);
}

}  // namespace samply

#endif