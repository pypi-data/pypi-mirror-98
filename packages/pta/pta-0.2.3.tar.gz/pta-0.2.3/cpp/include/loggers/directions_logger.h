// Copyright (c) 2020 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef HYPERFLUX_DIRECTIONS_LOGGER_H
#define HYPERFLUX_DIRECTIONS_LOGGER_H

#include <chord_samplers/mvn_pdf_sampler.h>
#include <loggers/state_logger.h>

#include <dynamic_bitset.hpp>
#include <unordered_map>
#include <vector>

#include "steady_state_free_energies_descriptor.h"

namespace hyperflux {

struct DirectionHasher {
    std::size_t operator()(const std::vector<uint8_t>& k) const
    {
        std::size_t seed = k.size();
        for (auto& i : k) {
            seed ^= i + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
        return seed;
    }
};

template <typename ChainState, typename DurationFormat = std::chrono::milliseconds>
class DirectionsLogger : public samply::StateLogger<ChainState, DurationFormat> {
public:
    typedef std::vector<uint8_t> Direction;
    typedef std::unordered_map<Direction, uint32_t, DirectionHasher> DirectionsMap;

    DirectionsLogger(const size_t worker_id,
                     const size_t steps_log_interval,
                     const size_t num_skipped_steps = 0u)
        : samply::StateLogger<ChainState, DurationFormat>(
              worker_id, steps_log_interval, num_skipped_steps),
          descriptor_(nullptr),
          sampler_(nullptr)
    {
    }

    DirectionsLogger(const DirectionsLogger<ChainState>& other)
        : samply::StateLogger<ChainState, DurationFormat>(other),
          directions_counts_(std::move(other.directions_counts_)),
          descriptor_(other.descriptor_),
          sampler_(other.sampler_)
    {
    }

    void start() override
    {
    }

    void stop(const bool time_limit_reached = false) override
    {
    }

    const DirectionsMap& get_directions_counts() const
    {
        return directions_counts_;
    }

    void set_descriptor(const SteadyStateFreeEnergiesDescriptor<double>& descriptor)
    {
        descriptor_ = &descriptor;
    }

    void set_sampler(const samply::MvnPdfSampler<double>& sampler)
    {
        sampler_ = &sampler;
    }

protected:
    void log_state(ChainState& chain_state, const size_t step_idx) override
    {
        samply::Vector<double> ts = sampler_->get_last_sampled_ts();
        samply::Matrix<double> drgs = descriptor_->evaluate_last_drg_rays_at(ts);

        for (size_t sample_idx = 0u; sample_idx < drgs.cols(); sample_idx++) {
            dynamic_bitset direction_sample_bits(drgs.rows());
            for (size_t i = 0u; i < drgs.rows(); ++i) {
                direction_sample_bits.set(i, drgs(i, sample_idx) < 0);
            }

            auto insertion_result = directions_counts_.insert(
                {std::move(direction_sample_bits.vector()), 1});
            if (!insertion_result.second) {
                insertion_result.first->second++;
            }
        }
    }

private:
    DirectionsMap directions_counts_;

    const SteadyStateFreeEnergiesDescriptor<double>* descriptor_;
    const samply::MvnPdfSampler<double>* sampler_;
};

}  // namespace hyperflux

#endif
