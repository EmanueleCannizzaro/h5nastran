from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range
from collections import OrderedDict
from typing import List, Dict, Any

import tables
import numpy as np
from pandas import DataFrame

from result_table import ResultTable, TableDef, ResultTableData
from _shell_results import ShellElementForceStressResultTable, ShellElementForceStressResultTableComplex


class ElementForce(object):
    def __init__(self, h5n, elemental):
        self._h5n = h5n
        self._elemental = elemental

        self.bar = BAR(self._h5n, self)
        self.bars = BARS(self._h5n, self)
        self.bars_cplx = BARS_CPLX(self._h5n, self)
        self.bar_cplx = BAR_CPLX(self._h5n, self)
        self.beam = BEAM(self._h5n, self)
        self.beam3 = BEAM3(self._h5n, self)
        self.beam3_cplx = BEAM3_CPLX(self._h5n, self)
        self.beam_cplx = BEAM_CPLX(self._h5n, self)
        self.bend = BEND(self._h5n, self)
        self.bend_cplx = BEND_CPLX(self._h5n, self)
        self.bush = BUSH(self._h5n, self)
        self.bush1d = BUSH1D(self._h5n, self)
        self.bush_cplx = BUSH_CPLX(self._h5n, self)
        self.cone = CONE(self._h5n, self)
        self.conrod = CONROD(self._h5n, self)
        self.conrod_cplx = CONROD_CPLX(self._h5n, self)
        self.conv = CONV(self._h5n, self)
        self.convm = CONVM(self._h5n, self)
        self.damp1 = DAMP1(self._h5n, self)
        self.damp1_cplx = DAMP1_CPLX(self._h5n, self)
        self.damp2 = DAMP2(self._h5n, self)
        self.damp2_cplx = DAMP2_CPLX(self._h5n, self)
        self.damp3 = DAMP3(self._h5n, self)
        self.damp3_cplx = DAMP3_CPLX(self._h5n, self)
        self.damp4 = DAMP4(self._h5n, self)
        self.damp4_cplx = DAMP4_CPLX(self._h5n, self)
        self.elas1 = ELAS1(self._h5n, self)
        self.elas1_cplx = ELAS1_CPLX(self._h5n, self)
        self.elas2 = ELAS2(self._h5n, self)
        self.elas2_cplx = ELAS2_CPLX(self._h5n, self)
        self.elas3 = ELAS3(self._h5n, self)
        self.elas3_cplx = ELAS3_CPLX(self._h5n, self)
        self.elas4 = ELAS4(self._h5n, self)
        self.elas4_cplx = ELAS4_CPLX(self._h5n, self)
        self.fast = FAST(self._h5n, self)
        self.fast_cplx = FAST_CPLX(self._h5n, self)
        self.gap = GAP(self._h5n, self)
        # self.grad_flux = None  # skipping for now
        self.hbdye = HBDYE(self._h5n, self)
        self.hbdyg = HBDYG(self._h5n, self)
        self.hbdyp = HBDYP(self._h5n, self)
        self.quad4 = QUAD4(self._h5n, self)
        self.quad4_cn = QUAD4_CN(self._h5n, self)
        self.quad4_cn_cplx = QUAD4_CN_CPLX(self._h5n, self)
        self.quad4_comp = QUAD4_COMP(self._h5n, self)
        self.quad4_cplx = QUAD4_CPLX(self._h5n, self)
        self.quad8 = QUAD8(self._h5n, self)
        self.quad8_comp = QUAD8_COMP(self._h5n, self)
        self.quad8_cplx = QUAD8_CPLX(self._h5n, self)
        self.quadr = QUADR(self._h5n, self)
        self.quadr_cplx = QUADR_CPLX(self._h5n, self)
        self.rac2d = RAC2D(self._h5n, self)
        self.rac2d_cplx = RAC2D_CPLX(self._h5n, self)
        self.rac3d = RAC3D(self._h5n, self)
        self.rac3d_cplx = RAC3D_CPLX(self._h5n, self)
        self.radbc = RADBC(self._h5n, self)
        self.radint = RADINT(self._h5n, self)
        self.rod = ROD(self._h5n, self)
        self.rod_cplx = ROD_CPLX(self._h5n, self)
        self.seam = SEAM(self._h5n, self)
        self.seam_cplx = SEAM_CPLX(self._h5n, self)
        self.shear = SHEAR(self._h5n, self)
        self.shear_cplx = SHEAR_CPLX(self._h5n, self)
        self.tria3 = TRIA3(self._h5n, self)
        self.tria3_comp = TRIA3_COMP(self._h5n, self)
        self.tria3_cplx = TRIA3_CPLX(self._h5n, self)
        self.tria6 = TRIA6(self._h5n, self)
        self.tria6_comp = TRIA6_COMP(self._h5n, self)
        self.tria6_cplx = TRIA6_CPLX(self._h5n, self)
        self.triar = TRIAR(self._h5n, self)
        self.triar_cplx = TRIAR_CPLX(self._h5n, self)
        self.tube = TUBE(self._h5n, self)
        self.tube_cplx = TUBE_CPLX(self._h5n, self)
        self.visc = VISC(self._h5n, self)
        self.visc_cplx = VISC_CPLX(self._h5n, self)
        self.weld = WELD(self._h5n, self)
        self.weldc = WELDC(self._h5n, self)
        self.weldc_cplx = WELDC_CPLX(self._h5n, self)
        self.weldp = WELDP(self._h5n, self)
        self.weldp_cplx = WELDP_CPLX(self._h5n, self)
        self.weld_cplx = WELD_CPLX(self._h5n, self)

    def path(self):
        return self._elemental.path() + ['ELEMENT_FORCE']

    def search(self, element_ids, domain_ids=(), material_sys=False):
        # :type (List[int], List[int]) -> ElementForceResult
        result = ElementForceResult()
        _result = result.__dict__
        table_ids = self.__dict__.keys()
        _tables = self.__dict__
        for table_id in table_ids:
            if table_id.startswith('_'):  # not a table
                continue
            _result[table_id] = _tables[table_id].search(element_ids, domain_ids, material_sys=material_sys)
                
        return result
    
    
