'''_5285.py

SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5283, _5284, _5202
from mastapy.system_model.analyses_and_results.mbd_analyses import _5147
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis',)


class SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis(_5202.BevelGearSetCompoundMultibodyDynamicsAnalysis):
    '''SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis.TYPE'):
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
    def spiral_bevel_gears_compound_multibody_dynamics_analysis(self) -> 'List[_5283.SpiralBevelGearCompoundMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearCompoundMultibodyDynamicsAnalysis]: 'SpiralBevelGearsCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundMultibodyDynamicsAnalysis, constructor.new(_5283.SpiralBevelGearCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_meshes_compound_multibody_dynamics_analysis(self) -> 'List[_5284.SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis]: 'SpiralBevelMeshesCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundMultibodyDynamicsAnalysis, constructor.new(_5284.SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5147.SpiralBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5147.SpiralBevelGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_multibody_dynamics_analysis_load_cases(self) -> 'List[_5147.SpiralBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultibodyDynamicsAnalysis]: 'AssemblyMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultibodyDynamicsAnalysisLoadCases, constructor.new(_5147.SpiralBevelGearSetMultibodyDynamicsAnalysis))
        return value
