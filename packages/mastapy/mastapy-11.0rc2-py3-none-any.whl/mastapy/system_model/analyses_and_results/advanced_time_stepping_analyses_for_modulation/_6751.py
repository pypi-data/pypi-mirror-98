﻿'''_6751.py

SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6593
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6749, _6750, _6667
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation',)


class SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation(_6667.BevelGearSetAdvancedTimeSteppingAnalysisForModulation):
    '''SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2218.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2218.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6593.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6593.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def spiral_bevel_gears_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6749.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation]: 'SpiralBevelGearsAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6749.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spiral_bevel_meshes_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6750.SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'SpiralBevelMeshesAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6750.SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
