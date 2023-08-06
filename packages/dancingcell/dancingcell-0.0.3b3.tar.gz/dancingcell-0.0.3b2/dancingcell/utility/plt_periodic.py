#   coding: utf-8
#   This file is part of potentialmind.

#   potentialmind is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/07/25"


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from dancingcell.core.element import Element
import json
import os

config_path = os.path.dirname('.')
get_fn = lambda x: os.path.join(config_path, x)


class PlotElement(object):
    font_family = "Times New Roman"
    need_added_column = {1: 'IA', 2: '0', 4: 'IIA', 5: 'IIIA', 6: 'IVA', 7: 'VA', 8: 'VIA', 9: 'VIIA',
                         21: 'IIIB',  22: 'IVB', 23: 'VB', 24: 'VIB', 25: 'VIIB', 27: 'VIII', 29: 'IB', 30: 'IIB'}
    need_added_row = {1: '1', 3: '2', 11: '3', 19: '4', 37: '5', 55: '6', 87: '7'}

    row_column_size = 10

    def __init__(self, ax, visible, atomic_number=None, single_ele=True):
        # xy, width, height, angle=0.0, **kwargs):
        # super(PlotElement, self).__init__(xy, width, height, angle=0.0, **kwargs)
        ax.axis('off')
        # ax.spines['top'].setvisible(True)
        # ax.spines['right'].setvisible(True)
        # ax.spines['bottom'].setvisible(True)
        # ax.spines['left'].setvisible(True)
        ax.set_xlim(-0.01, 0.91)
        ax.set_ylim(-0.01, 0.91)
        self.ax = ax
        self._visible = visible
        self._atomic_number = atomic_number
        self._single_ele = single_ele

        if self._visible:
            self._rect = Rectangle((0, 0), 0.9, 0.9, 0.0, linewidth=1, edgecolor='black', facecolor='None')
            # rect.set_bounds(left, bottom, width, height)
            self.ax.add_patch(self._rect)
            self._add_column()
            self._add_row()
            self._add_element()
            self._ele = self._add_element()
        else:
            self._rect = None
            self._ele = None
            pass

    @property
    def rect(self):
        return self._rect

    @property
    def atomic_number(self):
        return self._atomic_number

    @atomic_number.setter
    def atomic_number(self, value):
        self._atomic_number = value

    @property
    def visible(self):
        return self._visible

    @property
    def element(self):
        return self._ele

    @property
    def single_ele(self):
        return self._single_ele

    def _add_element(self):
        if self.atomic_number is not None:
            ele = Element.from_Z(self.atomic_number)
            if len(ele.symbol) == 1:
                _x = 0.4
            elif len(ele.symbol) == 2:
                _x = 0.3
            else:
                raise  ValueError("Can't find %s " % ele.symbol)

            self.ax.text(_x, 0.25, ele.symbol, fontdict={'fontsize': 16, 'family': self.font_family})
        else:
            ele = None
        return ele

    def _add_column(self):
        if self._single_ele and (self._atomic_number in self.need_added_column):
            self.ax.text(0.3, 1, self.need_added_column[self._atomic_number], fontdict= {'weight': 'bold',
                                                                                   'fontsize': self.row_column_size,
                                                                                   'family': self.font_family})

    def _add_row(self):
        laacfontdict = {'weight': 'bold', 'fontsize': 16, 'color': 'red', 'family': self.font_family}
        if self._single_ele:
            if self._atomic_number in self.need_added_row:
                self.ax.text(-0.3, 0.5, self.need_added_row[self._atomic_number], fontdict= {'weight': 'bold',
                                                                                   'fontsize': self.row_column_size,
                                                                                   'family': self.font_family})
            elif self._atomic_number == 57:
                self.ax.text(-0.6, 0.25, "LA", fontdict=laacfontdict )

            elif self._atomic_number == 89:
                self.ax.text(-0.6, 0.25, 'AC', fontdict=laacfontdict)

    def set_facecolor(self, color):
        if (self.rect is not None) and self.visible and self.single_ele:
            self.rect.set_facecolor(color)

    def add_number(self):
        _x = 0.45
        if self.atomic_number > 9:
            _x = 0.35
        if self.atomic_number > 99:
            _x = 0.3

        if self._visible and self._single_ele:
            self.ax.text(_x, 0.65, str(self._atomic_number), fontsize=self.row_column_size)

    def __call__(self, *args, **kwargs):
        return self.ax


