'''_5147.py

SpiralBevelGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6593
from mastapy.system_model.analyses_and_results.mbd_analyses import _5146, _5145, _5052
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SpiralBevelGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetMultibodyDynamicsAnalysis',)


class SpiralBevelGearSetMultibodyDynamicsAnalysis(_5052.BevelGearSetMultibodyDynamicsAnalysis):
    '''SpiralBevelGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2218.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2218.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6593.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6593.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5146.SpiralBevelGearMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5146.SpiralBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gears_multibody_dynamics_analysis(self) -> 'List[_5146.SpiralBevelGearMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMultibodyDynamicsAnalysis]: 'SpiralBevelGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsMultibodyDynamicsAnalysis, constructor.new(_5146.SpiralBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_meshes_multibody_dynamics_analysis(self) -> 'List[_5145.SpiralBevelGearMeshMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMeshMultibodyDynamicsAnalysis]: 'SpiralBevelMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesMultibodyDynamicsAnalysis, constructor.new(_5145.SpiralBevelGearMeshMultibodyDynamicsAnalysis))
        return value
