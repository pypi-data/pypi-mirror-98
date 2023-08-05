'''_6307.py

WormGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2226
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6624
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6305, _6306, _6242
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'WormGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCriticalSpeedAnalysis',)


class WormGearSetCriticalSpeedAnalysis(_6242.GearSetCriticalSpeedAnalysis):
    '''WormGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2226.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2226.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6624.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6624.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def worm_gears_critical_speed_analysis(self) -> 'List[_6305.WormGearCriticalSpeedAnalysis]':
        '''List[WormGearCriticalSpeedAnalysis]: 'WormGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCriticalSpeedAnalysis, constructor.new(_6305.WormGearCriticalSpeedAnalysis))
        return value

    @property
    def worm_meshes_critical_speed_analysis(self) -> 'List[_6306.WormGearMeshCriticalSpeedAnalysis]':
        '''List[WormGearMeshCriticalSpeedAnalysis]: 'WormMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCriticalSpeedAnalysis, constructor.new(_6306.WormGearMeshCriticalSpeedAnalysis))
        return value
