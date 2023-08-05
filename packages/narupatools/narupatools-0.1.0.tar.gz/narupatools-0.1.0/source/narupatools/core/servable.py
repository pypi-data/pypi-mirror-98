from __future__ import annotations

from abc import abstractmethod, ABCMeta

import narupatools.core.session as session


class Servable(metaclass=ABCMeta):

    @abstractmethod
    def start_being_served(self, server: session.NarupaSession) -> None:
        ...

    @abstractmethod
    def end_being_served(self, server: session.NarupaSession) -> None:
        ...
