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
from dancingcell.core.atoms import Atoms
from dancingcell.utility.dcjson import array2d

class TestAtom(unittest.TestCase):

    def setUp(self):
        positions = array2d(np.random.randn(4,3))
        forces = array2d(np.random.randn(4, 3))
        energies = np.random.random(4)
        species = ['Sb'] * 1 + ['Te'] * 3

        self.atoms = Atoms(positions=positions, species=species, forces=forces, energies=energies,
                           coords_are_cartesian=False)

    def test_atom(self):
        print(self.atoms.positions.x)
        print(self.atoms._symbols)
        print(self.atoms._species[0].as_dict())
        print(self.atoms.get_distances(0, 1))
        print(self.atoms.atom_numbers)
        print(self.atoms.get_all_distances())
        print(self.atoms.as_dict())
        print(self.atoms[[1,2,3]])


if __name__ == '__main__':
    unittest.main()