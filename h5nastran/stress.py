from __future__ import print_function, absolute_import
from six import iteritems, itervalues
from six.moves import range

import tables
import numpy as np

from result_table import ResultTable, TableDef, DataGetter
from _shell_results import ShellElementForceStressResultTable, ShellElementForceStressResultTableComplex


class Stress(object):
    def __init__(self, h5n, elemental):
        self._h5n = h5n
        self._elemental = elemental

        self.axif2 = AXIF2(self._h5n, self)
        self.axif2_cplx = AXIF2_CPLX(self._h5n, self)
        self.axif3 = AXIF3(self._h5n, self)
        self.axif3_cplx = AXIF3_CPLX(self._h5n, self)
        self.axif4 = AXIF4(self._h5n, self)
        self.axif4_cplx = AXIF4_CPLX(self._h5n, self)
        self.axisym = AXISYM(self._h5n, self)
        self.bar = BAR(self._h5n, self)
        self.bars = BARS(self._h5n, self)
        self.bars_cplx = BARS_CPLX(self._h5n, self)
        self.bar_cplx = BAR_CPLX(self._h5n, self)
        self.bar_nl = BAR_NL(self._h5n, self)
        self.bar_rr = BAR_RR(self._h5n, self)
        self.beam = BEAM(self._h5n, self)
        self.beam3 = BEAM3(self._h5n, self)
        self.beam3_cplx = BEAM3_CPLX(self._h5n, self)
        self.beam_cplx = BEAM_CPLX(self._h5n, self)
        self.beam_nl = BEAM_NL(self._h5n, self)
        self.beam_rr = BEAM_RR(self._h5n, self)
        self.bush = BUSH(self._h5n, self)
        self.bush1d = BUSH1D(self._h5n, self)
        self.bush1d_cplx = BUSH1D_CPLX(self._h5n, self)
        self.bush1d_rr = BUSH1D_RR(self._h5n, self)
        self.bush_cplx = BUSH_CPLX(self._h5n, self)
        self.bush_nl = BUSH_NL(self._h5n, self)
        self.cone = CONE(self._h5n, self)
        self.conrod = CONROD(self._h5n, self)
        self.conrod_cplx = CONROD_CPLX(self._h5n, self)
        self.conrod_nl = CONROD_NL(self._h5n, self)
        self.conrod_rr = CONROD_RR(self._h5n, self)
        self.elas1 = ELAS1(self._h5n, self)
        self.elas1_cplx = ELAS1_CPLX(self._h5n, self)
        self.elas1_nl = ELAS1_NL(self._h5n, self)
        self.elas2 = ELAS2(self._h5n, self)
        self.elas2_cplx = ELAS2_CPLX(self._h5n, self)
        self.elas3 = ELAS3(self._h5n, self)
        self.elas3_cplx = ELAS3_CPLX(self._h5n, self)
        self.elas3_nl = ELAS3_NL(self._h5n, self)
        # self.elem_comp = None  # skipping for now
        # self.extreme_fibre = None  # skipping for now
        # self.extreme_fibre_cplx = None  # skipping for now
        self.fast = FAST(self._h5n, self)
        self.fast_cplx = FAST_CPLX(self._h5n, self)
        self.gap = GAP(self._h5n, self)
        self.gap_nl = GAP_NL(self._h5n, self)
        self.hexa = HEXA(self._h5n, self)
        self.hexa20_27fdnl = HEXA20_27FDNL(self._h5n, self)
        self.hexa20_8fdnl = HEXA20_8FDNL(self._h5n, self)
        self.hexa20_fd = HEXA20_FD(self._h5n, self)
        self.hexa_cplx = HEXA_CPLX(self._h5n, self)
        self.hexa_fd = HEXA_FD(self._h5n, self)
        self.hexa_fdnl = HEXA_FDNL(self._h5n, self)
        self.hexa_nl = HEXA_NL(self._h5n, self)
        self.ifhexa = IFHEXA(self._h5n, self)
        self.ifpenta = IFPENTA(self._h5n, self)
        self.penta = PENTA(self._h5n, self)
        self.penta15_21fdnl = PENTA15_21FDNL(self._h5n, self)
        self.penta15_6fdnl = PENTA15_6FDNL(self._h5n, self)
        self.penta15_fd = PENTA15_FD(self._h5n, self)
        self.penta_fdnl = PENTA_FDNL(self._h5n, self)
        self.penta_nl = PENTA_NL(self._h5n, self)
        self.quad4 = QUAD4(self._h5n, self)
        self.quad4_comp = QUAD4_COMP(self._h5n, self)
        self.quad4_comp_cplx = QUAD4_COMP_CPLX(self._h5n, self)
        self.quad4_cplx = QUAD4_CPLX(self._h5n, self)
        self.quad4_fd = QUAD4_FD(self._h5n, self)
        self.quad4_fdnl = QUAD4_FDNL(self._h5n, self)
        self.quad4_fd_cplx = QUAD4_FD_CPLX(self._h5n, self)
        self.quad4_nl = QUAD4_NL(self._h5n, self)
        self.quad8 = QUAD8(self._h5n, self)
        self.quad8_4fdnl = QUAD8_4FDNL(self._h5n, self)
        self.quad8_9fdnl = QUAD8_9FDNL(self._h5n, self)
        self.quad8_comp = QUAD8_COMP(self._h5n, self)
        self.quad8_comp_cplx = QUAD8_COMP_CPLX(self._h5n, self)
        self.quad8_cplx = QUAD8_CPLX(self._h5n, self)
        self.quad8_fd = QUAD8_FD(self._h5n, self)
        self.quad8_fd_cplx = QUAD8_FD_CPLX(self._h5n, self)
        self.quadr = QUADR(self._h5n, self)
        self.quadr_comp = QUADR_COMP(self._h5n, self)
        self.quadr_comp_cplx = QUADR_COMP_CPLX(self._h5n, self)
        self.quadr_cplx = QUADR_CPLX(self._h5n, self)
        # self.quadr_fd = None  # skipping for now
        # self.quadr_fd_cplx = None  # skipping for now
        self.quadr_nl = QUADR_NL(self._h5n, self)
        self.quadx4_fd = QUADX4_FD(self._h5n, self)
        self.quadx4_fdnl = QUADX4_FDNL(self._h5n, self)
        self.quadx4_fd_cplx = QUADX4_FD_CPLX(self._h5n, self)
        self.quadx8_4fdnl = QUADX8_4FDNL(self._h5n, self)
        self.quadx8_9fdnl = QUADX8_9FDNL(self._h5n, self)
        self.quadx8_fd = QUADX8_FD(self._h5n, self)
        self.quadx8_fd_cplx = QUADX8_FD_CPLX(self._h5n, self)
        self.quad_cn = QUAD_CN(self._h5n, self)
        self.quad_cn_cplx = QUAD_CN_CPLX(self._h5n, self)
        self.rac2d = RAC2D(self._h5n, self)
        self.rac3d = RAC3D(self._h5n, self)
        self.rod = ROD(self._h5n, self)
        self.rod_cplx = ROD_CPLX(self._h5n, self)
        self.rod_nl = ROD_NL(self._h5n, self)
        self.rod_rr = ROD_RR(self._h5n, self)
        self.seam = SEAM(self._h5n, self)
        self.seamp = SEAMP(self._h5n, self)
        self.seamp_cplx = SEAMP_CPLX(self._h5n, self)
        self.shear = SHEAR(self._h5n, self)
        self.shear_cplx = SHEAR_CPLX(self._h5n, self)
        self.shear_rr = SHEAR_RR(self._h5n, self)
        self.slot3 = SLOT3(self._h5n, self)
        self.slot3_cplx = SLOT3_CPLX(self._h5n, self)
        self.slot4 = SLOT4(self._h5n, self)
        self.slot4_cplx = SLOT4_CPLX(self._h5n, self)
        self.tetra = TETRA(self._h5n, self)
        self.tetra10_4fdnl = TETRA10_4FDNL(self._h5n, self)
        self.tetra10_5fdnl = TETRA10_5FDNL(self._h5n, self)
        self.tetra10_fd = TETRA10_FD(self._h5n, self)
        self.tetra4_fdnl = TETRA4_FDNL(self._h5n, self)
        self.tetra_cplx = TETRA_CPLX(self._h5n, self)
        self.tetra_fd = TETRA_FD(self._h5n, self)
        self.tetra_fdnl = TETRA_FDNL(self._h5n, self)
        self.tetra_nl = TETRA_NL(self._h5n, self)
        self.tria3 = TRIA3(self._h5n, self)
        self.tria3_1fdnl = TRIA3_1FDNL(self._h5n, self)
        self.tria3_3fdnl = TRIA3_3FDNL(self._h5n, self)
        self.tria3_comp = TRIA3_COMP(self._h5n, self)
        self.tria3_comp_cplx = TRIA3_COMP_CPLX(self._h5n, self)
        self.tria3_cplx = TRIA3_CPLX(self._h5n, self)
        self.tria3_fd = TRIA3_FD(self._h5n, self)
        self.tria3_fd_cplx = TRIA3_FD_CPLX(self._h5n, self)
        self.tria3_nl = TRIA3_NL(self._h5n, self)
        self.tria6 = TRIA6(self._h5n, self)
        self.tria6_comp = TRIA6_COMP(self._h5n, self)
        self.tria6_comp_cplx = TRIA6_COMP_CPLX(self._h5n, self)
        self.tria6_cplx = TRIA6_CPLX(self._h5n, self)
        self.tria6_fd = TRIA6_FD(self._h5n, self)
        self.tria6_fdnl = TRIA6_FDNL(self._h5n, self)
        self.tria6_fd_cplx = TRIA6_FD_CPLX(self._h5n, self)
        self.triar = TRIAR(self._h5n, self)
        # self.triar_1fd = None  # skipping for now
        # self.triar_1fd_cplx = None  # skipping for now
        # self.triar_4fd = None  # skipping for now
        # self.triar_4fd_cplx = None  # skipping for now
        self.triar_comp = TRIAR_COMP(self._h5n, self)
        self.triar_comp_cplx = TRIAR_COMP_CPLX(self._h5n, self)
        self.triar_cplx = TRIAR_CPLX(self._h5n, self)
        self.triar_nl = TRIAR_NL(self._h5n, self)
        self.triax3_1fdnl = TRIAX3_1FDNL(self._h5n, self)
        self.triax3_3fdnl = TRIAX3_3FDNL(self._h5n, self)
        self.triax3_fd = TRIAX3_FD(self._h5n, self)
        self.triax3_fd_cplx = TRIAX3_FD_CPLX(self._h5n, self)
        self.triax6 = TRIAX6(self._h5n, self)
        self.triax6_cplx = TRIAX6_CPLX(self._h5n, self)
        self.triax6_fd = TRIAX6_FD(self._h5n, self)
        self.triax6_fdnl = TRIAX6_FDNL(self._h5n, self)
        self.triax6_fd_cplx = TRIAX6_FD_CPLX(self._h5n, self)
        self.tube = TUBE(self._h5n, self)
        self.tube_cplx = TUBE_CPLX(self._h5n, self)
        self.tube_nl = TUBE_NL(self._h5n, self)
        self.tube_rr = TUBE_RR(self._h5n, self)
        self.visc_cplx = VISC_CPLX(self._h5n, self)
        self.visc_rr = VISC_RR(self._h5n, self)
        self.weld = WELD(self._h5n, self)
        self.weld_cplx = WELD_CPLX(self._h5n, self)
        self.weldc = WELDC(self._h5n, self)
        self.weldc_cplx = WELDC_CPLX(self._h5n, self)
        self.weldp = WELDP(self._h5n, self)
        self.weldp_cplx = WELDP_CPLX(self._h5n, self)

    def path(self):
        return self._elemental.path() + ['STRESS']

    def search(self, element_ids, domain_ids=()):
        # :type (List[int], List[int]) -> StressResult
        result = StressResult()
        _result = result.__dict__
        table_ids = self.__dict__.keys()
        _tables = self.__dict__
        for table_id in table_ids:
            if table_id.startswith('_'):  # not a table
                continue
            _result[table_id] = _tables[table_id].search(element_ids, domain_ids)

        return result

