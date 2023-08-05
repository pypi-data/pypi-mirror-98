"""
Utility methods for using vectors.
"""

import numpy as np

from .typing import Vector3, Matrix3x3


def zero_vector() -> Vector3:
    return np.zeros(3)


def cross_product_matrix(vector: Vector3) -> Matrix3x3:
    """
    Calculate the skew-symmetric matrix `F` that for all vectors :math:`v` fufills the identity:

    .. math:: F v = a \\times v

    This converts taking the cross product on the left by :math:`a` to a matrix multiplication.

    :param vector: Vector :math:`a`.
    """
    return np.array([[0, -vector[2], vector[1]],
                     [vector[2], 0, -vector[0]],
                     [-vector[1], vector[0], 0]])


def right_cross_product_matrix(vector: Vector3) -> Matrix3x3:
    """
    Calculate the skew-symmetric matrix `F` that for all vectors :math:`v` fufills the identity:

    .. math:: F v = v \\times a

    This converts taking the cross product on the right by :math:`a` to a matrix multiplication.

    :param vector: Vector :math:`a`.
    """
    return np.array([[0, vector[2], -vector[1]],
                     [-vector[2], 0, vector[0]],
                     [vector[1], -vector[0], 0]])


def left_vector_triple_product_matrix(vector1: Vector3, vector2: Vector3) -> Matrix3x3:
    """
    Calculate the matrix `F` that for all vectors :math:`v` fufills the identity:

    .. math:: F v = a \\times (b \\times v)

    This converts taking the cross product on the left by :math:`b` and then by :math:`a` to a matrix multiplication.

    :param vector1: Vector :math:`a`.
    :param vector2: Vector :math:`b`.
    """
    return np.matmul(cross_product_matrix(vector1), cross_product_matrix(vector2))  # type: ignore
