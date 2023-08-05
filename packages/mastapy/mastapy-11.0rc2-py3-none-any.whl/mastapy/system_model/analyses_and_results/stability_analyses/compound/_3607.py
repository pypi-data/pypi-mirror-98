﻿'''_3607.py

CylindricalGearCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2199, _2201
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _3478
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3618
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CylindricalGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundStabilityAnalysis',)


class CylindricalGearCompoundStabilityAnalysis(_3618.GearCompoundStabilityAnalysis):
    '''CylindricalGearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2199.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2199.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3478.CylindricalGearStabilityAnalysis]':
        '''List[CylindricalGearStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3478.CylindricalGearStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3478.CylindricalGearStabilityAnalysis]':
        '''List[CylindricalGearStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3478.CylindricalGearStabilityAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearCompoundStabilityAnalysis]':
        '''List[CylindricalGearCompoundStabilityAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearCompoundStabilityAnalysis))
        return value
