﻿'''_5711.py

RollingRingHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2270
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6584
from mastapy.system_model.analyses_and_results.system_deflections import _2464
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5632
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'RollingRingHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingHarmonicAnalysis',)


class RollingRingHarmonicAnalysis(_5632.CouplingHalfHarmonicAnalysis):
    '''RollingRingHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingHarmonicAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2464.RollingRingSystemDeflection':
        '''RollingRingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2464.RollingRingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[RollingRingHarmonicAnalysis]':
        '''List[RollingRingHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingHarmonicAnalysis))
        return value
