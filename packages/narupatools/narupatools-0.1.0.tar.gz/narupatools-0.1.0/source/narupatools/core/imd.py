from typing import Any, Dict, Tuple

import numpy as np
from narupatools.physics.force import gaussian_force_and_energy, mass_weighted_forces, spring_force_and_energy
from narupatools.physics.rigidbody import center_of_mass
from narupatools.physics.typing import Vector3Array, Vector3, ScalarArray
from typing_extensions import Protocol


class OffsetForceFunction(Protocol):
    def __call__(self, *, offset: np.ndarray, **kwargs: Any) -> Tuple[np.ndarray, float]:
        ...


OFFSET_FORCES: Dict[str, OffsetForceFunction] = {
    'gaussian': gaussian_force_and_energy,  # type: ignore
    'spring': spring_force_and_energy  # type: ignore
}


def calculate_imd_force(positions: Vector3Array, masses: ScalarArray, interaction_type: str,
                        interaction_point: Vector3, interaction_scale: float) -> Tuple[Vector3Array, float]:
    particle_count = len(positions)

    if particle_count > 1:
        center = center_of_mass(positions=positions, masses=masses)
    else:
        center = positions[0]

    try:
        potential_method = OFFSET_FORCES[interaction_type]
    except KeyError:
        raise KeyError(f"Unknown interactive force type {interaction_type}.")

    offset = center - interaction_point

    force, energy = potential_method(offset=offset)

    force *= interaction_scale
    energy *= interaction_scale

    return mass_weighted_forces(force=force, masses=masses), energy
