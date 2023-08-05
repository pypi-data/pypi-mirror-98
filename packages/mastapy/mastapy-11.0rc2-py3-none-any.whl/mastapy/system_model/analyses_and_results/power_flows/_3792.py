﻿'''_3792.py

RootAssemblyPowerFlow
'''


from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3783, _3702
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RootAssemblyPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyPowerFlow',)


class RootAssemblyPowerFlow(_3702.AssemblyPowerFlow):
    '''RootAssemblyPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2150.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def power_flow_inputs(self) -> '_3783.PowerFlow':
        '''PowerFlow: 'PowerFlowInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3783.PowerFlow)(self.wrapped.PowerFlowInputs) if self.wrapped.PowerFlowInputs else None
