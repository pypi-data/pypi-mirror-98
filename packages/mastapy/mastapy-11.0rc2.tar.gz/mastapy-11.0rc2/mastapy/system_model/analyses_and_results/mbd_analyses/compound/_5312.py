'''_5312.py

ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5310, _5311, _5202
from mastapy.system_model.analyses_and_results.mbd_analyses import _5177
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis',)


class ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis(_5202.BevelGearSetCompoundMultibodyDynamicsAnalysis):
    '''ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_multibody_dynamics_analysis(self) -> 'List[_5310.ZerolBevelGearCompoundMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearCompoundMultibodyDynamicsAnalysis]: 'ZerolBevelGearsCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundMultibodyDynamicsAnalysis, constructor.new(_5310.ZerolBevelGearCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_multibody_dynamics_analysis(self) -> 'List[_5311.ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis]: 'ZerolBevelMeshesCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundMultibodyDynamicsAnalysis, constructor.new(_5311.ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5177.ZerolBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5177.ZerolBevelGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_multibody_dynamics_analysis_load_cases(self) -> 'List[_5177.ZerolBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetMultibodyDynamicsAnalysis]: 'AssemblyMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultibodyDynamicsAnalysisLoadCases, constructor.new(_5177.ZerolBevelGearSetMultibodyDynamicsAnalysis))
        return value
