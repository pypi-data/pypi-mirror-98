﻿'''_5494.py

ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5492, _5493, _5523
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5364
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5523.GearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2196.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2196.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5492.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptGearCompoundHarmonicAnalysisOfSingleExcitation]: 'ConceptGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5492.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def concept_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5493.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'ConceptMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5493.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5364.ConceptGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptGearSetHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5364.ConceptGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5364.ConceptGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5364.ConceptGearSetHarmonicAnalysisOfSingleExcitation))
        return value
