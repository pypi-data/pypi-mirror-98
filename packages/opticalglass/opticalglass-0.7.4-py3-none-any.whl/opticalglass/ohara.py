#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Michael J. Hayford
""" Support for the Ohara Glass catalog

.. codeauthor: Michael J. Hayford
"""
import logging
from .util import Singleton

import numpy as np

from . import glass


class OharaCatalog(glass.GlassCatalogXLSX, metaclass=Singleton):
    #    data_header = 1
    #    data_start = 2
    #    num_glasses = 134
    #    name_col_offset = 1
    #    coef_col_offset = 60
    #    index_col_offset = 4
    nline_str = {'t': 'nt',
                 's': 'ns',
                 'r': 'nr',
                 'C': 'nC',
                 "C'": "nC'",
                 'D': 'nD',
                 'd': 'nd',
                 'e': 'ne',
                 'F': 'nF',
                 "F'": "nF'",
                 'g': 'ng',
                 'h': 'nh',
                 'i': 'ni'}

    def __init__(self, fname='OHARA.xlsx'):
        super().__init__('Ohara', fname, 'Glass ', 'A1', 'n2325',
                         transmission_offset=81, num_wvls=32)

    def create_glass(self, gname, gcat):
        return OharaGlass(gname)


class OharaGlass(glass.Glass):
    catalog = OharaCatalog()

    def __init__(self, gname, catalog=None):
        if catalog is not None:
            self.catalog = catalog
        super().__init__(gname)

    def glass_code(self):
        return super().glass_code('nd', 'νd')

    def calc_rindex(self, wv_nm):
        wv = 0.001*wv_nm
        wv2 = wv*wv
        coefs = self.coefs
        n2 = 1 + coefs[0]*wv2/(wv2 - coefs[3])
        n2 += coefs[1]*wv2/(wv2 - coefs[4])
        n2 += coefs[2]*wv2/(wv2 - coefs[5])
        return np.sqrt(n2)
