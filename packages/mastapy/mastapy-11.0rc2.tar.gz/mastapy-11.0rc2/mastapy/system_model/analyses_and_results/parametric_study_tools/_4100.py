'''_4100.py

WormGearSetParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2226
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6624
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4099, _4098, _4024
from mastapy.system_model.analyses_and_results.system_deflections import _2502
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'WormGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetParametricStudyTool',)


class WormGearSetParametricStudyTool(_4024.GearSetParametricStudyTool):
    '''WormGearSetParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2226.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2226.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6624.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6624.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def worm_gears_parametric_study_tool(self) -> 'List[_4099.WormGearParametricStudyTool]':
        '''List[WormGearParametricStudyTool]: 'WormGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsParametricStudyTool, constructor.new(_4099.WormGearParametricStudyTool))
        return value

    @property
    def worm_meshes_parametric_study_tool(self) -> 'List[_4098.WormGearMeshParametricStudyTool]':
        '''List[WormGearMeshParametricStudyTool]: 'WormMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesParametricStudyTool, constructor.new(_4098.WormGearMeshParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2502.WormGearSetSystemDeflection]':
        '''List[WormGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2502.WormGearSetSystemDeflection))
        return value
