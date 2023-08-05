"""
Utility methods for using matrices.
"""

import numpy as np

from .typing import Matrix3x3


def zero_matrix() -> Matrix3x3:
    """
    Create a 3x3 matrix with all zero entries.
    """
    return np.zeros((3, 3))


def kronecker_delta(i: int, j: int) -> float:
    """
    Evaluates as 1 where parameters i and j are equal and 0 otherwise.
    """
    return 1.0 if i == j else 0.0
