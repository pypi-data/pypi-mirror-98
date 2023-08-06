#   coding: utf-8
#   This file is part of DancingCell.

#   DancingCell is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/21"

from typing import Union
import numpy as np
import itertools
from dancingcell.utility.dcjson import DcJson, array2d
from dancingcell.core.atom import Atom
from dancingcell.core.element import Element


class Atoms(DcJson):

    def __init__(self,
                 positions: array2d,
                 species: Union[list, np.ndarray],
                 forces: array2d = None,
                 energies: Union[list, np.ndarray] = None,
                 coords_are_cartesian: bool = True,
                 ):

        self._symbols = species if isinstance(species, list) else species.tolist()

        if isinstance(positions, array2d):
            self._positions = positions
        else:
            self._positions = array2d(positions)

        self._natom = self._positions.shape[0]

        if forces is None:
            self._forces = array2d(np.zeros((self._natom, 3)))
        else:
            if isinstance(forces, (array2d, np.ndarray)):
                self._forces = forces
            else:
                self._forces = array2d(forces)

        if len(self._symbols) != self._positions.shape[0] != self._forces.shape[0]:
            raise AtomsError("The list of atomic species must be of the same length as the list of coordinates.")

        self._coords_are_cartesian = coords_are_cartesian
        self._atoms = []
        self._species = []
        self._energies = energies if energies is not None else np.zeros(self._natom)

    @property
    def atoms(self):
        for i in range(self._natom):
            tmp_info = [self._symbols[i], ' '.join(self._positions[i]), ' '.join(self._forces[i])]
            self._atoms.append(Atom(atom_info=' '.join(tmp_info), atom_ene=self._energies[i]))
        return self._atoms

    @property
    def positions(self):
        return self._positions

    @property
    def forces(self):
        return self._forces

    @property
    def symbols(self):
        return self._symbols

    @property
    def species(self):
        self._species = [Element(i) for i in list(self._symbols)]
        return self._species

    @property
    def energies(self):
        return self._energies

    @property
    def atom_numbers(self):
        return self._natom

    @property
    def natoms_split_by_symbol(self):
        return [i[1] for i in self.species_and_accord_numbers()]

    @property
    def total_energy(self):
        return np.sum(self.energies)

    def species_and_accord_numbers(self):
        ttt = [(a[0], len(tuple(a[1]))) for a in itertools.groupby(self.symbols)]
        return ttt

    @property
    def formula(self):
        a = self.species_and_accord_numbers()
        return ''.join(['%s%d'%(i[0], i[1]) for i in a])

    def get(self, name, tp=None, to_list=False):
        tmp = np.array([i.get(name) for i in self._atoms], dtype=tp)
        if to_list:
            return tmp.tolist()
        return tmp

    def get_distance(self, a0, a1, vector=False):
        """Return distance between two atoms.

        Use mic=True to use the Minimum Image Convention.
        vector=True gives the distance vector (from a0 to a1).
        """

        tmp_r = self.positions.data
        tmp_d = np.array([tmp_r[a1] - tmp_r[a0]])

        tmp_d_len = np.linalg.norm(tmp_d)

        if vector:
            return tmp_d[0]

        return tmp_d_len[0]

    def get_distances(self, a, indices, vector=False):
        """Return distances of atom No.i with a list of atoms.

        Use mic=True to use the Minimum Image Convention.
        vector=True gives the distance vector (from a to self[indices]).
        """

        tmp_r = self.positions.data
        tmp_d = tmp_r[indices] - tmp_r[a]

        tmp_d_len = np.linalg.norm(tmp_d)

        if vector:
            return tmp_d

        return tmp_d_len

    def get_all_distances(self):
        """Return distances of all of the atoms with all of the atoms.

        Use mic=True to use the Minimum Image Convention.
        """
        ll = len(self)
        tmp_r = self.positions.data

        tmp_d = []
        for i in range(ll - 1):
            tmp_d.append(tmp_r[i + 1:] - tmp_r[i])
        tmp_d = np.concatenate(tmp_d)

        tmp_d_len = np.linalg.norm(tmp_d, axis=1)

        results = np.zeros((ll, ll), dtype=float)
        start = 0
        for i in range(ll - 1):
            results[i, i + 1:] = tmp_d_len[start:start + ll - i - 1]
            start += ll - i - 1
        return results + results.T

    def __len__(self):
        return self.atom_numbers

    def __getitem__(self, i):
        if isinstance(i, int) or isinstance(i, slice):
            return self._atoms[i]
        elif isinstance(i, list) or isinstance(i, tuple) or isinstance(i, np.ndarray):
            return [self[int(x)] for x in i]

    def as_dict(self):
        d = {"positions": self.positions.as_dict(),
             "forces": self.forces.as_dict(),
             "symbols": self.symbols,
             "energies": self.energies,
             "atom_numbers": self.atom_numbers,
             "total_energy": self.total_energy,
             "formula": self.formula}
        d['*mod'] = self.__class__.__module__
        d['*clas'] = self.__class__.__name__
        return d

    def as_str(self):
        pass

    def from_dict(cls, d):
        pass


class AtomsError(Exception):

    pass