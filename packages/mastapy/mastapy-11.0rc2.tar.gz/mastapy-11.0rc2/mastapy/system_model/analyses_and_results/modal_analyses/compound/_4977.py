﻿'''_4977.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2215
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4975, _4976, _4971
from mastapy.system_model.analyses_and_results.modal_analyses import _4826
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis(_4971.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2215.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2215.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2215.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2215.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_modal_analysis(self) -> 'List[_4975.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysis, constructor.new(_4975.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_modal_analysis(self) -> 'List[_4976.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysis, constructor.new(_4976.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4826.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4826.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4826.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4826.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis))
        return value
