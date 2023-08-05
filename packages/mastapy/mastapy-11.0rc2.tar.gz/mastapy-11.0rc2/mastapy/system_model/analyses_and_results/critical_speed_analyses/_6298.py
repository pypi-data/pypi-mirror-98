﻿'''_6298.py

SynchroniserSleeveCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model.couplings import _2280
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6609
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6297
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'SynchroniserSleeveCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCriticalSpeedAnalysis',)


class SynchroniserSleeveCriticalSpeedAnalysis(_6297.SynchroniserPartCriticalSpeedAnalysis):
    '''SynchroniserSleeveCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2280.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2280.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6609.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6609.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
