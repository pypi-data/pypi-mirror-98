'''_3558.py

ZerolBevelGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6627
from mastapy.system_model.analyses_and_results.stability_analyses import _3559, _3557, _3445
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ZerolBevelGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetStabilityAnalysis',)


class ZerolBevelGearSetStabilityAnalysis(_3445.BevelGearSetStabilityAnalysis):
    '''ZerolBevelGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6627.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6627.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_stability_analysis(self) -> 'List[_3559.ZerolBevelGearStabilityAnalysis]':
        '''List[ZerolBevelGearStabilityAnalysis]: 'ZerolBevelGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsStabilityAnalysis, constructor.new(_3559.ZerolBevelGearStabilityAnalysis))
        return value

    @property
    def zerol_bevel_meshes_stability_analysis(self) -> 'List[_3557.ZerolBevelGearMeshStabilityAnalysis]':
        '''List[ZerolBevelGearMeshStabilityAnalysis]: 'ZerolBevelMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesStabilityAnalysis, constructor.new(_3557.ZerolBevelGearMeshStabilityAnalysis))
        return value
