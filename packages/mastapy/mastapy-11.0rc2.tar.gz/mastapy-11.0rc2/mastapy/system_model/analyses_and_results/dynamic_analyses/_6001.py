﻿'''_6001.py

PlanetCarrierDynamicAnalysis
'''


from mastapy.system_model.part_model import _2145
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6572
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5993
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'PlanetCarrierDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierDynamicAnalysis',)


class PlanetCarrierDynamicAnalysis(_5993.MountableComponentDynamicAnalysis):
    '''PlanetCarrierDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2145.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6572.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6572.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
