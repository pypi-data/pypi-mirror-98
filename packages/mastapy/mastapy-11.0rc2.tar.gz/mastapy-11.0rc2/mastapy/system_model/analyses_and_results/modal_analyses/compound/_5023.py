﻿'''_5023.py

TorqueConverterTurbineCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2284
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4877
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4942
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'TorqueConverterTurbineCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundModalAnalysis',)


class TorqueConverterTurbineCompoundModalAnalysis(_4942.CouplingHalfCompoundModalAnalysis):
    '''TorqueConverterTurbineCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2284.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2284.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4877.TorqueConverterTurbineModalAnalysis]':
        '''List[TorqueConverterTurbineModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4877.TorqueConverterTurbineModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4877.TorqueConverterTurbineModalAnalysis]':
        '''List[TorqueConverterTurbineModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4877.TorqueConverterTurbineModalAnalysis))
        return value
