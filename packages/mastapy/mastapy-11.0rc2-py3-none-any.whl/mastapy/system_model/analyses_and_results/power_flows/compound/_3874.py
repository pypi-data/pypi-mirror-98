﻿'''_3874.py

CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2017
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3740
from mastapy.system_model.analyses_and_results.power_flows.compound import _3831
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow',)


class CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow(_3831.AbstractShaftToMountableComponentConnectionCompoundPowerFlow):
    '''CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2017.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2017.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3740.CycloidalDiscPlanetaryBearingConnectionPowerFlow]':
        '''List[CycloidalDiscPlanetaryBearingConnectionPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3740.CycloidalDiscPlanetaryBearingConnectionPowerFlow))
        return value

    @property
    def connection_power_flow_load_cases(self) -> 'List[_3740.CycloidalDiscPlanetaryBearingConnectionPowerFlow]':
        '''List[CycloidalDiscPlanetaryBearingConnectionPowerFlow]: 'ConnectionPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionPowerFlowLoadCases, constructor.new(_3740.CycloidalDiscPlanetaryBearingConnectionPowerFlow))
        return value
