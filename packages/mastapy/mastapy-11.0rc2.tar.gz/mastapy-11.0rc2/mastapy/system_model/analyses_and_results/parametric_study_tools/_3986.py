﻿'''_3986.py

ConceptGearMeshParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6476
from mastapy.system_model.analyses_and_results.system_deflections import _2387
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4022
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ConceptGearMeshParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshParametricStudyTool',)


class ConceptGearMeshParametricStudyTool(_4022.GearMeshParametricStudyTool):
    '''ConceptGearMeshParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1984.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6476.ConceptGearMeshLoadCase':
        '''ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6476.ConceptGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2387.ConceptGearMeshSystemDeflection]':
        '''List[ConceptGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2387.ConceptGearMeshSystemDeflection))
        return value
