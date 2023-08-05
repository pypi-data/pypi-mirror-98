﻿'''_2399.py

CVTBeltConnectionSystemDeflection
'''


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import _1952
from mastapy.system_model.analyses_and_results.power_flows import _3735
from mastapy.system_model.analyses_and_results.system_deflections import _2366
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CVTBeltConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionSystemDeflection',)


class CVTBeltConnectionSystemDeflection(_2366.BeltConnectionSystemDeflection):
    '''CVTBeltConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum_required_clamping_force(self) -> 'float':
        '''float: 'MinimumRequiredClampingForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumRequiredClampingForce

    @property
    def belt_clamping_force_safety_factor(self) -> 'float':
        '''float: 'BeltClampingForceSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BeltClampingForceSafetyFactor

    @property
    def total_efficiency(self) -> 'float':
        '''float: 'TotalEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalEfficiency

    @property
    def variator_efficiency(self) -> 'float':
        '''float: 'VariatorEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.VariatorEfficiency

    @property
    def pump_efficiency(self) -> 'float':
        '''float: 'PumpEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PumpEfficiency

    @property
    def connection_design(self) -> '_1952.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1952.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def power_flow_results(self) -> '_3735.CVTBeltConnectionPowerFlow':
        '''CVTBeltConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3735.CVTBeltConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
