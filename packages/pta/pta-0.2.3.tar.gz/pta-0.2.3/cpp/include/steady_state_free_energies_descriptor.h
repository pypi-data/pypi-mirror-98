// Copyright (c) 2020 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef HYPERFLUX_STEADY_STATE_FREE_ENERGIES_DESCRIPTOR_H
#define HYPERFLUX_STEADY_STATE_FREE_ENERGIES_DESCRIPTOR_H

#include <descriptors/ellipsoid.h>
#include <descriptors/polytope.h>
#include <intersections_packet.h>
#include <rays_packet.h>
#include <reparametrized_object.h>

#include <Eigen/Dense>
#include <exception>
#include <utility>

#include "flux_constraints.h"
#include "settings/free_energy_sampling_settings.h"
#include "steady_state_verifier.h"
#include "thermodynamic_constraints.h"
#include "utilities.h"

namespace hyperflux {

/**
 * @brief Class describing a n-dimensional ellipsoid.
 */
template <typename ScalarType>
class SteadyStateFreeEnergiesDescriptor {
public:
    typedef ScalarType Scalar;

    /**
     * @brief Construct a new Ellipsoid object. The ellipsoid is defined as the
     * set { x \in R^d | x = E*y + f, |y| <= 1 }
     */
    SteadyStateFreeEnergiesDescriptor(
        const samply::Ellipsoid<Scalar>& dfg_estimate_constraints,
        const FluxConstraints& flux_constraints,
        const ThermodynamicConstraints& thermodynamic_constraints,
        const samply::AffineTransform<double>& directions_transform,
        const FreeEnergySamplingSettings& settings);

    SteadyStateFreeEnergiesDescriptor(
        const SteadyStateFreeEnergiesDescriptor<Scalar>& other);

    void initialize(const samply::Matrix<Scalar>& state);

    /**
     * @brief Find the intersections between the given rays and the ellipsoid.
     */
    samply::IntersectionsPacket<Scalar> intersect(
        const samply::RaysPacket<Scalar>& rays);

    void update_position(const samply::Vector<Scalar>& t);

    samply::ReparametrizedObject<SteadyStateFreeEnergiesDescriptor<Scalar>>
    get_optimally_reparametrized_descriptor(
        const std::string& optimality_criterion) const;

    Eigen::Index dimensionality() const;

    const samply::Matrix<Scalar> evaluate_last_drg_rays_at(
        const samply::Vector<Scalar>& t) const;

private:
    samply::Polytope<Scalar> make_vars_direction_constraints_(
        const FluxConstraints& flux_constriants,
        const ThermodynamicConstraints& thermodynamic_constraints,
        const double drg_epsilon) const;

    samply::AffineTransform<Scalar> make_vars_to_reversible_drg_transform_(
        const FluxConstraints& flux_constriants,
        const ThermodynamicConstraints& thermodynamic_constraints);

    const samply::Ellipsoid<Scalar> vars_estimate_constraints_;
    samply::Polytope<Scalar> vars_direction_constraints_;
    const FluxConstraints flux_constraints_;
    const ThermodynamicConstraints thermodynamic_constraints_;
    const samply::AffineTransform<double> directions_transform_;

    const FreeEnergySamplingSettings settings_;
    const samply::AffineTransform<Scalar> vars_to_rev_drg_;

    SteadyStateVerifier<Scalar> verifier_;

