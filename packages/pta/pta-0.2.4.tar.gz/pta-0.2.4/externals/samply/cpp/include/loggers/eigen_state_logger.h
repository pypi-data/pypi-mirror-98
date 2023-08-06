// Copyright(C) 2019 Mattia Gollub, mattia.gollub@bsse.ethz.ch
// Computational Systems Biology group, ETH Zurich
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef HYPERFLUX_EIGEN_STATE_LOGGER_H
#define HYPERFLUX_EIGEN_STATE_LOGGER_H

#include <Eigen/StdVector>
#include <vector>

#include "state_logger.h"

namespace samply {

template <typename ChainState, typename DurationFormat = std::chrono::milliseconds>
class EigenStateLogger : public StateLogger<ChainState, DurationFormat> {
public:
    typedef Eigen::MatrixXd StoredState;
    typedef std::vector<StoredState, Eigen::aligned_allocator<StoredState>>
        StoredStates;

    EigenStateLogger(const size_t worker_id,
                     const size_t steps_log_interval,
                     const size_t num_skipped_steps = 0u,
                     const size_t num_preallocated_states = 1u)
        : StateLogger<ChainState, DurationFormat>(
              worker_id, steps_log_interval, num_skipped_steps)
    {
        states_.reserve(num_preallocated_states);
    }

    EigenStateLogger(const EigenStateLogger<ChainState>& other)
        : StateLogger<ChainState, DurationFormat>(other),
          states_(std::move(other.states_))
    {
    }

    void start() override
    {
    }

    void stop(const bool time_limit_reached = false) override
    {
    }

    const StoredStates& get_states() const
    {
        return states_;
    }

protected:
    void log_state(ChainState& chain_state, const size_t step_idx) override
    {
        states_.push_back(chain_state.get().template cast<double>());
    }

private:
    StoredStates states_;
};

}  // namespace samply

#endif
