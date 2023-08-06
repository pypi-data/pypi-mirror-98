#   coding: utf-8
#   This file is part of potentialmind.

#   potentialmind is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/07/17"

import numpy as np
import unittest
from dancingcell.utility.dcjson import array2d
from dancingcell.core.cell import Cell
from dancingcell.lammps.data import LammpsData
from dancingcell.vasp.poscar import Poscar


class TestPoscar(unittest.TestCase):

    def setUp(self):
        np.random.seed(1)
        positions = array2d(np.random.randn(4, 3))
        forces = array2d(np.random.randn(4, 3))
        energies = np.random.random(4)
        species = ['Si'] * 1 + ['O'] * 3
        lattice = np.diag(np.diagonal(np.random.randn(3, 3)))
        # charges = {'O': -1.2, 'Si': 2.4}
        self.cell = Cell(positions, species, forces=forces, energies=energies, lattice=lattice, labels='sdfsdfsd')
        self.data = LammpsData(self.cell)

    def test_get_str(self):
        print(self.data.atomindex)
        self.data.get_str()

    def test_write_poscar(self):
        self.data.write_poscar('test.vasp')

    def test_poscar2data(self):
        a = Poscar.from_file('POSCAR-324').cell
        d = LammpsData(cell=a)
        d.write_poscar('data.sio2')


if __name__ == '__main__':
    unittest.main()