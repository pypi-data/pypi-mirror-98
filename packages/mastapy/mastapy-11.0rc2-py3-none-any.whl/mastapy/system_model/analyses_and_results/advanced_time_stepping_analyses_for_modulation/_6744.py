﻿'''_6744.py

RootAssemblyAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _2297, _6655
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'RootAssemblyAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyAdvancedTimeSteppingAnalysisForModulation',)


class RootAssemblyAdvancedTimeSteppingAnalysisForModulation(_6655.AssemblyAdvancedTimeSteppingAnalysisForModulation):
    '''RootAssemblyAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2150.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def advanced_time_stepping_analysis_for_modulation_inputs(self) -> '_2297.AdvancedTimeSteppingAnalysisForModulation':
        '''AdvancedTimeSteppingAnalysisForModulation: 'AdvancedTimeSteppingAnalysisForModulationInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2297.AdvancedTimeSteppingAnalysisForModulation)(self.wrapped.AdvancedTimeSteppingAnalysisForModulationInputs) if self.wrapped.AdvancedTimeSteppingAnalysisForModulationInputs else None
