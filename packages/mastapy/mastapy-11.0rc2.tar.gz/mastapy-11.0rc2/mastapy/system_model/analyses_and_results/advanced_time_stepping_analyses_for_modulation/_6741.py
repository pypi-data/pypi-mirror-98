﻿'''_6741.py

RollingRingAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2270
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6584
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6688
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'RollingRingAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAdvancedTimeSteppingAnalysisForModulation',)


class RollingRingAdvancedTimeSteppingAnalysisForModulation(_6688.CouplingHalfAdvancedTimeSteppingAnalysisForModulation):
    '''RollingRingAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2270.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2270.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6584.RollingRingLoadCase':
        '''RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6584.RollingRingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RollingRingAdvancedTimeSteppingAnalysisForModulation]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingAdvancedTimeSteppingAnalysisForModulation))
        return value
