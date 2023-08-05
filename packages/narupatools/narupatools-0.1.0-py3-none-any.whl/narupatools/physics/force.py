"""
Common force calculations such as springs and linear drag.
"""

import math
from typing import Tuple

import numpy as np

from .matrix import zero_matrix
from .rigidbody import center_of_mass, angular_velocity
from .typing import Vector3, ScalarArray, Vector3Array
from .vector import cross_product_matrix, left_vector_triple_product_matrix


def spring_force(*, offset: Vector3, spring_constant: float = 1) -> Vector3:
    """
    Calculate the force :math:`F` caused by a spring using Hooke's law:

    .. math:: F = - k x

    :param offset: Offset :math:`x` of the spring from its resting position.
    :param spring_constant: Spring constant :math:`k` that scales the force.
    :return: Force :math:`F` applied by the spring.
    """
    return - offset * spring_constant  # type: ignore


def spring_force_and_energy(*, offset: Vector3, spring_constant: float = 1) -> Tuple[Vector3, float]:
    """
    Calculate the force :math:`F` and potential energy :math:`V` caused by a spring using Hooke's law:

    .. math:: V = \\frac{1}{2} k x^2

    .. math:: F = - k x

    :param offset: Offset :math:`x` of the spring from its resting position.
    :param spring_constant: Spring constant :math:`k` that scales the force.
    :return: Tuple of the force :math:`F` applied by the spring and potential energy :math:`V`.
    """
    return - offset * spring_constant, 0.5 * np.dot(offset, offset) * spring_constant


def gaussian_force_and_energy(*, offset: Vector3, depth: float = 1, sigma: float = 1) -> Tuple[Vector3, float]:
    """
    Calculate the force :math:`F` and potential energy :math:`V` caused by a gaussian well

    .. math:: V = - k \\exp(-\\frac{x^2}{2 \\sigma^2}))

    .. math:: F = - k \\frac{x}{\\sigma^2} \\exp(-\\frac{x^2}{2 \\sigma^2}))

    :param offset: Offset :math:`x` of the spring from its resting position.
    :param depth: Depth :math:`k` of the gaussian well.
    :param sigma: The standard deviation of the gaussian, describing its width.
    :return: Tuple of the force :math:`F` applied by the spring and potential energy :math:`V`.
    """
    sigma_sqr = sigma * sigma

    gauss = math.exp(-np.dot(offset, offset) / (2 * sigma_sqr))
    energy = - depth * gauss
    force = - depth * (offset / sigma_sqr) * gauss
    return force, energy


def linear_drag_force(*, velocity: Vector3, damping_coefficient: float) -> Vector3:
    """
    Calculate the linear drag force :math:`F` which opposes and scales linearly with velocity:

    .. math:: F = - \\gamma v

    :param velocity: Velocity :math:`v` of the particle.
    :param damping_coefficient: Damping coefficient :math:`\\gamma` that scales the force.
    :return: Force :math:`F` applied by the drag.
    """
    return - damping_coefficient * velocity  # type: ignore


def damped_spring_force(*, offset: Vector3, velocity: Vector3, spring_constant: float,
                        damping_coefficient: float) -> Vector3:
    """
    Calculate the force caused by a damped spring using Hooke's law:

    .. math:: F = - k x - \\gamma v

    This is a sum of a standard spring force and a linear damping.

    :param offset: Offset :math:`x` of the spring from its resting position.
    :param velocity: Velocity :math:`v` of the particle.
    :param spring_constant: Spring constant :math:`k` that scales the force.
    :param damping_coefficient: Damping coefficient :math:`\\gamma` that scales the force.
    :return: Force :math:`F` applied by the spring.
    """
    force = spring_force(offset=offset, spring_constant=spring_constant)
    force += linear_drag_force(velocity=velocity, damping_coefficient=damping_coefficient)
    return force


def critically_damped_spring_force(*, mass: float, offset: Vector3, velocity: Vector3,
                                   spring_constant: float) -> Vector3:
    """
    Calculate the force caused by a critically damped spring using Hooke's law:

    .. math:: F = - k x - \\gamma v

    This is a sum of a standard spring force and a linear damping, with the damping coefficient chosen to minimize
    the time taken to achieve equilibrium whilst avoiding oscillations.

    :param mass: Mass :math:`m` of the particle.
    :param offset: Offset :math:`x` of the spring from its resting position.
    :param velocity: Velocity :math:`v` of the particle.
    :param spring_constant: Spring constant :math:`k` that scales the force.
    :return: Force :math:`F` applied by the spring.
    """
    damping_coefficient = 2 * math.sqrt(mass * spring_constant)
    return damped_spring_force(offset=offset,
                               velocity=velocity,
                               spring_constant=spring_constant,
                               damping_coefficient=damping_coefficient)


def mass_weighted_forces(*, masses: ScalarArray, force: Vector3) -> Vector3Array:
    """
    Calculate the forces on a collection of particles obtained by distributing a given force :math:`F` such that the
    acceleration that this force causes on the system's center of mass is equal to the acceleration that :math:`F_i`
    will cause on each particle. This distributes the force such that all particles experiance an equal acceleration.
    The force :math:`F_i` is given by:

    .. math:: F_i = m_i F / M

    where :math:`M` is the total mass.

    :param masses: List of masses :math:`m_i` of each particle.
    :param force: Force :math:`F` to apply to the collection of particles.
    :return: List of forces :math:`F_i` on each particle, in the same units as :math:`F`.
    """
    total_mass = masses.sum()
    return np.array([mass / total_mass * force for mass in masses])


def damped_rotational_spring_forces(*, masses: ScalarArray, positions: Vector3Array, velocities: Vector3Array,
                                    angle: Vector3, spring_constant: float,
                                    damping_coefficient: float) -> Vector3Array:
    """
    Calculate the forces :math:`F_i` on a collection of particles corresponding to a damped rotational spring,
    consisting of three forces:

    A rotational torque to rotate the system in the direction of angle

    .. math:: F_i = m_i k \\theta \\times r_i

    A rotational torque opposing the current angular velocity of the system

    .. math:: F_i = - m_i \\gamma \\omega \\times r_i

    A centripetal force holding the system together

    .. math:: F_i = m_i \\omega \\times (\\omega \\times r_i)

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param velocities: List of velocities :math:`v_i` of each particle.
    :param angle: 3D vector indicating the angle :math:`\\theta` to rotate around and which axis to do so.
    :param spring_constant: Spring constant :math:`k` which scales the force used to rotate the system in the desired
    direction.
    :param damping_coefficient: Damping coefficient :math:`\\gamma` to scale the force which decelerates the rotational
    motion of the system.
    :return: List of forces :math:`F_i` for each particle.
    """
    com = center_of_mass(masses=masses, positions=positions)
    omega = angular_velocity(masses=masses, positions=positions, velocities=velocities)
    # Create the matrix K that applies all three forces
    K = zero_matrix()
    K += spring_constant * cross_product_matrix(angle)
    K += - damping_coefficient * cross_product_matrix(omega)
    K += left_vector_triple_product_matrix(omega, omega)
    return np.array([masses[i] * np.matmul(K, positions[i] - com) for i in range(0, len(positions))])
