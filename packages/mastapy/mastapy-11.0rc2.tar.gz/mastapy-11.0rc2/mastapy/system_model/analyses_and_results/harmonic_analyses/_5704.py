'''_5704.py

PointLoadHarmonicAnalysis
'''


from mastapy.system_model.part_model import _2147
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6575
from mastapy.system_model.analyses_and_results.system_deflections import _2456
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5743
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'PointLoadHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadHarmonicAnalysis',)


class PointLoadHarmonicAnalysis(_5743.VirtualComponentHarmonicAnalysis):
    '''PointLoadHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2147.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2147.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6575.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6575.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2456.PointLoadSystemDeflection':
        '''PointLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2456.PointLoadSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
