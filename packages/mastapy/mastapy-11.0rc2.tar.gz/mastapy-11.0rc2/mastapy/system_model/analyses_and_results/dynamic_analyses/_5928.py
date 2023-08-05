'''_5928.py

BevelDifferentialGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2190
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6459
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5926, _5927, _5933
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'BevelDifferentialGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetDynamicAnalysis',)


class BevelDifferentialGearSetDynamicAnalysis(_5933.BevelGearSetDynamicAnalysis):
    '''BevelDifferentialGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetDynamicAnalysis.TYPE'):
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
    def bevel_differential_gears_dynamic_analysis(self) -> 'List[_5926.BevelDifferentialGearDynamicAnalysis]':
        '''List[BevelDifferentialGearDynamicAnalysis]: 'BevelDifferentialGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsDynamicAnalysis, constructor.new(_5926.BevelDifferentialGearDynamicAnalysis))
        return value

    @property
    def bevel_differential_meshes_dynamic_analysis(self) -> 'List[_5927.BevelDifferentialGearMeshDynamicAnalysis]':
        '''List[BevelDifferentialGearMeshDynamicAnalysis]: 'BevelDifferentialMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesDynamicAnalysis, constructor.new(_5927.BevelDifferentialGearMeshDynamicAnalysis))
        return value