########################################################################################################################


class StressResult(object):
    def __init__(self):
        self.axif2 = None  # type: DataFrame
        self.axif2_cplx = None  # type: DataFrame
        self.axif3 = None  # type: DataFrame
        self.axif3_cplx = None  # type: DataFrame
        self.axif4 = None  # type: DataFrame
        self.axif4_cplx = None  # type: DataFrame
        self.axisym = None  # type: DataFrame
        self.bar = None  # type: DataFrame
        self.bars = None  # type: DataFrame
        self.bars_cplx = None  # type: DataFrame
        self.bar_cplx = None  # type: DataFrame
        self.bar_nl = None  # type: DataFrame
        self.bar_rr = None  # type: DataFrame
        self.beam = None  # type: DataFrame
        self.beam3 = None  # type: DataFrame
        self.beam3_cplx = None  # type: DataFrame
        self.beam_cplx = None  # type: DataFrame
        self.beam_nl = None  # type: DataFrame
        self.beam_rr = None  # type: DataFrame
        self.bush = None  # type: DataFrame
        self.bush1d = None  # type: DataFrame
        self.bush1d_cplx = None  # type: DataFrame
        self.bush1d_rr = None  # type: DataFrame
        self.bush_cplx = None  # type: DataFrame
        self.bush_nl = None  # type: DataFrame
        self.cone = None  # type: DataFrame
        self.conrod = None  # type: DataFrame
        self.conrod_cplx = None  # type: DataFrame
        self.conrod_nl = None  # type: DataFrame
        self.conrod_rr = None  # type: DataFrame
        self.elas1 = None  # type: DataFrame
        self.elas1_cplx = None  # type: DataFrame
        self.elas1_nl = None  # type: DataFrame
        self.elas2 = None  # type: DataFrame
        self.elas2_cplx = None  # type: DataFrame
        self.elas3 = None  # type: DataFrame
        self.elas3_cplx = None  # type: DataFrame
        self.elas3_nl = None  # type: DataFrame
        # self.elem_comp = None  # skipping for now
        # self.extreme_fibre = None  # skipping for now
        # self.extreme_fibre_cplx = None  # skipping for now
        self.fast = None  # type: DataFrame
        self.fast_cplx = None  # type: DataFrame
        self.gap = None  # type: DataFrame
        self.gap_nl = None  # type: DataFrame
        self.hexa = None  # type: DataFrame
        self.hexa20_27fdnl = None  # type: DataFrame
        self.hexa20_8fdnl = None  # type: DataFrame
        self.hexa20_fd = None  # type: DataFrame
        self.hexa_cplx = None  # type: DataFrame
        self.hexa_fd = None  # type: DataFrame
        self.hexa_fdnl = None  # type: DataFrame
        self.hexa_nl = None  # type: DataFrame
        self.ifhexa = None  # type: DataFrame
        self.ifpenta = None  # type: DataFrame
        self.penta = None  # type: DataFrame
        self.penta15_21fdnl = None  # type: DataFrame
        self.penta15_6fdnl = None  # type: DataFrame
        self.penta15_fd = None  # type: DataFrame
        self.penta_fdnl = None  # type: DataFrame
        self.penta_nl = None  # type: DataFrame
        self.quad4 = None  # type: DataFrame
        self.quad4_comp = None  # type: DataFrame
        self.quad4_comp_cplx = None  # type: DataFrame
        self.quad4_cplx = None  # type: DataFrame
        self.quad4_fd = None  # type: DataFrame
        self.quad4_fdnl = None  # type: DataFrame
        self.quad4_fd_cplx = None  # type: DataFrame
        self.quad4_nl = None  # type: DataFrame
        self.quad8 = None  # type: DataFrame
        self.quad8_4fdnl = None  # type: DataFrame
        self.quad8_9fdnl = None  # type: DataFrame
        self.quad8_comp = None  # type: DataFrame
        self.quad8_comp_cplx = None  # type: DataFrame
        self.quad8_cplx = None  # type: DataFrame
        self.quad8_fd = None  # type: DataFrame
        self.quad8_fd_cplx = None  # type: DataFrame
        self.quadr = None  # type: DataFrame
        self.quadr_comp = None  # type: DataFrame
        self.quadr_comp_cplx = None  # type: DataFrame
        self.quadr_cplx = None  # type: DataFrame
        # self.quadr_fd = None  # skipping for now
        # self.quadr_fd_cplx = None  # skipping for now
        self.quadr_nl = None  # type: DataFrame
        self.quadx4_fd = None  # type: DataFrame
        self.quadx4_fdnl = None  # type: DataFrame
        self.quadx4_fd_cplx = None  # type: DataFrame
        self.quadx8_4fdnl = None  # type: DataFrame
        self.quadx8_9fdnl = None  # type: DataFrame
        self.quadx8_fd = None  # type: DataFrame
        self.quadx8_fd_cplx = None  # type: DataFrame
        self.quad_cn = None  # type: DataFrame
        self.quad_cn_cplx = None  # type: DataFrame
        self.rac2d = None  # type: DataFrame
        self.rac3d = None  # type: DataFrame
        self.rod = None  # type: DataFrame
        self.rod_cplx = None  # type: DataFrame
        self.rod_nl = None  # type: DataFrame
        self.rod_rr = None  # type: DataFrame
        self.seam = None  # type: DataFrame
        self.seamp = None  # type: DataFrame
        self.seamp_cplx = None  # type: DataFrame
        self.shear = None  # type: DataFrame
        self.shear_cplx = None  # type: DataFrame
        self.shear_rr = None  # type: DataFrame
        self.slot3 = None  # type: DataFrame
        self.slot3_cplx = None  # type: DataFrame
        self.slot4 = None  # type: DataFrame
        self.slot4_cplx = None  # type: DataFrame
        self.tetra = None  # type: DataFrame
        self.tetra10_4fdnl = None  # type: DataFrame
        self.tetra10_5fdnl = None  # type: DataFrame
        self.tetra10_fd = None  # type: DataFrame
        self.tetra4_fdnl = None  # type: DataFrame
        self.tetra_cplx = None  # type: DataFrame
        self.tetra_fd = None  # type: DataFrame
        self.tetra_fdnl = None  # type: DataFrame
        self.tetra_nl = None  # type: DataFrame
        self.tria3 = None  # type: DataFrame
        self.tria3_1fdnl = None  # type: DataFrame
        self.tria3_3fdnl = None  # type: DataFrame
        self.tria3_comp = None  # type: DataFrame
        self.tria3_comp_cplx = None  # type: DataFrame
        self.tria3_cplx = None  # type: DataFrame
        self.tria3_fd = None  # type: DataFrame
        self.tria3_fd_cplx = None  # type: DataFrame
        self.tria3_nl = None  # type: DataFrame
        self.tria6 = None  # type: DataFrame
        self.tria6_comp = None  # type: DataFrame
        self.tria6_comp_cplx = None  # type: DataFrame
        self.tria6_cplx = None  # type: DataFrame
        self.tria6_fd = None  # type: DataFrame
        self.tria6_fdnl = None  # type: DataFrame
        self.tria6_fd_cplx = None  # type: DataFrame
        self.triar = None  # type: DataFrame
        # self.triar_1fd = None  # skipping for now
        # self.triar_1fd_cplx = None  # skipping for now
        # self.triar_4fd = None  # skipping for now
        # self.triar_4fd_cplx = None  # skipping for now
        self.triar_comp = None  # type: DataFrame
        self.triar_comp_cplx = None  # type: DataFrame
        self.triar_cplx = None  # type: DataFrame
        self.triar_nl = None  # type: DataFrame
        self.triax3_1fdnl = None  # type: DataFrame
        self.triax3_3fdnl = None  # type: DataFrame
        self.triax3_fd = None  # type: DataFrame
        self.triax3_fd_cplx = None  # type: DataFrame
        self.triax6 = None  # type: DataFrame
        self.triax6_cplx = None  # type: DataFrame
        self.triax6_fd = None  # type: DataFrame
        self.triax6_fdnl = None  # type: DataFrame
        self.triax6_fd_cplx = None  # type: DataFrame
        self.tube = None  # type: DataFrame
        self.tube_cplx = None  # type: DataFrame
        self.tube_nl = None  # type: DataFrame
        self.tube_rr = None  # type: DataFrame
        self.visc_cplx = None  # type: DataFrame
        self.visc_rr = None  # type: DataFrame
        self.weld = None  # type: DataFrame
        self.weld_cplx = None  # type: DataFrame
        self.weldc = None  # type: DataFrame
        self.weldc_cplx = None  # type: DataFrame
        self.weldp = None  # type: DataFrame
        self.weldp_cplx = None  # type: DataFrame


