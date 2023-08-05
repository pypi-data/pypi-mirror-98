﻿'''_4523.py

ConceptGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6477
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4522, _4521, _4552
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ConceptGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetModalAnalysisAtASpeed',)


class ConceptGearSetModalAnalysisAtASpeed(_4552.GearSetModalAnalysisAtASpeed):
    '''ConceptGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2196.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6477.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6477.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_modal_analysis_at_a_speed(self) -> 'List[_4522.ConceptGearModalAnalysisAtASpeed]':
        '''List[ConceptGearModalAnalysisAtASpeed]: 'ConceptGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsModalAnalysisAtASpeed, constructor.new(_4522.ConceptGearModalAnalysisAtASpeed))
        return value

    @property
    def concept_meshes_modal_analysis_at_a_speed(self) -> 'List[_4521.ConceptGearMeshModalAnalysisAtASpeed]':
        '''List[ConceptGearMeshModalAnalysisAtASpeed]: 'ConceptMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesModalAnalysisAtASpeed, constructor.new(_4521.ConceptGearMeshModalAnalysisAtASpeed))
        return value
