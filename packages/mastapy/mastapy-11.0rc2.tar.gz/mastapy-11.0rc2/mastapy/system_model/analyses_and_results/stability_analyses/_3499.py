'''_3499.py

KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2213
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6554
from mastapy.system_model.analyses_and_results.stability_analyses import _3500, _3498, _3496
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis(_3496.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2213.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2213.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6554.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6554.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_stability_analysis(self) -> 'List[_3500.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsStabilityAnalysis, constructor.new(_3500.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_stability_analysis(self) -> 'List[_3498.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesStabilityAnalysis, constructor.new(_3498.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis))
        return value
