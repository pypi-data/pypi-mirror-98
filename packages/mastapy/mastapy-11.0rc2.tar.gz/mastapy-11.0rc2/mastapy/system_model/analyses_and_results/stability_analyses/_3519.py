﻿'''_3519.py

RingPinsToDiscConnectionStabilityAnalysis
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2020
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6581
from mastapy.system_model.analyses_and_results.stability_analyses import _3494
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'RingPinsToDiscConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionStabilityAnalysis',)


class RingPinsToDiscConnectionStabilityAnalysis(_3494.InterMountableComponentConnectionStabilityAnalysis):
    '''RingPinsToDiscConnectionStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2020.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2020.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6581.RingPinsToDiscConnectionLoadCase':
        '''RingPinsToDiscConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6581.RingPinsToDiscConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
