﻿'''_3256.py

RingPinsSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.cycloidal import _2244
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6580
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3244
from mastapy._internal.python_net import python_net_import

_RING_PINS_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'RingPinsSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsSteadyStateSynchronousResponse',)


class RingPinsSteadyStateSynchronousResponse(_3244.MountableComponentSteadyStateSynchronousResponse):
    '''RingPinsSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2244.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6580.RingPinsLoadCase':
        '''RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6580.RingPinsLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
