﻿'''_5731.py

StraightBevelPlanetGearHarmonicAnalysis
'''


from mastapy.system_model.part_model.gears import _2223
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2484
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5725
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'StraightBevelPlanetGearHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearHarmonicAnalysis',)


class StraightBevelPlanetGearHarmonicAnalysis(_5725.StraightBevelDiffGearHarmonicAnalysis):
    '''StraightBevelPlanetGearHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2223.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2484.StraightBevelPlanetGearSystemDeflection':
        '''StraightBevelPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2484.StraightBevelPlanetGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
