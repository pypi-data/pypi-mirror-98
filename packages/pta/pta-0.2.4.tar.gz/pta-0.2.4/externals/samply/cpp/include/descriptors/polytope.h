// Copyright (c) 2020 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_POLYTOPE_H
#define SAMPLY_POLYTOPE_H

#include <Eigen/Dense>
#include <utility>

#include "axis_rays_packet.h"
#include "commons.h"
#include "intersections_packet.h"
#include "rays_packet.h"
#include "reparametrized_object.h"

namespace samply {

/**
 * @brief Class describing a n-dimensional polytope.
 *
 * @tparam Scalar Type used for intersection operations.
 */
template <typename ScalarType>
class Polytope {
public:
    /**
     * @brief Scalar type used for intersection operations.
     */
    typedef ScalarType Scalar;

    /**
     * @brief Construct a new Polytope object. The polytope is defined as the
     * set { x \in R^d | G*x <= h } and is assumed to have maximum isotropy.
     *
     * @param G NumConstraints-by-NumDimensions matrix containing the normal
     * vectors of the planes constraining the polytope.
     * @param h NumConstraints-by-1 vector containing the offsets of the planes
     * constraining the polytope.
     */
    Polytope(const Matrix<double>& G, const Matrix<double>& h)
        : Polytope(G, h, AffineTransform<double>::identity(G.cols()))
    {
    }

    /**
     * @brief Construct a new Polytope object. The polytope is defined as the
     * set { x \in R^d | G*x <= h }
     *
     * @param G NumConstraints-by-NumDimensions matrix containing the normal
     * vectors of the planes constraining the polytope.
     * @param h NumConstraints-by-1 vector containing the offsets of the planes
     * constraining the polytope.
     * @param from_max_isotropy_frame_transform Transform from a coordinate
     * frame in which the polytope has maximum isotropy to the frame in which G
     * and h are given.
     */
    Polytope(const Matrix<double>& G,
             const Matrix<double>& h,
             const AffineTransform<double>& from_max_isotropy_frame_transform)
        : G_full_precision(G),
          h_full_precision(h),
          G_(G.cast<Scalar>()),
          h_(h.cast<Scalar>()),
          from_max_isotropy_frame_transform_(from_max_isotropy_frame_transform),
          numerator_cache_(),
          denominator_cache_()
    {
        // Make sure that the constraint matrix doesn't contain zero-rows.
        assert((G.cwiseAbs().rowwise().sum().array() != Scalar(0.0)).all());
    }

    /**
     * @brief Set the current state of the Markov Chains. This is used to cache
     * values that speed up ray-object intersections.
     *
     * @param state Current state of the Markov Chains.
     */
    void initialize(const Matrix<Scalar>& state);

    /**
     * @brief Find the intersections between a set of rays and the polytope.
     *
     * @param rays A set of rays for which intersections with the polytope must
     * be found.
     * @return An object describing all the intersections of the rays with the
     * polytope.
     */
    IntersectionsPacket<Scalar> intersect(const RaysPacket<Scalar>& rays);

    /**
     * @brief Find the intersections between a set of rays and the polytope.
     *
     * @param rays A set of rays for which intersections with the polytope must
     * be found.
     * @return An object describing all the intersections of the rays with the
     * polytope.
     */
    IntersectionsPacket<Scalar> intersect(const AxisRaysPacket<Scalar>& rays);

    /**
     * @brief Update the positions of the Markov Chains relative to the previous
     * state, in the directions given by the rays for which intersections where
     * last tested.
     *
     * @param t Distance of the new states along each ray.
     */
    void update_position(const Vector<Scalar>& t);

    /**
     * @brief Get a reparametrized version of this object such that intersection
     * operations are easy.
     *
     * @return Reparametrized version of this object, containing the
     * transforms mapping between the two parametrizations.
     */
    ReparametrizedObject<Polytope<Scalar>> get_optimally_reparametrized_descriptor(
        const std::string& optimality_criterion) const;

private:
    // NumConstraints-by-NumDimensions matrix containing the normal
    // vectors of the planes constraining the polytope.
    const Matrix<double> G_full_precision;

    // NumConstraints-by-1 vector containing the offsets of the planes
    // constraining the polytope.
    const Vector<double> h_full_precision;

    // NumConstraints-by-NumDimensions matrix containing the normal
    // vectors of the planes constraining the polytope.
    const Matrix<Scalar> G_;

    // NumConstraints-by-1 vector containing the offsets of the planes
    // constraining the polytope.
    const Vector<Scalar> h_;

    // Transform from a coordinate frame in which the polytope has maximum
    // isotropy to the frame in which G and h are given.
    const AffineTransform<double> from_max_isotropy_frame_transform_;

