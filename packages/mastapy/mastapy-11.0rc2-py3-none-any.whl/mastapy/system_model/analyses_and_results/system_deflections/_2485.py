﻿'''_2485.py

StraightBevelSunGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2224
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3810
from mastapy.system_model.analyses_and_results.system_deflections import _2480
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'StraightBevelSunGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearSystemDeflection',)


class StraightBevelSunGearSystemDeflection(_2480.StraightBevelDiffGearSystemDeflection):
    '''StraightBevelSunGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2224.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2224.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def power_flow_results(self) -> '_3810.StraightBevelSunGearPowerFlow':
        '''StraightBevelSunGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3810.StraightBevelSunGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
