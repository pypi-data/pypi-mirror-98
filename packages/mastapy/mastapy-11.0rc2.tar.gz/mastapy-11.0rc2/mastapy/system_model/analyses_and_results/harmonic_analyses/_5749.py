'''_5749.py

ZerolBevelGearSetHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6627
from mastapy.system_model.analyses_and_results.system_deflections import _2505
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5747, _5748, _5611
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ZerolBevelGearSetHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetHarmonicAnalysis',)


class ZerolBevelGearSetHarmonicAnalysis(_5611.BevelGearSetHarmonicAnalysis):
    '''ZerolBevelGearSetHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetHarmonicAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2505.ZerolBevelGearSetSystemDeflection':
        '''ZerolBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2505.ZerolBevelGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_harmonic_analysis(self) -> 'List[_5747.ZerolBevelGearHarmonicAnalysis]':
        '''List[ZerolBevelGearHarmonicAnalysis]: 'GearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsHarmonicAnalysis, constructor.new(_5747.ZerolBevelGearHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_gears_harmonic_analysis(self) -> 'List[_5747.ZerolBevelGearHarmonicAnalysis]':
        '''List[ZerolBevelGearHarmonicAnalysis]: 'ZerolBevelGearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsHarmonicAnalysis, constructor.new(_5747.ZerolBevelGearHarmonicAnalysis))
        return value

    @property
    def meshes_harmonic_analysis(self) -> 'List[_5748.ZerolBevelGearMeshHarmonicAnalysis]':
        '''List[ZerolBevelGearMeshHarmonicAnalysis]: 'MeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesHarmonicAnalysis, constructor.new(_5748.ZerolBevelGearMeshHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_meshes_harmonic_analysis(self) -> 'List[_5748.ZerolBevelGearMeshHarmonicAnalysis]':
        '''List[ZerolBevelGearMeshHarmonicAnalysis]: 'ZerolBevelMeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesHarmonicAnalysis, constructor.new(_5748.ZerolBevelGearMeshHarmonicAnalysis))
        return value
