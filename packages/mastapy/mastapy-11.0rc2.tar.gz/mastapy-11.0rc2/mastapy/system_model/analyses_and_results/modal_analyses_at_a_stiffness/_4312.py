'''_4312.py

OilSealModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _2142
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6563
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4269
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'OilSealModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealModalAnalysisAtAStiffness',)


class OilSealModalAnalysisAtAStiffness(_4269.ConnectorModalAnalysisAtAStiffness):
    '''OilSealModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2142.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6563.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6563.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
