﻿'''_2885.py

StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2220
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2883, _2884, _2796
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2755
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft',)


class StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft(_2796.BevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft):
    '''StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2220.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2220.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2220.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2220.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2883.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearCompoundSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelDiffGearsCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundSteadyStateSynchronousResponseOnAShaft, constructor.new(_2883.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_diff_meshes_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2884.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelDiffMeshesCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundSteadyStateSynchronousResponseOnAShaft, constructor.new(_2884.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2755.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2755.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def assembly_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2755.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft]: 'AssemblySteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2755.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft))
        return value
