﻿'''_2742.py

RootAssemblySteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2753, _2655
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'RootAssemblySteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblySteadyStateSynchronousResponseOnAShaft',)


class RootAssemblySteadyStateSynchronousResponseOnAShaft(_2655.AssemblySteadyStateSynchronousResponseOnAShaft):
    '''RootAssemblySteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblySteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2150.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def steady_state_synchronous_response_on_a_shaft_inputs(self) -> '_2753.SteadyStateSynchronousResponseOnAShaft':
        '''SteadyStateSynchronousResponseOnAShaft: 'SteadyStateSynchronousResponseOnAShaftInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2753.SteadyStateSynchronousResponseOnAShaft)(self.wrapped.SteadyStateSynchronousResponseOnAShaftInputs) if self.wrapped.SteadyStateSynchronousResponseOnAShaftInputs else None
