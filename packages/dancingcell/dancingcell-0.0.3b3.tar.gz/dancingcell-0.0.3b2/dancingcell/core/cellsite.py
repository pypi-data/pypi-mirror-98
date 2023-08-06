#   coding: utf-8
#   This file is part of DancingCell.

#   DancingCell is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/20"

from typing import Sequence
import numpy as np
from dancingcell.core.atom import Atom
from dancingcell.core.lattice import Lattice

class CellSite(Atom):
    """ CellSite class is used for assigning attributes to atoms.
        The atoms belong to periodictable, they have many important properties for materials.

    Attributes:
        set_sf: Decide whether to set symmetric function or not.
        atom_info: include some information about CellSite.
        atom_ene: the total energy which an CellSite has.
        data: the data about element.
        coort: the coordinate of an CellSite.
        atomic_number: the number of an CellSite.
        hasforce: Decide whether to have information about force or not.
        force: the cohesion force for atoms.
        __dircoort:Conversion of coordinates to Cartesian coordinates.
    """
    def __init__(self,
                 atom_info: str,
                 atom_ene: float=None,
                 cell: Lattice=None,
                 is_frac: bool=True,
                 addition_atom: Sequence[str]=None,
                 addition_occupy: Sequence[float]=None):
        """ function to relate fundamental information to atoms.

           Args:
               atom_info:  information about elements.
               atom_ene:  information about energy for atoms.
               icell: inverse matrix of Lattice vector
        """
        super(CellSite, self).__init__(atom_info=atom_info, atom_ene=atom_ene)

        if not isinstance(cell, Lattice):
            cell = Lattice(cell)
        self._cell = cell
        self._is_frac = is_frac

        self._species = [self.get('symbol')]
        self._occuption = [1]

        if addition_occupy:
            self._occuption = [1-sum(addition_occupy)]
            self._occuption.extend(addition_occupy)
            if addition_atom:
                self._species.extend(addition_atom)
            else:
                raise ValueError("Only have addition occupy,can't find addition atom!")

        # self._icell = np.linalg.inv(self._cell.matrix)

        # super(PmAtom, self).__init__(symbol=self.symbol, position=self._coort)
        self.data['cell'] = self._cell

        if self._is_frac:
            self._frac_coords = self._coort
            self._coort = self._cell.get_cartesian_coords(self._coort)
        else:
            self._frac_coords = self._cell.get_fractional_coords(self._coort)
            self._coort = self._coort

    @property
    def coords(self):
        return self._coort

    @property
    def frac_coords(self):
        return self._frac_coords

    def distance(self, other):
        """
        Get distance between two sites.

        Args:
            other: Other site.

        Returns:
            Distance (float)
        """
        return np.linalg.norm(other.coords - self._coort)

    @property
    def x(self):
        """
        Cartesian x coordinate
        """
        return self._coort[0]

    @property
    def y(self):
        """
        Cartesian y coordinate
        """
        return self._coort[1]

    @property
    def z(self):
        """
        Cartesian z coordinate
        """
        return self._coort[2]

    def distance_from_point(self, pt):
        """
        Returns distance between the site and a point in space.

        Args:
            pt: Cartesian coordinates of point.

        Returns:
            Distance (float)
        """
        return np.linalg.norm(np.array(pt) - self._coort)

    @property
    def symbol(self):
        """
        Total number of atoms in Composition. For negative amounts, sum
        of absolute values
        """
        return self.get('symbol') if self.is_ordered else ['%s%.2f'%(self._species[i],
                                                                     self._occuption[i])
                                                           for i in range(len(self._species))]
    @property
    def is_ordered(self):
        """
        True if site is an ordered site, i.e., with a single species with
        occupancy 1.
        """
        return True if self._occuption == [1] else False

    def as_dict(self):
        d = {"coordinate": self._coort,
             "force": self._force,
             "energy": self.atom_ene,
             "symbol": self._element.symbol,
             "element": self._element,
             "cell": self._cell.as_dict(),
             "is_frac": self._is_frac,
             'occupies': self._occuption,
             'species': self._species,
             'is_ordered': self.is_ordered}

        d["*mod"] = self.__class__.__module__
        d["*clas"] = self.__class__.__name__
        return d

    @classmethod
    def from_atom(cls, atom: Atom, cell: Lattice, is_frac=True, addition_atom=None, addition_occupy=None):
        d = atom.as_dict()
        d['cell'] = cell
        d['is_frac'] = is_frac
        d['addition_atom'] = addition_atom
        d['addition_occupy'] = addition_occupy
        return cls.from_dict(d)

    @classmethod
    def from_str(cls, atom_info, cell=None, atom_ene=0.0, is_frac=True, addition_atom=None, addition_occupy=None):
        if cell is None:
            raise ValueError("Must input cell")
        return cls(atom_info=atom_info, atom_ene=atom_ene, cell=cell, is_frac=is_frac, addition_atom=addition_atom,
                   addition_occupy=addition_occupy)

    @classmethod
    def from_dict(cls, d):
        _tmp = ' '.join([d['symbol'], ' '.join(d['coordinate'].astype(np.str)), ' '.join(d['force'].astype(np.str))])

        occupy = d.get('occupies', [])
        species = d.get('species', [])

        if occupy and species:
            if len(occupy) == 1 and len(species) == 1:
                addition_occupy = None
                addition_atom = None
            else:
                addition_occupy = occupy[1:]
                addition_atom = species[1:]
        else:
            addition_occupy = None
            addition_atom = None

        cell = Lattice(d['cell']) if isinstance(d['cell'], dict) else Lattice(d['cell'])

        return cls(atom_info=_tmp, atom_ene=d['energy'], cell=cell,
                   is_frac=d.get('is_frac', None),
                   addition_atom=d.get('addition_atom', addition_atom),
                   addition_occupy=d.get('addition_occupy', addition_occupy))

    def __len__(self):
        return len(self._species)

    def __call__(self, dicts=False):
        """ If function call class,return dicts.If not call, return tuple.

        Args:
            dicts: feedback situation of function call.

        Return:
            According to function call, return dict or tuple.
        """
        return self._element, self._coort, self._force, self.atom_ene, self._cell

