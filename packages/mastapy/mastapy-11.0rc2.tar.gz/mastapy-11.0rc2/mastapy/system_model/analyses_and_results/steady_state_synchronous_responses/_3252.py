﻿'''_3252.py

PlanetCarrierSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _2145
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6572
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3244
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'PlanetCarrierSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierSteadyStateSynchronousResponse',)


class PlanetCarrierSteadyStateSynchronousResponse(_3244.MountableComponentSteadyStateSynchronousResponse):
    '''PlanetCarrierSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierSteadyStateSynchronousResponse.TYPE'):
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
