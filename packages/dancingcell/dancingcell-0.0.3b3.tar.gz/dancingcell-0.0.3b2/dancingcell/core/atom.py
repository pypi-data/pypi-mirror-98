#   coding: utf-8
#   This file is part of DancingCell.

#   DancingCell is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/20"

import numpy as np
from dancingcell.utility.dcjson import DcJson, array2d
from dancingcell.core.element import Element


class Atom(DcJson):
    """ CellSite class is used for assigning attributes to atoms.
        The atoms belong to periodictable, they have many important properties for materials.

    Attributes:
        set_sf: Decide whether to set symmetric function or not.
        atom_info: include some information about atoms.
        atom_ene: the total energy which an atoms has.
        coort: the coordinate of an atoms.
        atomic_number: the number of an atoms.
        hasforce: Decide whether to have information about force or not.
        force: the cohesion force for atoms.
    """
    def __init__(self, atom_info, atom_ene=None):
        """ function to relate fundamental information to atoms.

           Args:
               atom_info:  information about elements.
               atom_ene:  information about energy for atoms.
               icell: inverse matrix of Lattice vector
        """
        self.data = {}
        self.atom_info = atom_info.strip().replace('\n', '').split()
        self.atom_ene = atom_ene if atom_ene else 0.0

        try:
            atomic_number = int(self.atom_info[0])
            self._element = Element.from_Z(atomic_number)
        except ValueError:
            symbol = self.atom_info[0]
            self._element = Element(symbol)

        self._atomic_number = self._element.number
        self._coort = np.array([x for x in self.atom_info[1:4]], dtype=np.float)

        if len(self.atom_info) >= 7:
            self.hasforce = True
            self._force = np.array([x for x in self.atom_info[4:]], dtype=np.float)
        else:
            self.hasforce = False
            self._force = np.zeros_like(self._coort, dtype=np.float)

        self.data["coordinate"] = self._coort
        self.data["force"] = self._force
        self.data["energy"] = self.atom_ene
        self.data['symbol'] = self._element.symbol
        self.data['element'] = self._element

    def get(self, name):
        """obtain information about element.

        Args:
            name: element name.

        Return:
            data[name]: obtained element name.
        """
        return self.data[name]

    def set(self, name, value):
        """Relate element information to correct name.

        Args:
            name: obtained element name.
            value: information about elements.
        """
        self.data[name] = value

    def delete(self, name):
        """delete wrong or uncorrect information about elements.

        Args:
            name: name of element.
        """
        self.data[name] = None

    def as_dict(self):
        return {"coordinate": self._coort,
                "force": self._force,
                "energy": self.atom_ene,
                'symbol': self._element.symbol,
                'element': self._element,
                '*mod': self.__class__.__module__,
                '*clas': self.__class__.__name__}

    @classmethod
    def from_str(cls, atom_info):
        return cls(atom_info=atom_info, atom_ene=0.0)

    @classmethod
    def from_dict(cls, d):
        _tmp = ' '.join([d['symbol'], ' '.join(d['coordinate'].astype(np.str)), ' '.join(d['force'].astype(np.str))])
        return cls(atom_info=_tmp, atom_ene=d['energy'])

    def __call__(self):
        """ If function call class,return dicts.If not call, return tuple.

        Args:
            dicts: feedback situation of function call.

        Return:
            According to function call, return dict or tuple.
        """
        return self._element, self._coort, self._force, self.atom_ene
