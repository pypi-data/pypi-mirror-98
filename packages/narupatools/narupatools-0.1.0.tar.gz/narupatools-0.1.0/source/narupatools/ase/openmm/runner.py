"""
Runner for running an OpenMM simulation through an ASE calculator, giving access to ASE integrators.

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

from os import PathLike
from typing import Union

from narupa.openmm import serializer

from narupatools.ase.runner import from_ase_dynamics
from .converter import openmm_simulation_to_ase_molecular_dynamics
from .. import ASEDynamics


def from_openmm_xml(path: Union[str, bytes, PathLike]) -> ASEDynamics:
    with open(path) as infile:
        return from_openmm_xml_string(infile.read())


def from_openmm_xml_string(string: str) -> ASEDynamics:
    simulation = serializer.deserialize_simulation(string)
    dynamics = openmm_simulation_to_ase_molecular_dynamics(simulation)
    return from_ase_dynamics(dynamics)
