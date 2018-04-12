from __future__ import print_function, absolute_import
from six import iteritems, itervalues, iterkeys
from six.moves import range
from collections import defaultdict

import tables
import numpy as np

from card_table import CardTable, TableDef
from data_helper import DataHelper


class Dynamic(object):
    def __init__(self, h5n, input):
        self._h5n = h5n
        self._input = input

        self.eigrl = EIGRL(self._h5n, self)
        self.freq1 = FREQ1(self._h5n, self)

    def path(self):
        return self._input.path() + ['DYNAMIC']

    def read(self):
        for key, item in iteritems(self.__dict__):
            if key.startswith('_'):
                continue
            try:
                item.read()
            except AttributeError:
                pass


########################################################################################################################


class EIGRL(CardTable):
    table_def = TableDef.create('/NASTRAN/INPUT/DYNAMIC/EIGRL/IDENTITY')

    @classmethod
    def from_bdf(cls, cards):
        card_ids = sorted(cards.keys())

        freqs = {'IDENTITY': {'FI': []}}

        result = {'IDENTITY': {'SID': [], 'V1': [], 'V2': [], 'ND': [], 'MSGLVL': [], 'MAXSET': [],
                               'SHFSCL': [], 'FLAG1': [], 'FLAG2': [], 'NORM': [], 'ALPH': [], 'FREQS_POS': [],
                               'FREQS_LEN': [], 'DOMAIN_ID': []},
                  'FREQS': freqs,
                  '_subtables': ['FREQS']}

        fi = freqs['IDENTITY']['FI']
        identity = result['IDENTITY']
        sid = identity['SID']
        v1 = identity['V1']
        v2 = identity['V2']
        nd = identity['ND']
        msglvl = identity['MSGLVL']
        maxset = identity['MAXSET']
        shfscl = identity['SHFSCL']
        flag1 = identity['FLAG1']
        flag2 = identity['FLAG2']
        norm = identity['NORM']
        alph = identity['ALPH']
        freqs_pos = identity['FREQS_POS']
        freqs_len = identity['FREQS_LEN']

        def _get_option(val, option, option_data, default):
            if val in ('', None):
                val = option_data.get(option, None)
            if val is None:
                val = default
            return val

        _pos = 0

        for card_id in card_ids:
            card = cards[card_id]

            option_data = defaultdict(list)

            for i in range(len(card.options)):
                option_data[card.options[i]].append(card.values[i])

            _v1 = _get_option(card.v1, 'V1', option_data, DataHelper.default_double)
            _v2 = _get_option(card.v2, 'V2', option_data, DataHelper.default_double)
            _nd = _get_option(card.nd, 'ND', option_data, DataHelper.default_int)
            _msglvl = _get_option(card.msglvl, 'MSGLVL', option_data, DataHelper.default_int)
            _maxset = _get_option(card.maxset, 'MAXSET', option_data, DataHelper.default_int)
            _shfscl = _get_option(card.shfscl, 'SHFSCL', option_data, DataHelper.default_double)
            _norm = _get_option(card.norm, 'NORM', option_data, DataHelper.default_str)
            _alph = _get_option(None, 'ALPH', option_data, DataHelper.default_double)

            # TODO: EIGRL how is nums used?, what is flag1 and flag2?
            # _nums = _get_option(None, 'NUMS', option_data, 1)
            _fi = _get_option(None, 'Fi', option_data, [])

            sid.append(card.sid)
            v1.append(_v1)
            v2.append(_v2)
            nd.append(_nd)
            msglvl.append(_msglvl)
            maxset.append(_maxset)
            shfscl.append(_shfscl)
            norm.append(_norm)
            alph.append(_alph)
            flag1.append(DataHelper.unknown_int)
            flag2.append(DataHelper.unknown_int)
            freqs_pos.append(_pos)
            _len = len(_fi)
            _pos += _len
            freqs_len.append(_len)
            fi += _fi
            
        return result


########################################################################################################################


class FREQ1(CardTable):
    table_def = TableDef.create('/NASTRAN/INPUT/DYNAMIC/FREQ1')

    @classmethod
    def from_bdf(cls, cards):
        card_ids = sorted(cards.keys())

        result = {'IDENTITY': {'SID': [], 'F1': [], 'DF': [], 'NDF': [], 'DOMAIN_ID': []}}

        identity = result['IDENTITY']
        sid = identity['SID']
        f1 = identity['F1']
        df = identity['DF']
        ndf = identity['NDF']

        for card_id in card_ids:
            card_list = cards[card_id]

            for card in card_list:
                sid.append(card.sid)
                f1.append(card.f1)
                df.append(card.df)
                ndf.append(card.ndf)

        return result
