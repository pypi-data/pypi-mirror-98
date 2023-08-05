﻿'''_4395.py

ConicalGearCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4421
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ConicalGearCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearCompoundModalAnalysisAtAStiffness',)


class ConicalGearCompoundModalAnalysisAtAStiffness(_4421.GearCompoundModalAnalysisAtAStiffness):
    '''ConicalGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetaries(self) -> 'List[ConicalGearCompoundModalAnalysisAtAStiffness]':
        '''List[ConicalGearCompoundModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearCompoundModalAnalysisAtAStiffness))
        return value
