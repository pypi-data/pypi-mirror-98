﻿'''_5882.py

StraightBevelDiffGearCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2219, _2223, _2224
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5725
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5793
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'StraightBevelDiffGearCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearCompoundHarmonicAnalysis',)


class StraightBevelDiffGearCompoundHarmonicAnalysis(_5793.BevelGearCompoundHarmonicAnalysis):
    '''StraightBevelDiffGearCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2219.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2219.StraightBevelDiffGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5725.StraightBevelDiffGearHarmonicAnalysis]':
        '''List[StraightBevelDiffGearHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5725.StraightBevelDiffGearHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5725.StraightBevelDiffGearHarmonicAnalysis]':
        '''List[StraightBevelDiffGearHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5725.StraightBevelDiffGearHarmonicAnalysis))
        return value
