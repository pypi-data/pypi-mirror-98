"""
Base class for trajectories that can be played back.

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

from abc import ABCMeta, abstractmethod
from typing import Collection

from narupa.trajectory import FrameData

from .playable import Playable
from ..frame.frame_source import FrameSource


class TrajectoryPlayback(Playable, FrameSource, metaclass=ABCMeta):
    _looping: bool

    def __init__(self, playback_interval: float = 0.1, looping: bool = True):
        """
        Create a new playback for a trajectory.
        :param playback_interval: The interval between consecutive trajectory frames as it is played back, in seconds.
        :param looping: Should playback restart from the beginning when the end of the trajectory is reached.
        """
        super().__init__(playback_interval)
        self._looping = looping
        self._index = 0

    @property
    def looping(self) -> bool:
        """Should playback restart from the beginning when the end of the trajectory is reached."""
        return self._looping

    @abstractmethod
    def _trajectory_length(self) -> int:
        """Length of the trajectory."""
        pass

    @abstractmethod
    def get_frame(self, fields: Collection[str]) -> FrameData:
        """
        Get the `FrameData` representing the current frame of the trajectory.

        :param fields: Collection of fields to include in the `FrameData`.
        :return: A Narupa `FrameData` representing the current frame of the trajectory.
        """
        pass

    @property
    def index(self) -> int:
        """Index of the current frame in the trajectory."""
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        if value < 0 or value >= self._trajectory_length():
            raise IndexError(f"Cannot set trajectory index {value}")
        self._index = value

    def _advance(self) -> bool:
        self._index += 1
        if self._index > self._trajectory_length():
            if self.looping:
                self._index = 0
            else:
                return False
        return True

    def _restart(self) -> None:
        self._index = 0
