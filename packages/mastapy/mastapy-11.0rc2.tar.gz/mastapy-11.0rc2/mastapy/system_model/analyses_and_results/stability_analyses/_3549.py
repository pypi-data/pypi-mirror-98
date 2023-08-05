'''_3549.py

TorqueConverterPumpStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2282
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6614
from mastapy.system_model.analyses_and_results.stability_analyses import _3466
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'TorqueConverterPumpStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpStabilityAnalysis',)


class TorqueConverterPumpStabilityAnalysis(_3466.CouplingHalfStabilityAnalysis):
    '''TorqueConverterPumpStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2282.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2282.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6614.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6614.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
