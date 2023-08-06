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
from dancingcell.core.atom import Atom


class TestAtom(unittest.TestCase):

    def setUp(self):
        self.atom = Atom(atom_info='Sb     4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156',
                         atom_ene=0.5)

    def test_atom(self):
        atom = Atom(atom_info='Sb     4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156',
                    atom_ene=0.5)
        print(atom())
        print('------1--------')
        print(atom.as_dict())
        print(atom.get('force'))
        print(atom.to_json())

    def test_fromdict(self):
        atom = Atom.from_dict(self.atom.as_dict())
        print('------2----------')
        print(atom.as_dict())
        print(atom.to_json())

    def test_fromstr(self):
        atom = Atom.from_str('Sb    4.63664      0.8867    11.10743   -0.465561    0.476976     0.11156')
        print('-------3------')
        print(atom.as_dict())
        print(atom.to_json())


if __name__ == '__main__':
    unittest.main()