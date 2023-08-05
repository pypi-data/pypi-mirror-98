"""
Conversion functions for converting ASE objects to Narupa objects.

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
from contextlib import suppress
from typing import Optional, Collection, Dict, Any

import ase.units as units
from ase.atoms import Atoms
from ase.calculators.calculator import PropertyNotImplementedError
from narupa.trajectory.frame_data import FrameData

from narupatools.frame import ParticlePositions, ParticleCount, ParticleElements, BoxVectors, \
    ParticleMasses, ParticleVelocities, ParticleForces, KineticEnergy, PotentialEnergy, ParticleCharges, ResidueNames, \
    ParticleNames, ParticleResidues, ResidueCount

FS_TO_ASE_TIME = units.fs
PS_TO_ASE_TIME = units.fs * 1000.0
KJMOL_TO_EV = units.kJ / units.mol
KCALMOL_TO_EV = units.kcal / units.mol

ASE_TIME_TO_PS = 1.0 / PS_TO_ASE_TIME

NM_TO_ANG = units.nm
EV_TO_KJMOL = 1.0 / KJMOL_TO_EV
ANG_TO_NM = 1.0 / NM_TO_ANG

ASE_PROPERTIES = (
    ParticlePositions.key, ParticleElements.key, BoxVectors.key, ParticleCount.key, ResidueNames.key, ParticleNames.key,
    ParticleResidues.key, ResidueCount.key)


def ase_atoms_to_frame(atoms: Atoms, properties: Collection[str] = ASE_PROPERTIES,
                       frame: Optional[FrameData] = None) -> FrameData:
    """
    Convert an ASE Atoms object to a Narupa FrameData.

    :param atoms: ASE Atoms object to convert.
    :param properties: A collection of keys that should be added to the frame if available.
    :param frame: An optional preexisting FrameData to populate.
    :return: A FrameData populated with information available in the ASE atoms object whose keys are present in
        the properties parameter.
    """
    if frame is None:
        frame = FrameData()

    _add_ase_atoms_particles_to_frame(atoms, properties, frame)
    _add_ase_atoms_residues_to_frame(atoms, properties, frame)
    if BoxVectors.key in properties:
        # todo: is this copy necessary?
        BoxVectors.set(frame, atoms.get_cell().copy() * ANG_TO_NM)

    if KineticEnergy.key in properties:
        KineticEnergy.set(frame, atoms.get_kinetic_energy() * EV_TO_KJMOL)

    if PotentialEnergy.key in properties:
        with suppress(PropertyNotImplementedError):
            PotentialEnergy.set(frame, atoms.get_potential_energy() * EV_TO_KJMOL)

    return frame


def _add_ase_atoms_particles_to_frame(atoms: Atoms, properties: Collection[str], frame: FrameData) -> None:
    if ParticlePositions.key in properties:
        ParticlePositions.set(frame, atoms.get_positions() * ANG_TO_NM)

    if ParticleCharges.key in properties:
        ParticleCharges.set(frame, atoms.get_charges())

    if ParticleCount.key in properties:
        ParticleCount.set(frame, len(atoms))

    if ParticleElements.key in properties:
        elements = []
        for atom in atoms:
            elements.append(atom.number)

        ParticleElements.set(frame, elements)

    if ParticleMasses.key in properties:
        ParticleMasses.set(frame, atoms.get_masses())

    if ParticleVelocities.key in properties:
        ParticleVelocities.set(frame, atoms.get_velocities() * ANG_TO_NM / ASE_TIME_TO_PS)

    if ParticleForces.key in properties:
        ParticleForces.set(frame, atoms.get_forces() * EV_TO_KJMOL * ANG_TO_NM)

    if ParticleNames.key in properties and 'atomtypes' in atoms.arrays:
        ParticleNames.set(frame, atoms.arrays['atomtypes'])


def _add_ase_atoms_residues_to_frame(atoms: Atoms, properties: Collection[str], frame: FrameData) -> None:
    if (ResidueNames.key in properties or ResidueCount.key in properties or ParticleResidues.key in properties) \
            and 'residuenumbers' in atoms.arrays:
        segid_to_index: Dict[Any, int] = {}
        res_to_first_particle_index = []
        index = 0
        for atom_index, segid in enumerate(atoms.arrays['residuenumbers']):
            if segid not in segid_to_index:
                segid_to_index[segid] = index
                res_to_first_particle_index.append(atom_index)
                index += 1

        if ParticleResidues.key in properties:
            ParticleResidues.set(frame, [segid_to_index[segid] for segid in atoms.arrays['residuenumbers']])

        if ResidueNames.key in properties and 'residuenames' in atoms.arrays:
            ResidueNames.set(frame, [str(atoms.arrays['residuenames'][atom_index]).strip() for atom_index in
                                     res_to_first_particle_index])

        if ResidueCount.key in properties and 'residuenames' in atoms.arrays:
            ResidueCount.set(frame, len(res_to_first_particle_index))
