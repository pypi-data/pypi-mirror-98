// Copyright (c) 2019 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_COORDINATE_HIT_AND_RUN_TRANSFORMS_H
#define SAMPLY_COORDINATE_HIT_AND_RUN_TRANSFORMS_H

#include <Eigen/Dense>

#include "hit_and_run_transforms.h"
#include "reparametrized_object.h"

namespace samply {

template <typename TransformationScalar>
class CoordinateHitAndRunTransforms : public HitAndRunTransforms<TransformationScalar> {
public:
    using HitAndRunTransforms<TransformationScalar>::HitAndRunTransforms;

    RaysPacket<TransformationScalar> transform_rays_from_Fi_to_Fs(
        const AxisRaysPacket<TransformationScalar>& rays_Fi)
    {
        if (this->Fs_equal_Fi) {
            return AffineTransform<TransformationScalar>::identity(
                       rays_Fi.origins.rows()) *
                   rays_Fi;
        } else {
            return this->Fi_to_Fs * rays_Fi;
        }
    }
};

}  // namespace samply

#endif
