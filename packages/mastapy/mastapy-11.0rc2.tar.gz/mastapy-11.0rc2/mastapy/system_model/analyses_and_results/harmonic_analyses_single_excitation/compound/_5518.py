﻿'''_5518.py

FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5516, _5517, _5523
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5388
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5523.GearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2203.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5516.FaceGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearCompoundHarmonicAnalysisOfSingleExcitation]: 'FaceGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5516.FaceGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def face_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5517.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'FaceMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5517.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5388.FaceGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearSetHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5388.FaceGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5388.FaceGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5388.FaceGearSetHarmonicAnalysisOfSingleExcitation))
        return value
