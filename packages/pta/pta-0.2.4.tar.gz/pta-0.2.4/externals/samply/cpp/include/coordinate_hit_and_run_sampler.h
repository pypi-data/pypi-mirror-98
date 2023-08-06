// Copyright (c) 2019 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_COORDINATE_HIT_AND_RUN_SAMPLER_H
#define SAMPLY_COORDINATE_HIT_AND_RUN_SAMPLER_H

#include "axis_rays_packet.h"
#include "coordinate_hit_and_run_transforms.h"
#include "helpers/sampling_helper.h"
#include "intersections_packet.h"
#include "markov_chain.h"
#include "reparametrized_object.h"

namespace samply {

/**
 * @brief Implements hit-and-run sampling with general space descriptors and
 * probability distributions.
 *
 * The sampler supports simulation of multiple chains in parallel, which is
 * computationally more efficient than simulating each chain in a separate
 * sampler because of optimization of linear algebra operations.
 *
 * @tparam Scalar Floating point type used in the simulation.
 * @tparam NumDimensions Number of dimensions of the sampling space.
 * @tparam NumChains Number of chains to pack in a single simulation. Packed
 * chains can be simulated faster than using multiple parallel samplers.
 * @tparam SpaceDescriptor Type of the descriptor used to constrain the sampling
 * space.
 * @tparam ChordSampler Type of the sampler used for sampling on the
 * 1-dimensional chord at each step of the simulation.
 * @tparam Type of the logger used for monitoring the state of the simulation.
 */
template <typename Scalar,
          template <typename>
          typename SpaceDescriptor,
          template <typename>
          typename ChordSampler,
          template <typename, typename>
          typename Logger>
class CoordinateHitAndRunSampler
    : public MarkovChain<
          CoordinateHitAndRunSampler<Scalar, SpaceDescriptor, ChordSampler, Logger>,
          Matrix<Scalar>,
          Matrix<Scalar>,
          Logger> {
public:
    /**
     * @brief Base class of the sampler providing general operations for Markov
     * Chains.
     */
    typedef MarkovChain<CoordinateHitAndRunSampler,
                        Matrix<Scalar>,
                        Matrix<Scalar>,
                        Logger>
        Base;

    // Make sure that the MarkovChain class can access the protected methods of
    // this, in particular the next_state() implementation.
    friend Base;

    /**
     * @brief The type of a state of the simulation.
     */
    typedef typename Base::State State;
    typedef typename Base::InternalState InternalState;

    /**
     * @brief Construct a new HitAndRunSampler object.
     *
     * @param descriptor Descriptor of the bounds of the sampling space.
     * @param sampler Object used for sampling points on the 1-d chord at each
     * step of the simulation.
     * @param initial_state Initial state of the chain.
     * @param logger Instance of the logger used to monitor the state of the
     * simulation.
     */
    CoordinateHitAndRunSampler(const SpaceDescriptor<Scalar>& descriptor,
                               const ChordSampler<Scalar>& sampler,
                               const typename Base::LoggerType& logger)
        : Base(logger),
          space_descriptor(descriptor),
          chord_sampler(sampler),
          space_descriptor_Fd(
              descriptor.get_optimally_reparametrized_descriptor("isotropy-chrr")),
          space_descriptor_Fi(
              descriptor.get_optimally_reparametrized_descriptor("intersection-chrr")),
          chord_sampler_Fs(sampler.get_optimally_reparametrized_sampler()),
          transforms_(space_descriptor_Fd, space_descriptor_Fi, chord_sampler_Fs)
    {
    }

protected:
    void initialize(const InternalState& state) override
    {
        space_descriptor_Fi.initialize(state);
    }

    /**
     * @brief Execute one step of the simulation.
     *
     * @param state Current state of the chain.
     * @return The new state of the chain.
     */
    InternalState next_state(const InternalState& state) override
    {
        // 1) Sample new directions uniformly distributed in the Fd frame.
        auto axis_ids =
            sampling_helper.get_random_integers(0, state.rows() - 1, state.cols());

        // 2) Find the intersections between the current rays and the space
        //    descriptor in the Fi frame.
        const AxisRaysPacket<Scalar> rays_Fi = {state, axis_ids};
        const IntersectionsPacket<Scalar> intersections =
            space_descriptor_Fi.intersect(rays_Fi);

        // 3) Sample new points along the resulting chords in the Fs frame. Then
        //    compute the new states in the internal frame (i.e. Fi).
        Vector<Scalar> t;
        if (transforms_.is_Fs_equal_Fi()) {
            t = chord_sampler_Fs.sample1d(rays_Fi, intersections, sampling_helper);
        } else {
            const RaysPacket<Scalar> rays_Fs =
                transforms_.transform_rays_from_Fi_to_Fs(rays_Fi);
            t = chord_sampler_Fs.sample1d(rays_Fs, intersections, sampling_helper);
        }
        space_descriptor_Fi.update_position(t);

        return rays_Fi.at(t);
    }

    State convert_from_internal_state(const InternalState& internal_state) override
    {
        return transforms_.transform_from_Fi(internal_state);
    }

    InternalState convert_to_internal_state(const State& state) override
    {
        return transforms_.transform_to_Fi(state);
    }

private:
    // Helper object used to generate random numbers.
    SamplingHelper sampling_helper;

    // Descriptor of the sampling space.
    SpaceDescriptor<Scalar> space_descriptor;
    ReparametrizedObject<SpaceDescriptor<Scalar>> space_descriptor_Fd;
    ReparametrizedObject<SpaceDescriptor<Scalar>> space_descriptor_Fi;

    // Object used for sampling on the 1-d chord of each hit-and-run step.
    ChordSampler<Scalar> chord_sampler;
    ReparametrizedObject<ChordSampler<Scalar>> chord_sampler_Fs;

    CoordinateHitAndRunTransforms<Scalar> transforms_;
};

}  // namespace samply

#endif
