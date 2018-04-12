from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

import tables
import numpy as np

from card_table import CardTable, TableDef
from transformation import Transformation


class CoordinateSystem(object):
    def __init__(self, h5n, input):
        self._h5n = h5n
        self._input = input

        self.cord1c = CORD1C(self._h5n, self)
        self.cord1r = CORD1R(self._h5n, self)
        self.cord1s = CORD1S(self._h5n, self)
        self.cord2c = CORD2C(self._h5n, self)
        self.cord2r = CORD2R(self._h5n, self)
        self.cord2s = CORD2S(self._h5n, self)
        self.cord3g = CORD3G(self._h5n, self)
        self.cord3r = CORD3R(self._h5n, self)
        # self.transformation = TRANSFORMATION(self._h5n, self)
        self.h5n_transformation = Transformation(self._h5n, self)

    def path(self):
        return self._input.path() + ['COORDINATE_SYSTEM']

    def read(self):
        for key, item in iteritems(self.__dict__):
            if key.startswith('_'):
                continue
            try:
                item.read()
            except AttributeError:
                pass

    def update(self):
        self.h5n_transformation.update()


########################################################################################################################


class CORD1C(CardTable):
    table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/CORD1C')

########################################################################################################################


class CORD1R(CardTable):
    table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/CORD1R')

########################################################################################################################

class CORD1S(CardTable):
    table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/CORD1S')

########################################################################################################################


class _CORD2(CardTable):
    @classmethod
    def from_bdf(cls, cards):
        card_ids = sorted(cards.keys())

        data = np.empty(len(card_ids), dtype=cls.table_def.dtype)

        cid = data['CID']
        rid = data['RID']
        a1 = data['A1']
        a2 = data['A2']
        a3 = data['A3']
        b1 = data['B1']
        b2 = data['B2']
        b3 = data['B3']
        c1 = data['C1']
        c2 = data['C2']
        c3 = data['C3']

        i = -1
        for card_id in card_ids:
            i += 1
            card = cards[card_id]

            cid[i] = card.cid
            rid[i] = card.rid
            a1[i], a2[i], a3[i] = card.e1
            b1[i], b2[i], b3[i] = card.e2
            c1[i], c2[i], c3[i] = card.e3

        result = {'IDENTITY': data}

        return result


########################################################################################################################


class CORD2C(_CORD2):
    table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/CORD2C')

########################################################################################################################


class CORD2R(_CORD2):
    table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/CORD2R')

########################################################################################################################


class CORD2S(_CORD2):
    table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/CORD2S')

########################################################################################################################


class CORD3G(CardTable):
    table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/CORD3G')

########################################################################################################################


class CORD3R(CardTable):
    table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/CORD3R')

########################################################################################################################


# class TRANSFORMATION(CardTable):
#     table_def = TableDef.create('/NASTRAN/INPUT/COORDINATE_SYSTEM/TRANSFORMATION/IDENTITY')

########################################################################################################################
