"""
Conversion methods between MDAnalysis and Narupa.

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

from typing import List, Optional, Collection, Tuple, Dict

from MDAnalysis import AtomGroup, Universe
from MDAnalysis.topology.guessers import guess_atom_element
from ase.geometry import cellpar_to_cell
from narupa.mdanalysis.converter import ELEMENT_INDEX, mdanalysis_to_frame_data
from narupa.trajectory import FrameData

from narupatools.frame import ParticleNames, ParticlePositions, ChainCount, ResidueCount, ParticleCount, BondPairs, \
    ResidueChains, ParticleResidues, ResidueNames, ParticleElements, BoxVectors, BondCount

DEFAULT_MDA_ATOMGROUP_PROPERTIES = (
    ParticleNames.key, ParticlePositions.key, ChainCount.key, ResidueCount.key, ParticleCount.key, BondPairs.key,
    ResidueChains.key, ParticleResidues.key, ResidueNames.key, ParticleElements.key)

DEFAULT_MDA_UNIVERSE_PROPERTIES = (
    BoxVectors.key, BondCount.key
)

ANGSTROM_TO_NM = 0.1


def mdanalysis_universe_to_frame(universe: Universe, properties: Collection[str] = DEFAULT_MDA_UNIVERSE_PROPERTIES,
                                 frame: Optional[FrameData] = None) -> FrameData:
    if frame is None:
        frame = FrameData()
    frame.raw.MergeFrom(mdanalysis_to_frame_data(universe).raw)

    if BoxVectors.key in properties:
        BoxVectors.set(frame, cellpar_to_cell(universe.dimensions) * ANGSTROM_TO_NM)

    if BondCount.key in properties:
        BondCount.set(frame, len(frame.bond_pairs))

    return frame


def _get_mdanalysis_group_bonds(group: AtomGroup, properties: Collection[str], frame: FrameData,
                                particle_ix_to_index: Dict[int, int]) -> None:
    if BondPairs.key in properties or BondCount.key in properties:
        bond_pairs = []

        for indices in group.atoms.bonds.indices:
            try:
                i = particle_ix_to_index[indices[0]]
                j = particle_ix_to_index[indices[1]]
                bond_pairs.append([i, j])
            except KeyError:
                pass
        if BondPairs.key in properties:
            BondPairs.set(frame, bond_pairs)
        if BondCount.key in properties:
            BondCount.set(frame, len(bond_pairs))


def mdanalysis_atomgroup_to_frame(group: AtomGroup, properties: Collection[str],
                                  frame: Optional[FrameData] = None) -> FrameData:
    if frame is None:
        frame = FrameData()

    particle_ix_to_index, residue_ix_to_index, segment_ix_to_index = _create_ix_to_indices(group)

    frame_data = FrameData()

    _get_mdanalysis_group_counts(group, properties, frame)

    if ParticlePositions.key in properties:
        ParticlePositions.set(frame, group.positions * 0.1)
    if ParticleNames.key in properties:
        ParticleNames.set(frame, group.names)
    if ParticleElements.key in properties:
        ParticleElements.set(frame, [
            ELEMENT_INDEX[guess_atom_element(name).capitalize()]
            for name in group.types
        ])
    if ParticleResidues.key in properties:
        ParticleResidues.set(frame, [residue_ix_to_index[ix] for ix in group.resindices])
    if ResidueNames.key in properties:
        ResidueNames.set(frame, group.residues.resnames)

    if ResidueChains.key in properties:
        ResidueChains.set(frame, [segment_ix_to_index[ix] for ix in group.residues.segindices])

    _get_mdanalysis_group_bonds(group, properties, frame, particle_ix_to_index)

    return frame_data


def mdanalysis_atomgroup_to_indices(group: AtomGroup) -> List[int]:
    idx_array = group.indices
    return list(map(int, idx_array))


def _create_ix_to_indices(group: AtomGroup) -> Tuple[Dict[int, int], Dict[int, int], Dict[int, int]]:
    particle_ix_to_index = {particle_ix: index for index, particle_ix in enumerate(group.ix)}
    residue_ix_to_index = {residue_ix: index for index, residue_ix in enumerate(group.residues.ix)}
    segment_ix_to_index = {segment_ix: index for index, segment_ix in enumerate(group.segments.ix)}

    return particle_ix_to_index, residue_ix_to_index, segment_ix_to_index


def _get_mdanalysis_group_counts(group: AtomGroup, properties: Collection[str], frame: FrameData) -> None:
    if ParticleCount.key in properties:
        ParticleCount.set(frame, len(group))
    if ResidueCount.key in properties:
        ResidueCount.set(frame, len(group.residues))
    if ChainCount.key in properties:
        ChainCount.set(frame, len(group.segments))
