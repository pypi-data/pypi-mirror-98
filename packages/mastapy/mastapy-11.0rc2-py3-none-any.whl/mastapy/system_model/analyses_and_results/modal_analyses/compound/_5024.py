﻿'''_5024.py

UnbalancedMassCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2153
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4878
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5025
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'UnbalancedMassCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundModalAnalysis',)


class UnbalancedMassCompoundModalAnalysis(_5025.VirtualComponentCompoundModalAnalysis):
    '''UnbalancedMassCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2153.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2153.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4878.UnbalancedMassModalAnalysis]':
        '''List[UnbalancedMassModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4878.UnbalancedMassModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4878.UnbalancedMassModalAnalysis]':
        '''List[UnbalancedMassModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4878.UnbalancedMassModalAnalysis))
        return value
