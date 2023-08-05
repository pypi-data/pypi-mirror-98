"""
Implementation of IMD for an ASE dynamics simulation as dynamics restraints added and removed from the ASE atoms object.

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

from __future__ import annotations

from typing import Dict, Mapping, Any

import narupatools.ase.dynamics as dynamics
import numpy as np
from ase import Atoms
from narupa.imd import ParticleInteraction
from narupatools.ase.constraints.imd_constraint import InteractionConstraint
from narupatools.core.dynamics import SimulationDynamics
from narupatools.core.event import Event, EventListener
from narupatools.core.session import NarupaSession
from typing_extensions import Protocol


class OnStartInteractionCallback(Protocol):
    def __call__(self, *, key: str, interaction: ParticleInteraction) -> None:
        ...


class OnEndInteractionCallback(Protocol):
    def __call__(self, *, key: str, work_done: float, duration: float) -> None:
        ...


class InteractionsSource(Protocol):
    @property
    def active_interactions(self) -> Mapping[str, ParticleInteraction]:
        ...


class ASEImdProvider:
    current_interactions: Dict[str, InteractionConstraint]
    _on_start_interaction: Event[OnStartInteractionCallback]
    _on_end_interaction: Event[OnEndInteractionCallback]

    def __init__(self,
                 imd_source: InteractionsSource,
                 atoms: Atoms,
                 dynamics: SimulationDynamics):

        self._imd_source = imd_source
        self._atoms = atoms
        self._dynamics = dynamics
        self._dynamics.on_pre_step.add_callback(self._on_pre_step)
        self._dynamics.on_post_step.add_callback(self._on_post_step)
        self._dynamics.on_reset.add_callback(self._on_reset)

        self.current_interactions = {}

        self._on_start_interaction = Event()
        self._on_end_interaction = Event()

        self._has_reset = True

    def close(self) -> None:
        self._dynamics.on_pre_step.remove_callback(self._on_pre_step)
        self._dynamics.on_post_step.remove_callback(self._on_post_step)
        self._dynamics.on_reset.remove_callback(self._on_reset)

    @classmethod
    def add_to_dynamics(cls, dynamics: dynamics.ASEDynamics, session: NarupaSession) -> ASEImdProvider:
        source = session.server.imd
        atoms = dynamics.atoms
        return ASEImdProvider(source, atoms, dynamics)

    @property
    def on_start_interaction(self) -> EventListener[OnStartInteractionCallback]:
        return self._on_start_interaction

    @property
    def on_end_interaction(self) -> EventListener[OnEndInteractionCallback]:
        return self._on_end_interaction

    @property
    def total_work(self) -> float:
        total_work = [interaction.total_work for interaction in self.current_interactions.values()]
        return np.array(total_work).sum()  # type:ignore

    @property
    def work_last_step(self) -> float:
        work_last_step = [interaction.work_last_step for interaction in self.current_interactions.values()]
        return np.array(work_last_step).sum()  # type:ignore

    @property
    def potential_energy(self) -> float:
        potential_energy = [interaction.energy for interaction in self.current_interactions.values()]
        return np.array(potential_energy).sum()  # type:ignore

    def _on_pre_step(self, **kwargs: Any) -> None:
        """
        Called before each dynamics step. Here we will update the interactions and corresponding constraints.
        """
        interactions = self._imd_source.active_interactions
        for key in list(self.current_interactions.keys()):
            if self._has_reset or key not in interactions.keys():
                constraint = self._remove_interaction(key)
                end_time = self._dynamics.total_time
                duration = end_time - constraint.start_time
                self._on_end_interaction.invoke(key=key, work_done=constraint.total_work, duration=duration)
            self._has_reset = False

        for key in interactions.keys():
            if key not in self.current_interactions.keys():
                self._add_interaction(key, interactions[key])
                self._on_start_interaction.invoke(key=key, interaction=interactions[key])
            else:
                self.current_interactions[key].interaction = interactions[key]

        for interaction in self.current_interactions.values():
            interaction.on_pre_step(self._atoms)

    def _on_post_step(self, **kwargs: Any) -> None:
        for interaction in self.current_interactions.values():
            interaction.on_post_step(self._atoms)

    def _add_interaction(self, key: str, interaction: ParticleInteraction) -> None:
        constraint = InteractionConstraint(key, interaction, self._dynamics.total_time)
        self.current_interactions[key] = constraint
        self._atoms.constraints.append(constraint)

    def _remove_interaction(self, key: str) -> InteractionConstraint:
        constraint = self.current_interactions[key]
        del self.current_interactions[key]
        self._atoms.constraints.remove(constraint)
        return constraint

    def _on_reset(self, **kwargs: Any) -> None:
        self._has_reset = True
