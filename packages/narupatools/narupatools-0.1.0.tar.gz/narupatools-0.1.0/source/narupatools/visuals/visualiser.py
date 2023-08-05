"""
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

from typing import Union, Optional

from narupatools.visuals.typing import SerializableDictionary

Subgraph = Union[str, SerializableDictionary]


class Visualiser:

    @classmethod
    def create(cls,
               type: Subgraph,
               color: Optional[Subgraph] = None,
               scale: Optional[Subgraph] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["render"] = type
        if color is not None:
            data["color"] = color
        if scale is not None:
            data["scale"] = scale
        return data
