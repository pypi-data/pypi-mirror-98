﻿'''_4227.py

WormGearCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2225
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4099
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4162
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'WormGearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundParametricStudyTool',)


class WormGearCompoundParametricStudyTool(_4162.GearCompoundParametricStudyTool):
    '''WormGearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2225.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4099.WormGearParametricStudyTool]':
        '''List[WormGearParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4099.WormGearParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_4099.WormGearParametricStudyTool]':
        '''List[WormGearParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_4099.WormGearParametricStudyTool))
        return value
