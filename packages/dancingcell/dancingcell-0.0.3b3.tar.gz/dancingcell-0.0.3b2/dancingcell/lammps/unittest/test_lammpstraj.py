#   coding: utf-8
#   This file is part of potentialmind.

#   potentialmind is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/07/17"

import unittest
from dancingcell.lammps.io import read_data, LammpsTraj


class TestPoscar(unittest.TestCase):

    def setUp(self):
        self.data = read_data('final-500w.lammps')


    def test_get_str(self):
        cell = LammpsTraj.from_one_str(self.data, atom_types=['O', 'Si'])
        print(cell.cell.as_dict())

    def test_from_str(self):
        cell = LammpsTraj.from_one_str(self.data, atom_types=['O', 'Si'])
        cell.to_poscar('SiO2-lammpstraj500w.vasp', direct=True)


if __name__ == '__main__':
    unittest.main()