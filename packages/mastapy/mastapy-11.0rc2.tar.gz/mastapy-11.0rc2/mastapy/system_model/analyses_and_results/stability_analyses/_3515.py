'''_3515.py

PointLoadStabilityAnalysis
'''


from mastapy.system_model.part_model import _2147
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6575
from mastapy.system_model.analyses_and_results.stability_analyses import _3553
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'PointLoadStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadStabilityAnalysis',)


class PointLoadStabilityAnalysis(_3553.VirtualComponentStabilityAnalysis):
    '''PointLoadStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadStabilityAnalysis.TYPE'):
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
