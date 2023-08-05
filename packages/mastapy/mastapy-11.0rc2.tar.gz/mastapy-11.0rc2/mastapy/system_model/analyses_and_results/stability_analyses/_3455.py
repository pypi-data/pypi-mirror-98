'''_3455.py

ConceptCouplingHalfStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2256
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6473
from mastapy.system_model.analyses_and_results.stability_analyses import _3466
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ConceptCouplingHalfStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfStabilityAnalysis',)


class ConceptCouplingHalfStabilityAnalysis(_3466.CouplingHalfStabilityAnalysis):
    '''ConceptCouplingHalfStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2256.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2256.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6473.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6473.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