    // Matrix caching the numerator and denominator used in the last
    // intersection tests.
    Matrix<Scalar> numerator_cache_;
    Matrix<Scalar> denominator_cache_;
};

//==============================================================================
//	Polytope public methods implementation.
//==============================================================================

template <typename ScalarType>
void Polytope<ScalarType>::initialize(const Matrix<ScalarType>& state)
{
    numerator_cache_ = G_ * state - h_.replicate(1, state.cols());
}

template <typename ScalarType>
IntersectionsPacket<ScalarType> Polytope<ScalarType>::intersect(
    const RaysPacket<ScalarType>& rays)
{
    const Eigen::Index num_rays = rays.origins.cols();
    Scalar infinity = std::numeric_limits<Scalar>::infinity();

    // Find all intersections with the constraints. Note that if any
    // element of G*directions is zero, NaNs will be generated. Since
    // IEC 559 guarantees that <= and >= involving NaNs return false, these
    // will be replaced by infinity when choosing the closest intersection
    // later on.
    denominator_cache_.noalias() = G_ * rays.directions;

    auto all_intersections_t =
        (Matrix<Scalar>(2 + h_.size(), num_rays)
             << (-numerator_cache_.cwiseQuotient(denominator_cache_)),
         RowVector<Scalar>::Ones(num_rays) * -infinity,
         RowVector<Scalar>::Ones(num_rays) * infinity)
            .finished();

    // For each ray, find the first intersections in the positive and
    // negative directions. For each direction, only select the elements
    // with the correct sign and replace the others with +/- infinity.
    IntersectionsPacket<Scalar> intersections(
        (all_intersections_t.array() <= 0.0)
            .select(all_intersections_t, -infinity)
            .eval()
            .colwise()
            .maxCoeff(),
        (all_intersections_t.array() >= 0.0)
            .select(all_intersections_t, infinity)
            .eval()
            .colwise()
            .minCoeff());
    return intersections;
}

template <typename ScalarType>
IntersectionsPacket<ScalarType> Polytope<ScalarType>::intersect(
    const AxisRaysPacket<ScalarType>& rays)
{
    const Eigen::Index num_rays = rays.origins.cols();
    Scalar infinity = std::numeric_limits<Scalar>::infinity();

    // Find all intersections with the constraints. Note that if any
    // element of G*directions is zero, NaNs will be generated. Since
    // IEC 559 guarantees that <= and >= involving NaNs return false, these
    // will be replaced by infinity when choosing the closest intersection
    // later on.
    denominator_cache_.noalias() = G_(Eigen::all, rays.axis_ids);

    auto all_intersections_t =
        (Matrix<Scalar>(2 + h_.size(), num_rays)
             << (-numerator_cache_.cwiseQuotient(denominator_cache_)),
         RowVector<Scalar>::Ones(num_rays) * -infinity,
         RowVector<Scalar>::Ones(num_rays) * infinity)
            .finished();

    // For each ray, find the first intersections in the positive and
    // negative directions. For each direction, only select the elements
    // with the correct sign and replace the others with +/- infinity.
    IntersectionsPacket<Scalar> intersections(
        (all_intersections_t.array() <= 0.0)
            .select(all_intersections_t, -infinity)
            .eval()
            .colwise()
            .maxCoeff(),
        (all_intersections_t.array() >= 0.0)
            .select(all_intersections_t, infinity)
            .eval()
            .colwise()
            .minCoeff());
    return intersections;
}

template <typename ScalarType>
void Polytope<ScalarType>::update_position(const Vector<Scalar>& t)
{
    numerator_cache_ += denominator_cache_ * t.asDiagonal();
}

template <typename ScalarType>
ReparametrizedObject<Polytope<ScalarType>>
Polytope<ScalarType>::get_optimally_reparametrized_descriptor(
    const std::string& optimality_criterion) const
{
    if (optimality_criterion.compare("isotropy") == 0) {
        return ReparametrizedObject<Polytope<Scalar>>(
            Polytope<Scalar>(G_full_precision, h_full_precision,
                             AffineTransform<double>::identity(G_.cols())),
            from_max_isotropy_frame_transform_,
            from_max_isotropy_frame_transform_.inverse());
    } else if (optimality_criterion.compare("intersection") == 0) {
        AffineTransform<double> from_parametrization =
            AffineTransform<double>::identity(G_.cols());
        return ReparametrizedObject<Polytope<Scalar>>(
            Polytope<Scalar>(G_full_precision, h_full_precision,
                             from_max_isotropy_frame_transform_),
            from_parametrization, from_parametrization.inverse());
    } else if (optimality_criterion.compare("isotropy-chrr") == 0) {
        AffineTransform<double> from_parametrization =
            from_max_isotropy_frame_transform_;
        AffineTransform<double> to_parametrization =
            from_max_isotropy_frame_transform_.inverse();

        return ReparametrizedObject<Polytope<Scalar>>(
            Polytope<Scalar>(G_full_precision, h_full_precision,
                             AffineTransform<double>::identity(G_.cols())),
            from_parametrization, to_parametrization);
    } else if (optimality_criterion.compare("intersection-chrr") == 0) {
        AffineTransform<double> from_parametrization =
            from_max_isotropy_frame_transform_;
        AffineTransform<double> to_parametrization =
            from_max_isotropy_frame_transform_.inverse();

        return ReparametrizedObject<Polytope<Scalar>>(
            Polytope<Scalar>(
                G_full_precision * from_parametrization.get_linear(),
                h_full_precision - G_full_precision * from_parametrization.get_shift(),
                AffineTransform<double>::identity(G_.cols())),
            from_parametrization, to_parametrization);
    } else {
        throw std::runtime_error(
            std::string("The '") + optimality_criterion +
            std::string("' "
                        "optimality criterion is not recognized by the Ellipsoid "
                        "descriptor"));
    }
}

}  // namespace samply

#endif