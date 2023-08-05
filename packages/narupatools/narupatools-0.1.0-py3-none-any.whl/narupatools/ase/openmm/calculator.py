"""
ASE Calculator that interfaces with OpenMM to provide forces.

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

Originally part of the narupa-ase package. Adapted under the terms of the GPL.
"""
from typing import Optional, Tuple, List, Collection, Any

import numpy as np
from ase.atoms import Atoms
from ase.calculators.calculator import Calculator, all_changes
from simtk.openmm.app import Simulation
from simtk.openmm.openmm import Context
from simtk.unit import angstrom, kilojoules_per_mole, kilojoule_per_mole

import narupatools.ase.openmm.converter as converter
from narupatools.ase.converter import KJMOL_TO_EV
from narupatools.ase.constraints.observer import ASEObserver


class OpenMMCalculator(Calculator):
    """
    Simple implementation of a ASE calculator for OpenMM.

    The context of the OpenMM simulation is used to compute forces and energies given a set of positions. When the
    ASE `Atoms` object has its positions changed by an integrator, these changes are pushed to the OpenMM context to
    enable the calculation of new forces and energies.
    """

    _context: Context
    implemented_properties = ['energy', 'forces']
    _atoms: Atoms

    def __init__(self, simulation: Simulation,
                 atoms: Optional[Atoms] = None, **kwargs: Any):
        """
        Create a calculator for the given simulation.

        :param simulation: OpenMM simulation to use as a calculator.
        :param atoms: ASE atoms object to use. If None, this will be generated from the OpenMM simulation. If
        provided, it must be consistent with the OpenMM simulation in terms of atom count.
        :param kwargs: Dictionary of keywords to pass to the base ASE calculator.
        """
        super().__init__(**kwargs)
        self._context = simulation.context
        if atoms is None:
            atoms = converter.openmm_simulation_to_ase_atoms(simulation)
        self._atoms = atoms

        _position_observer = ASEObserver()
        _position_observer.on_set_positions.add_callback(self._mark_positions_as_dirty)
        atoms.constraints.append(_position_observer)
        self._positions_dirty = True

        self._energy = 0.0
        self._forces = np.zeros((3, len(self._atoms)))

    def _mark_positions_as_dirty(self, **kwargs: Any) -> None:
        self._positions_dirty = True

    def calculate(self, atoms: Optional[Atoms] = None,
                  properties: Collection[str] = ('energy', 'forces'),
                  system_changes: List[str] = all_changes) -> None:  # noqa: D102
        if atoms is self._atoms or atoms is None:
            if self._positions_dirty:
                self._set_positions(self._atoms.get_positions())
                self._positions_dirty = False
                self._energy, self._forces = self._calculate_openmm()
        else:
            self._set_positions(atoms.get_positions())
            self._positions_dirty = True
            self._energy, self._forces = self._calculate_openmm()

        self.results['energy'] = self._energy
        self.results['forces'] = self._forces

    def _calculate_openmm(self) -> Tuple[float, np.ndarray]:
        state = self._context.getState(getEnergy=True, getForces=True)
        energy = state.getPotentialEnergy().value_in_unit(kilojoules_per_mole)
        forces = state.getForces(asNumpy=True).value_in_unit(kilojoule_per_mole / angstrom)
        return energy * KJMOL_TO_EV, forces * KJMOL_TO_EV

    def _set_positions(self, positions: np.ndarray) -> None:
        self._context.setPositions(positions * angstrom)
