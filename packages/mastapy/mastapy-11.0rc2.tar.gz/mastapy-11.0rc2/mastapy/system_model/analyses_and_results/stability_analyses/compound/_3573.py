'''_3573.py

BevelDifferentialGearSetCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2190
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3571, _3572, _3578
from mastapy.system_model.analyses_and_results.stability_analyses import _3440
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'BevelDifferentialGearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundStabilityAnalysis',)


class BevelDifferentialGearSetCompoundStabilityAnalysis(_3578.BevelGearSetCompoundStabilityAnalysis):
    '''BevelDifferentialGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2190.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2190.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_stability_analysis(self) -> 'List[_3571.BevelDifferentialGearCompoundStabilityAnalysis]':
        '''List[BevelDifferentialGearCompoundStabilityAnalysis]: 'BevelDifferentialGearsCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundStabilityAnalysis, constructor.new(_3571.BevelDifferentialGearCompoundStabilityAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_stability_analysis(self) -> 'List[_3572.BevelDifferentialGearMeshCompoundStabilityAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundStabilityAnalysis]: 'BevelDifferentialMeshesCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundStabilityAnalysis, constructor.new(_3572.BevelDifferentialGearMeshCompoundStabilityAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3440.BevelDifferentialGearSetStabilityAnalysis]':
        '''List[BevelDifferentialGearSetStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3440.BevelDifferentialGearSetStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3440.BevelDifferentialGearSetStabilityAnalysis]':
        '''List[BevelDifferentialGearSetStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3440.BevelDifferentialGearSetStabilityAnalysis))
        return value
