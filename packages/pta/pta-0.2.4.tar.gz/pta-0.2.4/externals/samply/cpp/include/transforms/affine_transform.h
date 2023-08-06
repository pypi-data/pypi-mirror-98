// Copyright(C) 2018 Mattia Gollub, mattia.gollub@bsse.ethz.ch
// Computational Systems Biology group, ETH Zurich
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_AFFINE_TRANSFORM_H
#define SAMPLY_AFFINE_TRANSFORM_H

#include <Eigen/QR>

#include "affine_dense_transform.h"
#include "affine_diagonal_transform.h"
#include "affine_transform_base.h"
#include "affine_transform_storage.h"
#include "axis_rays_packet.h"
#include "identity_transform.h"
#include "linear_diagonal_transform.h"
#include "linear_transform.h"
#include "rays_packet.h"
#include "reset_transform.h"
#include "translation_transform.h"
#include "zero_transform.h"

namespace samply {

/**
 * @brief Generic affine transform.
 *
 * @tparam Storage Class implementing the representation of the transform in
 * memory.
 */
template <typename Scalar, typename Storage = AffineTransformStorage<Scalar>>
class AffineTransform
    : public AffineTransformBase<AffineTransform<Scalar, Storage>, Storage> {
public:
    using AffineTransformBase<AffineTransform<Scalar, Storage>,
                              Storage>::AffineTransformBase;
    using StorageRef = AffineTransformStorageConstRef<Scalar>;

    /**
     * @brief Constructs a new AffineTransform object.
     *
     * @param T Linear component of the transform.
     * @param shift Translation component of the transform.
     */
    AffineTransform(const Matrix<Scalar>& T, const Vector<Scalar>& shift);

    /**
     * @brief Move-constructs a new AffineTransform object.
     *
     * @param other The object moved into the newly created instance.
     */
    template <typename OtherTransform, typename OtherStorage>
    AffineTransform(AffineTransformBase<OtherTransform, OtherStorage>&& other);

    /**
     * @brief Move assignment of an AffineTransform object.
     *
     * @param other The object moved into this instance.
     * @return Reference to this instance.
     */
    template <typename OtherTransform, typename OtherStorage>
    AffineTransform<Scalar>& operator=(
        AffineTransformBase<OtherTransform, OtherStorage>&& other);

    /**
     * @brief Applies this affine transform after another transform. The
     * resulting transform transforms a vector v as (this * (other * v)).
     *
     * @param transform Transform to which this transform is applied.
     * @return Transform resulting from the concatenation.
     */
    template <typename OtherTransform, typename OtherStorage>
    auto operator*(
        const AffineTransformBase<OtherTransform, OtherStorage>& transform) const;

    /**
     * @brief Applies this affine transform to a matrix or vector.
     *
     * @param matrix Matrix or vector to which the transform must be applied.
     * @return The transformed matrix.
     */
    template <typename MatrixType>
    Matrix<Scalar> operator*(const Eigen::MatrixBase<MatrixType>& matrix) const;

    /**
     * @brief Apply this affine transform to a RaysPacket object.
     *
     * @param rays Rays to which the transform must be applied.
     * @return The transformed rays.
     */
    RaysPacket<Scalar> operator*(const RaysPacket<Scalar>& rays) const;

    /**
     * @brief Apply this affine transform to a AxisRaysPacket object.
     *
     * @param rays Rays to which the transform must be applied.
     * @return The transformed rays.
     */
    RaysPacket<Scalar> operator*(const AxisRaysPacket<Scalar>& rays) const;

    /**
     * @brief Returns a new affine transform containing only the linear part of
     * this transform.
     *
     * @return The linear part of the transform.
     */
    AffineTransform<Scalar> linear() const;

    /**
     * @brief Returns the inverse of this affine transform. If the inverse is
     * not defined for this transform, the pseudoinverse is returned.
     *
     * @return The inverse or pseudoinverse of the matrix.
     */
    auto inverse() const;

    template <typename CastScalar>
    AffineTransform<CastScalar> cast() const;

    /**
     * @brief Create an identity affine transform of the specified size.
     *
     * @param n_dimensions Size of the identity transform.
     * @return The constructed identity transform.
     */
    static AffineTransform<Scalar> identity(const Eigen::Index n_dimensions);

private:
    // Types of affine transforms.
    enum class TransformType_ {
        AffineDiagonal,
        Dense,
        Identity,
        Linear,
        LinearDiagonal,
        Reset,
        Translation,
        Zero
    };

    // The type of this transform.
    TransformType_ type_;

    // Recompute the type of this transform.
    void reset_transform_type_();

    // Utilities casting this transform as an affine transform of a specific
    // type. This enables the usage of optimized operations provided by the
    // specialized transforms.
    const auto asAffineDiagonal_() const noexcept;
    const auto asDense_() const noexcept;
    const auto asIdentity_() const noexcept;
    const auto asLinear_() const noexcept;
    const auto asLinearDiagonal_() const noexcept;
    const auto asReset_() const noexcept;
    const auto asTranslation_() const noexcept;
    const auto asZero_() const noexcept;
};

//==============================================================================
//	AffineTransform private methods implementation.
//==============================================================================

template <typename Scalar, typename Storage>
inline void AffineTransform<Scalar, Storage>::reset_transform_type_()
{
    if (this->get_shift().isZero()) {
        // Linear transform.
        if (this->get_linear().isZero())
            type_ = TransformType_::Zero;
        else if (this->get_linear().isIdentity())
            type_ = TransformType_::Identity;
        else if (this->get_linear().isDiagonal())
            type_ = TransformType_::LinearDiagonal;
        else
            type_ = TransformType_::Linear;
    } else {
        // Affine transform.
        if (this->get_linear().isZero())
            type_ = TransformType_::Reset;
        else if (this->get_linear().isIdentity())
            type_ = TransformType_::Translation;
        else if (this->get_linear().isDiagonal())
            type_ = TransformType_::AffineDiagonal;
        else
            type_ = TransformType_::Dense;
    }
}

template <typename Scalar, typename Storage>
inline const auto AffineTransform<Scalar, Storage>::asAffineDiagonal_() const noexcept
{
    return AffineDiagonalTransform<Scalar, StorageRef>(StorageRef(this->storage_));
}

template <typename Scalar, typename Storage>
inline const auto AffineTransform<Scalar, Storage>::asDense_() const noexcept
{
    return AffineDenseTransform<Scalar, StorageRef>(StorageRef(this->storage_));
}

template <typename Scalar, typename Storage>
inline const auto AffineTransform<Scalar, Storage>::asIdentity_() const noexcept
{
    return IdentityTransform<Scalar, StorageRef>(StorageRef(this->storage_));
}

template <typename Scalar, typename Storage>
inline const auto AffineTransform<Scalar, Storage>::asLinear_() const noexcept
{
    return LinearTransform<Scalar, StorageRef>(StorageRef(this->storage_));
}

template <typename Scalar, typename Storage>
inline const auto AffineTransform<Scalar, Storage>::asLinearDiagonal_() const noexcept
{
    return LinearDiagonalTransform<Scalar, StorageRef>(StorageRef(this->storage_));
}

template <typename Scalar, typename Storage>
inline const auto AffineTransform<Scalar, Storage>::asReset_() const noexcept
{
    return ResetTransform<Scalar, StorageRef>(StorageRef(this->storage_));
}

template <typename Scalar, typename Storage>
inline const auto AffineTransform<Scalar, Storage>::asTranslation_() const noexcept
{
    return TranslationTransform<Scalar, StorageRef>(StorageRef(this->storage_));
}

template <typename Scalar, typename Storage>
inline const auto AffineTransform<Scalar, Storage>::asZero_() const noexcept
{
    return ZeroTransform<Scalar, StorageRef>(StorageRef(this->storage_));
}

//==============================================================================
//	AffineTransform public methods implementation.
//==============================================================================

template <typename Scalar, typename Storage>
inline AffineTransform<Scalar, Storage>::AffineTransform(const Matrix<Scalar>& T,
                                                         const Vector<Scalar>& shift)
    : AffineTransformBase<AffineTransform<Scalar>, AffineTransformStorage<Scalar>>(
          T, shift)
{
    reset_transform_type_();
}

template <typename Scalar, typename Storage>
template <typename OtherTransform, typename OtherStorage>
inline AffineTransform<Scalar, Storage>::AffineTransform(
    AffineTransformBase<OtherTransform, OtherStorage>&& other)
    : AffineTransformBase<AffineTransform<Scalar>, AffineTransformStorage<Scalar>>(
          std::move(other))
{
    reset_transform_type_();
}

template <typename Scalar, typename Storage>
template <typename OtherTransform, typename OtherStorage>
inline AffineTransform<Scalar>& AffineTransform<Scalar, Storage>::operator=(
    AffineTransformBase<OtherTransform, OtherStorage>&& other)
{
    if (this != &other) {
        this->storage_ = std::move(other.storage_);
    }
    return *this;
}

template <typename Scalar, typename Storage>
template <typename OtherTransform, typename OtherStorage>
inline auto AffineTransform<Scalar, Storage>::operator*(
    const AffineTransformBase<OtherTransform, OtherStorage>& transform) const
{
    return AffineTransform<Scalar>(
        this->get_linear() * transform.get_linear(),
        this->get_linear() * transform.get_shift() + this->get_shift());
}

template <typename Scalar, typename Storage>
template <typename MatrixType>
inline Matrix<Scalar> AffineTransform<Scalar, Storage>::operator*(
    const Eigen::MatrixBase<MatrixType>& matrix) const
{
    switch (type_) {
    case TransformType_::AffineDiagonal:
        return asAffineDiagonal_() * matrix;
        break;
    default:
    case TransformType_::Dense:
        return asDense_() * matrix;
        break;
    case TransformType_::Identity:
        return asIdentity_() * matrix;
        break;
    case TransformType_::Linear:
        return asLinear_() * matrix;
        break;
    case TransformType_::LinearDiagonal:
        return asLinearDiagonal_() * matrix;
        break;
    case TransformType_::Reset:
        return asReset_() * matrix;
        break;
    case TransformType_::Translation:
        return asTranslation_() * matrix;
        break;
    case TransformType_::Zero:
        return asZero_() * matrix;
        break;
    }
}

template <typename Scalar, typename Storage>
inline RaysPacket<Scalar> AffineTransform<Scalar, Storage>::operator*(
    const RaysPacket<Scalar>& rays) const
{
    switch (type_) {
    case TransformType_::AffineDiagonal:
        return RaysPacket<Scalar>{asAffineDiagonal_() * rays.origins,
                                  asLinearDiagonal_() * rays.directions};
        break;
    default:
    case TransformType_::Dense:
        return RaysPacket<Scalar>{asDense_() * rays.origins,
                                  asLinear_() * rays.directions};
        break;
    case TransformType_::Identity:
        return RaysPacket<Scalar>{asIdentity_() * rays.origins,
                                  asIdentity_() * rays.directions};
        break;
    case TransformType_::Linear:
        return RaysPacket<Scalar>{asLinear_() * rays.origins,
                                  asLinear_() * rays.directions};
        break;
    case TransformType_::LinearDiagonal:
        return RaysPacket<Scalar>{asLinearDiagonal_() * rays.origins,
                                  asLinearDiagonal_() * rays.directions};
        break;
    case TransformType_::Translation:
        return RaysPacket<Scalar>{asTranslation_() * rays.origins, rays.directions};
        break;
    case TransformType_::Reset:
        return RaysPacket<Scalar>{asReset_() * rays.origins,
                                  asZero_() * rays.directions};
        break;
    case TransformType_::Zero:
        return RaysPacket<Scalar>{asZero_() * rays.origins,
                                  asZero_() * rays.directions};
        break;
    }
}

template <typename Scalar, typename Storage>
inline RaysPacket<Scalar> AffineTransform<Scalar, Storage>::operator*(
    const AxisRaysPacket<Scalar>& rays) const
{
    switch (type_) {
    case TransformType_::AffineDiagonal:
        return RaysPacket<Scalar>{asAffineDiagonal_() * rays.origins,
                                  this->get_linear()(Eigen::all, rays.axis_ids)};
        break;
    default:
    case TransformType_::Dense:
        return RaysPacket<Scalar>{asDense_() * rays.origins,
                                  this->get_linear()(Eigen::all, rays.axis_ids)};
        break;
    case TransformType_::Identity:
        return RaysPacket<Scalar>{asIdentity_() * rays.origins,
                                  this->get_linear()(Eigen::all, rays.axis_ids)};
        break;
    case TransformType_::Linear:
        return RaysPacket<Scalar>{asLinear_() * rays.origins,
                                  this->get_linear()(Eigen::all, rays.axis_ids)};
        break;
    case TransformType_::LinearDiagonal:
        return RaysPacket<Scalar>{asLinearDiagonal_() * rays.origins,
                                  this->get_linear()(Eigen::all, rays.axis_ids)};
        break;
    case TransformType_::Translation:
        return RaysPacket<Scalar>{asTranslation_() * rays.origins,
                                  this->get_linear()(Eigen::all, rays.axis_ids)};
        break;
    case TransformType_::Reset:
        return RaysPacket<Scalar>{asReset_() * rays.origins,
                                  this->get_linear()(Eigen::all, rays.axis_ids)};
        break;
    case TransformType_::Zero:
        return RaysPacket<Scalar>{asZero_() * rays.origins,
                                  this->get_linear()(Eigen::all, rays.axis_ids)};
        break;
    }
}

template <typename Scalar, typename Storage>
inline AffineTransform<Scalar> AffineTransform<Scalar, Storage>::linear() const
{
    return AffineTransform<Scalar>(
        this->storage_.get_linear(),
        Vector<Scalar>::Zero(this->storage_.get_shift().size()));
}

template <typename Scalar, typename Storage>
inline auto AffineTransform<Scalar, Storage>::inverse() const
{
    Matrix<Scalar> inv_T;
    if (this->storage_.get_linear().rows() == this->storage_.get_linear().cols()) {
        inv_T = this->storage_.get_linear().inverse();
    } else {
        inv_T = this->storage_.get_linear()
                    .completeOrthogonalDecomposition()
                    .pseudoInverse();
    }
    return AffineTransform<Scalar>(inv_T, -inv_T * this->storage_.get_shift());
}

template <typename Scalar, typename Storage>
template <typename CastScalar>
inline AffineTransform<CastScalar> AffineTransform<Scalar, Storage>::cast() const
{
    return AffineTransform<CastScalar>(
        this->storage_.get_linear().template cast<CastScalar>(),
        this->storage_.get_shift().template cast<CastScalar>());
}

//==============================================================================
//	AffineTransform public static methods implementation.
//==============================================================================

template <typename Scalar, typename Storage>
inline AffineTransform<Scalar> AffineTransform<Scalar, Storage>::identity(
    const Eigen::Index n_dimensions)
{
    return AffineTransform<Scalar>(Matrix<Scalar>::Identity(n_dimensions, n_dimensions),
                                   Vector<Scalar>::Zero(n_dimensions));
}

}  // namespace samply

#endif
