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
from dancingcell.core.cell import Cell
from dancingcell.utility.dcjson import array2d

class TestCell(unittest.TestCase):

    def setUp(self):
        np.random.seed(1)
        positions = array2d(np.random.randn(4,3))
        forces = array2d(np.random.randn(4, 3))
        energies = np.random.random(4)
        species = ['Sb'] * 1 + ['Te'] * 3
        lattice = np.random.randn(3, 3)

        self.cell = Cell(positions, species, forces=forces, energies=energies, lattice=lattice, labels='sdfsdfsd')
        _la = np.eye(3) * 3
        self.eyecell = Cell(positions, species, forces=forces, energies=energies, lattice=_la, labels='sdfsdfsd')


    def test_ccc(self):
        print(self.cell.as_dict())

    def test_distance(self):
        print('------------distance---------------')
        a = self.cell.get_all_distances(mic=True)
        print(a)
        b = self.cell.get_all_distances(mic=False)
        print(b)

    def test_set_strain(self):
        print(self.cell.lattice)
        a = self.cell.apply_strain(1.3)
        print(self.cell.lattice)

    def test_scale(self):
        print(self.eyecell.lattice)
        print(self.eyecell.lattice.volume)
        """
        scale 有bug，333到444就无法价算出来，因为算法中self.abc/self.c 会出现inf
        """
        self.eyecell.scale_lattice(64)
        # from pymatgen.core.lattice import Lattice
        # a = Lattice(self.eyecell.lattice)
        # print(a.scale(64))
        print(self.eyecell.lattice)

    def test_pertub(self):
        self.cell.perturb(distance=0.2)
        print(self.cell.as_dict())
        print(self.cell.is_ordered)
        print(self.cell.to_json())
        print('--------99999------------')
        print(self.cell.to_db(simple=True))


if __name__ == '__main__':
    unittest.main()