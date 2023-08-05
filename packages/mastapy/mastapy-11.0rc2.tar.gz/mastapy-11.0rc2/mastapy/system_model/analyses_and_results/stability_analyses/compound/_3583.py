'''_3583.py

ClutchHalfCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3450
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3599
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ClutchHalfCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundStabilityAnalysis',)


class ClutchHalfCompoundStabilityAnalysis(_3599.CouplingHalfCompoundStabilityAnalysis):
    '''ClutchHalfCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundStabilityAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3450.ClutchHalfStabilityAnalysis]':
        '''List[ClutchHalfStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3450.ClutchHalfStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3450.ClutchHalfStabilityAnalysis]':
        '''List[ClutchHalfStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3450.ClutchHalfStabilityAnalysis))
        return value
