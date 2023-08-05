'''_2457.py

PowerLoadSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2148
from mastapy.system_model.analyses_and_results.static_loads import _6576
from mastapy.system_model.analyses_and_results.power_flows import _3785
from mastapy.system_model.analyses_and_results.system_deflections import _2498, _2500
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PowerLoadSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadSystemDeflection',)


class PowerLoadSystemDeflection(_2500.VirtualComponentSystemDeflection):
    '''PowerLoadSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def power(self) -> 'float':
        '''float: 'Power' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Power

    @property
    def torque(self) -> 'float':
        '''float: 'Torque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Torque

    @property
    def component_design(self) -> '_2148.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2148.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6576.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6576.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3785.PowerLoadPowerFlow':
        '''PowerLoadPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3785.PowerLoadPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def transmission_error_to_other_power_loads(self) -> 'List[_2498.TransmissionErrorResult]':
        '''List[TransmissionErrorResult]: 'TransmissionErrorToOtherPowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TransmissionErrorToOtherPowerLoads, constructor.new(_2498.TransmissionErrorResult))
        return value
