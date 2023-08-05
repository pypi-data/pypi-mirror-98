"""
Methods for dealing with systems of particles, such as center of mass and angular momentum.

Methods here are not specific with units - as long as arguments are provided in consistent units, then
the calculated result will be correct.
"""

import numpy as np

from .matrix import zero_matrix
from .typing import Vector3, ScalarArray, Vector3Array, Matrix3x3
from .vector import zero_vector, left_vector_triple_product_matrix


def center_of_mass(*, masses: ScalarArray, positions: Vector3Array) -> Vector3:
    """
    Calculate the center of mass :math:`R` of a collection of particles, defined as the mass weighted average position:

    .. math:: R = \\frac{\\sum_i m_i r_i}{\\sum_i m_i}

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`r_i` of each particle.
    :return: Center of mass of the particles, in the same units as positions was provided in.
    """
    count = len(positions)
    total_mass = 0.0
    total_center = zero_vector()
    for i in range(0, count):
        total_mass += masses[i]
        total_center += masses[i] * positions[i]
    return total_center / total_mass  # type: ignore


def center_of_mass_velocity(*, masses: ScalarArray, velocities: Vector3Array) -> Vector3:
    """
    Calculate the velocity :math:`V_R` of the center of mass of a collection of particles, defined as the mass weighted
    average velocity:

    .. math:: V_R = \\frac{\\sum_i m_i v_i}{\\sum_i v_i}

    :param masses: List of masses :math:`m_i` of each particle.
    :param velocities: List of velocities :math:`v_i` of each particle.
    :return: Velocity of the center of mass of the particles, in units of [distance] / [time].
    """
    # Reuse center of mass calculation, as its the same with positions exchanged for velocities
    return center_of_mass(masses=masses, positions=velocities)


def spin_angular_momentum(*, masses: ScalarArray, positions: Vector3Array, velocities: Vector3Array) -> Vector3:
    """
    Calculate the spin angular momentum :math:`L` of a collection of particles about their center of mass, defined as:

    .. math:: L = \\sum_i m_i r_i \\times v_i

    where :math:`r_i` and :math:`v_i` are the particles' position and velocity relative to the center of mass.

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param velocities: List of velocities :math:`V_i` of each particle.
    :return: Spin angular momentum :math:`L` in units of [mass] * [distance] squared / [time].
    """
    com = center_of_mass(masses=masses, positions=positions)
    com_velocity = center_of_mass_velocity(masses=masses, velocities=velocities)
    angular_momentum = np.array([0.0, 0.0, 0.0])
    for i in range(0, len(masses)):
        angular_momentum += masses[i] * np.cross(positions[i] - com, velocities[i] - com_velocity)
    return angular_momentum


def orbital_angular_momentum(*, masses: ScalarArray, positions: Vector3Array, velocities: Vector3Array) -> Vector3:
    """
    Calculate the orbital angular momentum :math:`L` of a collection of particles about the origin, defined as:

    .. math:: L = M R \\times V

    where :math:`M`, :math:`R` and :math:`V` are the total mass, center of mass and the velocity of the center of mass
    respectively.

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param velocities: List of velocities :math:`V_i` of each particle.
    :return: Orbital angular momentum :math:`L` in units of [mass] * [distance] squared / [time].
    """
    com = center_of_mass(masses=masses, positions=positions)
    com_velocity = center_of_mass_velocity(masses=masses, velocities=velocities)
    total_mass = masses.sum()
    return total_mass * np.cross(com, com_velocity)  # type: ignore


def moment_of_inertia_tensor(*, masses: ScalarArray, positions: Vector3Array) -> Matrix3x3:
    """
    Calculate the moment of inertia tensor :math:`I` of a collection of particles with respect to their center of mass.
    This matrix fufills the identity:

    .. math:: I v = \\sum_i m_i r_i \\times (v \\times r_i)

    for all vectors :math:`v`. Here, :math:`r_i` is the position of the i-th particle relative to the center of mass.

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :return: Moment of inertia tensor :math:`I` with respect to the center of mass, in units of [mass] * [distance]
    squared
    """
    com = center_of_mass(masses=masses, positions=positions)
    tensor = zero_matrix()
    for i in range(0, len(masses)):
        tensor -= masses[i] * left_vector_triple_product_matrix(positions[i] - com, positions[i] - com)
    return tensor


def angular_velocity(*, masses: ScalarArray, positions: Vector3Array, velocities: Vector3Array) -> Vector3:
    """
    Calculate the angular velocity :math:`\\omega` of a collection of particles with respect to their center of mass by
    calculating the angular momentum about the center of mass, and inverting the inertia tensor to obtain
    :math:`\\omega`:

    .. math:: \\omega = I^{-1} L

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param velocities: List of velocities :math:`V_i` of each particle.
    :return: Angular velocity :math:`\\omega` in units of radians / [time].
    """
    L = spin_angular_momentum(masses=masses, positions=positions, velocities=velocities)
    inertia = moment_of_inertia_tensor(masses=masses, positions=positions)
    return np.matmul(np.linalg.inv(inertia), L)   # type: ignore


def velocities_for_angular_velocity(*, masses: ScalarArray, positions: Vector3Array,
                                    angular_velocity: Vector3) -> Vector3Array:
    """
    Calculate the velocities that should be assigned to each particle in a collection of particles to correspond to a
    given angular velocity :math:`\\omega`, defined by:

    .. math:: v = \\omega \\times r_i

    where :math:`r_i` is the position of the i-th particle relative to the center of mass.

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param angular_velocity: Angular velocity :math:`\\omega` to assign to the system.
    :return: Velocities :math:`V_i` in units of [distance] / [time].
    """
    com = center_of_mass(masses=masses, positions=positions)
    return np.array([np.cross(angular_velocity, position - com) for position in positions])
