﻿'''_5028.py

WormGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2226
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5026, _5027, _4963
from mastapy.system_model.analyses_and_results.modal_analyses import _4887
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'WormGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundModalAnalysis',)


class WormGearSetCompoundModalAnalysis(_4963.GearSetCompoundModalAnalysis):
    '''WormGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2226.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2226.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2226.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2226.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_modal_analysis(self) -> 'List[_5026.WormGearCompoundModalAnalysis]':
        '''List[WormGearCompoundModalAnalysis]: 'WormGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundModalAnalysis, constructor.new(_5026.WormGearCompoundModalAnalysis))
        return value

    @property
    def worm_meshes_compound_modal_analysis(self) -> 'List[_5027.WormGearMeshCompoundModalAnalysis]':
        '''List[WormGearMeshCompoundModalAnalysis]: 'WormMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundModalAnalysis, constructor.new(_5027.WormGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4887.WormGearSetModalAnalysis]':
        '''List[WormGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4887.WormGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4887.WormGearSetModalAnalysis]':
        '''List[WormGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4887.WormGearSetModalAnalysis))
        return value