########################################################################################################################

class ElementForceResult(object):
    def __init__(self):
        self.bar = None  # type: DataFrame
        self.bars = None  # type: DataFrame
        self.bars_cplx = None  # type: DataFrame
        self.bar_cplx = None  # type: DataFrame
        self.beam = None  # type: DataFrame
        self.beam3 = None  # type: DataFrame
        self.beam3_cplx = None  # type: DataFrame
        self.beam_cplx = None  # type: DataFrame
        self.bend = None  # type: DataFrame
        self.bend_cplx = None  # type: DataFrame
        self.bush = None  # type: DataFrame
        self.bush1d = None  # type: DataFrame
        self.bush_cplx = None  # type: DataFrame
        self.cone = None  # type: DataFrame
        self.conrod = None  # type: DataFrame
        self.conrod_cplx = None  # type: DataFrame
        self.conv = None  # type: DataFrame
        self.convm = None  # type: DataFrame
        self.damp1 = None  # type: DataFrame
        self.damp1_cplx = None  # type: DataFrame
        self.damp2 = None  # type: DataFrame
        self.damp2_cplx = None  # type: DataFrame
        self.damp3 = None  # type: DataFrame
        self.damp3_cplx = None  # type: DataFrame
        self.damp4 = None  # type: DataFrame
        self.damp4_cplx = None  # type: DataFrame
        self.elas1 = None  # type: DataFrame
        self.elas1_cplx = None  # type: DataFrame
        self.elas2 = None  # type: DataFrame
        self.elas2_cplx = None  # type: DataFrame
        self.elas3 = None  # type: DataFrame
        self.elas3_cplx = None  # type: DataFrame
        self.elas4 = None  # type: DataFrame
        self.elas4_cplx = None  # type: DataFrame
        self.fast = None  # type: DataFrame
        self.fast_cplx = None  # type: DataFrame
        self.gap = None  # type: DataFrame
        self.hbdye = None  # type: DataFrame
        self.hbdyg = None  # type: DataFrame
        self.hbdyp = None  # type: DataFrame
        self.quad4 = None  # type: DataFrame
        self.quad4_cn = None  # type: DataFrame
        self.quad4_cn_cplx = None  # type: DataFrame
        self.quad4_comp = None  # type: DataFrame
        self.quad4_cplx = None  # type: DataFrame
        self.quad8 = None  # type: DataFrame
        self.quad8_comp = None  # type: DataFrame
        self.quad8_cplx = None  # type: DataFrame
        self.quadr = None  # type: DataFrame
        self.quadr_cplx = None  # type: DataFrame
        self.rac2d = None  # type: DataFrame
        self.rac2d_cplx = None  # type: DataFrame
        self.rac3d = None  # type: DataFrame
        self.rac3d_cplx = None  # type: DataFrame
        self.radbc = None  # type: DataFrame
        self.radint = None  # type: DataFrame
        self.rod = None  # type: DataFrame
        self.rod_cplx = None  # type: DataFrame
        self.seam = None  # type: DataFrame
        self.seam_cplx = None  # type: DataFrame
        self.shear = None  # type: DataFrame
        self.shear_cplx = None  # type: DataFrame
        self.tria3 = None  # type: DataFrame
        self.tria3_comp = None  # type: DataFrame
        self.tria3_cplx = None  # type: DataFrame
        self.tria6 = None  # type: DataFrame
        self.tria6_comp = None  # type: DataFrame
        self.tria6_cplx = None  # type: DataFrame
        self.triar = None  # type: DataFrame
        self.triar_cplx = None  # type: DataFrame
        self.tube = None  # type: DataFrame
        self.tube_cplx = None  # type: DataFrame
        self.visc = None  # type: DataFrame
        self.visc_cplx = None  # type: DataFrame
        self.weld = None  # type: DataFrame
        self.weldc = None  # type: DataFrame
        self.weldc_cplx = None  # type: DataFrame
        self.weldp = None  # type: DataFrame
        self.weldp_cplx = None  # type: DataFrame
        self.weld_cplx = None  # type: DataFrame
        