########################################################################################################################


class AXIF2(ResultTable):
    result_type = 'ELEMENT STRESSES 47 AXIF2 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/AXIF2', result_type)


########################################################################################################################


class AXIF2_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 47 AXIF2 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/AXIF2_CPLX', result_type)


########################################################################################################################


class AXIF3(ResultTable):
    result_type = 'ELEMENT STRESSES 48 AXIF3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/AXIF3', result_type)


########################################################################################################################


class AXIF3_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 48 AXIF3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/AXIF3_CPLX', result_type)


########################################################################################################################


class AXIF4(ResultTable):
    result_type = 'ELEMENT STRESSES 49 AXIF4 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/AXIF4', result_type)


########################################################################################################################


class AXIF4_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 49 AXIF4 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/AXIF4_CPLX', result_type)


########################################################################################################################


class AXISYM(ResultTable):
    result_type = 'ELEMENT STRESSES 241 AXISYM REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/AXISYM', result_type)


########################################################################################################################


class BAR(ResultTable):
    result_type = 'ELEMENT STRESSES 34 BAR REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BAR', result_type)


########################################################################################################################


class BARS(ResultTable):
    result_type = 'ELEMENT STRESSES 100 BARS REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BARS', result_type)


########################################################################################################################


class BARS_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 100 BARS COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BARS_CPLX', result_type)


