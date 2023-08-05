﻿'''_5705.py

PowerLoadHarmonicAnalysis
'''


from mastapy.system_model.part_model import _2148
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6576
from mastapy.system_model.analyses_and_results.system_deflections import _2457
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5743
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'PowerLoadHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadHarmonicAnalysis',)


class PowerLoadHarmonicAnalysis(_5743.VirtualComponentHarmonicAnalysis):
    '''PowerLoadHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2148.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2148.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6576.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6576.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2457.PowerLoadSystemDeflection':
        '''PowerLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2457.PowerLoadSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
