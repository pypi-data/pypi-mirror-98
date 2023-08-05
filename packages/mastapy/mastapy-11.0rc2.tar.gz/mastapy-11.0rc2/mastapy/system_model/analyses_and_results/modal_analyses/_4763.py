'''_4763.py

BevelDifferentialGearSetModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2190
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6459
from mastapy.system_model.analyses_and_results.system_deflections import _2369
from mastapy.system_model.analyses_and_results.modal_analyses import _4762, _4761, _4768
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BevelDifferentialGearSetModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetModalAnalysis',)


class BevelDifferentialGearSetModalAnalysis(_4768.BevelGearSetModalAnalysis):
    '''BevelDifferentialGearSetModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2190.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6459.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6459.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2369.BevelDifferentialGearSetSystemDeflection':
        '''BevelDifferentialGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2369.BevelDifferentialGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def bevel_differential_gears_modal_analysis(self) -> 'List[_4762.BevelDifferentialGearModalAnalysis]':
        '''List[BevelDifferentialGearModalAnalysis]: 'BevelDifferentialGearsModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsModalAnalysis, constructor.new(_4762.BevelDifferentialGearModalAnalysis))
        return value

    @property
    def bevel_differential_meshes_modal_analysis(self) -> 'List[_4761.BevelDifferentialGearMeshModalAnalysis]':
        '''List[BevelDifferentialGearMeshModalAnalysis]: 'BevelDifferentialMeshesModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesModalAnalysis, constructor.new(_4761.BevelDifferentialGearMeshModalAnalysis))
        return value
