from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

import tables
import numpy as np

from result_table import ResultTable, TableDef, DataGetter
from data_helper import DataHelper


class Energy(object):
    def __init__(self, h5n, elemental):
        self._h5n = h5n
        self._elemental = elemental

        self.strain_elem = STRAIN_ELEM(self._h5n, self)

    def path(self):
        return self._elemental.path() + ['ENERGY']

########################################################################################################################


def _validator(data):
    # TODO: what is IDENT in STRAIN_ELEM table?
    data.append(DataHelper.unknown_int)  # this is why indices_len=5
    return data


# TODO: STRAIN_ELEM tables needs to be sorted properly
class STRAIN_ELEM(ResultTable):
    result_type = [
        'ELEMENT STRAIN ENERGIES %s REAL' % etype for etype in
        ['BAR', 'BEAM', 'QUAD4', 'TRIA3']
    ]
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ENERGY/STRAIN_ELEM', result_type,
                                indices=DataGetter(indices=[0, 2, 3, 4], indices_len=5),
                                validator=_validator
                                )
