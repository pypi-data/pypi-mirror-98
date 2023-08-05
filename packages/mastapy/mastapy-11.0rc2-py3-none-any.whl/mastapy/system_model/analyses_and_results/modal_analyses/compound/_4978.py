﻿'''_4978.py

MassDiscCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2138
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4827
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5025
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'MassDiscCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundModalAnalysis',)


class MassDiscCompoundModalAnalysis(_5025.VirtualComponentCompoundModalAnalysis):
    '''MassDiscCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2138.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2138.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4827.MassDiscModalAnalysis]':
        '''List[MassDiscModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4827.MassDiscModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4827.MassDiscModalAnalysis]':
        '''List[MassDiscModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4827.MassDiscModalAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundModalAnalysis]':
        '''List[MassDiscCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundModalAnalysis))
        return value
