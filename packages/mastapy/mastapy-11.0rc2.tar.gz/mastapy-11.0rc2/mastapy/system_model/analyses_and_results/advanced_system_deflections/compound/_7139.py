﻿'''_7139.py

ShaftCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2157
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7009
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7045
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ShaftCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundAdvancedSystemDeflection',)


class ShaftCompoundAdvancedSystemDeflection(_7045.AbstractShaftCompoundAdvancedSystemDeflection):
    '''ShaftCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2157.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2157.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_7009.ShaftAdvancedSystemDeflection]':
        '''List[ShaftAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_7009.ShaftAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_7009.ShaftAdvancedSystemDeflection]':
        '''List[ShaftAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_7009.ShaftAdvancedSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundAdvancedSystemDeflection]':
        '''List[ShaftCompoundAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundAdvancedSystemDeflection))
        return value
