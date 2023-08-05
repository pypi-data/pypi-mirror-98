﻿'''_6342.py

ConceptGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6340, _6341, _6371
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6211
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'ConceptGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundCriticalSpeedAnalysis',)


class ConceptGearSetCompoundCriticalSpeedAnalysis(_6371.GearSetCompoundCriticalSpeedAnalysis):
    '''ConceptGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundCriticalSpeedAnalysis.TYPE'):
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
    def concept_gears_compound_critical_speed_analysis(self) -> 'List[_6340.ConceptGearCompoundCriticalSpeedAnalysis]':
        '''List[ConceptGearCompoundCriticalSpeedAnalysis]: 'ConceptGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundCriticalSpeedAnalysis, constructor.new(_6340.ConceptGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_meshes_compound_critical_speed_analysis(self) -> 'List[_6341.ConceptGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[ConceptGearMeshCompoundCriticalSpeedAnalysis]: 'ConceptMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6341.ConceptGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6211.ConceptGearSetCriticalSpeedAnalysis]':
        '''List[ConceptGearSetCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6211.ConceptGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6211.ConceptGearSetCriticalSpeedAnalysis]':
        '''List[ConceptGearSetCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6211.ConceptGearSetCriticalSpeedAnalysis))
        return value
