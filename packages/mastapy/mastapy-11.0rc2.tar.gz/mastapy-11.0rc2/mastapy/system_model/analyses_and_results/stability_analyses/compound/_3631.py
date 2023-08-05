'''_3631.py

KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2213
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3629, _3630, _3628
from mastapy.system_model.analyses_and_results.stability_analyses import _3499
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis(_3628.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2213.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2213.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2213.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2213.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_stability_analysis(self) -> 'List[_3629.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundStabilityAnalysis, constructor.new(_3629.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_stability_analysis(self) -> 'List[_3630.KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundStabilityAnalysis, constructor.new(_3630.KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3499.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3499.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3499.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3499.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis))
        return value
