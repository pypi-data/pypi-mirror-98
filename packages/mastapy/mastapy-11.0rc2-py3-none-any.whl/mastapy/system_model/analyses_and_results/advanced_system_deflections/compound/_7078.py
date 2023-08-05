﻿'''_7078.py

ConicalGearSetCompoundAdvancedSystemDeflection
'''


from mastapy.gears.rating.conical import _489
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7104
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ConicalGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearSetCompoundAdvancedSystemDeflection',)


class ConicalGearSetCompoundAdvancedSystemDeflection(_7104.GearSetCompoundAdvancedSystemDeflection):
    '''ConicalGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_rating(self) -> '_489.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_489.ConicalGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def conical_gear_duty_cycle_rating(self) -> '_489.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'ConicalGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_489.ConicalGearSetDutyCycleRating)(self.wrapped.ConicalGearDutyCycleRating) if self.wrapped.ConicalGearDutyCycleRating else None
