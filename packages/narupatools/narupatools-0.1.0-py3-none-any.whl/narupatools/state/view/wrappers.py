"""
Both the client and the server have access to a shared state dictionary and can make modifications,
however the API for each of these is slightly different.

SharedStateClientWrapper and SharedStateServerWrapper are implementations of the more general
SerializableDictionary. SerializableDictionary is just a alias for a mutable mapping or dictionary
from string keys to serializable values, which is what a shared state dictionary is.
This exposes both shared state dictionaries in a pythonic and unified way, that is also
compatible with using a standard dictionary for testing.

These classes are not intended to be use directly. Both NarupaImdClient and NarupaServer have a
shared_state property which returns a SerializableDictionary, which uses these two classes internally.

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

from typing import Iterator, MutableMapping

from narupa.app import NarupaImdClient
from narupa.core import NarupaServer, NarupaClient
from narupa.utilities.change_buffers import DictionaryChange

from narupatools.state.typing import Serializable


class SharedStateClientWrapper(MutableMapping[str, Serializable]):
    """A wrapper around a client side shared state that exposes it as a mutable mapping."""

    _client: NarupaImdClient

    def __init__(self, client: NarupaImdClient):
        self._client = client

    def _multiplayer_client(self) -> NarupaClient:
        client = self._client._multiplayer_client
        if client is None:
            raise ValueError("Client is not connected to Multiplayer")
        return client

    def __getitem__(self, key: str) -> Serializable:
        return self._client.get_shared_value(key)  # type: ignore

    def __setitem__(self, key: str, value: Serializable) -> None:
        self._client.set_shared_value(key, value)

    def __delitem__(self, key: str) -> None:
        self[key]  # Throws KeyError if value not found
        self._client.remove_shared_value(key)

    def __iter__(self) -> Iterator[str]:
        with self._multiplayer_client().lock_state() as state:
            keys = state.keys()
        return keys.__iter__()

    def __len__(self) -> int:
        with self._multiplayer_client().lock_state() as state:
            keys = state.keys()
        return len(keys)


class SharedStateServerWrapper(MutableMapping[str, Serializable]):
    """A wrapper around an actual state dictionary that exposes it as a mutable mapping."""

    _server: NarupaServer

    def __init__(self, server: NarupaServer):
        self._server = server

    def __getitem__(self, key: str) -> Serializable:
        with self._server.lock_state() as dict:
            return dict[key]  # type: ignore

    def __setitem__(self, key: str, value: Serializable) -> None:
        self._server.update_state(None, DictionaryChange(updates={key: value}))

    def __delitem__(self, key: str) -> None:
        with self._server.lock_state() as dict:
            if key not in dict:
                raise KeyError
        self._server.update_state(None, DictionaryChange(removals={key}))

    def __iter__(self) -> Iterator[str]:
        with self._server.lock_state() as dict:
            return dict.__iter__()

    def __len__(self) -> int:
        with self._server.lock_state() as dict:
            return dict.__len__()
