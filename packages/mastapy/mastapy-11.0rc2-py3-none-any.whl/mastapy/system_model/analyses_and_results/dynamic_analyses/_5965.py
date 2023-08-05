﻿'''_5965.py

CylindricalPlanetGearDynamicAnalysis
'''


from mastapy.system_model.part_model.gears import _2201
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5962
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'CylindricalPlanetGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearDynamicAnalysis',)


class CylindricalPlanetGearDynamicAnalysis(_5962.CylindricalGearDynamicAnalysis):
    '''CylindricalPlanetGearDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2201.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2201.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