########################################################################################################################


class BAR_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 34 BAR COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BAR_CPLX', result_type)


########################################################################################################################


class BAR_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 240 BAR_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BAR_NL', result_type)


########################################################################################################################


class BAR_RR(ResultTable):
    result_type = 'ELEMENT STRESSES 34 BAR_RR RANDOM'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BAR_RR', result_type)


########################################################################################################################


class BEAM(ResultTable):
    result_type = 'ELEMENT STRESSES 2 BEAM REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BEAM', result_type)


########################################################################################################################


class BEAM3(ResultTable):
    result_type = 'ELEMENT STRESSES 184 BEAM3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BEAM3', result_type)


########################################################################################################################


class BEAM3_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 184 BEAM3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BEAM3_CPLX', result_type)


########################################################################################################################


class BEAM_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 2 BEAM COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BEAM_CPLX', result_type)


########################################################################################################################


class BEAM_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 94 BEAM_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BEAM_NL', result_type)


########################################################################################################################


class BEAM_RR(ResultTable):
    result_type = 'ELEMENT STRESSES 2 BEAM_RR RANDOM'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BEAM_RR', result_type)


########################################################################################################################


class BUSH(ResultTable):
    result_type = 'ELEMENT STRESSES 102 BUSH REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BUSH', result_type)


