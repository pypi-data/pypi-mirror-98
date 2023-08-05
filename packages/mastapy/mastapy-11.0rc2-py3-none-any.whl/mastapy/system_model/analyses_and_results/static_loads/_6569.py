﻿'''_6569.py

PlanetaryConnectionLoadCase
'''


from mastapy.system_model.connections_and_sockets import _1966
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6588
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PlanetaryConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionLoadCase',)


class PlanetaryConnectionLoadCase(_6588.ShaftToMountableComponentConnectionLoadCase):
    '''PlanetaryConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1966.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
