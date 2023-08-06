// Copyright(C) 2018 Mattia Gollub, mattia.gollub@bsse.ethz.ch
// Computational Systems Biology group, ETH Zurich
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_RAYS_PACKET_H
#define SAMPLY_RAYS_PACKET_H

#include "commons.h"

namespace samply {

template <typename Scalar>
struct RaysPacket {
    Matrix<Scalar> origins;
    Matrix<Scalar> directions;

    Matrix<Scalar> at(const Vector<Scalar>& t) const
    {
        return origins + directions * t.asDiagonal();
    }

    Matrix<Scalar> at(const Eigen::VectorXi& ray_indices, const Vector<Scalar>& t) const
    {
        return origins(Eigen::all, ray_indices) +
               directions(Eigen::all, ray_indices) * t.asDiagonal();
    }

    Vector<Scalar> at(const int& ray_index, const Scalar t) const
    {
        return origins.col(ray_index) + directions.col(ray_index) * t;
    }

    template <typename IndexList>
    RaysPacket<Scalar> operator()(const IndexList& ray_indices) const
    {
        return RaysPacket<Scalar>{origins(Eigen::all, ray_indices),
                                  directions(Eigen::all, ray_indices)};
    }
};

}  // namespace samply

#endif