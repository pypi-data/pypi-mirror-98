﻿'''_4620.py

ZerolBevelGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6627
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4619, _4618, _4510
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ZerolBevelGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetModalAnalysisAtASpeed',)


class ZerolBevelGearSetModalAnalysisAtASpeed(_4510.BevelGearSetModalAnalysisAtASpeed):
    '''ZerolBevelGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6627.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6627.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_modal_analysis_at_a_speed(self) -> 'List[_4619.ZerolBevelGearModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearModalAnalysisAtASpeed]: 'ZerolBevelGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsModalAnalysisAtASpeed, constructor.new(_4619.ZerolBevelGearModalAnalysisAtASpeed))
        return value

    @property
    def zerol_bevel_meshes_modal_analysis_at_a_speed(self) -> 'List[_4618.ZerolBevelGearMeshModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearMeshModalAnalysisAtASpeed]: 'ZerolBevelMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesModalAnalysisAtASpeed, constructor.new(_4618.ZerolBevelGearMeshModalAnalysisAtASpeed))
        return value
