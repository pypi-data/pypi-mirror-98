// Copyright(C) 2018 Mattia Gollub, mattia.gollub@bsse.ethz.ch
// Computational Systems Biology group, ETH Zurich
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_INTERSECTIONS_PACKET_H
#define SAMPLY_INTERSECTIONS_PACKET_H

#include <Eigen/Dense>

#include "commons.h"

namespace samply {

template <typename Scalar>
struct IntersectionsPacket {
    Vector<Scalar> segment_starts;
    Vector<Scalar> segment_ends;
    Eigen::VectorXi ray_indices;
    Eigen::Index num_rays;
    bool one_ray_one_intersection;

    IntersectionsPacket(const Vector<Scalar>& segment_starts,
                        const Vector<Scalar>& segment_ends)
        : segment_starts(segment_starts),
          segment_ends(segment_ends),
          num_rays(segment_starts.size()),
          one_ray_one_intersection(true)
    {
    }

    IntersectionsPacket(const Vector<Scalar>& segment_starts,
                        const Vector<Scalar>& segment_ends,
                        const Eigen::VectorXi& ray_indices,
                        const Eigen::Index num_rays)
        : segment_starts(segment_starts),
          segment_ends(segment_ends),
          ray_indices(ray_indices),
          num_rays(num_rays),
          one_ray_one_intersection(false)
    {
    }

    template <typename IndexList>
    IntersectionsPacket<Scalar> operator()(const IndexList& ray_indices) const
    {
        if (!one_ray_one_intersection)
            throw std::runtime_error("Not implemented yet.");
        return IntersectionsPacket<Scalar>(segment_starts(ray_indices),
                                           segment_ends(ray_indices));
    }

    IntersectionsPacket<Scalar> intersect(
        const IntersectionsPacket<Scalar>& other) const
    {
        if (!other.one_ray_one_intersection || !one_ray_one_intersection)
            throw std::runtime_error(
                "IntersectionsPacket::intersect can "
                "be used only if all rays have a single intersection");

        if (!((segment_ends.array() > other.segment_starts.array()) &&
              (other.segment_ends.array() > segment_starts.array()))
                 .all()) {
            throw std::runtime_error(
                "The intersections don't overlap on "
                "at least one ray");
        }

        return IntersectionsPacket<Scalar>(
            segment_starts.cwiseMax(other.segment_starts),
            segment_ends.cwiseMin(other.segment_ends));
    }

    template <typename Function>
    Vector<Scalar> for_each_ray(Function&& ray_function) const
    {
        assert(!one_ray_one_intersection);
        Eigen::Index current_ray = 0;
        Eigen::Index current_ray_start_idx = 0;
        Vector<Scalar> result(num_rays);

        for (Eigen::Index segment_idx = 0; segment_idx < segment_starts.size();
             segment_idx++) {
            if (segment_idx + 1 == segment_starts.size() ||
                ray_indices(segment_idx + 1) != current_ray) {
                // The current segment belongs to a new ray.
                Eigen::Index num_ray_segments = segment_idx - current_ray_start_idx + 1;

                // Execute the function on the ray we just completed.
                result(current_ray) = ray_function(
                    segment_starts.segment(current_ray_start_idx, num_ray_segments),
                    segment_ends.segment(current_ray_start_idx, num_ray_segments),
                    current_ray);

                // Advance indices to start a new ray.
                if (segment_idx + 1 != segment_starts.size())
                    assert(ray_indices(segment_idx + 1) == current_ray + 1);
                current_ray_start_idx = segment_idx + 1;
                current_ray++;
            }
        }

        return result;
    }
};

}  // namespace samply

#endif