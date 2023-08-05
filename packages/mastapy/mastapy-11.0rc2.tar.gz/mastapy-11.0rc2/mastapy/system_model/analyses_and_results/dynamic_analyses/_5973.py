'''_5973.py

FlexiblePinAssemblyDynamicAnalysis
'''


from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6523
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6014
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'FlexiblePinAssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyDynamicAnalysis',)


class FlexiblePinAssemblyDynamicAnalysis(_6014.SpecialisedAssemblyDynamicAnalysis):
    '''FlexiblePinAssemblyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2130.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6523.FlexiblePinAssemblyLoadCase':
        '''FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6523.FlexiblePinAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
