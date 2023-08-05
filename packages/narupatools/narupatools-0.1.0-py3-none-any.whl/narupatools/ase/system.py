"""
Simple wrapper around an ASE atoms object.

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

from typing import Collection

from ase import Atoms
from narupa.trajectory import FrameData

from narupatools.ase import ase_atoms_to_frame
from narupatools.frame.frame_source import FrameSource


class ASESystem(FrameSource):
    """Wrapper around an ASE `Atoms` object so it is exposed consistently."""

    def __init__(self, atoms: Atoms):
        """
        Create a wrapper around the given ASE `Atoms` object.

        :param atoms: ASE `Atoms` to wrap.
        """
        self._atoms = atoms

    def get_frame(self, fields: Collection[str]) -> FrameData:  # noqa: D102
        return ase_atoms_to_frame(self._atoms, fields)
