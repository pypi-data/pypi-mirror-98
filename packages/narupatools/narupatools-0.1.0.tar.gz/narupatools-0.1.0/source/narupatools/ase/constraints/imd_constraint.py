"""
An ASE constraint that applies an interactive force.

This file is part of narupatools (https://gitlab.com/alexjbinnie/narupatools)
Copyright (c) University of Bristol. All rights reserved.

narupatools is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

narupatools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with narupatools.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Tuple

import numpy as np
from ase.atoms import Atoms
from narupa.imd import ParticleInteraction
from narupatools.ase.converter import KJMOL_TO_EV, ANG_TO_NM, NM_TO_ANG, EV_TO_KJMOL
from narupatools.core.imd import calculate_imd_force
from narupatools.physics.typing import Vector3Array

from .constraint import ASEEnergyConstraint


class InteractionConstraint(ASEEnergyConstraint):
    """An ASE constraint that applies an iMD force."""
    _interaction: ParticleInteraction
    key: str
    _total_work: float
    _last_step_work: float
    _previous_positions: Vector3Array
    _previous_forces: Vector3Array

    def __init__(self, key: str, interaction: ParticleInteraction, start_time: float):
        self.key = key
        self._total_work = 0.0
        self._last_step_work = 0.0
        self.interaction = interaction
        self._previous_positions = np.zeros(0)
        self._previous_forces = np.zeros(0)
        self._start_time = start_time

    @property
    def start_time(self) -> float:
        """Start time of the interaction in picoseconds."""
        return self._start_time

    @property
    def total_work(self) -> float:
        """Total work performed by interaction in kJ/mol."""
        return self._total_work

    @property
    def work_last_step(self) -> float:
        """Work performed last step in kJ/mol."""
        return self._last_step_work

    @property
    def interaction(self) -> ParticleInteraction:
        return self._interaction

    @interaction.setter
    def interaction(self, value: ParticleInteraction) -> None:
        self._interaction = value

    def on_pre_step(self, atoms: Atoms) -> None:
        self._previous_positions = atoms.positions[self._interaction.particles]
        self.energy, self.forces = self._calculate(atoms)
        self._previous_forces = self.forces

    def on_post_step(self, atoms: Atoms) -> None:
        _current_positions = atoms.positions[self._interaction.particles]

        work_this_step = 0.0

        for i in range(len(self._interaction.particles)):
            work_this_step += np.dot(self._previous_forces[i], (_current_positions[i] - self._previous_positions[i]))

        # work this step is in eV, store it in KJ/MOL
        work_this_step *= EV_TO_KJMOL

        self._last_step_work = work_this_step
        self._total_work += work_this_step

        self._previous_positions = _current_positions

    def adjust_positions(self, atoms: Atoms, positions: np.ndarray) -> None:
        pass

    def adjust_forces(self, atoms: Atoms, forces: np.ndarray) -> None:
        self.energy, self.forces = self._calculate(atoms)
        forces[self._interaction.particles] += self.forces

    def adjust_potential_energy(self, atoms: Atoms) -> float:
        self.energy, self.forces = self._calculate(atoms)
        return self.energy

    def _calculate(self, atoms: Atoms) -> Tuple[float, Vector3Array]:
        positions_nm = atoms.positions[self._interaction.particles] * ANG_TO_NM
        masses_amu = atoms.get_masses()[self._interaction.particles]

        forces_kjmol, energy_kjmol = calculate_imd_force(positions_nm,
                                                         masses_amu,
                                                         self._interaction.interaction_type,
                                                         self._interaction.position,
                                                         self._interaction.scale)

        energy_ev = energy_kjmol * KJMOL_TO_EV
        forces_ev = forces_kjmol * KJMOL_TO_EV / NM_TO_ANG

        return energy_ev, forces_ev
