﻿'''_4934.py

ConceptGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4932, _4933, _4963
from mastapy.system_model.analyses_and_results.modal_analyses import _4781
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ConceptGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundModalAnalysis',)


class ConceptGearSetCompoundModalAnalysis(_4963.GearSetCompoundModalAnalysis):
    '''ConceptGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2196.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2196.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_modal_analysis(self) -> 'List[_4932.ConceptGearCompoundModalAnalysis]':
        '''List[ConceptGearCompoundModalAnalysis]: 'ConceptGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundModalAnalysis, constructor.new(_4932.ConceptGearCompoundModalAnalysis))
        return value

    @property
    def concept_meshes_compound_modal_analysis(self) -> 'List[_4933.ConceptGearMeshCompoundModalAnalysis]':
        '''List[ConceptGearMeshCompoundModalAnalysis]: 'ConceptMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundModalAnalysis, constructor.new(_4933.ConceptGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4781.ConceptGearSetModalAnalysis]':
        '''List[ConceptGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4781.ConceptGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4781.ConceptGearSetModalAnalysis]':
        '''List[ConceptGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4781.ConceptGearSetModalAnalysis))
        return value
