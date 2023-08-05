﻿'''_4926.py

ClutchHalfCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4772
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4942
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ClutchHalfCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundModalAnalysis',)


class ClutchHalfCompoundModalAnalysis(_4942.CouplingHalfCompoundModalAnalysis):
    '''ClutchHalfCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2253.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4772.ClutchHalfModalAnalysis]':
        '''List[ClutchHalfModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4772.ClutchHalfModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4772.ClutchHalfModalAnalysis]':
        '''List[ClutchHalfModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4772.ClutchHalfModalAnalysis))
        return value
