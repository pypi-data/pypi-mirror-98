'''_3279.py

StraightBevelGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2222
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6603
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3280, _3278, _3183
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'StraightBevelGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetSteadyStateSynchronousResponse',)


class StraightBevelGearSetSteadyStateSynchronousResponse(_3183.BevelGearSetSteadyStateSynchronousResponse):
    '''StraightBevelGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2222.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2222.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6603.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6603.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_steady_state_synchronous_response(self) -> 'List[_3280.StraightBevelGearSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearSteadyStateSynchronousResponse]: 'StraightBevelGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsSteadyStateSynchronousResponse, constructor.new(_3280.StraightBevelGearSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_meshes_steady_state_synchronous_response(self) -> 'List[_3278.StraightBevelGearMeshSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearMeshSteadyStateSynchronousResponse]: 'StraightBevelMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesSteadyStateSynchronousResponse, constructor.new(_3278.StraightBevelGearMeshSteadyStateSynchronousResponse))
        return value
