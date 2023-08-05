﻿'''_5004.py

SpiralBevelGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5002, _5003, _4921
from mastapy.system_model.analyses_and_results.modal_analyses import _4858
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SpiralBevelGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundModalAnalysis',)


class SpiralBevelGearSetCompoundModalAnalysis(_4921.BevelGearSetCompoundModalAnalysis):
    '''SpiralBevelGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2218.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2218.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2218.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2218.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_modal_analysis(self) -> 'List[_5002.SpiralBevelGearCompoundModalAnalysis]':
        '''List[SpiralBevelGearCompoundModalAnalysis]: 'SpiralBevelGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundModalAnalysis, constructor.new(_5002.SpiralBevelGearCompoundModalAnalysis))
        return value

    @property
    def spiral_bevel_meshes_compound_modal_analysis(self) -> 'List[_5003.SpiralBevelGearMeshCompoundModalAnalysis]':
        '''List[SpiralBevelGearMeshCompoundModalAnalysis]: 'SpiralBevelMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundModalAnalysis, constructor.new(_5003.SpiralBevelGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4858.SpiralBevelGearSetModalAnalysis]':
        '''List[SpiralBevelGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4858.SpiralBevelGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4858.SpiralBevelGearSetModalAnalysis]':
        '''List[SpiralBevelGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4858.SpiralBevelGearSetModalAnalysis))
        return value
