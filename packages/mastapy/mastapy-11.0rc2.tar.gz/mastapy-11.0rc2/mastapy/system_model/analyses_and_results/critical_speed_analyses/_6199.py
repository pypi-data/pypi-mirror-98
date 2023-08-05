﻿'''_6199.py

BoltCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model import _2119
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6466
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6205
from mastapy._internal.python_net import python_net_import

_BOLT_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'BoltCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCriticalSpeedAnalysis',)


class BoltCriticalSpeedAnalysis(_6205.ComponentCriticalSpeedAnalysis):
    '''BoltCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2119.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2119.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6466.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6466.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
