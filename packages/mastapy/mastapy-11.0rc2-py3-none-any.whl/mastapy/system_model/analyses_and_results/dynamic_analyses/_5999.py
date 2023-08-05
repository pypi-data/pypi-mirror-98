﻿'''_5999.py

PlanetaryConnectionDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1966
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6569
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6013
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'PlanetaryConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionDynamicAnalysis',)


class PlanetaryConnectionDynamicAnalysis(_6013.ShaftToMountableComponentConnectionDynamicAnalysis):
    '''PlanetaryConnectionDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1966.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6569.PlanetaryConnectionLoadCase':
        '''PlanetaryConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6569.PlanetaryConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
