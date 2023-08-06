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
from dancingcell.core.lattice import Lattice


class TestLattice(unittest.TestCase):

    def setUp(self):
        a = np.random.random((3, 3))
        self.lattice = Lattice(a)
        self.replattice = self.lattice.reciprocal_lattice

    def test_atom(self):
        print(self.lattice.matrix)
        print(self.lattice.reciprocal_lattice)
        print(self.lattice.rhombohedral(10, 80))
        print(self.lattice.get_lll_reduced_lattice())
        print(self.lattice.d_hkl(self.lattice.matrix))

        print(self.lattice.get_cartesian_coords(self.lattice.matrix))
        print(self.lattice.get_fractional_coords(self.lattice.matrix))

    def test_rep_rep(self):
        # print(self.replattice.reciprocal_lattice)
        pass

if __name__ == '__main__':
    unittest.main()