########################################################################################################################


class BAR(ResultTable):
    result_type = 'ELEMENT FORCES 34 BAR REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BAR', result_type)


########################################################################################################################


class BARS(ResultTable):
    result_type = 'ELEMENT FORCES 100 BARS REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BARS', result_type)


########################################################################################################################


class BARS_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 100 BARS COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BARS_CPLX', result_type)


########################################################################################################################


class BAR_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 34 BAR COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BAR_CPLX', result_type)


########################################################################################################################


class BEAM(ResultTable):
    result_type = 'ELEMENT FORCES 2 BEAM REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BEAM', result_type)


########################################################################################################################


class BEAM3(ResultTable):
    result_type = 'ELEMENT FORCES 184 BEAM3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BEAM3', result_type)


########################################################################################################################


class BEAM3_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 184 BEAM3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BEAM3_CPLX', result_type)


########################################################################################################################


class BEAM_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 2 BEAM COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BEAM_CPLX', result_type)


########################################################################################################################


class BEND(ResultTable):
    result_type = 'ELEMENT FORCES 69 BEND REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BEND', result_type)


########################################################################################################################


class BEND_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 69 BEND COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BEND_CPLX', result_type)


########################################################################################################################


class BUSH(ResultTable):
    result_type = 'ELEMENT FORCES 102 BUSH REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BUSH', result_type)


########################################################################################################################


class BUSH1D(ResultTable):
    result_type = 'ELEMENT FORCES 40 BUSH1D REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BUSH1D', result_type)


########################################################################################################################


class BUSH_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 102 BUSH COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/BUSH_CPLX', result_type)


########################################################################################################################


class CONE(ResultTable):
    result_type = 'ELEMENT FORCES 35 CONE REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/CONE', result_type)


########################################################################################################################


class CONROD(ResultTable):
    result_type = 'ELEMENT FORCES 10 CONROD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/CONROD', result_type)


########################################################################################################################


class CONROD_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 10 CONROD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/CONROD_CPLX', result_type)


########################################################################################################################


class CONV(ResultTable):
    result_type = 'ELEMENT FORCES 110 CONV REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/CONV', result_type)


########################################################################################################################


class CONVM(ResultTable):
    result_type = 'ELEMENT FORCES 111 CONVM REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/CONVM', result_type)


########################################################################################################################


class DAMP1(ResultTable):
    result_type = 'ELEMENT FORCES 20 DAMP1 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/DAMP1', result_type)


########################################################################################################################


class DAMP1_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 20 DAMP1 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/DAMP1_CPLX', result_type)


