"""
Classes derived from Structure that allow NGLView to render new systems.

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

from io import StringIO

import nglview
from ase.atoms import Atoms
from ase.io import write
from narupa.ase.converter import frame_data_to_ase
from narupa.trajectory.frame_data import FrameData


class ASEStructure(nglview.Structure):
    """
    ASE Structure for nglview that does not use temporary files.
    """

    def __init__(self, atoms: Atoms) -> None:
        super().__init__()
        self.atoms = atoms

    def get_structure_string(self) -> str:
        file = StringIO("")
        write(file, self.atoms, 'proteindatabank')
        return file.getvalue()


class FrameDataStructure(ASEStructure):
    """
    FrameData Structure for nglview that does not use temporary files.
    """

    def __init__(self, frame_data: FrameData) -> None:
        super().__init__(frame_data_to_ase(frame_data, True, True))