class PltPeriodic(object):
    font_family = "Times New Roman"

    def __init__(self):
        self.fig, self.axes = plt.subplots(9, 18, figsize=(12, 7))
        self._colors = {}

    @property
    def color(self):
        return self._colors

    @color.setter
    def color(self, colors):
        """

                Args:
                    colors: {atomic_number: color,  ...}

        """
        self._colors = colors

    def blank_periodic(self):
        atomic_numebr = 0
        la_number = 56
        rc_number = 88
        increament = 1
        for i in range(9):
            for j in range(18):
                visible = True
                single_ele = True
                if i == 0:
                    if j > 0 and j < 17:
                        visible = False

                if i >= 1 and i <= 2:
                    if j > 1 and j < 12:
                        visible = False

                if i > 6:
                    if j < 3:
                        visible = False

                if visible:
                    if i <= 6:
                        atomic_numebr += increament
                        if atomic_numebr == 57 or atomic_numebr == 89:
                            increament = 15
                            single_ele = False

                        if (atomic_numebr >= 72 and atomic_numebr < 89) or (atomic_numebr >= 104):
                            increament = 1

                    if i == 7:
                        la_number += 1
                        atomic_numebr = la_number
                    if i == 8:
                        rc_number += 1
                        atomic_numebr = rc_number


                ax = self.axes[i, j]
                pe = PlotElement(ax, visible=visible, atomic_number=atomic_numebr, single_ele=single_ele)
                if len(self._colors) > 0:
                    if atomic_numebr in self._colors:
                        pe.set_facecolor(self._colors[atomic_numebr])
                    else:
                        pass
                pe.add_number()

        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.94, wspace=0.03, hspace=0.03)

    def _label_ax(self, num):
        _a = np.array([[self.axes[i, 3] for i in range(0, 3)],
                       [self.axes[i, 6] for i in range(0, 3)],
                       [self.axes[i, 9] for i in range(0, 3)]]).T
        if num == 1:
            return [_a[1, 1]]
        elif num == 2:
            return _a[:2, 1].flatten().tolist()
        elif num == 3:
            return np.hstack((_a[:2, 1], _a[0, 2])).flatten().tolist()
        elif num == 4:
            return _a[:2, 1:].flatten().tolist()
        elif num == 5:
            return np.hstack((_a[:2, :2].flatten(), _a[0, 2])).flatten().tolist()
        elif num == 6:
            return _a[:2, :].flatten().tolist()
        elif num == 7:
            assert np.hstack((_a[:2, :].flatten(), _a[2, 0])).flatten().tolist()
        elif num == 8:
            return np.hstack((_a[:2, :].flatten(), _a[2, :2].flatten())).flatten().tolist()
        else:
            return _a.flatten().tolist()

    def set_label(self, labels: dict):
        if len(labels) > 9:
            raise ValueError()
        else:
            self._aa = self._label_ax(len(labels))
            for i, (c, l) in enumerate(labels.items()):
                # a = PlotElement(self._aa[i], True)
                ax = self._aa[i]
                ax.set_xlim(-0.01, 0.91)
                ax.set_ylim(-0.01, 0.91)
                rect = Rectangle((0.3, 0.4), 0.5, 0.5, 0.0, linewidth=1, edgecolor='black', facecolor=c)
                ax.add_patch(rect)
                # a.set_facecolor(c)
                ax.text(1, 0.5, l, fontdict={'fontsize': 16, 'family': self.font_family})

    def set_colors(self, colors: dict):
        """

        Args:
            colors: {color1: [atomic_number1, atomic_number2, ...],
                     coloe2: [...]}

        Returns:

        """
        tmp = {}
        for k, v in colors.items():
            for i in v:
                if i in tmp:
                    print("color for %s  of %s will be replaced % s" % (i, tmp[i], k))
                tmp[i] = k
        self._colors = tmp

    def set_colors_for_blank_periodic(self, colors: dict):
        self.set_colors(colors)
        self.blank_periodic()

    def show(self):
        plt.show()

    def savefig(self, name):
        plt.savefig(name)


