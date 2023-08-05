﻿'''_6133.py

PulleyCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2264, _2261
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6004
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6084
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'PulleyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundDynamicAnalysis',)


class PulleyCompoundDynamicAnalysis(_6084.CouplingHalfCompoundDynamicAnalysis):
    '''PulleyCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2264.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6004.PulleyDynamicAnalysis]':
        '''List[PulleyDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6004.PulleyDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_6004.PulleyDynamicAnalysis]':
        '''List[PulleyDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_6004.PulleyDynamicAnalysis))
        return value
