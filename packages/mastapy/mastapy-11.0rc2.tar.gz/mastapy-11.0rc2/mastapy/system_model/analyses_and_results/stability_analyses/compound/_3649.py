'''_3649.py

RingPinsCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2244
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3518
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3637
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'RingPinsCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundStabilityAnalysis',)


class RingPinsCompoundStabilityAnalysis(_3637.MountableComponentCompoundStabilityAnalysis):
    '''RingPinsCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2244.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3518.RingPinsStabilityAnalysis]':
        '''List[RingPinsStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3518.RingPinsStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3518.RingPinsStabilityAnalysis]':
        '''List[RingPinsStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3518.RingPinsStabilityAnalysis))
        return value
