'''_3385.py

PointLoadCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2147
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3253
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3421
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'PointLoadCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundSteadyStateSynchronousResponse',)


class PointLoadCompoundSteadyStateSynchronousResponse(_3421.VirtualComponentCompoundSteadyStateSynchronousResponse):
    '''PointLoadCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2147.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2147.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3253.PointLoadSteadyStateSynchronousResponse]':
        '''List[PointLoadSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3253.PointLoadSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_3253.PointLoadSteadyStateSynchronousResponse]':
        '''List[PointLoadSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_3253.PointLoadSteadyStateSynchronousResponse))
        return value
