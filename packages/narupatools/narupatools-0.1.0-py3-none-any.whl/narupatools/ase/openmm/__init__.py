"""
Classes and methods for interfacing OpenMM with ASE as a calculator.

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

from .calculator import OpenMMCalculator
from .converter import openmm_simulation_to_ase_molecular_dynamics, openmm_simulation_to_ase_atoms
from .runner import from_openmm_xml, from_openmm_xml_string

__all__ = ["OpenMMCalculator", "openmm_simulation_to_ase_atoms", "openmm_simulation_to_ase_molecular_dynamics",
           "from_openmm_xml", "from_openmm_xml_string"]
