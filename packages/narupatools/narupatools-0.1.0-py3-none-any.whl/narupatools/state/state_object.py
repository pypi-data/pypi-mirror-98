"""
SharedStateObject is an implementation of a SerializableObject, that can store arbitrary data as a dictionary, but also
automatically use any properties defined in the class. In most cases, this class is the appropriate one to subclass
for defining a specific kind of object that's storable in the shared state dictionary.

.. code:: python

    from narupa.state.state_object import SharedStateObject


    # Define a custom class, with a property x that must be non-negative.
    class MyObject(SharedStateObject):

        _x: int

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            x = 0

        @property
        def x(self) -> int:
            return self._x

        @x.setter
        def x(self, value):
            if value < 0:
                value = 0
            self._x = value


    # Define a dictionary we want to deserialize
    dictionary = {'x': -1, 'y': 2}

    # Create the object using the class method load()
    myobj = MyObject.load(dictionary)

    # Check that the property setter was called
    print(myobj['x'])  # we could also use myobj.x

    # Check that y was also stored
    print(myobj['y'])

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

from collections.abc import Mapping
from typing import Dict, ClassVar, Union, Any

from narupatools.state.typing import Serializable
from .serializable_object import SerializableObject


class SharedStateObject(SerializableObject):
    """
    A base class for an object which is stored in the shared state dictionary as a dictionary, which stores arbitrary
    fields of serializable data. Any properties that are defined on a subclass of SharedStateObject are
    serialized automatically, calling their get and set methods as appropriate.
    """

    _arbitrary_data: Dict[str, Serializable]
    _serializable_properties: ClassVar[Dict[str, property]] = {}

    def __init__(self, **kwargs: Serializable):
        self._arbitrary_data = kwargs

    def __init_subclass__(cls, **kwargs: Any):
        # Find all properties in this class
        cls._serializable_properties = {}
        for key, value in cls.__dict__.items():
            if isinstance(value, property):
                cls._serializable_properties[key] = value

    @classmethod
    def deserialize(cls, value: Serializable) -> 'SharedStateObject':
        obj = cls()
        if isinstance(value, Mapping):
            obj._arbitrary_data = {k: v for k, v in value.items()}
        for key, python_property in cls._serializable_properties.items():
            if key in obj._arbitrary_data:
                python_property.fset(obj, obj._arbitrary_data.pop(key))  # type: ignore
        return obj

    def serialize(self) -> Dict[str, Serializable]:
        dictionary = {k: v for k, v in self._arbitrary_data.items()}
        for key, python_property in self.__class__._serializable_properties.items():
            value = python_property.fget(self)  # type: ignore
            if value is not None:  # Only save non None values
                dictionary[key] = value
        return dictionary

    def __setitem__(self, key: str, value: Union[Serializable, Any]) -> None:
        """
        Set a value, using a property if the key corresponds to a property of this object and using an internal
        dictionary for other arbitrary values

        :param key: The key to store the value under. This will be the key used in the serialized form of this object
        :param value: The value to be stored. If key does not correspond to a property, this value must be
                      serializable. If the key does correspond to a property, then the properties setter must be
                      able to handle converting the value to something serializable
        """
        if key in self.__class__._serializable_properties:
            self.__class__._serializable_properties[key].fset(self, value)  # type: ignore
        else:
            self._arbitrary_data[key] = value

    def __getitem__(self, key: str) -> Serializable:
        """
        Get a value, using a property if the key corresponds to a property of this object and using an internal
        dictionary for other arbitrary values

        :param key: The key to store the value under. This will be the key used in the serialized form of this object

        :raises KeyError: If the given key is not present
        """
        if key in self.__class__._serializable_properties:
            return self.__class__._serializable_properties[key].fget(self)  # type: ignore
        else:
            return self._arbitrary_data[key]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SharedStateObject) and self._arbitrary_data == other._arbitrary_data
