#   coding: utf-8
#   This file is part of DancingCell.

#   DancingCell is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/21"

import numpy as np
import collections
import json
from typing import Union, Sequence

from dancingcell.utility.dcjson import array2d
from dancingcell.core.atoms import Atoms
from dancingcell.core.lattice import Lattice
from dancingcell.core.cellsite import CellSite
from dancingcell.utility.dcjson import DcEncoder


class Cell(Atoms):

    def __init__(self,
                 positions: array2d,
                 species: Union[list, np.ndarray],
                 lattice: Union[array2d, np.ndarray, Lattice],
                 forces: array2d = None,
                 energies: Union[list, np.ndarray] = None,
                 coords_are_cartesian: bool = True,
                 pbc: Sequence[bool] = (True, True, True),
                 labels=None
                 ):

        super(Cell, self).__init__(positions=positions,
                                   species=species,
                                   forces=forces,
                                   energies=energies,
                                   coords_are_cartesian=coords_are_cartesian)

        self._lattice = Lattice(lattice)
        self._pbc = pbc
        self._labels = labels
        self._if_frac = not self._coords_are_cartesian

    @property
    def cellsites(self):
        return [CellSite.from_atom(atom=i, cell=self.lattice, is_frac= self._if_frac) for i in self.atoms]

    @property
    def pbc(self):
        return self._pbc

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, x):
        self._labels = x

    @property
    def lattice(self):
        return self._lattice

    @property
    def is_ordered(self) -> bool:
        """
        Checks if structure is ordered, meaning no partial occupancies in any
        of the sites.
        """
        return all((cellsite.is_ordered for cellsite in self))

    @property
    def cartesian(self):
        if self._coords_are_cartesian:
            return self.positions
        else:
            return array2d(self.lattice.get_cartesian_coords(self.positions.data))

    @property
    def fraction(self):
        if self._coords_are_cartesian:
            return array2d(self.lattice.get_fractional_coords(self.positions.data))
        else:
            return self.positions

    def get_scaled_positions(self, wrap=True):
        """Get positions relative to unit cell.

        If wrap is True, atoms outside the unit cell will be wrapped into
        the cell in those directions with periodic boundary conditions
        so that the scaled coordinates are between zero and one."""

        fractional = np.linalg.solve(self._lattice.matrix.T, self.positions.T).T
        # fractional1 = np.linalg.pinv(self._lattice)
        if wrap:
            for i, periodic in enumerate(self._pbc):
                if periodic:
        #             Yes, we need to do it twice.
        #             See the scaled_positions.py test.
                    fractional[:, i] %= 1.0
                    fractional[:, i] %= 1.0
        # return np.dot(self.positions, fractional1)
        return array2d(fractional)

    @staticmethod
    def find_mic(D, cell, pbc=(True, True, True)):
        """Finds the minimum-image representation of vector(s) D

        Args:
            D: 'mic' vectors
            cell: cell type
            pbc: dimension of matrix
        """

        # Calculate the 4 unique unit cell diagonal lengths
        diags = np.sqrt((np.dot([[1, 1, 1],
                                 [-1, 1, 1],
                                 [1, -1, 1],
                                 [-1, -1, 1],
                                 ], cell) ** 2).sum(1))

        # calculate 'mic' vectors (D) and lengths (D_len) using simple method
        Dr = np.dot(D, np.linalg.inv(cell))
        D = np.dot(Dr - np.round(Dr) * pbc, cell)
        D_len = np.sqrt((D ** 2).sum(1))
        # return mic vectors and lengths for only orthorhombic cells,
        # as the results may be wrong for non-orthorhombic cells
        if (max(diags) - min(diags)) / max(diags) < 1e-9:
            return D, D_len

        # The cutoff radius is the longest direct distance between atoms
        # or half the longest lattice diagonal, whichever is smaller
        cutoff = min(max(D_len), max(diags) / 2.)

        # The number of neighboring images to search in each direction is
        # equal to the ceiling of the cutoff distance (defined above) divided
        # by the length of the projection of the lattice vector onto its
        # corresponding surface normal. a's surface normal vector is e.g.
        # b x c / (|b| |c|), so this projection is (a . (b x c)) / (|b| |c|).
        # The numerator is just the lattice volume, so this can be simplified
        # to V / (|b| |c|). This is rewritten as V |a| / (|a| |b| |c|)
        # for vectorization purposes.
        latt_len = np.sqrt((cell ** 2).sum(1))
        V = abs(np.linalg.det(cell))
        n = pbc * np.array(np.ceil(cutoff * np.prod(latt_len) /
                                   (V * latt_len)), dtype=int)

        # Construct a list of translation vectors. For example, if we are
        # searching only the nearest images (27 total), tvecs will be a
        # 27x3 array of translation vectors. This is the only nested loop
        # in the routine, and it takes a very small fraction of the total
        # execution time, so it is not worth optimizing further.
        tvecs = []
        for i in range(-n[0], n[0] + 1):
            latt_a = i * cell[0]
            for j in range(-n[1], n[1] + 1):
                latt_ab = latt_a + j * cell[1]
                for k in range(-n[2], n[2] + 1):
                    tvecs.append(latt_ab + k * cell[2])
        tvecs = np.array(tvecs)

        # Translate the direct displacement vectors by each translation
        # vector, and calculate the corresponding lengths.
        D_trans = tvecs[np.newaxis] + D[:, np.newaxis]
        D_trans_len = np.sqrt((D_trans ** 2).sum(2))

        # Find mic distances and corresponding vector(s) for each given pair
        # of atoms. For symmetrical systems, there may be more than one
        # translation vector corresponding to the MIC distance; this finds the
        # first one in D_trans_len.
        D_min_len = np.min(D_trans_len, axis=1)
        D_min_ind = D_trans_len.argmin(axis=1)
        D_min = D_trans[list(range(len(D_min_ind))), D_min_ind]

        return D_min, D_min_len

    def get_distance(self, a0, a1, mic=False, vector=False):
        """Return distance between two atoms.

        Use mic=True to use the Minimum Image Convention.
        vector=True gives the distance vector (from a0 to a1).
        """

        R = self.positions.data
        D = np.array([R[a1] - R[a0]])
        if mic:
            D, D_len = self.find_mic(D, self._lattice.matrix, self._pbc)
        else:
            D_len = np.array([np.sqrt((D**2).sum())])
        if vector:
            return D[0]

        return D_len[0]

    def get_distances(self, a, indices, mic=False, vector=False):
        """Return distances of atom No.i with a list of atoms.

        Use mic=True to use the Minimum Image Convention.
        vector=True gives the distance vector (from a to self[indices]).
        """

        R = self.positions.data
        D = R[indices] - R[a]
        if mic:
            D, D_len = self.find_mic(D, self._lattice.matrix, self._pbc)
        else:
            D_len = np.sqrt((D**2).sum(1))
        if vector:
            return D
        return D_len

    def get_all_distances(self, mic=False):
        """Return distances of all of the atoms with all of the atoms.

        Use mic=True to use the Minimum Image Convention.
        """
        L = len(self)
        R = self.positions.data

        D = []
        for i in range(L - 1):
            D.append(R[i + 1:] - R[i])
        D = np.concatenate(D)

        if mic:
            D, D_len = self.find_mic(D, self._lattice.matrix, self._pbc)
        else:
            D_len = np.sqrt((D**2).sum(1))

        results = np.zeros((L, L), dtype=float)
        start = 0
        for i in range(L - 1):
            results[i, i + 1:] = D_len[start:start + L - i - 1]
            start += L - i - 1
        return results + results.T

    def apply_strain(self, strain):
        """
        Apply a strain to the lattice.

        Args:
            strain (float or list): Amount of strain to apply. Can be a float,
                or a sequence of 3 numbers. E.g., 0.01 means all lattice
                vectors are increased by 1%. This is equivalent to calling
                modify_lattice with a lattice with lattice parameters that
                are 1% larger.
        """
        s = (1 + np.array(strain)) * np.eye(3)
        self._lattice = Lattice(np.dot(self._lattice.data.T, s).T)

    def translate_sites(self, indices, vector, frac_coords=True,
                        to_unit_cell=True):
        """
        Translate specific sites by some vector, keeping the sites within the
        unit cell.

        Args:
            indices: Integer or List of site indices on which to perform the
                translation.
            vector: Translation vector for sites.
            frac_coords (bool): Whether the vector corresponds to fractional or
                cartesian coordinates.
            to_unit_cell (bool): Whether new sites are transformed to unit
                cell
        """
        if not isinstance(indices, collections.abc.Iterable):
            indices = [indices]

        for i in indices:
            site = self.cellsites[i]
            if frac_coords:
                fcoords = site.frac_coords + vector
            else:
                fcoords = self._lattice.get_fractional_coords(
                    site.coords + vector)
            if to_unit_cell:
                fcoords = np.mod(fcoords, 1)

            self.cellsites[i]._frac_coords = fcoords

    def perturb(self, distance, min_distance=None):
        """
        Performs a random perturbation of the sites in a structure to break
        symmetries.

        Args:
            distance (float): Distance in angstroms by which to perturb each
                site.
            min_distance (None, int, or float): if None, all displacements will
                be equal amplitude. If int or float, perturb each site a
                distance drawn from the uniform distribution between
                'min_distance' and 'distance'.

        """

        def get_rand_vec():
            # deals with zero vectors.
            vector = np.random.randn(3)
            vnorm = np.linalg.norm(vector)
            dist = distance
            if isinstance(min_distance, (float, int)):
                dist = np.random.uniform(min_distance, dist)
            return vector / vnorm * dist if vnorm != 0 else get_rand_vec()

        for i in range(len(self)):
            self.translate_sites([i], get_rand_vec(), frac_coords=False)

    def scale_lattice(self, volume):
        """
        Performs a scaling of the lattice vectors so that length proportions
        and angles are preserved.

        Args:
            volume (float): New volume of the unit cell in A^3.
        """
        self._lattice = self._lattice.scale(volume)

    def __iter__(self):
        return self.cellsites.__iter__()

    def __getitem__(self, i):
        if isinstance(i, int) or isinstance(i, slice):
            return self.cellsites[i]
        elif isinstance(i, list) or isinstance(i, tuple) or isinstance(i, np.ndarray):
            return [self[int(x)] for x in i]


    def as_dict(self):
        d = {"positions": self.positions.as_dict(),
             "forces": self.forces.as_dict(),
             "symbols": self.symbols,
             "energies": self.energies,
             "atom_numbers": self.atom_numbers,
             "total_energy": self.total_energy,
             "formula": self.formula,
             'labels': self.labels,
             'lattice': self.lattice.as_dict(verbosity=1),
             'pbc': self.pbc}

        d['*mod'] = self.__class__.__module__
        d['*clas'] = self.__class__.__name__
        return d

    @classmethod
    def from_cellsite(cls, cellsite: Sequence[CellSite], pbc=None):
        positions = array2d([i.frac_coords for i in cellsite])
        species = [i.get('symbol') for i in cellsite]
        forces = array2d([i.get('force') for i in cellsite])
        lattice = cellsite[0].get('cell')
        energies = [i.get('energy') for i in cellsite]
        return cls(positions, species, lattice, forces, energies, coords_are_cartesian=False, pbc=pbc)

    def to_db(self, simple: bool=True):
        ddd = self.as_dict()

        if simple:
            _sp = self.forces.data.shape[0]
            if ((self.forces.data - np.zeros((_sp, 3))) <= (np.ones((_sp, 3)) * 1e-10)).all():
                ddd.pop('forces')
            try:
                ddd.pop('species')
                ddd.pop('lattice')
                ddd.pop('pbc')
                ddd.pop('*clas')
                ddd.pop('energies')
                ddd.pop('formula')
                ddd.pop('atom_numbers')
            except KeyError as kk:
                print("KyeError: %s " % kk)

        ddd = json.loads(json.dumps(ddd, cls=DcEncoder))
        return ddd
