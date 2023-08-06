#   coding: utf-8
#   This file is part of potentialmind.

#   potentialmind is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/07/17"

from dancingcell.core.cell import Cell
from dancingcell.core.element import Element
from dancingcell.utility.tools import is_diagonal


class LammpsData(object):

    def __init__(self,
                 cell: Cell,
                 charge: dict=None,
                 set_atomindex: dict=None,
                 ):
        self.cell = cell
        if charge is not None:
            self.charge = charge
        else:
            self.charge = {i: 0.0 for i in self.cell.symbols}

        if set_atomindex:
            self.atomindex = set_atomindex
        else:
            self.atomindex = {v : k + 1 for k, v in enumerate(set(self.cell.symbols))}

    def get_str(self, atom_type='charge'):
        info = ['# LAMMPS data file from DancingCell of ALKEMIE', ' ']
        ap = info.append
        ap('%d atoms' % self.cell.atom_numbers)
        ap('%d atom types' % len(self.atomindex))
        ap(' ')
        if is_diagonal(self.cell.lattice.data):
            ap('%9.8f   %15.8f   xlo xhi' % (0.0, self.cell.lattice.a[0]))
            ap('%9.8f   %15.8f   ylo yhi' % (0.0, self.cell.lattice.b[1]))
            ap('%9.8f   %15.8f   zlo zhi' % (0.0, self.cell.lattice.c[2]))
            ap(' ')
        else:
            raise ValueError("only support diagonal lattice ")
        ap('Masses')
        ap(' ')
        for k, v in self.atomindex.items():
            ap('%d  %15.8f' % (v, Element(k).atomic_mass))
        ap(' ')
        ap('Atoms')
        ap(' ')
        if atom_type == 'charge':
            _temple_atom_info = '%6d     %3d      %8.5f    %15.8f    %15.8f   %15.8f'
            for i in range(self.cell.atom_numbers):
                ele = self.cell.symbols[i]
                ap(_temple_atom_info % (i+1, self.atomindex[ele], self.charge[ele], *self.cell.cartesian.data[i]))
            pass
        else:
            raise TypeError("Only support atom_type=charge")

        return info

    def write_poscar(self, fn):
        info = self.get_str()
        with open(fn, 'w') as f:
            f.write('\n'.join(info))

    def from_str(self, content):
        lines = content.split('\n')
        return None

    def from_file(self, fn):
        with open(fn, 'r') as f:
            return self.from_str(''.join(f.readlines()))