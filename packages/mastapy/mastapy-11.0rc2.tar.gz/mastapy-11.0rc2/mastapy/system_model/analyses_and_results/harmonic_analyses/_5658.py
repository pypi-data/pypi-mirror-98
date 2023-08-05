'''_5658.py

ExternalCADModelHarmonicAnalysis
'''


from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6518
from mastapy.system_model.analyses_and_results.system_deflections import _2417
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5619
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ExternalCADModelHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelHarmonicAnalysis',)


class ExternalCADModelHarmonicAnalysis(_5619.ComponentHarmonicAnalysis):
    '''ExternalCADModelHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6518.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6518.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2417.ExternalCADModelSystemDeflection':
        '''ExternalCADModelSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2417.ExternalCADModelSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
