﻿'''_6477.py

ConceptGearSetLoadCase
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6475, _6476, _6530
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetLoadCase',)


class ConceptGearSetLoadCase(_6530.GearSetLoadCase):
    '''ConceptGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetLoadCase.TYPE'):
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
    def gears(self) -> 'List[_6475.ConceptGearLoadCase]':
        '''List[ConceptGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_6475.ConceptGearLoadCase))
        return value

    @property
    def concept_gears_load_case(self) -> 'List[_6475.ConceptGearLoadCase]':
        '''List[ConceptGearLoadCase]: 'ConceptGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsLoadCase, constructor.new(_6475.ConceptGearLoadCase))
        return value

    @property
    def concept_meshes_load_case(self) -> 'List[_6476.ConceptGearMeshLoadCase]':
        '''List[ConceptGearMeshLoadCase]: 'ConceptMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesLoadCase, constructor.new(_6476.ConceptGearMeshLoadCase))
        return value
