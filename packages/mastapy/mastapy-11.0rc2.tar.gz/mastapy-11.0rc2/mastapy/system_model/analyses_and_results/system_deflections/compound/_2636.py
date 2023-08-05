﻿'''_2636.py

TorqueConverterConnectionCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2031
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2493
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2554
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'TorqueConverterConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundSystemDeflection',)


class TorqueConverterConnectionCompoundSystemDeflection(_2554.CouplingConnectionCompoundSystemDeflection):
    '''TorqueConverterConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2031.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2031.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2031.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2031.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2493.TorqueConverterConnectionSystemDeflection]':
        '''List[TorqueConverterConnectionSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2493.TorqueConverterConnectionSystemDeflection))
        return value

    @property
    def connection_system_deflection_load_cases(self) -> 'List[_2493.TorqueConverterConnectionSystemDeflection]':
        '''List[TorqueConverterConnectionSystemDeflection]: 'ConnectionSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionLoadCases, constructor.new(_2493.TorqueConverterConnectionSystemDeflection))
        return value
