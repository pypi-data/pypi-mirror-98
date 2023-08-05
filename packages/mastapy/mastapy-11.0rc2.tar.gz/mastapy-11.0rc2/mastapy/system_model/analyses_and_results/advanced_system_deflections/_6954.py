﻿'''_6954.py

CVTPulleyAdvancedSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2261
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7002
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CVTPulleyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyAdvancedSystemDeflection',)


class CVTPulleyAdvancedSystemDeflection(_7002.PulleyAdvancedSystemDeflection):
    '''CVTPulleyAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2261.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2261.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
