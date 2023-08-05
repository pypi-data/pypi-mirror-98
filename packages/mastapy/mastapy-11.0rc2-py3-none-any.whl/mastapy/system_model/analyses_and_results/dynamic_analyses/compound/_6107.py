﻿'''_6107.py

HypoidGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2208
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5978
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6049
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'HypoidGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundDynamicAnalysis',)


class HypoidGearCompoundDynamicAnalysis(_6049.AGMAGleasonConicalGearCompoundDynamicAnalysis):
    '''HypoidGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2208.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2208.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5978.HypoidGearDynamicAnalysis]':
        '''List[HypoidGearDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5978.HypoidGearDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5978.HypoidGearDynamicAnalysis]':
        '''List[HypoidGearDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5978.HypoidGearDynamicAnalysis))
        return value
