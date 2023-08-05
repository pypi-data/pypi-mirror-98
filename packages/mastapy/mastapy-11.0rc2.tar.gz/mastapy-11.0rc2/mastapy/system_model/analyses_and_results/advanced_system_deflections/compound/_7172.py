﻿'''_7172.py

ZerolBevelGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7170, _7171, _7062
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7043
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ZerolBevelGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundAdvancedSystemDeflection',)


class ZerolBevelGearSetCompoundAdvancedSystemDeflection(_7062.BevelGearSetCompoundAdvancedSystemDeflection):
    '''ZerolBevelGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_advanced_system_deflection(self) -> 'List[_7170.ZerolBevelGearCompoundAdvancedSystemDeflection]':
        '''List[ZerolBevelGearCompoundAdvancedSystemDeflection]: 'ZerolBevelGearsCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundAdvancedSystemDeflection, constructor.new(_7170.ZerolBevelGearCompoundAdvancedSystemDeflection))
        return value

    @property
    def zerol_bevel_meshes_compound_advanced_system_deflection(self) -> 'List[_7171.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]':
        '''List[ZerolBevelGearMeshCompoundAdvancedSystemDeflection]: 'ZerolBevelMeshesCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundAdvancedSystemDeflection, constructor.new(_7171.ZerolBevelGearMeshCompoundAdvancedSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_7043.ZerolBevelGearSetAdvancedSystemDeflection]':
        '''List[ZerolBevelGearSetAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_7043.ZerolBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_7043.ZerolBevelGearSetAdvancedSystemDeflection]':
        '''List[ZerolBevelGearSetAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_7043.ZerolBevelGearSetAdvancedSystemDeflection))
        return value
