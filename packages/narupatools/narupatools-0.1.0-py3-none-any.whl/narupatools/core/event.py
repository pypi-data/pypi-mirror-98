"""
Event-based callback system with support for typing.

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

Originally part of the narupa-core package. Adapted under the terms of the GPL.
"""

from __future__ import annotations

import contextlib
import warnings
from inspect import signature, Parameter, Signature
from typing import TypeVar, Generic, List, Any, Callable, Optional, Type, AbstractSet

from typing_extensions import Protocol

TCallback = TypeVar('TCallback', contravariant=True)


class EventListener(Protocol[TCallback]):

    def add_callback(self, callback: TCallback) -> None:
        ...

    def remove_callback(self, callback: TCallback) -> None:
        ...


TEventCallback = TypeVar('TEventCallback', bound=Callable[..., None])


class Event(Generic[TEventCallback]):
    """
    A class which stores a set of callbacks, which are invoked when an event is published.

    The narupatools version of Event also performs some simple type checking, to ensure that callbacks support all the
    parameters that this event produces. It also prints a warning if an added callback does not handle generic **kwargs,
    which is good practise that future proof callbacks.
    """

    _callbacks: List[TEventCallback]
    _parameter_names: AbstractSet[str]

    def __init__(self, callback_type: Optional[Type] = None) -> None:
        self._callbacks = []
        self._parameter_names = set()
        if callback_type is not None:
            with contextlib.suppress(AttributeError):
                self._parameter_names = _get_named_parameters(signature(callback_type.__call__))

    def add_callback(self, callback: TEventCallback) -> None:
        """
        Add a callback to this event, which will be invoked everytime this event is invoked.

        :param callback: The callback to be called when this event is triggered
        """
        callback_signature = signature(callback)

        has_kwargs = any(param.kind == Parameter.VAR_KEYWORD for param in callback_signature.parameters.values())

        if not has_kwargs:
            warnings.warn("Adding callback which doesn't take **kwargs. This makes it susceptible to breaking if new "
                          "parameters are added to the event.")

        if not has_kwargs and len(self._parameter_names) > 0:
            params = _get_named_parameters(callback_signature)
            missing_params = self._parameter_names - params
            if len(missing_params) > 0:
                raise ValueError(f"Invalid callback for event - missing parameter(s) with name(s) {missing_params}. "
                                 "Either add these parameters to the callback or use **kwargs.")

        self._callbacks.append(callback)

    def remove_callback(self, callback: TEventCallback) -> None:
        """
        Remove a callback from this event.

        :param callback: The callback to be removed from this event's callbacks
        """
        self._callbacks.remove(callback)

    @property
    def invoke(self) -> TEventCallback:
        """Invoke the callbacks associated with this event with the provided arguments."""

        def _invoke(*args: Any, **kwargs: Any) -> None:
            for callback in self._callbacks:
                callback(*args, **kwargs)

        return _invoke  # type: ignore


def _get_named_parameters(func_signature: Signature) -> AbstractSet[str]:
    return {name for name, param in func_signature.parameters.items() if
            (param.kind == Parameter.POSITIONAL_OR_KEYWORD
             or param.kind == Parameter.KEYWORD_ONLY)
            and name != "self"}
