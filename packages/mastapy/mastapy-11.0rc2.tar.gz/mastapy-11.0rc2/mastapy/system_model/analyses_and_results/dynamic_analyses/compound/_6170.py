﻿'''_6170.py

WormGearSetCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2226
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6168, _6169, _6105
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6041
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'WormGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundDynamicAnalysis',)


class WormGearSetCompoundDynamicAnalysis(_6105.GearSetCompoundDynamicAnalysis):
    '''WormGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundDynamicAnalysis.TYPE'):
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
    def worm_gears_compound_dynamic_analysis(self) -> 'List[_6168.WormGearCompoundDynamicAnalysis]':
        '''List[WormGearCompoundDynamicAnalysis]: 'WormGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundDynamicAnalysis, constructor.new(_6168.WormGearCompoundDynamicAnalysis))
        return value

    @property
    def worm_meshes_compound_dynamic_analysis(self) -> 'List[_6169.WormGearMeshCompoundDynamicAnalysis]':
        '''List[WormGearMeshCompoundDynamicAnalysis]: 'WormMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundDynamicAnalysis, constructor.new(_6169.WormGearMeshCompoundDynamicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6041.WormGearSetDynamicAnalysis]':
        '''List[WormGearSetDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6041.WormGearSetDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_6041.WormGearSetDynamicAnalysis]':
        '''List[WormGearSetDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_6041.WormGearSetDynamicAnalysis))
        return value
