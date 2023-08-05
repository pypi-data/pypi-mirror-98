﻿'''_5727.py

StraightBevelDiffGearSetHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2220
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6600
from mastapy.system_model.analyses_and_results.system_deflections import _2479
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5725, _5726, _5611
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'StraightBevelDiffGearSetHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetHarmonicAnalysis',)


class StraightBevelDiffGearSetHarmonicAnalysis(_5611.BevelGearSetHarmonicAnalysis):
    '''StraightBevelDiffGearSetHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2220.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2220.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6600.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6600.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2479.StraightBevelDiffGearSetSystemDeflection':
        '''StraightBevelDiffGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2479.StraightBevelDiffGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_harmonic_analysis(self) -> 'List[_5725.StraightBevelDiffGearHarmonicAnalysis]':
        '''List[StraightBevelDiffGearHarmonicAnalysis]: 'GearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsHarmonicAnalysis, constructor.new(_5725.StraightBevelDiffGearHarmonicAnalysis))
        return value

    @property
    def straight_bevel_diff_gears_harmonic_analysis(self) -> 'List[_5725.StraightBevelDiffGearHarmonicAnalysis]':
        '''List[StraightBevelDiffGearHarmonicAnalysis]: 'StraightBevelDiffGearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsHarmonicAnalysis, constructor.new(_5725.StraightBevelDiffGearHarmonicAnalysis))
        return value

    @property
    def meshes_harmonic_analysis(self) -> 'List[_5726.StraightBevelDiffGearMeshHarmonicAnalysis]':
        '''List[StraightBevelDiffGearMeshHarmonicAnalysis]: 'MeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesHarmonicAnalysis, constructor.new(_5726.StraightBevelDiffGearMeshHarmonicAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_harmonic_analysis(self) -> 'List[_5726.StraightBevelDiffGearMeshHarmonicAnalysis]':
        '''List[StraightBevelDiffGearMeshHarmonicAnalysis]: 'StraightBevelDiffMeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesHarmonicAnalysis, constructor.new(_5726.StraightBevelDiffGearMeshHarmonicAnalysis))
        return value
