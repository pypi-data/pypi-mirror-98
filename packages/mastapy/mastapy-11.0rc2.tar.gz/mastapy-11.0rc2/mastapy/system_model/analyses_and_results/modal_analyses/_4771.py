'''_4771.py

ClutchConnectionModalAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _2021
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6467
from mastapy.system_model.analyses_and_results.system_deflections import _2378
from mastapy.system_model.analyses_and_results.modal_analyses import _4788
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ClutchConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionModalAnalysis',)


class ClutchConnectionModalAnalysis(_4788.CouplingConnectionModalAnalysis):
    '''ClutchConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2021.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2021.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6467.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6467.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2378.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2378.ClutchConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
