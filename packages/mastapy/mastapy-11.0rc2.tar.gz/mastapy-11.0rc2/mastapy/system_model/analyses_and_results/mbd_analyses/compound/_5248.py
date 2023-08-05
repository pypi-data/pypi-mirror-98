﻿'''_5248.py

HypoidGearSetCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2209
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5246, _5247, _5190
from mastapy.system_model.analyses_and_results.mbd_analyses import _5100
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'HypoidGearSetCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundMultibodyDynamicsAnalysis',)


class HypoidGearSetCompoundMultibodyDynamicsAnalysis(_5190.AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis):
    '''HypoidGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2209.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2209.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_multibody_dynamics_analysis(self) -> 'List[_5246.HypoidGearCompoundMultibodyDynamicsAnalysis]':
        '''List[HypoidGearCompoundMultibodyDynamicsAnalysis]: 'HypoidGearsCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundMultibodyDynamicsAnalysis, constructor.new(_5246.HypoidGearCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def hypoid_meshes_compound_multibody_dynamics_analysis(self) -> 'List[_5247.HypoidGearMeshCompoundMultibodyDynamicsAnalysis]':
        '''List[HypoidGearMeshCompoundMultibodyDynamicsAnalysis]: 'HypoidMeshesCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundMultibodyDynamicsAnalysis, constructor.new(_5247.HypoidGearMeshCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5100.HypoidGearSetMultibodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5100.HypoidGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_multibody_dynamics_analysis_load_cases(self) -> 'List[_5100.HypoidGearSetMultibodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultibodyDynamicsAnalysis]: 'AssemblyMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultibodyDynamicsAnalysisLoadCases, constructor.new(_5100.HypoidGearSetMultibodyDynamicsAnalysis))
        return value