########################################################################################################################


class BUSH1D(ResultTable):
    result_type = 'ELEMENT STRESSES 40 BUSH1D REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BUSH1D', result_type)


########################################################################################################################


class BUSH1D_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 40 BUSH1D COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BUSH1D_CPLX', result_type)


########################################################################################################################


class BUSH1D_RR(ResultTable):
    result_type = 'ELEMENT STRESSES 40 BUSH1D_RR RANDOM'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BUSH1D_RR', result_type)


########################################################################################################################


class BUSH_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 102 BUSH COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BUSH_CPLX', result_type)


########################################################################################################################


class BUSH_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 226 BUSH_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/BUSH_NL', result_type)


########################################################################################################################


class CONE(ResultTable):
    result_type = 'ELEMENT STRESSES 35 CONE REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/CONE', result_type)


########################################################################################################################


class CONROD(ResultTable):
    result_type = 'ELEMENT STRESSES 10 CONROD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/CONROD', result_type)


########################################################################################################################


class CONROD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 10 CONROD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/CONROD_CPLX', result_type)


########################################################################################################################


class CONROD_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 92 CONROD_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/CONROD_NL', result_type)


########################################################################################################################


class CONROD_RR(ResultTable):
    result_type = 'ELEMENT STRESSES 10 CONROD_RR RANDOM'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/CONROD_RR', result_type)


########################################################################################################################


class ELAS1(ResultTable):
    result_type = 'ELEMENT STRESSES 11 ELAS1 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ELAS1', result_type)


########################################################################################################################


class ELAS1_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 11 ELAS1 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ELAS1_CPLX', result_type)


########################################################################################################################


class ELAS1_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 224 ELAS1_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ELAS1_NL', result_type)


########################################################################################################################


class ELAS2(ResultTable):
    result_type = 'ELEMENT STRESSES 12 ELAS2 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ELAS2', result_type)


########################################################################################################################


class ELAS2_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 12 ELAS2 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ELAS2_CPLX', result_type)


########################################################################################################################


class ELAS3(ResultTable):
    result_type = 'ELEMENT STRESSES 13 ELAS3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ELAS3', result_type)


########################################################################################################################


