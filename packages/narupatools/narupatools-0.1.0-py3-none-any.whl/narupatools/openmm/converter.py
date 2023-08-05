"""
Conversion functions between OpenMM objects and Narupa objects.

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

Originally part of the narupa-openmm package. Adapted under the terms of the GPL.
"""

from typing import Collection, Optional

import numpy as np
from narupa.trajectory.frame_data import FrameData
from simtk.openmm.app import Topology
from simtk.openmm.openmm import State, Context

from narupatools.frame import ParticlePositions, ParticleForces, ParticleVelocities, BoxVectors, ParticleNames, \
    ChainNames, ChainCount, ParticleElements, ParticleResidues, ResidueNames, ResidueIds, ResidueChains, ResidueCount, \
    ParticleCount, BondPairs, PotentialEnergy, BondCount

ALL_OPENMM_STATE_PROPERTIES = (ParticlePositions.key, ParticleVelocities.key, ParticleForces.key, BoxVectors.key)

DEFAULT_OPENMM_STATE_PROPERTIES = (ParticlePositions.key, BoxVectors.key)


def openmm_context_to_frame(context: Context, properties: Collection[str] = DEFAULT_OPENMM_STATE_PROPERTIES,
                            frame: Optional[FrameData] = None) -> FrameData:
    if frame is None:
        frame = FrameData()

    needPositions = ParticlePositions.key in properties
    needForces = ParticleForces.key in properties
    needVelocities = ParticleVelocities.key in properties
    needEnergy = PotentialEnergy.key in properties

    state = context.getState(getPositions=needPositions, getForces=needForces,
                             getEnergy=needEnergy, getVelocities=needVelocities)

    return openmm_state_to_frame(state, properties, frame)


def openmm_state_to_frame(state: State, properties: Collection[str] = DEFAULT_OPENMM_STATE_PROPERTIES,
                          frame: Optional[FrameData] = None) -> FrameData:
    """
    Convert an OpenMM state object to a Narupa FrameData

    :param state: The OpenMM state to convert.
    :param properties: A list of properties to include.
    :param frame_data: An optional pre-existing FrameData to populate
    :return: A FrameData populated with the requested properties that could be obtained from the state object.
    """
    if frame is None:
        frame = FrameData()

    if ParticlePositions.key in properties:
        ParticlePositions.set(frame, state.getPositions(asNumpy=True)._value)
    if ParticleForces.key in properties:
        ParticleForces.set(frame, state.getForces(asNumpy=True)._value)
    if ParticleVelocities.key in properties:
        ParticleVelocities.set(frame, state.getVelocities(asNumpy=True)._value)

    if PotentialEnergy.key in properties:
        PotentialEnergy.set(frame, state.getPotentialEnergy()._value)

    if BoxVectors.key in properties:
        BoxVectors.set(frame, state.getPeriodicBoxVectors()._value)

    return frame


DEFAULT_OPENMM_TOPOLOGY_PROPERTIES = (
    ResidueNames.key, ResidueChains.key, ResidueCount.key, ParticleCount.key, ChainNames.key, ChainCount.key,
    ParticleNames.key, ParticleElements.key, ParticleResidues.key, BondPairs.key, BondCount.key, BoxVectors.key)


def openmm_topology_to_frame(topology: Topology, properties: Collection[str] = DEFAULT_OPENMM_TOPOLOGY_PROPERTIES,
                             frame: Optional[FrameData] = None) -> FrameData:
    """
    Convert an OpenMM topology object to a Narupa FrameData

    :param topology: The OpenMM topology to convert.
    :param properties: A list of properties to include.
    :param frame_data: An optional pre-existing FrameData to populate
    :return: A FrameData populated with the requested properties that could be obtained from the topology object.
    """
    if frame is None:
        frame = FrameData()

    if ParticleCount.key in properties:
        ParticleCount.set(frame, topology.getNumAtoms())

    _get_openmm_topology_residue_info(topology, properties, frame)

    if ChainNames.key in properties:
        ChainNames.set(frame, [chain.id for chain in topology.chains()])
    if ChainCount.key in properties:
        ChainCount.set(frame, topology.getNumChains())

    _get_openmm_topology_atom_info(topology, properties, frame)

    _get_openmm_topology_bonds(topology, properties, frame)

    if BoxVectors.key in properties:
        box = topology.getPeriodicBoxVectors()
        if box is not None:
            BoxVectors.set(frame, box._value)

    return frame


def _get_openmm_topology_bonds(topology: Topology, properties: Collection[str], frame: FrameData) -> None:
    if BondPairs.key in properties:
        bonds = []
        for bond in topology.bonds():
            bonds.append((bond[0].index, bond[1].index))
        BondPairs.set(frame, bonds)
    if BondCount.key in properties:
        BondCount.set(frame, topology.getNumBonds())


def _get_openmm_topology_atom_info(topology: Topology, properties: Collection[str], frame: FrameData) -> None:
    if ParticleNames.key in properties or ParticleElements.key in properties or ParticleResidues.key in properties:

        n = topology.getNumAtoms()
        atom_names = np.empty(n, dtype=object)
        elements = np.empty(n, dtype=int)
        residue_indices = np.empty(n, dtype=int)

        for i, atom in enumerate(topology.atoms()):
            atom_names[i] = atom.name
            elements[i] = atom.element.atomic_number
            residue_indices[i] = atom.residue.index

        if ParticleNames.key in properties:
            ParticleNames.set(frame, atom_names)
        if ParticleElements.key in properties:
            ParticleElements.set(frame, elements)
        if ParticleResidues.key in properties:
            ParticleResidues.set(frame, residue_indices)


def _get_openmm_topology_residue_info(topology: Topology, properties: Collection[str], frame: FrameData) -> None:
    if ResidueNames.key in properties:
        ResidueNames.set(frame, [residue.name for residue in topology.residues()])
    if ResidueIds.key in properties:
        ResidueIds.set(frame, [residue.id for residue in topology.residues()])
    if ResidueChains.key in properties:
        ResidueChains.set(frame, [residue.chain.index for residue in topology.residues()])
    if ResidueCount.key in properties:
        ResidueCount.set(frame, topology.getNumResidues())
