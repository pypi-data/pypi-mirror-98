﻿'''_7129.py

PlanetCarrierCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2145
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6999
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7121
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'PlanetCarrierCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundAdvancedSystemDeflection',)


class PlanetCarrierCompoundAdvancedSystemDeflection(_7121.MountableComponentCompoundAdvancedSystemDeflection):
    '''PlanetCarrierCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2145.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6999.PlanetCarrierAdvancedSystemDeflection]':
        '''List[PlanetCarrierAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6999.PlanetCarrierAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6999.PlanetCarrierAdvancedSystemDeflection]':
        '''List[PlanetCarrierAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6999.PlanetCarrierAdvancedSystemDeflection))
        return value
