﻿'''_5723.py

SpringDamperHalfHarmonicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6595
from mastapy.system_model.analyses_and_results.system_deflections import _2476
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5632
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'SpringDamperHalfHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfHarmonicAnalysis',)


class SpringDamperHalfHarmonicAnalysis(_5632.CouplingHalfHarmonicAnalysis):
    '''SpringDamperHalfHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2275.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6595.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6595.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2476.SpringDamperHalfSystemDeflection':
        '''SpringDamperHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2476.SpringDamperHalfSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
