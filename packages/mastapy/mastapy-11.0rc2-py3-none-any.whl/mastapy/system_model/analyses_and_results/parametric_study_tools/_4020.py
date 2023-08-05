﻿'''_4020.py

FEPartParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2129
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6522
from mastapy.system_model.analyses_and_results.system_deflections import _2422
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3958
from mastapy._internal.python_net import python_net_import

_FE_PART_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'FEPartParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartParametricStudyTool',)


class FEPartParametricStudyTool(_3958.AbstractShaftOrHousingParametricStudyTool):
    '''FEPartParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _FE_PART_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2129.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2129.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6522.FEPartLoadCase':
        '''FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6522.FEPartLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[FEPartParametricStudyTool]':
        '''List[FEPartParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartParametricStudyTool))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2422.FEPartSystemDeflection]':
        '''List[FEPartSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2422.FEPartSystemDeflection))
        return value
