﻿'''_3521.py

RollingRingConnectionStabilityAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1971
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6583
from mastapy.system_model.analyses_and_results.stability_analyses import _3494
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'RollingRingConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionStabilityAnalysis',)


class RollingRingConnectionStabilityAnalysis(_3494.InterMountableComponentConnectionStabilityAnalysis):
    '''RollingRingConnectionStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1971.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1971.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6583.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6583.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionStabilityAnalysis]':
        '''List[RollingRingConnectionStabilityAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionStabilityAnalysis))
        return value