class ELAS3_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 13 ELAS3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ELAS3_CPLX', result_type)


########################################################################################################################


class ELAS3_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 225 ELAS3_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ELAS3_NL', result_type)


########################################################################################################################


class FAST(ResultTable):
    result_type = 'ELEMENT STRESSES 126 FAST REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/FAST', result_type)


########################################################################################################################


class FAST_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 126 FAST COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/FAST_CPLX', result_type)


########################################################################################################################


class GAP(ResultTable):
    result_type = 'ELEMENT STRESSES 38 GAP REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/GAP', result_type)


########################################################################################################################


class GAP_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 86 GAP_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/GAP_NL', result_type)


########################################################################################################################


class HEXA(ResultTable):
    result_type = 'ELEMENT STRESSES 67 HEXA REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/HEXA', result_type)


########################################################################################################################


class HEXA20_27FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 207 HEXA20_27FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/HEXA20_27FDNL', result_type)


########################################################################################################################


class HEXA20_8FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 202 HEXA20_8FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/HEXA20_8FDNL', result_type)


########################################################################################################################


class HEXA20_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 163 HEXA20_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/HEXA20_FD', result_type)


########################################################################################################################


class HEXA_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 67 HEXA COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/HEXA_CPLX', result_type)


########################################################################################################################


class HEXA_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 140 HEXA_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/HEXA_FD', result_type)


########################################################################################################################


class HEXA_FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 218 HEXA_FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/HEXA_FDNL', result_type)


########################################################################################################################


class HEXA_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 93 HEXA_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/HEXA_NL', result_type)


########################################################################################################################


class IFHEXA(ResultTable):
    result_type = 'ELEMENT STRESSES 65 IFHEXA REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/IFHEXA', result_type)


########################################################################################################################


class IFPENTA(ResultTable):
    result_type = 'ELEMENT STRESSES 66 IFPENTA REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/IFPENTA', result_type)


########################################################################################################################


class PENTA(ResultTable):
    result_type = 'ELEMENT STRESSES 68 PENTA REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/PENTA', result_type)


########################################################################################################################


class PENTA15_21FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 209 PENTA15_21FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/PENTA15_21FDNL', result_type)


########################################################################################################################


class PENTA15_6FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 204 PENTA15_6FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/PENTA15_6FDNL', result_type)


########################################################################################################################


class PENTA15_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 165 PENTA15_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/PENTA15_FD', result_type)


########################################################################################################################


class PENTA_FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 220 PENTA_FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/PENTA_FDNL', result_type)


########################################################################################################################


class PENTA_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 91 PENTA_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/PENTA_NL', result_type)


########################################################################################################################


class QUAD4(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT STRESSES 33 QUAD4 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD4', result_type)
    table_def.add_index_option('EFFE', DataGetter(indices=[0, 2, 3, 4, 5, 10, 11, 12, 13]))
    table_def.add_index_option('VONM', DataGetter(indices=[0, 2, 3, 4, 5, 10, 11, 12, 13]))


########################################################################################################################


class QUAD4_COMP(ResultTable):
    result_type = 'ELEMENT STRESSES 95 QUAD4LC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD4_COMP', result_type)


########################################################################################################################


class QUAD4_COMP_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 95 QUAD4LC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD4_COMP_CPLX', result_type)


########################################################################################################################


class QUAD4_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT STRESSES 33 QUAD4 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD4_CPLX', result_type)


########################################################################################################################


class QUAD4_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 139 QUAD4_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD4_FD', result_type)


########################################################################################################################


class QUAD4_FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 201 QUAD4_FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD4_FDNL', result_type)


########################################################################################################################


class QUAD4_FD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 139 QUAD4_FD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD4_FD_CPLX', result_type)


########################################################################################################################


class QUAD4_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 90 QUAD4_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD4_NL', result_type)


########################################################################################################################


class QUAD8(ResultTable):
    result_type = 'ELEMENT STRESSES 64 QUAD8 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD8', result_type)


########################################################################################################################


class QUAD8_4FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 219 QUAD8_4FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD8_4FDNL', result_type)


########################################################################################################################


class QUAD8_9FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 208 QUAD8_9FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD8_9FDNL', result_type)


########################################################################################################################


class QUAD8_COMP(ResultTable):
    result_type = 'ELEMENT STRESSES 96 QUAD8LC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD8_COMP', result_type)


########################################################################################################################


class QUAD8_COMP_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 96 QUAD8LC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD8_COMP_CPLX', result_type)


########################################################################################################################


class QUAD8_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 64 QUAD8 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD8_CPLX', result_type)


########################################################################################################################


class QUAD8_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 164 QUAD8_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD8_FD', result_type)


########################################################################################################################


class QUAD8_FD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 164 QUAD8_FD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD8_FD_CPLX', result_type)


########################################################################################################################


class QUADR(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT STRESSES 82 QUADR REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADR', result_type)


########################################################################################################################


class QUADR_COMP(ResultTable):
    result_type = 'ELEMENT STRESSES 232 QUADRLC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADR_COMP', result_type)


########################################################################################################################


class QUADR_COMP_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 232 QUADRLC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADR_COMP_CPLX', result_type)


