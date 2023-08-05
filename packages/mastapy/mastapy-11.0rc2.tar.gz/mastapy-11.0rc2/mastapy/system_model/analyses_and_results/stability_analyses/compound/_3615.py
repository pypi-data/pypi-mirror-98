'''_3615.py

FaceGearSetCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3613, _3614, _3620
from mastapy.system_model.analyses_and_results.stability_analyses import _3483
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'FaceGearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundStabilityAnalysis',)


class FaceGearSetCompoundStabilityAnalysis(_3620.GearSetCompoundStabilityAnalysis):
    '''FaceGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundStabilityAnalysis.TYPE'):
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
    def face_gears_compound_stability_analysis(self) -> 'List[_3613.FaceGearCompoundStabilityAnalysis]':
        '''List[FaceGearCompoundStabilityAnalysis]: 'FaceGearsCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundStabilityAnalysis, constructor.new(_3613.FaceGearCompoundStabilityAnalysis))
        return value

    @property
    def face_meshes_compound_stability_analysis(self) -> 'List[_3614.FaceGearMeshCompoundStabilityAnalysis]':
        '''List[FaceGearMeshCompoundStabilityAnalysis]: 'FaceMeshesCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundStabilityAnalysis, constructor.new(_3614.FaceGearMeshCompoundStabilityAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3483.FaceGearSetStabilityAnalysis]':
        '''List[FaceGearSetStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3483.FaceGearSetStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3483.FaceGearSetStabilityAnalysis]':
        '''List[FaceGearSetStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3483.FaceGearSetStabilityAnalysis))
        return value
