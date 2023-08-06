#   coding: utf-8
#   This file is part of potentialmind.

#   potentialmind is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/07/17"

import copy
import numpy as np

from dancingcell.utility.io_file import gopen
from dancingcell.core.lattice import Lattice
from dancingcell.core.cell import Cell
from dancingcell.vasp.poscar import Poscar


def read_data(fn):
    with gopen(fn, 'r') as f:
        return ''.join(f.readlines())


class LammpsTraj(object):

    def __init__(self, cell, comment=''):
        self.cell = cell
        self.comment = comment

    def to_poscar(self, fn, direct=True):
        _tmpfile = Poscar(self.cell, comment=self.comment)
        _st = _tmpfile.get_string(direct=direct)
        with open(fn, 'w') as f:
            f.write(_st)

    @classmethod
    def from_one_str(cls, content, atom_types):
        lines = content.strip().split('\n')
        timestep = int(lines[1])
        # natoms = int(lines[3])
        pbc = [i=='pp' for i in lines[4].split()[-3:]]
        _tmp_lat =  np.array([i.split() for i in lines[5:8]], dtype=np.float)
        _tmp_constant = np.abs(_tmp_lat[:, 1] - _tmp_lat[:, 0]).tolist()
        lattice = Lattice(np.diag(_tmp_constant))
        _atom_info = np.array([i.split() for i in lines[9:]], dtype=np.float)
        _atom_info = _atom_info[_atom_info[:, 0].argsort(), :]
        atom_info = copy.deepcopy(_atom_info).astype(np.str)
        atom_ele = dict(zip(set(_atom_info[:, 1].astype(np.int)), atom_types))
        for k, v in atom_ele.items():
            atom_info[_atom_info[:, 1] == k, 1] = v
        cell = Cell(positions=atom_info[:, 2:].astype(np.float),
                    species=atom_info[:, 1],
                    lattice= lattice,
                    pbc=pbc)
        return cls(cell, comment='lammps_traj_%d' % timestep)


if __name__ == '__main__':
    pass