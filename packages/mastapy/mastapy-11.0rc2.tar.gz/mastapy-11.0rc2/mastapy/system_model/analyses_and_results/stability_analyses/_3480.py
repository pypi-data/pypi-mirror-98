'''_3480.py

DatumStabilityAnalysis
'''


from mastapy.system_model.part_model import _2125
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6503
from mastapy.system_model.analyses_and_results.stability_analyses import _3453
from mastapy._internal.python_net import python_net_import

_DATUM_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'DatumStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumStabilityAnalysis',)


class DatumStabilityAnalysis(_3453.ComponentStabilityAnalysis):
    '''DatumStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2125.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2125.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6503.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6503.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
