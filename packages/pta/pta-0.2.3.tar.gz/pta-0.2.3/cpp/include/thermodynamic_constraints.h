// Copyright (c) 2019 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef HYPERFLUX_THERMODYNAMIC_CONSTRAINTS_H
#define HYPERFLUX_THERMODYNAMIC_CONSTRAINTS_H

#include <transforms/transforms.h>

#include <Eigen/Dense>

namespace hyperflux {

struct ThermodynamicConstraints {
    Eigen::Matrix<Eigen::Index, -1, 1> constrained_reactions_ids;
    samply::AffineTransform<double> vars_to_constrained_drg;
};

}  // namespace hyperflux

#endif