########################################################################################################################


class DAMP2(ResultTable):
    result_type = 'ELEMENT FORCES 21 DAMP2 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/DAMP2', result_type)


########################################################################################################################


class DAMP2_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 21 DAMP2 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/DAMP2_CPLX', result_type)


########################################################################################################################


class DAMP3(ResultTable):
    result_type = 'ELEMENT FORCES 22 DAMP3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/DAMP3', result_type)


########################################################################################################################


class DAMP3_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 22 DAMP3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/DAMP3_CPLX', result_type)


########################################################################################################################


class DAMP4(ResultTable):
    result_type = 'ELEMENT FORCES 23 DAMP4 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/DAMP4', result_type)


########################################################################################################################


class DAMP4_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 23 DAMP4 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/DAMP4_CPLX', result_type)


########################################################################################################################


class ELAS1(ResultTable):
    result_type = 'ELEMENT FORCES 11 ELAS1 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ELAS1', result_type)


########################################################################################################################


class ELAS1_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 11 ELAS1 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ELAS1_CPLX', result_type)


########################################################################################################################


class ELAS2(ResultTable):
    result_type = 'ELEMENT FORCES 12 ELAS2 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ELAS2', result_type)


########################################################################################################################


class ELAS2_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 12 ELAS2 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ELAS2_CPLX', result_type)


########################################################################################################################


class ELAS3(ResultTable):
    result_type = 'ELEMENT FORCES 13 ELAS3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ELAS3', result_type)


########################################################################################################################


class ELAS3_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 13 ELAS3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ELAS3_CPLX', result_type)


########################################################################################################################


class ELAS4(ResultTable):
    result_type = 'ELEMENT FORCES 14 ELAS4 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ELAS4', result_type)


########################################################################################################################


class ELAS4_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 14 ELAS4 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ELAS4_CPLX', result_type)


########################################################################################################################


class FAST(ResultTable):
    result_type = 'ELEMENT FORCES 126 FAST REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/FAST', result_type)


########################################################################################################################


class FAST_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 126 FAST COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/FAST_CPLX', result_type)


########################################################################################################################


class GAP(ResultTable):
    result_type = 'ELEMENT FORCES 38 GAP REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/GAP', result_type)


########################################################################################################################


class HBDYE(ResultTable):
    result_type = 'ELEMENT FORCES 107 HBDYE REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/HBDYE', result_type)


########################################################################################################################


class HBDYG(ResultTable):
    result_type = 'ELEMENT FORCES 108 HBDYG REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/HBDYG', result_type)


########################################################################################################################


class HBDYP(ResultTable):
    result_type = 'ELEMENT FORCES 109 HBDYP REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/HBDYP', result_type)


########################################################################################################################


class QUAD4(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT FORCES 33 QUAD4 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUAD4', result_type)
    table_def.add_index_option('MATERIAL', None)
    result_data_cols = ['MX', 'MY', 'MXY', 'BMX', 'BMY', 'BMXY', 'TX', 'TY']
    result_data_group_by = ['EID', 'DOMAIN_ID']


########################################################################################################################


class QUAD4_CN(ResultTable):
    result_type = 'ELEMENT FORCES 144 QUAD4C REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUAD4_CN', result_type)


########################################################################################################################


class QUAD4_CN_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 144 QUAD4C COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUAD4_CN_CPLX', result_type)


########################################################################################################################


class QUAD4_COMP(ResultTable):
    result_type = 'ELEMENT FORCES 95 QUAD4LC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUAD4_COMP', result_type)


########################################################################################################################


class QUAD4_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT FORCES 33 QUAD4 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUAD4_CPLX', result_type)


########################################################################################################################


class QUAD8(ResultTable):
    result_type = 'ELEMENT FORCES 64 QUAD8 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUAD8', result_type)


########################################################################################################################


class QUAD8_COMP(ResultTable):
    result_type = 'ELEMENT FORCES 96 QUAD8LC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUAD8_COMP', result_type)


########################################################################################################################


class QUAD8_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 64 QUAD8 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUAD8_CPLX', result_type)


########################################################################################################################


