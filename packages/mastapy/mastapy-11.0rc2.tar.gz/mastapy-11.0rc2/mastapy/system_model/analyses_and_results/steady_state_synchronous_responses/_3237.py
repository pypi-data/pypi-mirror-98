'''_3237.py

KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2213
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6554
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3238, _3236, _3234
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse',)


class KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse(_3234.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse):
    '''KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2213.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2213.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6554.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6554.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_steady_state_synchronous_response(self) -> 'List[_3238.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsSteadyStateSynchronousResponse, constructor.new(_3238.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_steady_state_synchronous_response(self) -> 'List[_3236.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesSteadyStateSynchronousResponse, constructor.new(_3236.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse))
        return value
