'''_3634.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2215
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3632, _3633, _3628
from mastapy.system_model.analyses_and_results.stability_analyses import _3502
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis(_3628.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2215.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2215.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2215.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2215.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_stability_analysis(self) -> 'List[_3632.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundStabilityAnalysis, constructor.new(_3632.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_stability_analysis(self) -> 'List[_3633.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundStabilityAnalysis, constructor.new(_3633.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3502.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3502.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3502.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3502.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis))
        return value