########################################################################################################################


class QUADR_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT STRESSES 82 QUADR COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADR_CPLX', result_type)


########################################################################################################################


class QUADR_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 172 QUADR_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADR_NL', result_type)


########################################################################################################################


class QUADX4_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 170 QUADX4_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADX4_FD', result_type)


########################################################################################################################


class QUADX4_FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 214 QUADX4_FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADX4_FDNL', result_type)


########################################################################################################################


class QUADX4_FD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 170 QUADX4_FD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADX4_FD_CPLX', result_type)


########################################################################################################################


class QUADX8_4FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 223 QUADX8_4FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADX8_4FDNL', result_type)


########################################################################################################################


class QUADX8_9FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 215 QUADX8_9FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADX8_9FDNL', result_type)


########################################################################################################################


class QUADX8_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 171 QUADX8_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADX8_FD', result_type)


########################################################################################################################


class QUADX8_FD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 171 QUADX8_FD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUADX8_FD_CPLX', result_type)


########################################################################################################################


class QUAD_CN(ResultTable):
    result_type = 'ELEMENT STRESSES 144 QUADC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD_CN', result_type)


########################################################################################################################


class QUAD_CN_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 144 QUADC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/QUAD_CN_CPLX', result_type)


########################################################################################################################


class RAC2D(ResultTable):
    result_type = 'ELEMENT STRESSES 60 RAC2D REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/RAC2D', result_type)


########################################################################################################################


class RAC3D(ResultTable):
    result_type = 'ELEMENT STRESSES 61 RAC3D REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/RAC3D', result_type)


########################################################################################################################


class ROD(ResultTable):
    result_type = 'ELEMENT STRESSES 1 ROD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ROD', result_type)


########################################################################################################################


class ROD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 1 ROD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ROD_CPLX', result_type)


########################################################################################################################


class ROD_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 89 ROD_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ROD_NL', result_type)


########################################################################################################################


class ROD_RR(ResultTable):
    result_type = 'ELEMENT STRESSES 1 ROD_RR RANDOM'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/ROD_RR', result_type)


########################################################################################################################


class SEAM(ResultTable):
    result_type = 'ELEMENT STRESSES 119 SEAM REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SEAM', result_type)


########################################################################################################################


class SEAMP(ResultTable):
    result_type = 'ELEMENT STRESSES 159 SEAMP REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SEAMP', result_type)


########################################################################################################################


class SEAMP_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 159 SEAMP COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SEAMP_CPLX', result_type)


########################################################################################################################


class SHEAR(ResultTable):
    result_type = 'ELEMENT STRESSES 4 SHEAR REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SHEAR', result_type)


########################################################################################################################


class SHEAR_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 4 SHEAR COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SHEAR_CPLX', result_type)


########################################################################################################################


class SHEAR_RR(ResultTable):
    result_type = 'ELEMENT STRESSES 4 SHEAR_RR RANDOM'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SHEAR_RR', result_type)


########################################################################################################################


class SLOT3(ResultTable):
    result_type = 'ELEMENT STRESSES 50 SLOT3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SLOT3', result_type)


########################################################################################################################


class SLOT3_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 50 SLOT3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SLOT3_CPLX', result_type)


########################################################################################################################


class SLOT4(ResultTable):
    result_type = 'ELEMENT STRESSES 51 SLOT4 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SLOT4', result_type)


########################################################################################################################


class SLOT4_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 51 SLOT4 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/SLOT4_CPLX', result_type)


########################################################################################################################


class TETRA(ResultTable):
    result_type = 'ELEMENT STRESSES 39 TETRA REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA', result_type)


########################################################################################################################


class TETRA10_4FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 221 TETRA10_4FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA10_4FDNL', result_type)


########################################################################################################################


class TETRA10_5FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 210 TETRA10_5FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA10_5FDNL', result_type)


########################################################################################################################


class TETRA10_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 166 TETRA10_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA10_FD', result_type)


########################################################################################################################


class TETRA4_FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 216 TETRA4_FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA4_FDNL', result_type)


########################################################################################################################


class TETRA_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 39 TETRA COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA_CPLX', result_type)


########################################################################################################################


class TETRA_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 161 TETRA_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA_FD', result_type)


########################################################################################################################


class TETRA_FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 205 TETRA_FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA_FDNL', result_type)


########################################################################################################################


class TETRA_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 85 TETRA_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TETRA_NL', result_type)


########################################################################################################################


class TRIA3(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT STRESSES 74 TRIA3 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3', result_type)
    table_def.add_index_option('EFFE', DataGetter(indices=[0, 2, 3, 4, 5, 10, 11, 12, 13]))
    table_def.add_index_option('VONM', DataGetter(indices=[0, 2, 3, 4, 5, 10, 11, 12, 13]))


########################################################################################################################


class TRIA3_1FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 206 TRIA3_1FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3_1FDNL', result_type)


########################################################################################################################


class TRIA3_3FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 217 TRIA3_3FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3_3FDNL', result_type)


########################################################################################################################


class TRIA3_COMP(ResultTable):
    result_type = 'ELEMENT STRESSES 97 TRIA3LC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3_COMP', result_type)


########################################################################################################################


