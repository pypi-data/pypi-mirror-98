"""
Runner that uses ASE to simulate a system.

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

from __future__ import annotations

from typing import TypeVar

from ase.atoms import Atoms
from ase.md import Langevin
from ase.md.md import MolecularDynamics

from . import ASEDynamics
from .null_calculator import NullCalculator
from .system import ASESystem


def from_ase_atoms(atoms: Atoms) -> ASESystem:
    if atoms.get_calculator() is None:
        atoms.set_calculator(NullCalculator())
    return ASESystem(atoms)


TIntegrator = TypeVar('TIntegrator', bound=MolecularDynamics)


def from_ase_dynamics(dynamics: TIntegrator) -> ASEDynamics[TIntegrator]:
    return ASEDynamics(dynamics)


def from_ase_atoms_langevin(atoms: Atoms, friction: float = 1e-2, temperature: float = 300,
                            timestep: float = 1) -> ASEDynamics[Langevin]:
    if atoms.get_calculator() is None:
        atoms.set_calculator(NullCalculator())
    dynamics = Langevin(atoms, timestep=timestep, temperature_K=temperature, friction=friction, fixcm=False)
    return from_ase_dynamics(dynamics)
