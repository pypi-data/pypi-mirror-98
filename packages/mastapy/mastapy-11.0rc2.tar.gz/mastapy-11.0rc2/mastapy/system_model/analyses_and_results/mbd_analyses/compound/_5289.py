﻿'''_5289.py

StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2219, _2223, _2224
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.mbd_analyses import _5152
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5200
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis',)


class StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis(_5200.BevelGearCompoundMultibodyDynamicsAnalysis):
    '''StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2219.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2219.StraightBevelDiffGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5152.StraightBevelDiffGearMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5152.StraightBevelDiffGearMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5152.StraightBevelDiffGearMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5152.StraightBevelDiffGearMultibodyDynamicsAnalysis))
        return value
