﻿'''_5903.py

ZerolBevelGearCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2227
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5747
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5793
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'ZerolBevelGearCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearCompoundHarmonicAnalysis',)


class ZerolBevelGearCompoundHarmonicAnalysis(_5793.BevelGearCompoundHarmonicAnalysis):
    '''ZerolBevelGearCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearCompoundHarmonicAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5747.ZerolBevelGearHarmonicAnalysis]':
        '''List[ZerolBevelGearHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5747.ZerolBevelGearHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5747.ZerolBevelGearHarmonicAnalysis]':
        '''List[ZerolBevelGearHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5747.ZerolBevelGearHarmonicAnalysis))
        return value