class QUADR(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT FORCES 82 QUADR REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUADR', result_type)


########################################################################################################################


class QUADR_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT FORCES 82 QUADR COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/QUADR_CPLX', result_type)


########################################################################################################################


class RAC2D(ResultTable):
    result_type = 'ELEMENT FORCES 60 RAC2D REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/RAC2D', result_type)


########################################################################################################################


class RAC2D_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 60 RAC2D COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/RAC2D_CPLX', result_type)


########################################################################################################################


class RAC3D(ResultTable):
    result_type = 'ELEMENT FORCES 61 RAC3D REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/RAC3D', result_type)


########################################################################################################################


class RAC3D_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 61 RAC3D COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/RAC3D_CPLX', result_type)


########################################################################################################################


class RADBC(ResultTable):
    result_type = 'ELEMENT FORCES 115 RADBC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/RADBC', result_type)


########################################################################################################################


class RADINT(ResultTable):
    result_type = 'ELEMENT FORCES 155 RADINT REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/RADINT', result_type)


########################################################################################################################


class ROD(ResultTable):
    result_type = 'ELEMENT FORCES 1 ROD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ROD', result_type)


########################################################################################################################


class ROD_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 1 ROD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/ROD_CPLX', result_type)


########################################################################################################################


class SEAM(ResultTable):
    result_type = 'ELEMENT FORCES 119 SEAM REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/SEAM', result_type)


########################################################################################################################


class SEAM_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 119 SEAM COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/SEAM_CPLX', result_type)


########################################################################################################################


class SHEAR(ResultTable):
    result_type = 'ELEMENT FORCES 4 SHEAR REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/SHEAR', result_type)


########################################################################################################################


class SHEAR_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 4 SHEAR COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/SHEAR_CPLX', result_type)


########################################################################################################################


class TRIA3(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT FORCES 74 TRIA3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TRIA3', result_type)
    table_def.add_index_option('MATERIAL', None)
    result_data_cols = ['MX', 'MY', 'MXY', 'BMX', 'BMY', 'BMXY', 'TX', 'TY']
    result_data_group_by = ['EID', 'DOMAIN_ID']


########################################################################################################################


class TRIA3_COMP(ResultTable):
    result_type = 'ELEMENT FORCES 97 TRIA3LC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TRIA3_COMP', result_type)


########################################################################################################################


class TRIA3_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT FORCES 74 TRIA3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TRIA3_CPLX', result_type)


########################################################################################################################


class TRIA6(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT FORCES 75 TRIA6 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TRIA6', result_type)


########################################################################################################################


class TRIA6_COMP(ResultTable):
    result_type = 'ELEMENT FORCES 98 TRIA6LC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TRIA6_COMP', result_type)


########################################################################################################################


class TRIA6_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT FORCES 75 TRIA6 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TRIA6_CPLX', result_type)


########################################################################################################################


class TRIAR(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT FORCES 70 TRIAR REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TRIAR', result_type)


########################################################################################################################


class TRIAR_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT FORCES 70 TRIAR COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TRIAR_CPLX', result_type)


########################################################################################################################


class TUBE(ResultTable):
    result_type = 'ELEMENT FORCES 3 TUBE REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TUBE', result_type)


########################################################################################################################


class TUBE_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 3 TUBE COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/TUBE_CPLX', result_type)


########################################################################################################################


class VISC(ResultTable):
    result_type = 'ELEMENT FORCES 24 VISC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/VISC', result_type)


########################################################################################################################


class VISC_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 24 VISC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/VISC_CPLX', result_type)


########################################################################################################################


class WELD(ResultTable):
    result_type = 'ELEMENT FORCES 200 WELD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/WELD', result_type)


########################################################################################################################


class WELDC(ResultTable):
    result_type = 'ELEMENT FORCES 117 WELDC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/WELDC', result_type)


########################################################################################################################


class WELDC_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 117 WELDC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/WELDC_CPLX', result_type)


########################################################################################################################


class WELDP(ResultTable):
    result_type = 'ELEMENT FORCES 118 WELDP REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/WELDP', result_type)


########################################################################################################################


class WELDP_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 118 WELDP COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/WELDP_CPLX', result_type)


########################################################################################################################


class WELD_CPLX(ResultTable):
    result_type = 'ELEMENT FORCES 200 WELD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/ELEMENT_FORCE/WELD_CPLX', result_type)


