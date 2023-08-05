﻿'''_5512.py

CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2200, _2216
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5510, _5511, _5523
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5382
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5523.GearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2200.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2200.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5510.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation]: 'CylindricalGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5510.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cylindrical_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5511.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'CylindricalMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5511.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5382.CylindricalGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearSetHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5382.CylindricalGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5382.CylindricalGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5382.CylindricalGearSetHarmonicAnalysisOfSingleExcitation))
        return value
