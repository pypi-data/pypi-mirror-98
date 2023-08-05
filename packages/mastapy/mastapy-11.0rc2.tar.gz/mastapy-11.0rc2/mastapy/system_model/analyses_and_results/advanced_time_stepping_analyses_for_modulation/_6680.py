﻿'''_6680.py

ConceptGearSetAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6477
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6678, _6679, _6709
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'ConceptGearSetAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetAdvancedTimeSteppingAnalysisForModulation',)


class ConceptGearSetAdvancedTimeSteppingAnalysisForModulation(_6709.GearSetAdvancedTimeSteppingAnalysisForModulation):
    '''ConceptGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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
    def concept_gears_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6678.ConceptGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearsAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6678.ConceptGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_meshes_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6679.ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'ConceptMeshesAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6679.ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
