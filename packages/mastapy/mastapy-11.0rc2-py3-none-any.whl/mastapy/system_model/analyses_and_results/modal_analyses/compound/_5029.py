﻿'''_5029.py

ZerolBevelGearCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2227
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4889
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4919
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ZerolBevelGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearCompoundModalAnalysis',)


class ZerolBevelGearCompoundModalAnalysis(_4919.BevelGearCompoundModalAnalysis):
    '''ZerolBevelGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2227.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2227.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4889.ZerolBevelGearModalAnalysis]':
        '''List[ZerolBevelGearModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4889.ZerolBevelGearModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4889.ZerolBevelGearModalAnalysis]':
        '''List[ZerolBevelGearModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4889.ZerolBevelGearModalAnalysis))
        return value
