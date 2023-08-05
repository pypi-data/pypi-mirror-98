﻿'''_2830.py

ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2700
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2803
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft',)


class ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft(_2803.ComponentCompoundSteadyStateSynchronousResponseOnAShaft):
    '''ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2700.ExternalCADModelSteadyStateSynchronousResponseOnAShaft]':
        '''List[ExternalCADModelSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2700.ExternalCADModelSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def component_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2700.ExternalCADModelSteadyStateSynchronousResponseOnAShaft]':
        '''List[ExternalCADModelSteadyStateSynchronousResponseOnAShaft]: 'ComponentSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2700.ExternalCADModelSteadyStateSynchronousResponseOnAShaft))
        return value
