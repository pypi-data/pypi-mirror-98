﻿'''_5644.py

CylindricalPlanetGearHarmonicAnalysis
'''


from mastapy.system_model.part_model.gears import _2201
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2415
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5641
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'CylindricalPlanetGearHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearHarmonicAnalysis',)


class CylindricalPlanetGearHarmonicAnalysis(_5641.CylindricalGearHarmonicAnalysis):
    '''CylindricalPlanetGearHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2201.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2201.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2415.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2415.CylindricalPlanetGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
