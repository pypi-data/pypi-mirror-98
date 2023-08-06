#   coding:utf-8
#   This file is part of DancingCell.
#
#   DancingCell is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = '2019/05/27 15:13:16'

import os
import json
from io import open
from enum import Enum

# import re
# from pymatgen.core.units import FloatWithUnit, Unit, SUPPORTED_UNIT_NAMES, Mass, Length, unitized
# import warnings
# import numpy as np
# from pymatgen.util.string import formula_double_format
# from monty.json import MSONable
# from itertools import product, combinations
# from collections import Counter

with open(os.path.join(os.path.dirname(__file__),
                       "periodic_table.json"), "rt") as f:
    PTINFO = json.load(f)

PTROWSIZE = (2, 8, 8, 18, 18, 32, 32)


class Element(Enum):

    H = "H"
    He = "He"
    Li = "Li"
    Be = "Be"
    B = "B"
    C = "C"
    N = "N"
    O = "O"
    F = "F"
    Ne = "Ne"
    Na = "Na"
    Mg = "Mg"
    Al = "Al"
    Si = "Si"
    P = "P"
    S = "S"
    Cl = "Cl"
    Ar = "Ar"
    K = "K"
    Ca = "Ca"
    Sc = "Sc"
    Ti = "Ti"
    V = "V"
    Cr = "Cr"
    Mn = "Mn"
    Fe = "Fe"
    Co = "Co"
    Ni = "Ni"
    Cu = "Cu"
    Zn = "Zn"
    Ga = "Ga"
    Ge = "Ge"
    As = "As"
    Se = "Se"
    Br = "Br"
    Kr = "Kr"
    Rb = "Rb"
    Sr = "Sr"
    Y = "Y"
    Zr = "Zr"
    Nb = "Nb"
    Mo = "Mo"
    Tc = "Tc"
    Ru = "Ru"
    Rh = "Rh"
    Pd = "Pd"
    Ag = "Ag"
    Cd = "Cd"
    In = "In"
    Sn = "Sn"
    Sb = "Sb"
    Te = "Te"
    I = "I"
    Xe = "Xe"
    Cs = "Cs"
    Ba = "Ba"
    La = "La"
    Ce = "Ce"
    Pr = "Pr"
    Nd = "Nd"
    Pm = "Pm"
    Sm = "Sm"
    Eu = "Eu"
    Gd = "Gd"
    Tb = "Tb"
    Dy = "Dy"
    Ho = "Ho"
    Er = "Er"
    Tm = "Tm"
    Yb = "Yb"
    Lu = "Lu"
    Hf = "Hf"
    Ta = "Ta"
    W = "W"
    Re = "Re"
    Os = "Os"
    Ir = "Ir"
    Pt = "Pt"
    Au = "Au"
    Hg = "Hg"
    Tl = "Tl"
    Pb = "Pb"
    Bi = "Bi"
    Po = "Po"
    At = "At"
    Rn = "Rn"
    Fr = "Fr"
    Ra = "Ra"
    Ac = "Ac"
    Th = "Th"
    Pa = "Pa"
    U = "U"
    Np = "Np"
    Pu = "Pu"
    Am = "Am"
    Cm = "Cm"
    Bk = "Bk"
    Cf = "Cf"
    Es = "Es"
    Fm = "Fm"
    Md = "Md"
    No = "No"
    Lr = "Lr"

    def __init__(self, symbol):
        self.symbol = "%s" % symbol
        d = PTINFO[symbol]

        # Store key variables for quick access
        self.Z = d["Atomic no"]

        self.atomic_radius = d.get("Atomic radius", None)
        self.atomic_mass = d.get(["Atomic mass"], None)
        self.long_name = d["Name"]
        self._data = d

    def __getattr__(self, item):
        if item in ["mendeleev_no", "electrical_resistivity",
                    "velocity_of_sound", "reflectivity",
                    "refractive_index", "poissons_ratio", "molar_volume",
                    "electronic_structure", "thermal_conductivity",
                    "boiling_point", "melting_point",
                    "critical_temperature", "superconduction_temperature",
                    "liquid_range", "bulk_modulus", "youngs_modulus",
                    "brinell_hardness", "rigidity_modulus",
                    "mineral_hardness", "vickers_hardness",
                    "density_of_solid", "atomic_radius_calculated",
                    "van_der_waals_radius", "atomic_orbitals",
                    "coefficient_of_linear_thermal_expansion",
                    "ground_state_term_symbol", "valence"]:
            kstr = item.capitalize().replace("_", " ")
            val = self._data.get(kstr, None)
            if str(val).startswith("no data"):
                val = None
            elif type(val) == dict:
                pass
            else:
                try:
                    val = float(val)
                except ValueError:
                    val = None
            return val
        raise AttributeError("Element has no attribute %s!" % item)

    @property
    def data(self):
        """
        Returns dict of data for element.
        """
        return self._data.copy()

    @property
    def number(self):
        """Alternative attribute for atomic number"""
        return self.Z

    @property
    def icsd_oxidation_states(self):
        """Tuple of all oxidation states with at least 10 instances in
        ICSD database AND at least 1% of entries for that element"""
        return tuple(self._data.get("ICSD oxidation states", list()))

    def __eq__(self, other):
        return isinstance(other, Element) and self.Z == other.Z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.Z

    def __repr__(self):
        return "Element " + self.symbol

    def __str__(self):
        return self.symbol

    def __lt__(self, other):
        """
        Sets a default sort order for atomic species by electronegativity. Very
        useful for getting correct formulas.  For example, FeO4PLi is
        automatically sorted into LiFePO4.
        """
        x1 = float("inf") if self.X != self.X else self.X
        x2 = float("inf") if other.X != other.X else other.X
        if x1 != x2:
            return x1 < x2
        else:
            # There are cases where the electronegativity are exactly equal.
            # We then sort by symbol.
            return self.symbol < other.symbol

    @staticmethod
    def from_Z(z):
        """
        Get an element from an atomic number.

        Args:
            z (int): Atomic number

        Returns:
            Element with atomic number z.
        """
        for sym, data in PTINFO.items():
            if data["Atomic no"] == z:
                return Element(sym)
        raise ValueError("No element with this atomic number %s" % z)

    @staticmethod
    def from_row_and_group(row, group):
        """
        Returns an element from a row and group number.

        Args:
            row (int): Row number
            group (int): Group number

        .. note::
            The 18 group number system is used, i.e., Noble gases are group 18.
        """
        for sym in PTINFO.keys():
            el = Element(sym)
            if el.row == row and el.group == group:
                return el
        raise ValueError("No element with this row and group!")

    @staticmethod
    def is_valid_symbol(symbol):
        """
        Returns true if symbol is a valid element symbol.

        Args:
            symbol (str): Element symbol

        Returns:
            True if symbol is a valid element (e.g., "H"). False otherwise
            (e.g., "Zebra").
        """
        try:
            Element(symbol)
            return True
        except:
            return False

    @property
    def row(self):
        """
        Returns the periodic table row of the element.
        """
        z = self.Z
        total = 0
        if 57 <= z <= 71:
            return 8
        elif 89 <= z <= 103:
            return 9

        for i in range(len(PTROWSIZE)):
            total += PTROWSIZE[i]
            if total >= z:
                return i + 1
        return 8

    @property
    def group(self):
        """
        Returns the periodic table group of the element.
        """
        z = self.Z
        if z == 1:
            return 1
        if z == 2:
            return 18
        if 3 <= z <= 18:
            if (z - 2) % 8 == 0:
                return 18
            elif (z - 2) % 8 <= 2:
                return (z - 2) % 8
            else:
                return 10 + (z - 2) % 8

        if 19 <= z <= 54:
            if (z - 18) % 18 == 0:
                return 18
            else:
                return (z - 18) % 18

        if (z - 54) % 32 == 0:
            return 18
        elif (z - 54) % 32 >= 18:
            return (z - 54) % 32 - 14
        else:
            return (z - 54) % 32

    def __deepcopy__(self, memo):
        return Element(self.symbol)

    @staticmethod
    def from_dict(d):
        """
        Makes Element obey the general json interface used in pymatgen for
        easier serialization.
        """
        return Element(d["element"])

    def as_dict(self):
        """
        Makes Element obey the general json interface used in pymatgen for
        easier serialization.
        """
        return {"-FromModule": self.__class__.__module__,
                "-FromClass": self.__class__.__name__,
                "element": self.symbol}

    @staticmethod
    def print_periodic_table(filter_function=None):
        """
        A pretty ASCII printer for the periodic table, based on some
        filter_function.

        Args:
            filter_function: A filtering function taking an Element as input
                and returning a boolean. For example, setting
                filter_function = lambda el: el.X > 2 will print a periodic
                table containing only elements with electronegativity > 2.
        """
        for row in range(1, 10):
            rowstr = []
            for group in range(1, 19):
                try:
                    el = Element.from_row_and_group(row, group)
                except ValueError:
                    el = None
                if el and ((not filter_function) or filter_function(el)):
                    rowstr.append("{:3s}".format(el.symbol))
                else:
                    rowstr.append("   ")
            print(" ".join(rowstr))


def get_el_sp(obj):
    """
    Utility method to get an Element or Specie from an input obj.
    If obj is in itself an element or a specie, it is returned automatically.
    If obj is an int or a string representing an integer, the Element
    with the atomic number obj is returned.
    If obj is a string, Specie parsing will be attempted (e.g., Mn2+), failing
    which Element parsing will be attempted (e.g., Mn), failing which
    DummyElement parsing will be attempted.

    Args:
        obj (Element/Specie/str/int): An arbitrary object.  Supported objects
            are actual Element/Specie objects, integers (representing atomic
            numbers) or strings (element symbols or species strings).

    Returns:
        Specie or Element, with a bias for the maximum number of properties
        that can be determined.

    Raises:
        ValueError if obj cannot be converted into an Element or Specie.
    """
    if isinstance(obj, Element):
        return obj

    if isinstance(obj, (list, tuple)):
        return [get_el_sp(o) for o in obj]

    try:
        c = float(obj)
        i = int(c)
        i = i if i == c else None
    except (ValueError, TypeError):
        i = None

    if i is not None:
        return Element.from_Z(i)
    else:
        raise ValueError("Can't parse Element or String from type"
                         " %s: %s." % (type(obj), obj))
