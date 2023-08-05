﻿'''_6776.py

ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.gears import _2227
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6625
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6665
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation',)


class ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation(_6665.BevelGearAdvancedTimeSteppingAnalysisForModulation):
    '''ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2227.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2227.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6625.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6625.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
