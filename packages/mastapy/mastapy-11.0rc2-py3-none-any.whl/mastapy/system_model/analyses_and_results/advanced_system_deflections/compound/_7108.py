﻿'''_7108.py

HypoidGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2209
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7106, _7107, _7050
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6977
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'HypoidGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundAdvancedSystemDeflection',)


class HypoidGearSetCompoundAdvancedSystemDeflection(_7050.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection):
    '''HypoidGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2209.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2209.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_advanced_system_deflection(self) -> 'List[_7106.HypoidGearCompoundAdvancedSystemDeflection]':
        '''List[HypoidGearCompoundAdvancedSystemDeflection]: 'HypoidGearsCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundAdvancedSystemDeflection, constructor.new(_7106.HypoidGearCompoundAdvancedSystemDeflection))
        return value

    @property
    def hypoid_meshes_compound_advanced_system_deflection(self) -> 'List[_7107.HypoidGearMeshCompoundAdvancedSystemDeflection]':
        '''List[HypoidGearMeshCompoundAdvancedSystemDeflection]: 'HypoidMeshesCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundAdvancedSystemDeflection, constructor.new(_7107.HypoidGearMeshCompoundAdvancedSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6977.HypoidGearSetAdvancedSystemDeflection]':
        '''List[HypoidGearSetAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6977.HypoidGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_6977.HypoidGearSetAdvancedSystemDeflection]':
        '''List[HypoidGearSetAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_6977.HypoidGearSetAdvancedSystemDeflection))
        return value
