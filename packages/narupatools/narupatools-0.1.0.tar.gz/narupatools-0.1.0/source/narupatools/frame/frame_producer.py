"""
Loop which tracks which fields of a system are dirty and produces frame data compatible with this.

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

from typing import Optional, Collection, Set

from narupa.trajectory import FrameData
from typing_extensions import Protocol

from narupatools.core.event import EventListener, Event
from narupatools.core.playable import Playable
from narupatools.frame import ParticlePositions, ParticleElements, ParticleNames, ParticleTypes, ParticleResidues, \
    ResidueNames, ResidueChains, ChainNames, ParticleCount, ResidueCount, ChainCount, BondCount, BondPairs, \
    KineticEnergy, PotentialEnergy, BoxVectors


class ProduceFrameCallback(Protocol):
    def __call__(self, *, fields: Collection[str]) -> FrameData:
        ...


class OnFrameProducedCallback(Protocol):
    def __call__(self, *, frame: FrameData) -> None:
        ...


DEFAULT_FIELDS = (ParticlePositions.key, ParticleElements.key, ParticleNames.key, ParticleTypes.key,
                  ParticleResidues.key, ResidueNames.key, ResidueChains.key, ChainNames.key, ParticleCount.key,
                  ResidueCount.key, ChainCount.key, BondCount.key, BondPairs.key, KineticEnergy.key,
                  PotentialEnergy.key, BoxVectors.key)


class FrameProducer(Playable):
    """
    A FrameProducer operates on a background thread, and at specified intervals produces a FrameData and triggers the
    on_frame_produced event. However, it only does this if the frame has been marked as dirty by using mark_dirty.
    If mark_dirty is provided a set of fields that have changed, then only these fields will then be added to the
    produced frame data.
    """

    _produce: ProduceFrameCallback
    _is_dirty: bool
    _fields: Set[str]
    _dirty_fields: Set[str]
    _on_frame_produced: Event[OnFrameProducedCallback]

    def __init__(self, produce: ProduceFrameCallback, fields: Collection[str] = DEFAULT_FIELDS,
                 frame_interval: float = 1.0 / 30.0):
        super().__init__(frame_interval)
        self._produce = produce
        self._is_dirty = True
        self._fields = set(fields)
        self._dirty_fields = set(fields)
        self._on_frame_produced = Event()

    def add_field(self, field: str) -> None:
        """
        Add a field that should be produced if possible.
        """
        self._fields.add(field)
        self._dirty_fields.add(field)

    @property
    def on_frame_produced(self) -> EventListener[OnFrameProducedCallback]:
        return self._on_frame_produced

    def mark_dirty(self, fields: Optional[Collection[str]] = None) -> None:
        """
        Inform the frame producer that the frame is dirty, and hence a new frame needs producing.
        """
        self._is_dirty = True
        if fields is None:
            self._dirty_fields = set(self._fields)
        else:
            self._dirty_fields = self._dirty_fields | (self._fields & set(fields))

    def _advance(self) -> bool:
        if self._is_dirty:
            frame = self._produce(fields=self._dirty_fields)
            self._on_frame_produced.invoke(frame=frame)
            self._is_dirty = False
            self._dirty_fields = set()
        return True

    def _restart(self) -> None:
        pass
