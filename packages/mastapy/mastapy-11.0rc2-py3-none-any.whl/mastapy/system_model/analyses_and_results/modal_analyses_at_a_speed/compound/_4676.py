﻿'''_4676.py

FaceGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4674, _4675, _4681
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4547
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'FaceGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundModalAnalysisAtASpeed',)


class FaceGearSetCompoundModalAnalysisAtASpeed(_4681.GearSetCompoundModalAnalysisAtASpeed):
    '''FaceGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2203.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_4674.FaceGearCompoundModalAnalysisAtASpeed]':
        '''List[FaceGearCompoundModalAnalysisAtASpeed]: 'FaceGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundModalAnalysisAtASpeed, constructor.new(_4674.FaceGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def face_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_4675.FaceGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[FaceGearMeshCompoundModalAnalysisAtASpeed]: 'FaceMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundModalAnalysisAtASpeed, constructor.new(_4675.FaceGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4547.FaceGearSetModalAnalysisAtASpeed]':
        '''List[FaceGearSetModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4547.FaceGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4547.FaceGearSetModalAnalysisAtASpeed]':
        '''List[FaceGearSetModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4547.FaceGearSetModalAnalysisAtASpeed))
        return value