class TRIA3_COMP_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 97 TRIA3LC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3_COMP_CPLX', result_type)


########################################################################################################################


class TRIA3_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT STRESSES 74 TRIA3 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3_CPLX', result_type)


########################################################################################################################


class TRIA3_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 162 TRIA3_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3_FD', result_type)


########################################################################################################################


class TRIA3_FD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 162 TRIA3_FD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3_FD_CPLX', result_type)


########################################################################################################################


class TRIA3_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 88 TRIA3_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA3_NL', result_type)


########################################################################################################################


class TRIA6(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT STRESSES 75 TRIA6 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA6', result_type)


########################################################################################################################


class TRIA6_COMP(ResultTable):
    result_type = 'ELEMENT STRESSES 98 TRIA6LC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA6_COMP', result_type)


########################################################################################################################


class TRIA6_COMP_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 98 TRIA6LC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA6_COMP_CPLX', result_type)


########################################################################################################################


class TRIA6_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT STRESSES 75 TRIA6 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA6_CPLX', result_type)


########################################################################################################################


class TRIA6_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 167 TRIA6_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA6_FD', result_type)


########################################################################################################################


class TRIA6_FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 211 TRIA6_FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA6_FDNL', result_type)


########################################################################################################################


class TRIA6_FD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 167 TRIA6_FD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIA6_FD_CPLX', result_type)


########################################################################################################################


class TRIAR(ResultTable, ShellElementForceStressResultTable):
    result_type = 'ELEMENT STRESSES 70 TRIAR REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAR', result_type)


########################################################################################################################


class TRIAR_COMP(ResultTable):
    result_type = 'ELEMENT STRESSES 233 TRIARLC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAR_COMP', result_type)


########################################################################################################################


class TRIAR_COMP_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 233 TRIARLC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAR_COMP_CPLX', result_type)


########################################################################################################################


class TRIAR_CPLX(ResultTable, ShellElementForceStressResultTableComplex):
    result_type = 'ELEMENT STRESSES 70 TRIAR COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAR_CPLX', result_type)


########################################################################################################################


class TRIAR_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 173 TRIAR_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAR_NL', result_type)


########################################################################################################################


class TRIAX3_1FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 212 TRIAX3_1FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX3_1FDNL', result_type)


########################################################################################################################


class TRIAX3_3FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 222 TRIAX3_3FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX3_3FDNL', result_type)


########################################################################################################################


class TRIAX3_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 168 TRIAX3_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX3_FD', result_type)


########################################################################################################################


class TRIAX3_FD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 168 TRIAX3_FD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX3_FD_CPLX', result_type)


########################################################################################################################


class TRIAX6(ResultTable):
    result_type = 'ELEMENT STRESSES 53 TRIAX6 REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX6', result_type)


########################################################################################################################


class TRIAX6_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 53 TRIAX6 COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX6_CPLX', result_type)


########################################################################################################################


class TRIAX6_FD(ResultTable):
    result_type = 'ELEMENT STRESSES 169 TRIAX6_FD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX6_FD', result_type)


########################################################################################################################


class TRIAX6_FDNL(ResultTable):
    result_type = 'ELEMENT STRESSES 213 TRIAX6_FDNL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX6_FDNL', result_type)


########################################################################################################################


class TRIAX6_FD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 169 TRIAX6_FD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TRIAX6_FD_CPLX', result_type)


########################################################################################################################


class TUBE(ResultTable):
    result_type = 'ELEMENT STRESSES 3 TUBE REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TUBE', result_type)


########################################################################################################################


class TUBE_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 3 TUBE COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TUBE_CPLX', result_type)


########################################################################################################################


class TUBE_NL(ResultTable):
    result_type = 'ELEMENT STRESSES 87 TUBE_NL REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TUBE_NL', result_type)


########################################################################################################################


class TUBE_RR(ResultTable):
    result_type = 'ELEMENT STRESSES 3 TUBE_RR RANDOM'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/TUBE_RR', result_type)


########################################################################################################################


class VISC_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 24 VISC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/VISC_CPLX', result_type)


########################################################################################################################


class VISC_RR(ResultTable):
    result_type = 'ELEMENT STRESSES 24 VISC_RR RANDOM'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/VISC_RR', result_type)


########################################################################################################################


class WELD(ResultTable):
    result_type = 'ELEMENT STRESSES 200 WELD REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/WELD', result_type)


########################################################################################################################


class WELD_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 200 WELD COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/WELD_CPLX', result_type)


########################################################################################################################


class WELDC(ResultTable):
    result_type = 'ELEMENT STRESSES 117 WELDC REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/WELDC', result_type)


########################################################################################################################


class WELDC_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 117 WELDC COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/WELDC_CPLX', result_type)


########################################################################################################################


class WELDP(ResultTable):
    result_type = 'ELEMENT STRESSES 118 WELDP REAL'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/WELDP', result_type)


########################################################################################################################


class WELDP_CPLX(ResultTable):
    result_type = 'ELEMENT STRESSES 118 WELDP COMPLEX'
    table_def = TableDef.create('/NASTRAN/RESULT/ELEMENTAL/STRESS/WELDP_CPLX', result_type)


