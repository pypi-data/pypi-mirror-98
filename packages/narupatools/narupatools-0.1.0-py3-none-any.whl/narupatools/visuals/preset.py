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


class Preset:

    @classmethod
    def ball_and_stick(cls) -> str:
        return "ball and stick"

    @classmethod
    def cartoon(cls) -> str:
        return "cartoon"

    @classmethod
    def cycles(cls) -> str:
        return "cycles"

    @classmethod
    def geometric_spline(cls) -> str:
        return "geometric spline"

    @classmethod
    def goodsell(cls) -> str:
        return "goodsell"

    @classmethod
    def hydrogen_caps(cls) -> str:
        return "hydrogen caps"

    @classmethod
    def hyperballs(cls) -> str:
        return "hyperballs"

    @classmethod
    def liquorice(cls) -> str:
        return "liquorice"

    @classmethod
    def noodles(cls) -> str:
        return "noodles"

    @classmethod
    def peptide_planes(cls) -> str:
        return "peptide planes"

    @classmethod
    def spline(cls) -> str:
        return "spline"

    @classmethod
    def vdw(cls) -> str:
        return "vdw"
