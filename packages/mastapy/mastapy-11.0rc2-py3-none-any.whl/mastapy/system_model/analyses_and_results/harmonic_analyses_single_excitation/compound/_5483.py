﻿'''_5483.py

BoltedJointCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5352
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5561
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'BoltedJointCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundHarmonicAnalysisOfSingleExcitation',)


class BoltedJointCompoundHarmonicAnalysisOfSingleExcitation(_5561.SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation):
    '''BoltedJointCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2120.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2120.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5352.BoltedJointHarmonicAnalysisOfSingleExcitation]':
        '''List[BoltedJointHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5352.BoltedJointHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5352.BoltedJointHarmonicAnalysisOfSingleExcitation]':
        '''List[BoltedJointHarmonicAnalysisOfSingleExcitation]: 'AssemblyHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5352.BoltedJointHarmonicAnalysisOfSingleExcitation))
        return value
