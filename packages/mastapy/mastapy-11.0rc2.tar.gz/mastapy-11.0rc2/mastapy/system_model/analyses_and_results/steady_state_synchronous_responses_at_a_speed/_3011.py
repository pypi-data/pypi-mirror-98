﻿'''_3011.py

SpringDamperSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2274
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6596
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2946
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'SpringDamperSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperSteadyStateSynchronousResponseAtASpeed',)


class SpringDamperSteadyStateSynchronousResponseAtASpeed(_2946.CouplingSteadyStateSynchronousResponseAtASpeed):
    '''SpringDamperSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2274.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2274.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6596.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6596.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
