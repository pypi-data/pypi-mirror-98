"""
Conversion methods for converting between MDTraj and Narupa.

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

from typing import Optional, Collection

from mdtraj import Topology, Trajectory
from narupa.trajectory.frame_data import FrameData

from narupatools.frame import ParticlePositions, ParticleCount, ParticleElements, BondPairs, ParticleResidues, \
    ParticleNames, ResidueNames, ResidueChains, ResidueCount, ChainCount, BondCount, BoxVectors

MDTRAJ_PROPERTIES = (
    ParticlePositions.key, BondPairs.key, ParticleResidues.key, ParticleElements.key, ParticleNames.key,
    ResidueNames.key, ResidueChains.key, ParticleCount.key, ResidueCount.key, BondCount.key, ChainCount.key,
    BoxVectors.key)


def mdtraj_trajectory_to_frame(trajectory: Trajectory,
                               *,
                               frame_index: int = 0,
                               properties: Collection[str] = MDTRAJ_PROPERTIES,
                               frame: Optional[FrameData] = None) -> FrameData:
    if frame is None:
        frame = FrameData()
    if ParticlePositions.key in properties:
        ParticlePositions.set(frame, trajectory.xyz[frame_index])
    if ParticleCount.key in properties:
        ParticleCount.set(frame, trajectory.n_atoms)
    if BoxVectors.key in properties:
        BoxVectors.set(frame, trajectory.unitcell_vectors[frame_index])
    mdtraj_topology_to_frame(trajectory.topology, properties, frame)
    return frame


def mdtraj_topology_to_frame(topology: Topology, properties: Collection[str] = MDTRAJ_PROPERTIES,
                             frame: Optional[FrameData] = None) -> FrameData:
    if frame is None:
        frame = FrameData()
    if BondPairs.key in properties:
        BondPairs.set(frame, [[bond[0].index, bond[1].index] for bond in topology.bonds])
    if ParticleResidues.key in properties:
        ParticleResidues.set(frame, [atom.residue.index for atom in topology.atoms])
    if ParticleElements.key in properties:
        ParticleElements.set(frame, [atom.element.number for atom in topology.atoms])
    if ParticleNames.key in properties:
        ParticleNames.set(frame, [atom.name for atom in topology.atoms])

    if ResidueNames.key in properties:
        ResidueNames.set(frame, [residue.name for residue in topology.residues])
    if ResidueChains.key in properties:
        ResidueChains.set(frame, [residue.chain.index for residue in topology.residues])

    _get_mdtraj_topology_counts(topology, properties, frame)
    return frame


def _get_mdtraj_topology_counts(topology: Topology, properties: Collection[str], frame: FrameData) -> None:
    if ParticleCount.key in properties:
        ParticleCount.set(frame, topology.n_atoms)
    if ResidueCount.key in properties:
        ResidueCount.set(frame, topology.n_residues)
    if ChainCount.key in properties:
        ChainCount.set(frame, topology.n_chains)
    if BondCount.key in properties:
        BondCount.set(frame, topology.n_bonds)
