"""
Defines objects that can be easily serialized and deserialized to a form that is compatible with serialization
formats such as JSON or protobuf.

Most serialization methods only work with primitive types (strings, floats and booleans), along with nest lists
and string-valued dictionaries of these types. It is therefore a common problem of wanting to have a class be
able to be serialized into these formats. This often means writing custom serialization and deserialization code
for each class you define.

SerializableObject is a metaclass for any object which is saying to Narupa that it can be converted to and from a form
that is serializable, and provides the load() and save() methods to do so.

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

from narupatools.state.typing import Serializable


class SerializableObject:
    __metaclass__ = ABCMeta
    """
    A base class for objects which can be converted to and from a form that is serializable by protobuf (consisting of
    primitive types, lists and dictionaries).
    """

    @classmethod
    def deserialize(cls, value: Serializable) -> 'SerializableObject':
        """
        Generate an object by reading data from a dictionary. Keys which share a name with a property will use that
        property's setter, whilst other keys will be stored as arbitrary data which can be accessed using an item
        accessor.
        """
        raise NotImplementedError

    @abstractmethod
    def serialize(self) -> Serializable:
        """
        Save the object to a dictionary. All properties and arbitrary data will be writen to the dictionary.
        """
        raise NotImplementedError
