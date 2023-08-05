﻿'''_2463.py

RollingRingConnectionSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets import _1971
from mastapy.system_model.analyses_and_results.static_loads import _6583
from mastapy.system_model.analyses_and_results.power_flows import _3790
from mastapy.system_model.analyses_and_results.system_deflections import _2432
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'RollingRingConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionSystemDeflection',)


class RollingRingConnectionSystemDeflection(_2432.InterMountableComponentConnectionSystemDeflection):
    '''RollingRingConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def separation(self) -> 'float':
        '''float: 'Separation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Separation

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
    def power_flow_results(self) -> '_3790.RollingRingConnectionPowerFlow':
        '''RollingRingConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3790.RollingRingConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionSystemDeflection]':
        '''List[RollingRingConnectionSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionSystemDeflection))
        return value
