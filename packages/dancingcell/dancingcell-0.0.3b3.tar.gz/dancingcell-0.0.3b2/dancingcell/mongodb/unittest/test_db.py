#   coding: utf-8
#   This file is part of potentialmind.

#   potentialmind is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/06/26"

import unittest
from dancingcell.mongodb.dancingdb import DancingDb
from dancingcell.utility.dcjson import array2d
from dancingcell.core.cell import Cell
import numpy as np
import json


class TestDb(unittest.TestCase):

    def setUp(self):
        self.db = DancingDb.from_dict({})

        np.random.seed(1)
        positions = array2d(np.random.randn(4, 3))
        forces = array2d(np.random.randn(4, 3))
        energies = np.random.random(4)
        species = ['Sb'] * 1 + ['Te'] * 3
        lattice = np.random.randn(3, 3)

        self.cell = Cell(positions, species, forces=forces, energies=energies, lattice=lattice, labels='sdfsdfsd')

    def test_1(self):
        print(self.db.all_databases)

    def test_222(self):
        print(self.db.all_collection_names)
        for collen in self.db.all_collection_names:
            rs = self.db[collen].find()
            for dc in rs:
                print(dc)

    def test_init(self):
        # self.db.init()
        pass

    def test_insert(self):
        # print(self.cell.to_json())
        self.db['dancingcell'].insert_one(self.cell.to_db())
        pass

if __name__ == '__main__':
    unittest.main()