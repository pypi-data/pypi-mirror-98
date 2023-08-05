﻿'''_4720.py

SpiralBevelGearCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2217
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4592
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4637
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'SpiralBevelGearCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearCompoundModalAnalysisAtASpeed',)


class SpiralBevelGearCompoundModalAnalysisAtASpeed(_4637.BevelGearCompoundModalAnalysisAtASpeed):
    '''SpiralBevelGearCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2217.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2217.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4592.SpiralBevelGearModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4592.SpiralBevelGearModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4592.SpiralBevelGearModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4592.SpiralBevelGearModalAnalysisAtASpeed))
        return value
