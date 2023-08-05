'''_5663.py

FlexiblePinAssemblyHarmonicAnalysis
'''


from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6523
from mastapy.system_model.analyses_and_results.system_deflections import _2423
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5717
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'FlexiblePinAssemblyHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyHarmonicAnalysis',)


class FlexiblePinAssemblyHarmonicAnalysis(_5717.SpecialisedAssemblyHarmonicAnalysis):
    '''FlexiblePinAssemblyHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyHarmonicAnalysis.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2423.FlexiblePinAssemblySystemDeflection':
        '''FlexiblePinAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2423.FlexiblePinAssemblySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
