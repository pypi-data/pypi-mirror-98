"""
An ASE constraint that triggers events when things change.

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

import numpy as np
from ase.atoms import Atoms
from narupa.utilities.event import Event
from narupatools.core.event import EventListener

from .constraint import ASEConstraint


class ASEObserver(ASEConstraint):
    """ASE `Constraint` which acts as a listener for when an ASE `Atoms` object has its positions modified."""

    def __init__(self) -> None:
        """Create a new `ASEObserver`."""
        self._on_set_positions = Event()

    @property
    def on_set_positions(self) -> EventListener:
        """Event triggered when the wrapped ASE `Atoms` object has its positions modified."""
        return self._on_set_positions

    def adjust_positions(self, atoms: Atoms, positions: np.ndarray) -> None:  # noqa: D102
        self._on_set_positions.invoke()

    def adjust_forces(self, atoms: Atoms, forces: np.ndarray) -> None:  # noqa: D102
        pass
