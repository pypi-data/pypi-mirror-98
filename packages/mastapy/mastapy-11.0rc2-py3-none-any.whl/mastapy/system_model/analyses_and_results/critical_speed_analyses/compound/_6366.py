﻿'''_6366.py

FaceGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6364, _6365, _6371
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6237
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'FaceGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundCriticalSpeedAnalysis',)


class FaceGearSetCompoundCriticalSpeedAnalysis(_6371.GearSetCompoundCriticalSpeedAnalysis):
    '''FaceGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2203.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_critical_speed_analysis(self) -> 'List[_6364.FaceGearCompoundCriticalSpeedAnalysis]':
        '''List[FaceGearCompoundCriticalSpeedAnalysis]: 'FaceGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundCriticalSpeedAnalysis, constructor.new(_6364.FaceGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def face_meshes_compound_critical_speed_analysis(self) -> 'List[_6365.FaceGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[FaceGearMeshCompoundCriticalSpeedAnalysis]: 'FaceMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6365.FaceGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6237.FaceGearSetCriticalSpeedAnalysis]':
        '''List[FaceGearSetCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6237.FaceGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6237.FaceGearSetCriticalSpeedAnalysis]':
        '''List[FaceGearSetCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6237.FaceGearSetCriticalSpeedAnalysis))
        return value