    samply::RaysPacket<Scalar> last_rev_drg_rays_;
};

//==============================================================================
//	SteadyStateFreeEnergiesDescriptor public methods implementation.
//==============================================================================

template <typename ScalarType>
SteadyStateFreeEnergiesDescriptor<ScalarType>::SteadyStateFreeEnergiesDescriptor(
    const samply::Ellipsoid<ScalarType>& vars_estimate_constraints,
    const FluxConstraints& flux_constraints,
    const ThermodynamicConstraints& thermodynamic_constraints,
    const samply::AffineTransform<double>& directions_transform,
    const FreeEnergySamplingSettings& settings)
    : vars_estimate_constraints_(vars_estimate_constraints),
      vars_direction_constraints_(make_vars_direction_constraints_(
          flux_constraints, thermodynamic_constraints, settings.drg_epsilon)),
      flux_constraints_(flux_constraints),
      thermodynamic_constraints_(thermodynamic_constraints),
      settings_(settings),
      vars_to_rev_drg_(make_vars_to_reversible_drg_transform_(
          flux_constraints, thermodynamic_constraints)),
      directions_transform_(directions_transform),
      verifier_(flux_constraints,
                thermodynamic_constraints.constrained_reactions_ids,
                settings.flux_epsilon,
                settings.feasibility_cache_size)
{
}

template <typename ScalarType>
SteadyStateFreeEnergiesDescriptor<ScalarType>::SteadyStateFreeEnergiesDescriptor(
    const SteadyStateFreeEnergiesDescriptor<ScalarType>& other)
    : SteadyStateFreeEnergiesDescriptor(other.vars_estimate_constraints_,
                                        other.flux_constraints_,
                                        other.thermodynamic_constraints_,
                                        other.directions_transform_,
                                        other.settings_)
{
}

template <typename ScalarType>
samply::IntersectionsPacket<ScalarType>
SteadyStateFreeEnergiesDescriptor<ScalarType>::intersect(
    const samply::RaysPacket<ScalarType>& rays)
{
    const samply::IntersectionsPacket<Scalar> intersections_polytope =
        vars_direction_constraints_.intersect(rays);
    const samply::IntersectionsPacket<Scalar> intersections_ellipsoid =
        vars_estimate_constraints_.intersect(rays);
    const samply::IntersectionsPacket<Scalar> intersections =
        intersections_polytope.intersect(intersections_ellipsoid);

    const auto rev_drg_rays = vars_to_rev_drg_ * rays;
    const samply::Matrix<Scalar> t_equienergy =
        -rev_drg_rays.origins.cwiseQuotient(rev_drg_rays.directions);

    Eigen::Index num_rays = rays.origins.cols();
    Eigen::Index num_regions = 0;
    samply::Vector<Scalar> region_starts(num_rays * (dimensionality() + 1));
    samply::Vector<Scalar> region_ends(num_rays * (dimensionality() + 1));
    Eigen::VectorXi ray_indices(num_rays * (dimensionality() + 1));

    for (Eigen::Index ray_idx = 0; ray_idx < num_rays; ray_idx++) {
        std::vector<Scalar> ts(t_equienergy.rows() + 2);
        const Scalar min_t = intersections.segment_starts(ray_idx);
        const Scalar max_t = intersections.segment_ends(ray_idx);
        const Scalar min_region_span =
            (max_t - min_t) * settings_.min_rel_region_length;
        ts[0] = min_t;
        ts[1] = max_t;

        // Collect intersections laying on the intersection segment.
        auto ray_t_equienergy = t_equienergy.col(ray_idx);
        auto ts_end = std::copy_if(
            ray_t_equienergy.begin(), ray_t_equienergy.end(), ts.begin() + 2,
            [&](const Scalar t) { return min_t <= t && t <= max_t; });

        // Sort and remove duplicates or regions that have negligible size.
        std::sort(ts.begin(), ts_end);

        ts_end = utilities::remove_if_precedent(
            ts.begin(), ts_end, [&](const Scalar t_predecessor, const Scalar t) {
                return (t - t_predecessor) < min_region_span;
            });
        ts.resize(std::distance(ts.begin(), ts_end));

        // Store the bounds of the regions for later processing.
        region_starts.segment(num_regions, ts.size() - 1) =
            Eigen::Map<samply::Vector<ScalarType>>(ts.data(), ts.size() - 1);
        region_ends.segment(num_regions, ts.size() - 1) =
            Eigen::Map<samply::Vector<ScalarType>>(ts.data() + 1, ts.size() - 1);
        ray_indices.segment(num_regions, ts.size() - 1).array() = ray_idx;
        num_regions += (ts.size() - 1);
    }

    const auto steady_state_orthants_ids = verifier_.get_steady_state_regions_ids(
        rev_drg_rays, region_starts.head(num_regions), region_ends.head(num_regions),
        ray_indices.head(num_regions));

    samply::IntersectionsPacket<ScalarType> steady_state_segments(
        region_starts(steady_state_orthants_ids),
        region_ends(steady_state_orthants_ids), ray_indices(steady_state_orthants_ids),
        num_rays);
    last_rev_drg_rays_ = rev_drg_rays;

    return steady_state_segments;
}

template <typename ScalarType>
void SteadyStateFreeEnergiesDescriptor<ScalarType>::initialize(
    const samply::Matrix<Scalar>& state)
{
    vars_direction_constraints_.initialize(state);
}

template <typename ScalarType>
void SteadyStateFreeEnergiesDescriptor<ScalarType>::update_position(
    const samply::Vector<Scalar>& t)
{
    vars_direction_constraints_.update_position(t);
}

template <typename ScalarType>
samply::ReparametrizedObject<SteadyStateFreeEnergiesDescriptor<ScalarType>>
SteadyStateFreeEnergiesDescriptor<ScalarType>::get_optimally_reparametrized_descriptor(
    const std::string& optimality_criterion) const
{
    if (optimality_criterion.compare("isotropy") == 0) {
        samply::ReparametrizedObject<samply::Ellipsoid<ScalarType>>
            reparametrized_ellipsoid =
                vars_estimate_constraints_.get_optimally_reparametrized_descriptor(
                    optimality_criterion);

        size_t num_variables = vars_to_rev_drg_.get_linear().cols();
        samply::AffineTransform<double> from_directions_frame =
            reparametrized_ellipsoid.from_frame() * directions_transform_;

        // TODO: only the transformations matter here, still we should construct
        // the reparametrized object correctly.

        samply::ReparametrizedObject<samply::Ellipsoid<ScalarType>>
            weighted_reparametrized_ellipsoid(
                samply::Ellipsoid<ScalarType>(num_variables), from_directions_frame,
                from_directions_frame.inverse());

        ThermodynamicConstraints reparametrized_thermo_constraints{
            thermodynamic_constraints_.constrained_reactions_ids,
            thermodynamic_constraints_.vars_to_constrained_drg *
                weighted_reparametrized_ellipsoid.from_frame()};

        return samply::ReparametrizedObject<
            SteadyStateFreeEnergiesDescriptor<ScalarType>>(
            SteadyStateFreeEnergiesDescriptor<ScalarType>(
                weighted_reparametrized_ellipsoid, flux_constraints_,
                reparametrized_thermo_constraints, directions_transform_, settings_),
            weighted_reparametrized_ellipsoid.from_frame(),
            weighted_reparametrized_ellipsoid.to_frame());
    } else if (optimality_criterion.compare("intersection") == 0) {
        samply::ReparametrizedObject<samply::Ellipsoid<ScalarType>>
            reparametrized_ellipsoid =
                vars_estimate_constraints_.get_optimally_reparametrized_descriptor(
                    optimality_criterion);

        ThermodynamicConstraints reparametrized_thermo_constraints{
            thermodynamic_constraints_.constrained_reactions_ids,
            thermodynamic_constraints_.vars_to_constrained_drg *
                reparametrized_ellipsoid.from_frame()};

        return samply::ReparametrizedObject<
            SteadyStateFreeEnergiesDescriptor<ScalarType>>(
            SteadyStateFreeEnergiesDescriptor<ScalarType>(
                reparametrized_ellipsoid, flux_constraints_,
                reparametrized_thermo_constraints, directions_transform_, settings_),
            reparametrized_ellipsoid.from_frame(), reparametrized_ellipsoid.to_frame());
    } else {
        throw std::runtime_error(
            std::string("The '") + optimality_criterion +
            std::string("' "
                        "optimality criterion is not recognized by the "
                        "SteadyStateFreeEnergiesDescriptor descriptor"));
    }
}

template <typename ScalarType>
Eigen::Index SteadyStateFreeEnergiesDescriptor<ScalarType>::dimensionality() const
{
    return vars_to_rev_drg_.get_linear().rows();
}

//==============================================================================
//	SteadyStateFreeEnergiesDescriptor private methods implementation.
//==============================================================================

template <typename ScalarType>
samply::Polytope<ScalarType>
SteadyStateFreeEnergiesDescriptor<ScalarType>::make_vars_direction_constraints_(
    const FluxConstraints& flux_constraints,
    const ThermodynamicConstraints& thermodynamic_constraints,
    const double drg_epsilon) const
{
    std::vector<Eigen::Index> forward_constraint_ids;
    std::vector<Eigen::Index> backward_constraint_ids;

    for (Eigen::Index constraint_idx = 0;
         constraint_idx < thermodynamic_constraints.constrained_reactions_ids.size();
         ++constraint_idx) {
        const Eigen::Index rxn_idx =
            thermodynamic_constraints.constrained_reactions_ids(constraint_idx);
        if (flux_constraints.lower_bounds(rxn_idx) >= 0)
            forward_constraint_ids.push_back(constraint_idx);
        if (flux_constraints.upper_bounds(rxn_idx) <= 0)
            backward_constraint_ids.push_back(constraint_idx);
    }

    const Eigen::Index num_constraints = static_cast<Eigen::Index>(
        forward_constraint_ids.size() + backward_constraint_ids.size());
    const samply::AffineTransform<double>& vars_to_drg =
        thermodynamic_constraints.vars_to_constrained_drg;

    samply::Matrix<double> G(num_constraints, vars_to_drg.get_linear().cols());
    samply::Vector<double> h(num_constraints);
    G << vars_to_drg.get_linear()(forward_constraint_ids, Eigen::all),
        -vars_to_drg.get_linear()(backward_constraint_ids, Eigen::all);
    h << -vars_to_drg.get_shift()(forward_constraint_ids).array() - drg_epsilon,
        vars_to_drg.get_shift()(backward_constraint_ids).array() - drg_epsilon;
    return samply::Polytope<ScalarType>(G, h);
}

template <typename ScalarType>
inline samply::AffineTransform<ScalarType>
SteadyStateFreeEnergiesDescriptor<ScalarType>::make_vars_to_reversible_drg_transform_(
    const FluxConstraints& flux_constraints,
    const ThermodynamicConstraints& thermodynamic_constraints)
{
    std::vector<Eigen::Index> constrained_rev_drg_ids;
    const size_t num_drgs = thermodynamic_constraints.constrained_reactions_ids.size();
    constrained_rev_drg_ids.reserve(num_drgs);

    // Find indices of all the reversible constrained reactions.
    for (size_t drg_idx = 0u; drg_idx < num_drgs; ++drg_idx) {
        const size_t rxn_idx =
            thermodynamic_constraints.constrained_reactions_ids(drg_idx);
        if (flux_constraints.lower_bounds[rxn_idx] < 0 &&
            flux_constraints.upper_bounds[rxn_idx] > 0)
            constrained_rev_drg_ids.push_back(drg_idx);
    }

    return samply::AffineTransform<ScalarType>(
        thermodynamic_constraints.vars_to_constrained_drg.get_linear()(
            constrained_rev_drg_ids, Eigen::all),
        thermodynamic_constraints.vars_to_constrained_drg.get_shift()(
            constrained_rev_drg_ids));
}

template <typename ScalarType>
inline const samply::Matrix<ScalarType>
SteadyStateFreeEnergiesDescriptor<ScalarType>::evaluate_last_drg_rays_at(
    const samply::Vector<ScalarType>& t) const
{
    return last_rev_drg_rays_.at(t);
}

}  // namespace hyperflux

#endif
