'''_4749.py

ZerolBevelGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4747, _4748, _4639
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4620
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'ZerolBevelGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundModalAnalysisAtASpeed',)


class ZerolBevelGearSetCompoundModalAnalysisAtASpeed(_4639.BevelGearSetCompoundModalAnalysisAtASpeed):
    '''ZerolBevelGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_4747.ZerolBevelGearCompoundModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearCompoundModalAnalysisAtASpeed]: 'ZerolBevelGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundModalAnalysisAtASpeed, constructor.new(_4747.ZerolBevelGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def zerol_bevel_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_4748.ZerolBevelGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearMeshCompoundModalAnalysisAtASpeed]: 'ZerolBevelMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundModalAnalysisAtASpeed, constructor.new(_4748.ZerolBevelGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4620.ZerolBevelGearSetModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearSetModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4620.ZerolBevelGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4620.ZerolBevelGearSetModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearSetModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4620.ZerolBevelGearSetModalAnalysisAtASpeed))
        return value
