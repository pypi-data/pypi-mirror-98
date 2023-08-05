﻿'''_6246.py

HypoidGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2209
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6544
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6244, _6245, _6186
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'HypoidGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCriticalSpeedAnalysis',)


class HypoidGearSetCriticalSpeedAnalysis(_6186.AGMAGleasonConicalGearSetCriticalSpeedAnalysis):
    '''HypoidGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2209.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6544.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6544.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_critical_speed_analysis(self) -> 'List[_6244.HypoidGearCriticalSpeedAnalysis]':
        '''List[HypoidGearCriticalSpeedAnalysis]: 'HypoidGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCriticalSpeedAnalysis, constructor.new(_6244.HypoidGearCriticalSpeedAnalysis))
        return value

    @property
    def hypoid_meshes_critical_speed_analysis(self) -> 'List[_6245.HypoidGearMeshCriticalSpeedAnalysis]':
        '''List[HypoidGearMeshCriticalSpeedAnalysis]: 'HypoidMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCriticalSpeedAnalysis, constructor.new(_6245.HypoidGearMeshCriticalSpeedAnalysis))
        return value
