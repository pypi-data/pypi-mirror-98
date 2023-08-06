#   coding: utf-8
#   This file is part of DancingCell.

#   DancingCell is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/20"

from enum import Enum
import warnings
import re
import numpy as np
from itertools import product, combinations
from collections import Counter

from dancingcell.constant.constant_units import FloatWithUnit, Unit, unitized, Mass, Length, SUPPORTED_UNIT_NAMES
from dancingcell.constant.constant_properties import CONSTANT_PROPERTIES

_pt_row_sizes = (2, 8, 8, 18, 18, 32, 32)


class Element(Enum):
    """
    Basic immutable element object with all relevant properties.
    Only one instance of Element for each symbol is stored after creation,
    ensuring that a particular element behaves like a singleton. For all
    attributes, missing data (i.e., data for which is not available) is
    represented by a None unless otherwise stated.

    Args:
        symbol (str): Element symbol, e.g., "H", "Fe"

    .. attribute:: Z

        Atomic number

    .. attribute:: symbol

        Element symbol

    .. attribute:: X

        Pauling electronegativity. Elements without an electronegativity
        number are assigned a value of zero by default.

    .. attribute:: number

        Alternative attribute for atomic number

    .. attribute:: max_oxidation_state

        Maximum oxidation state for element

    .. attribute:: min_oxidation_state

        Minimum oxidation state for element

    .. attribute:: oxidation_states

        Tuple of all known oxidation states

    .. attribute:: common_oxidation_states

        Tuple of all common oxidation states

    .. attribute:: full_electronic_structure

        Full electronic structure as tuple.
        E.g., The electronic structure for Fe is represented as:
        [(1, "s", 2), (2, "s", 2), (2, "p", 6), (3, "s", 2), (3, "p", 6),
        (3, "d", 6), (4, "s", 2)]

    .. attribute:: row

        Returns the periodic table row of the element.

    .. attribute:: group

        Returns the periodic table group of the element.

    .. attribute:: block

        Return the block character "s,p,d,f"

    .. attribute:: is_noble_gas

        True if element is noble gas.

    .. attribute:: is_transition_metal

        True if element is a transition metal.

    .. attribute:: is_post_transition_metal

        True if element is a post transition metal.

    .. attribute:: is_rare_earth_metal

        True if element is a rare earth metal.

    .. attribute:: is_metalloid

        True if element is a metalloid.

    .. attribute:: is_alkali

        True if element is an alkali metal.

    .. attribute:: is_alkaline

        True if element is an alkaline earth metal (group II).

    .. attribute:: is_halogen

        True if element is a halogen.

    .. attribute:: is_lanthanoid

        True if element is a lanthanoid.

    .. attribute:: is_actinoid

        True if element is a actinoid.

    .. attribute:: iupac_ordering

        Ordering according to Table VI of "Nomenclature of Inorganic Chemistry
        (IUPAC Recommendations 2005)". This ordering effectively follows the
        groups and rows of the periodic table, except the Lanthanides, Actanides
        and hydrogen.

    .. attribute:: long_name

       Long name for element. E.g., "Hydrogen".

    .. attribute:: atomic_mass

        Atomic mass for the element.

    .. attribute:: atomic_radius

        Atomic radius for the element. This is the empirical value. Data is
        obtained from
        http://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page).

    .. attribute:: atomic_radius_calculated

        Calculated atomic radius for the element. This is the empirical value.
        Data is obtained from
        http://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page).

    .. attribute:: van_der_waals_radius

        Van der Waals radius for the element. This is the empirical
        value. Data is obtained from
        http://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page).

    .. attribute:: mendeleev_no

        Mendeleev number

    .. attribute:: electrical_resistivity

        Electrical resistivity

    .. attribute:: velocity_of_sound

        Velocity of sound

    .. attribute:: reflectivity

        Reflectivity

    .. attribute:: refractive_index

        Refractice index

    .. attribute:: poissons_ratio

        Poisson's ratio

    .. attribute:: molar_volume

        Molar volume

    .. attribute:: electronic_structure

        Electronic structure. Simplified form with HTML formatting.
        E.g., The electronic structure for Fe is represented as
        [Ar].3d<sup>6</sup>.4s<sup>2</sup>

    .. attribute:: atomic_orbitals

        Atomic Orbitals. Energy of the atomic orbitals as a dict.
        E.g., The orbitals energies in eV are represented as
        {'1s': -1.0, '2s': -0.1}
        Data is obtained from
        https://www.nist.gov/pml/data/atomic-reference-data-electronic-structure-calculations
        The LDA values for neutral atoms are used

    .. attribute:: thermal_conductivity

        Thermal conductivity

    .. attribute:: boiling_point

        Boiling point

    .. attribute:: melting_point

        Melting point

    .. attribute:: critical_temperature

        Critical temperature

    .. attribute:: superconduction_temperature

        Superconduction temperature

    .. attribute:: liquid_range

        Liquid range

    .. attribute:: bulk_modulus

        Bulk modulus

    .. attribute:: youngs_modulus

        Young's modulus

    .. attribute:: brinell_hardness

        Brinell hardness

    .. attribute:: rigidity_modulus

        Rigidity modulus

    .. attribute:: mineral_hardness

        Mineral hardness

    .. attribute:: vickers_hardness

        Vicker's hardness

    .. attribute:: density_of_solid

        Density of solid phase

    .. attribute:: coefficient_of_linear_thermal_expansion

        Coefficient of linear thermal expansion

    .. attribute:: average_ionic_radius

        Average ionic radius for element in ang. The average is taken over all
        oxidation states of the element for which data is present.

    .. attribute:: average_cationic_radius

        Average cationic radius for element in ang. The average is taken over all
        positive oxidation states of the element for which data is present.

    .. attribute:: average_anionic_radius

        Average ionic radius for element in ang. The average is taken over all
        negative oxidation states of the element for which data is present.

    .. attribute:: ionic_radii

        All ionic radii of the element as a dict of
        {oxidation state: ionic radii}. Radii are given in ang.
    """

    # This name = value convention is redundant and dumb, but unfortunately is
    # necessary to preserve backwards compatibility with a time when Element is
    # a regular object that is constructed with Element(symbol).
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
    Rf = "Rf"
    Db = "Db"
    Sg = "Sg"
    Bh = "Bh"
    Hs = "Hs"
    Mt = "Mt"
    Ds = "Ds"
    Rg = "Rg"
    Cn = "Cn"
    Nh = "Nh"
    Fl = "Fl"
    Mc = "Mc"
    Lv = "Lv"
    Ts = "Ts"
    Og = "Og"

    def __init__(self, symbol: str):
        self.symbol = "%s" % symbol
        d = CONSTANT_PROPERTIES[symbol]

        # Store key variables for quick access
        self.Z = d["Atomic no"]

        at_r = d.get("Atomic radius", "no data")
        if str(at_r).startswith("no data"):
            self.atomic_radius = None
        else:
            self.atomic_radius = Length(at_r, "ang")
        self.atomic_mass = Mass(d["Atomic mass"], "amu")
        self.long_name = d["Name"]
        self._data = d

    @property
    def X(self):
        if "X" in self._data:
            return self._data["X"]
        else:
            warnings.warn("No electronegativity for %s. Setting to NaN. "
                          "This has no physical meaning, and is mainly done to "
                          "avoid errors caused by the code expecting a float."
                          % self.symbol)
            return float("NaN")

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
                    nobracket = re.sub(r'\(.*\)', "", val)
                    toks = nobracket.replace("about", "").strip().split(" ", 1)
                    if len(toks) == 2:
                        try:
                            if "10<sup>" in toks[1]:
                                base_power = re.findall(r'([+-]?\d+)', toks[1])
                                factor = "e" + base_power[1]
                                if toks[0] in ["&gt;", "high"]:
                                    toks[0] = "1"  # return the border value
                                toks[0] += factor
                                if item == "electrical_resistivity":
                                    unit = "ohm m"
                                elif item == "coefficient_of_linear_thermal_expansion":
                                    unit = "K^-1"
                                else:
                                    unit = toks[1]
                                val = FloatWithUnit(toks[0], unit)
                            else:
                                unit = toks[1].replace("<sup>", "^").replace(
                                    "</sup>", "").replace("&Omega;",
                                                          "ohm")
                                units = Unit(unit)
                                if set(units.keys()).issubset(
                                        SUPPORTED_UNIT_NAMES):
                                    val = FloatWithUnit(toks[0], unit)
                        except ValueError:
                            # Ignore error. val will just remain a string.
                            pass
            return val
        raise AttributeError("Element has no attribute %s!" % item)

    @property
    def data(self):
        """
        Returns dict of data for element.
        """
        return self._data.copy()

    @property
    @unitized("ang")
    def average_ionic_radius(self):
        """
        Average ionic radius for element (with units). The average is taken
        over all oxidation states of the element for which data is present.
        """
        if "Ionic radii" in self._data:
            radii = self._data["Ionic radii"]
            return sum(radii.values()) / len(radii)
        else:
            return 0

    @property
    @unitized("ang")
    def average_cationic_radius(self):
        """
        Average cationic radius for element (with units). The average is
        taken over all positive oxidation states of the element for which
        data is present.
        """
        if "Ionic radii" in self._data:
            radii = [v for k, v in self._data["Ionic radii"].items()
                     if int(k) > 0]
            if radii:
                return sum(radii) / len(radii)
        return 0

    @property
    @unitized("ang")
    def average_anionic_radius(self):
        """
        Average anionic radius for element (with units). The average is
        taken over all negative oxidation states of the element for which
        data is present.
        """
        if "Ionic radii" in self._data:
            radii = [v for k, v in self._data["Ionic radii"].items()
                     if int(k) < 0]
            if radii:
                return sum(radii) / len(radii)
        return 0

    @property
    @unitized("ang")
    def ionic_radii(self):
        """
        All ionic radii of the element as a dict of
        {oxidation state: ionic radii}. Radii are given in ang.
        """
        if "Ionic radii" in self._data:
            return {int(k): v for k, v in self._data["Ionic radii"].items()}
        else:
            return {}

    @property
    def number(self):
        """Alternative attribute for atomic number"""
        return self.Z

    @property
    def max_oxidation_state(self):
        """Maximum oxidation state for element"""
        if "Oxidation states" in self._data:
            return max(self._data["Oxidation states"])
        return 0

    @property
    def min_oxidation_state(self):
        """Minimum oxidation state for element"""
        if "Oxidation states" in self._data:
            return min(self._data["Oxidation states"])
        return 0

    @property
    def oxidation_states(self):
        """Tuple of all known oxidation states"""
        return tuple(self._data.get("Oxidation states", list()))

    @property
    def common_oxidation_states(self):
        """Tuple of all known oxidation states"""
        return tuple(self._data.get("Common oxidation states", list()))

    @property
    def icsd_oxidation_states(self):
        """Tuple of all oxidation states with at least 10 instances in
        ICSD database AND at least 1% of entries for that element"""
        return tuple(self._data.get("ICSD oxidation states", list()))

    @property
    @unitized("ang")
    def metallic_radius(self):
        """
        Metallic radius of the element. Radius is given in ang.
        """
        return self._data["Metallic radius"]

    @property
    def full_electronic_structure(self):
        """
        Full electronic structure as tuple.
        E.g., The electronic structure for Fe is represented as:
        [(1, "s", 2), (2, "s", 2), (2, "p", 6), (3, "s", 2), (3, "p", 6),
        (3, "d", 6), (4, "s", 2)]
        """
        estr = self._data["Electronic structure"]

        def parse_orbital(orbstr):
            m = re.match(r"(\d+)([spdfg]+)<sup>(\d+)</sup>", orbstr)
            if m:
                return int(m.group(1)), m.group(2), int(m.group(3))
            return orbstr

        data = [parse_orbital(s) for s in estr.split(".")]
        if data[0][0] == "[":
            sym = data[0].replace("[", "").replace("]", "")
            data = Element(sym).full_electronic_structure + data[1:]
        return data

    @property
    def valence(self):
        """
        # From full electron config obtain valence subshell
        # angular moment (L) and number of valence e- (v_e)

        """
        # the number of valence of noble gas is 0
        if self.group == 18:
            return (np.nan, 0)

        L_symbols = 'SPDFGHIKLMNOQRTUVWXYZ'
        valence = []
        full_electron_config = self.full_electronic_structure
        for _, l_symbol, ne in full_electron_config[::-1]:
            l = L_symbols.lower().index(l_symbol)
            if ne < (2 * l + 1) * 2:
                valence.append((l, ne))
        if len(valence) > 1:
            raise ValueError("Ambiguous valence")

        return valence[0]

    @property
    def term_symbols(self):
        """
        All possible  Russell-Saunders term symbol of the Element
        eg. L = 1, n_e = 2 (s2)
        returns
           [['1D2'], ['3P0', '3P1', '3P2'], ['1S0']]

        """
        L_symbols = 'SPDFGHIKLMNOQRTUVWXYZ'

        L, v_e = self.valence

        # for one electron in subshell L
        ml = list(range(-L, L + 1))
        ms = [1 / 2, -1 / 2]
        # all possible configurations of ml,ms for one e in subshell L
        ml_ms = list(product(ml, ms))

        # Number of possible configurations for r electrons in subshell L.
        n = (2 * L + 1) * 2
        # the combination of n_e electrons configurations
        # C^{n}_{n_e}
        e_config_combs = list(combinations(range(n), v_e))

        # Total ML = sum(ml1, ml2), Total MS = sum(ms1, ms2)
        TL = [sum([ml_ms[comb[e]][0] for e in range(v_e)])
              for comb in e_config_combs]
        TS = [sum([ml_ms[comb[e]][1] for e in range(v_e)])
              for comb in e_config_combs]
        comb_counter = Counter([r for r in zip(TL, TS)])

        term_symbols = []
        while sum(comb_counter.values()) > 0:
            # Start from the lowest freq combination,
            # which corresponds to largest abs(L) and smallest abs(S)
            L, S = min(comb_counter)

            J = list(np.arange(abs(L - S), abs(L) + abs(S) + 1))
            term_symbols.append([str(int(2 * (abs(S)) + 1))
                                 + L_symbols[abs(L)]
                                 + str(j) for j in J])
            # Without J
            # term_symbols.append(str(int(2 * (abs(S)) + 1)) \
            #                     + L_symbols[abs(L)])

            # Delete all configurations included in this term
            for ML in range(-L, L - 1, -1):
                for MS in np.arange(S, -S + 1, 1):
                    if (ML, MS) in comb_counter:

                        comb_counter[(ML, MS)] -= 1
                        if comb_counter[(ML, MS)] == 0:
                            del comb_counter[(ML, MS)]
        return term_symbols

    @property
    def ground_state_term_symbol(self):
        """
        Ground state term symbol
        Selected based on Hund's Rule

        """
        L_symbols = 'SPDFGHIKLMNOQRTUVWXYZ'

        term_symbols = self.term_symbols
        term_symbol_flat = {term: {"multiplicity": int(term[0]),
                                   "L": L_symbols.index(term[1]),
                                   "J": float(term[2:])}
                            for term in sum(term_symbols, [])}

        multi = [int(item['multiplicity'])
                 for terms, item in term_symbol_flat.items()]
        max_multi_terms = {symbol: item
                           for symbol, item in term_symbol_flat.items()
                           if item['multiplicity'] == max(multi)}

        Ls = [item['L'] for terms, item in max_multi_terms.items()]
        max_L_terms = {symbol: item
                       for symbol, item in term_symbol_flat.items()
                       if item['L'] == max(Ls)}

        J_sorted_terms = sorted(max_L_terms.items(),
                                key=lambda k: k[1]['J'])
        L, v_e = self.valence
        if v_e <= (2 * L + 1):
            return J_sorted_terms[0][0]
        else:
            return J_sorted_terms[-1][0]

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
    def from_Z(z: int):
        """
        Get an element from an atomic number.

        Args:
            z (int): Atomic number

        Returns:
            Element with atomic number z.
        """
        for sym, data in CONSTANT_PROPERTIES.items():
            if data["Atomic no"] == z:
                return Element(sym)
        raise ValueError("No element with this atomic number %s" % z)

    @staticmethod
    def from_row_and_group(row: int, group: int):
        """
        Returns an element from a row and group number.

        Args:
            row (int): Row number
            group (int): Group number

        .. note::
            The 18 group number system is used, i.e., Noble gases are group 18.
        """
        for sym in CONSTANT_PROPERTIES.keys():
            el = Element(sym)
            if el.row == row and el.group == group:
                return el
        raise ValueError("No element with this row and group!")

    @staticmethod
    def is_valid_symbol(symbol: str):
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

        for i in range(len(_pt_row_sizes)):
            total += _pt_row_sizes[i]
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

    @property
    def block(self):
        """
        Return the block character "s,p,d,f"
        """
        if (self.is_actinoid or self.is_lanthanoid) and self.Z not in [71, 103]:
            return "f"
        elif self.is_actinoid or self.is_lanthanoid:
            return "d"
        elif self.group in [1, 2]:
            return "s"
        elif self.group in range(13, 19):
            return "p"
        elif self.group in range(3, 13):
            return "d"
        raise ValueError("unable to determine block")

    @property
    def is_noble_gas(self):
        """
        True if element is noble gas.
        """
        return self.Z in (2, 10, 18, 36, 54, 86, 118)

    @property
    def is_transition_metal(self):
        """
        True if element is a transition metal.
        """
        ns = list(range(21, 31))
        ns.extend(list(range(39, 49)))
        ns.append(57)
        ns.extend(list(range(72, 81)))
        ns.append(89)
        ns.extend(list(range(104, 113)))
        return self.Z in ns

    @property
    def is_post_transition_metal(self):
        """
        True if element is a post-transition or poor metal.
        """
        return self.symbol in ("Al", "Ga", "In", "Tl", "Sn", "Pb", "Bi")

    @property
    def is_rare_earth_metal(self):
        """
        True if element is a rare earth metal.
        """
        return self.is_lanthanoid or self.is_actinoid

    @property
    def is_metalloid(self):
        """
        True if element is a metalloid.
        """
        return self.symbol in ("B", "Si", "Ge", "As", "Sb", "Te", "Po")

    @property
    def is_alkali(self):
        """
        True if element is an alkali metal.
        """
        return self.Z in (3, 11, 19, 37, 55, 87)

    @property
    def is_alkaline(self):
        """
        True if element is an alkaline earth metal (group II).
        """
        return self.Z in (4, 12, 20, 38, 56, 88)

    @property
    def is_halogen(self):
        """
        True if element is a halogen.
        """
        return self.Z in (9, 17, 35, 53, 85)

    @property
    def is_chalcogen(self):
        """
        True if element is a chalcogen.
        """
        return self.Z in (8, 16, 34, 52, 84)

    @property
    def is_lanthanoid(self):
        """
        True if element is a lanthanoid.
        """
        return 56 < self.Z < 72

    @property
    def is_actinoid(self):
        """
        True if element is a actinoid.
        """
        return 88 < self.Z < 104

    @property
    def is_quadrupolar(self):
        """
        Checks if this element can be quadrupolar
        """
        return len(self.data.get("NMR Quadrupole Moment", {})) > 0

    @property
    def nmr_quadrupole_moment(self):
        """
        Get a dictionary the nuclear electric quadrupole moment in units of
        e*millibarns for various isotopes
        """
        return {k: FloatWithUnit(v, "mbarn")
                for k, v in self.data.get("NMR Quadrupole Moment", {}).items()}

    @property
    def iupac_ordering(self):
        """
        Ordering according to Table VI of "Nomenclature of Inorganic Chemistry
        (IUPAC Recommendations 2005)". This ordering effectively follows the
        groups and rows of the periodic table, except the Lanthanides, Actanides
        and hydrogen.
        """
        return self._data["IUPAC ordering"]

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
        return {"*mod": self.__class__.__module__,
                "*clas": self.__class__.__name__,
                "element": self.symbol}

    @staticmethod
    def print_periodic_table(filter_function: callable = None):
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

