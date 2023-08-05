﻿'''_5364.py

ConceptGearSetHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6477
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5362, _5363, _5393
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ConceptGearSetHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetHarmonicAnalysisOfSingleExcitation',)


class ConceptGearSetHarmonicAnalysisOfSingleExcitation(_5393.GearSetHarmonicAnalysisOfSingleExcitation):
    '''ConceptGearSetHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2196.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6477.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6477.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_harmonic_analysis_of_single_excitation(self) -> 'List[_5362.ConceptGearHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptGearHarmonicAnalysisOfSingleExcitation]: 'ConceptGearsHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsHarmonicAnalysisOfSingleExcitation, constructor.new(_5362.ConceptGearHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def concept_meshes_harmonic_analysis_of_single_excitation(self) -> 'List[_5363.ConceptGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptGearMeshHarmonicAnalysisOfSingleExcitation]: 'ConceptMeshesHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesHarmonicAnalysisOfSingleExcitation, constructor.new(_5363.ConceptGearMeshHarmonicAnalysisOfSingleExcitation))
        return value
