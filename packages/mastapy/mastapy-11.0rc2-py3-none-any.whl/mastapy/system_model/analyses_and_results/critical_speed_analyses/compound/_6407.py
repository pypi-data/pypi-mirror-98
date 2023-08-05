﻿'''_6407.py

ShaftHubConnectionCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2272
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6278
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6347
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'ShaftHubConnectionCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundCriticalSpeedAnalysis',)


class ShaftHubConnectionCompoundCriticalSpeedAnalysis(_6347.ConnectorCompoundCriticalSpeedAnalysis):
    '''ShaftHubConnectionCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2272.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2272.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6278.ShaftHubConnectionCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6278.ShaftHubConnectionCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6278.ShaftHubConnectionCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6278.ShaftHubConnectionCriticalSpeedAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCompoundCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundCriticalSpeedAnalysis))
        return value
