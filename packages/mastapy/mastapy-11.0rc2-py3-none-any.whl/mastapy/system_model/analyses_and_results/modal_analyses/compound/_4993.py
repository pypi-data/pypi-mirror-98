﻿'''_4993.py

RingPinsToDiscConnectionCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2020
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4846
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4968
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'RingPinsToDiscConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionCompoundModalAnalysis',)


class RingPinsToDiscConnectionCompoundModalAnalysis(_4968.InterMountableComponentConnectionCompoundModalAnalysis):
    '''RingPinsToDiscConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2020.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2020.RingPinsToDiscConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2020.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2020.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4846.RingPinsToDiscConnectionModalAnalysis]':
        '''List[RingPinsToDiscConnectionModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4846.RingPinsToDiscConnectionModalAnalysis))
        return value

    @property
    def connection_modal_analysis_load_cases(self) -> 'List[_4846.RingPinsToDiscConnectionModalAnalysis]':
        '''List[RingPinsToDiscConnectionModalAnalysis]: 'ConnectionModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisLoadCases, constructor.new(_4846.RingPinsToDiscConnectionModalAnalysis))
        return value
