"""
Protocols to act as base classes for ASE constraints.

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

import numpy as np
from ase import Atoms
from typing_extensions import Protocol


class ASEConstraint(Protocol):
    """Protocol describing an ASE Constraint, as ASE uses duck typing."""

    def adjust_positions(self, atoms: Atoms, positions: np.ndarray) -> None:
        """
        Adjust the positions in-place for an ASE `Atoms` object.

        :param atoms: The ASE `Atoms` object this constraint applies to.
        :param positions: The positions to be modified by this constraint, in angstrom.
        """
        ...

    def adjust_forces(self, atoms: Atoms, forces: np.ndarray) -> None:
        """
        Adjust the forces in-place for an ASE `Atoms` object.

        :param atoms: The ASE `Atoms` object this constraint applies to.
        :param forces: The forces to be modified by this constraint, in eV per nm.
        """
        ...


class ASEEnergyConstraint(ASEConstraint, Protocol):
    """Protocol describing an ASE Constraint that modified potential energy, as ASE uses duck typing."""

    def adjust_potential_energy(self, atoms: Atoms) -> float:
        """
        Get the difference in potential energy due to this constraint.

        :param atoms: The ASE `Atoms` object this constraint applies to.
        :return: The difference in potential energy, in eV.
        """
