// Copyright (c) 2019 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_AXIS_RAYS_PACKET_H
#define SAMPLY_AXIS_RAYS_PACKET_H

#include "commons.h"

namespace samply {

template <typename Scalar>
struct AxisRaysPacket {
    Matrix<Scalar> origins;
    Vector<Eigen::Index> axis_ids;

    Matrix<Scalar> at(const Vector<Scalar>& t) const
    {
        Matrix<Scalar> result = origins;
        for (size_t i = 0u; i < t.size(); ++i)
            result(axis_ids(i), i) += t(i);

        return result;
    }

    Matrix<Scalar> at(const Eigen::VectorXi& ray_indices, const Vector<Scalar>& t) const
    {
        Matrix<Scalar> result = origins(Eigen::all, ray_indices);
        for (const auto& i : ray_indices)
            result(axis_ids(i), i) += t(i);

        return result;
    }

    Vector<Scalar> at(const int& ray_index, const Scalar t) const
    {
        Vector<Scalar> result = origins(Eigen::all, ray_index);
        result(axis_ids(ray_index), ray_index) += t(ray_index);

        return result;
    }
};

}  // namespace samply

#endif