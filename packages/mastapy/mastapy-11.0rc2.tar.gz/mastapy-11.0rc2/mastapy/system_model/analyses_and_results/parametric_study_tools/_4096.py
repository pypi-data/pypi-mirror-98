'''_4096.py

UnbalancedMassParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2153
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6620
from mastapy.system_model.analyses_and_results.system_deflections import _2499
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4097
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'UnbalancedMassParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassParametricStudyTool',)


class UnbalancedMassParametricStudyTool(_4097.VirtualComponentParametricStudyTool):
    '''UnbalancedMassParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2153.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2153.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6620.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6620.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2499.UnbalancedMassSystemDeflection]':
        '''List[UnbalancedMassSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2499.UnbalancedMassSystemDeflection))
        return value
