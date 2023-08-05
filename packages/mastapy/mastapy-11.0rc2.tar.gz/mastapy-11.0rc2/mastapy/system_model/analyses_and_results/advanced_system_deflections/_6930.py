﻿'''_6930.py

BoltAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2119
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6466
from mastapy.system_model.analyses_and_results.system_deflections import _2377
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6936
from mastapy._internal.python_net import python_net_import

_BOLT_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'BoltAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltAdvancedSystemDeflection',)


class BoltAdvancedSystemDeflection(_6936.ComponentAdvancedSystemDeflection):
    '''BoltAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLT_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2119.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2119.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6466.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6466.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2377.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2377.BoltSystemDeflection))
        return value
