#   coding: utf-8
#   This file is part of DancingCell.

#   DancingCell is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/20"

import unittest
import numpy as np
from dancingcell.core.cellsite import CellSite
from dancingcell.core.atom import Atom

class TestAtom(unittest.TestCase):

    def setUp(self):
        self.icell = np.random.random((3, 3))
        self.atom = CellSite(atom_info='Sb     4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156',
                         atom_ene=0.5, cell=self.icell)

    def test_atom(self):

        atom = CellSite(atom_info='Sb     4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156',
                    atom_ene=0.5, cell=self.icell)
        print(atom())
        print('------1--------')
        print(atom.as_dict())
        print(atom.get('force'))
        print(atom.to_json())

    def test_fromdict(self):
        atom = CellSite.from_dict(self.atom.as_dict())
        print('------2----------')
        print(atom.as_dict())
        print(atom.to_json())

    def test_fromstr(self):
        atom = CellSite.from_str('Sb    4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156',
                                 cell=self.icell, is_frac=False)
        print('-------3------')
        print(atom.as_dict())
        print(atom.to_json())
        print(atom.frac_coords, atom.coords)

        atom = CellSite.from_str('Sb    4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156',
                                 cell=self.icell, is_frac=True)
        print(atom.frac_coords, atom.coords)

    def test_fromatom(self):
        atom = Atom.from_str('Sb    4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156')
        cell = CellSite.from_atom(atom, cell=self.icell, is_frac=True)
        print(cell.as_dict())

    def test_opccupy(self):
        tt1 = CellSite.from_str(atom_info='Sb    4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156',
                                cell=self.icell, is_frac=False,
                                addition_atom=['C', "H"],
                                addition_occupy=[0.1, 0.1])
        print('--------5------------')
        ddd = tt1.as_dict()
        print(ddd)
        print('---------6----------')
        t2 = CellSite.from_dict(ddd)
        print(t2.as_dict())

if __name__ == '__main__':
    unittest.main()