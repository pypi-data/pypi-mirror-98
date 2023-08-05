"""
Conversion functions between OpenMM objects and ASE objects.

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

import logging

import ase.units as units
import numpy as np
from ase.atoms import Atoms
from ase.md import Langevin
from ase.md.md import MolecularDynamics
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from simtk.openmm import LangevinIntegrator
from simtk.openmm.app import Simulation
from simtk.unit import angstrom, kelvin, picoseconds

import narupatools.ase.openmm.calculator as omm_calculator
from narupatools.ase.converter import PS_TO_ASE_TIME

DEFAULT_LANGEVIN_FRICTION = 10  # Friction in per picosecond

INTEGRATOR_NOT_LANGEVIN_MESSAGE = ("Running OpenMM simulation that was not setup with Langevin Integrator. A Langevin "
                                   "integrator with friction 0.01 fs^{-1} will be used.")
CONSTRAINTS_UNSUPPORTED_MESSAGE = "The simulation contains constraints which will be ignored by this runner!"


def openmm_simulation_to_ase_atoms(simulation: Simulation) -> Atoms:
    """
    Generate an ASE atoms representation of the OpenMM simulation.

    :return: ASE atoms object, with positions and chemical symbols read from the current state of the OpenMM simulation.
    """
    topology = simulation.topology

    system = simulation.system
    context = simulation.context

    positions_openmm = context.getState(getPositions=True).getPositions(asNumpy=True)
    positions = positions_openmm.value_in_unit(angstrom)
    symbols = []
    for openmm_atom in topology.atoms():
        symbols.append(openmm_atom.element.symbol)

    atoms = Atoms(symbols=symbols, positions=positions)

    boxvectors = system.getDefaultPeriodicBoxVectors()
    atoms.set_pbc(system.usesPeriodicBoundaryConditions())
    atoms.set_cell(np.array([vector.value_in_unit(angstrom) for vector in boxvectors]))

    return atoms


def openmm_simulation_to_ase_molecular_dynamics(simulation: Simulation) -> MolecularDynamics:
    """
    Convert an OpenMM simulation to an ASE simulation.

    This both converts the system itself to an ASE atoms object
    and converts the simulation to an ASE Langevin integrator. The timestep and temperature are read from the OpenMM
    simulation's integrator. If the temperature is not present, a default of 300 kelvin is used. If the OpenMM
    integrator is Langevin, then  the friction is also copied. If no friction is present, a default friction of 10
    ps^{-1} is used.

    The ASE atoms object has a calculator which will call the original underlying simulation tp calculate forces.

    Constraints in the OpenMM simulation are not converted, and a warning will be issued if they are present.

    :param simulation: An OpenMM simulation object.

    :return: An ASE `MolecularDynamics` object representing the same system.
    """
    if simulation.system.getNumConstraints() > 0:
        logging.warning(CONSTRAINTS_UNSUPPORTED_MESSAGE)

    atoms = openmm_simulation_to_ase_atoms(simulation)
    calculator = omm_calculator.OpenMMCalculator(simulation)
    atoms.set_calculator(calculator)

    try:
        # Get temperature of OpenMM simulation in K
        temperature = simulation.integrator.getTemperature().value_in_unit(kelvin)  # type: ignore
    except AttributeError:
        # Use default temperature of 300 K
        temperature = 300

    time_step = simulation.integrator.getStepSize().value_in_unit(picoseconds)

    # friction in per femtosecond
    if not isinstance(simulation.integrator, LangevinIntegrator):
        logging.warning(INTEGRATOR_NOT_LANGEVIN_MESSAGE)
        friction = DEFAULT_LANGEVIN_FRICTION / 1000.0
    else:
        friction = simulation.integrator.getFriction().value_in_unit(picoseconds ** (-1)) / 1000.0

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature)

    # We do not remove the center of mass (fixcm=False). If the center of
    # mass translations should be removed, then the removal should be added
    # to the OpenMM system.
    molecular_dynamics = Langevin(
        atoms=atoms,
        timestep=time_step * PS_TO_ASE_TIME,
        temperature_K=temperature,
        friction=friction / units.fs,
        fixcm=False,
    )

    return molecular_dynamics
