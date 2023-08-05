﻿'''_4376.py

BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2190
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4374, _4375, _4381
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4246
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness',)


class BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness(_4381.BevelGearSetCompoundModalAnalysisAtAStiffness):
    '''BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2190.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2190.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4374.BevelDifferentialGearCompoundModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearCompoundModalAnalysisAtAStiffness]: 'BevelDifferentialGearsCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundModalAnalysisAtAStiffness, constructor.new(_4374.BevelDifferentialGearCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bevel_differential_meshes_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4375.BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness]: 'BevelDifferentialMeshesCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundModalAnalysisAtAStiffness, constructor.new(_4375.BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4246.BevelDifferentialGearSetModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearSetModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4246.BevelDifferentialGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4246.BevelDifferentialGearSetModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearSetModalAnalysisAtAStiffness]: 'AssemblyModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtAStiffnessLoadCases, constructor.new(_4246.BevelDifferentialGearSetModalAnalysisAtAStiffness))
        return value
