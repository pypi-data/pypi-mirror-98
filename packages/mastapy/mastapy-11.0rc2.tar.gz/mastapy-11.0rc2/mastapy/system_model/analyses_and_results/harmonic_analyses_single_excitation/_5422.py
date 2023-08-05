﻿'''_5422.py

PulleyHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2264, _2261
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6577, _6490
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5371
from mastapy._internal.python_net import python_net_import

_PULLEY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'PulleyHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyHarmonicAnalysisOfSingleExcitation',)


class PulleyHarmonicAnalysisOfSingleExcitation(_5371.CouplingHalfHarmonicAnalysisOfSingleExcitation):
    '''PulleyHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _PULLEY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2264.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6577.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6577.PulleyLoadCase.TYPE not in self.wrapped.ComponentLoadCase.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to PulleyLoadCase. Expected: {}.'.format(self.wrapped.ComponentLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentLoadCase.__class__)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
