'''_5462.py

ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6627
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5460, _5461, _5351
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation',)


class ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation(_5351.BevelGearSetHarmonicAnalysisOfSingleExcitation):
    '''ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6627.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6627.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_harmonic_analysis_of_single_excitation(self) -> 'List[_5460.ZerolBevelGearHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelGearsHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsHarmonicAnalysisOfSingleExcitation, constructor.new(_5460.ZerolBevelGearHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def zerol_bevel_meshes_harmonic_analysis_of_single_excitation(self) -> 'List[_5461.ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelMeshesHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesHarmonicAnalysisOfSingleExcitation, constructor.new(_5461.ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation))
        return value
