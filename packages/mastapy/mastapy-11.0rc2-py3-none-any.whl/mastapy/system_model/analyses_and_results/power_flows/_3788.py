﻿'''_3788.py

RingPinsToDiscConnectionPowerFlow
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2020
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6581
from mastapy.system_model.analyses_and_results.power_flows import _3761
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RingPinsToDiscConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionPowerFlow',)


class RingPinsToDiscConnectionPowerFlow(_3761.InterMountableComponentConnectionPowerFlow):
    '''RingPinsToDiscConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionPowerFlow.TYPE'):
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
