﻿'''_4078.py

SpringDamperHalfParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6595
from mastapy.system_model.analyses_and_results.system_deflections import _2476
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3995
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'SpringDamperHalfParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfParametricStudyTool',)


class SpringDamperHalfParametricStudyTool(_3995.CouplingHalfParametricStudyTool):
    '''SpringDamperHalfParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2275.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6595.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6595.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2476.SpringDamperHalfSystemDeflection]':
        '''List[SpringDamperHalfSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2476.SpringDamperHalfSystemDeflection))
        return value