def run_periodic(tmpargs=None):
    
    from dancingcell.utility.auxbool_argparse import str2bool, str2dict
    import argparse

    m_description = ""
    usage = """
    """
    
    parser = argparse.ArgumentParser(description=m_description, usage=usage)
    parser.add_argument('-b', '--blank', type=str2bool, default=False, help='Blank periodic')
    parser.add_argument('-l', '--labels', type=str2dict, default=None, help='Set labels for each color')
    parser.add_argument('-ns', '--noshow', type=str2bool, default=False, help='No show')
    parser.add_argument('-s', '--savefn', type=str, default='', help='Save file name')

    subparsers = parser.add_subparsers(help='command', dest='command')
    read_color_parser = subparsers.add_parser('read_color')
    read_color_parser.add_argument('-f', '--json_fn', type=str, default='', help='Read two-color table')
    read_color_parser.add_argument('-t', '--two', type=str2bool, default=False, help='Read two-color table')

    set_color_parser = subparsers.add_parser('set_color')
    set_color_parser.add_argument('-c', '--colors', type=str2dict, default=False, help='Set color for each element')

    args, unparsed = parser.parse_known_args(tmpargs)
    # at = {'Sb': (1, 2, 3), 'Te': '5 10', 'Ge': [12, 13, 43], 'C': '13 19'}
    # at = {'Zr': (1,), 'Al': '2 108'}
    pp = PltPeriodic()
    if args.blank:
        pp.blank_periodic()
    
    # if args.colors:
    #     pp.set_colors_for_blank_periodic(colors=args.colors)
    #
    if args.command == 'read_color':
        if args.json_fn:
            fn = args.json_fn
        elif args.two:
            fn = get_fn('gray.json')
        else:
            fn = 'gray.json'

        with open(fn, 'r') as f:
            co = json.load(f)
        pp.set_colors_for_blank_periodic(colors=co)
    elif args.command == 'set_color':
        if args.colors:
            pp.set_colors_for_blank_periodic(colors=args.colors)
    
    if args.labels:
        pp.set_label(args.labels)
    
    if args.noshow:
        pass
    else:
        pp.show()
        
    if args.savefn:
        pp.savefig(name=args.savefn)
    

if __name__ == '__main__':
    # pp = PltPeriodic()
    # # pp.blank_periodic()
    # pp.set_colors_for_blank_periodic(colors={'lightcoral': [2, 5, 6, 7, 11, 17, 24, 38, 42, 43, 75, 76, 82, 57, 59, 63, 89, 91, 92 ,93, 94],
    #                       'gray':[29, 84, 85, 86, 87, 88, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106,
    #                               107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118] })
    # pp.set_label({'lightcoral': 'Energy Unstable',
    #               'gray':'Not Calculated'})
    #
    # pp.show()
    # pp.savefig('example31.pdf')
    tt = 'read_color -t 1 -s 1'.split()
    setcolor = {'lightcoral': [2, 5, 6, 7, 11, 17, 24, 38, 42, 43, 75, 76, 82, 57, 59, 63, 89, 91, 92 ,93, 94],
                'gray':[29, 84, 85, 86, 87, 88, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106,
                        107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118] }
    setlabel = {'lightcoral': 'Energy Unstable',
                'gray':'Not Calculated'}
    
    ll =['-l', str(setlabel),  'set_color', '-c', str(setcolor)]
    run_periodic()