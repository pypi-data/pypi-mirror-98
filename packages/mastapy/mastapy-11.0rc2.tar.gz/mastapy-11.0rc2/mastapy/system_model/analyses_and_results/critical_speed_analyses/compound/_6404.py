'''_6404.py

RollingRingConnectionCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1971
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6274
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6376
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'RollingRingConnectionCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionCompoundCriticalSpeedAnalysis',)


class RollingRingConnectionCompoundCriticalSpeedAnalysis(_6376.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis):
    '''RollingRingConnectionCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1971.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1971.RollingRingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1971.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1971.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6274.RollingRingConnectionCriticalSpeedAnalysis]':
        '''List[RollingRingConnectionCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6274.RollingRingConnectionCriticalSpeedAnalysis))
        return value

    @property
    def connection_critical_speed_analysis_load_cases(self) -> 'List[_6274.RollingRingConnectionCriticalSpeedAnalysis]':
        '''List[RollingRingConnectionCriticalSpeedAnalysis]: 'ConnectionCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionCriticalSpeedAnalysisLoadCases, constructor.new(_6274.RollingRingConnectionCriticalSpeedAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingConnectionCompoundCriticalSpeedAnalysis]':
        '''List[RollingRingConnectionCompoundCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionCompoundCriticalSpeedAnalysis))
        return value
