﻿'''_6627.py

ZerolBevelGearSetLoadCase
'''


from typing import List

from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6625, _6626, _6464
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ZerolBevelGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetLoadCase',)


class ZerolBevelGearSetLoadCase(_6464.BevelGearSetLoadCase):
    '''ZerolBevelGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2228.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def gears(self) -> 'List[_6625.ZerolBevelGearLoadCase]':
        '''List[ZerolBevelGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_6625.ZerolBevelGearLoadCase))
        return value

    @property
    def zerol_bevel_gears_load_case(self) -> 'List[_6625.ZerolBevelGearLoadCase]':
        '''List[ZerolBevelGearLoadCase]: 'ZerolBevelGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsLoadCase, constructor.new(_6625.ZerolBevelGearLoadCase))
        return value

    @property
    def zerol_bevel_meshes_load_case(self) -> 'List[_6626.ZerolBevelGearMeshLoadCase]':
        '''List[ZerolBevelGearMeshLoadCase]: 'ZerolBevelMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesLoadCase, constructor.new(_6626.ZerolBevelGearMeshLoadCase))
        return value
