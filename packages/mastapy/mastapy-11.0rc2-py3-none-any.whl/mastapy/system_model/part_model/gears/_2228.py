﻿'''_2228.py

ZerolBevelGearSet
'''


from typing import List

from mastapy.gears.gear_designs.zerol_bevel import _884
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2227, _2194
from mastapy.system_model.connections_and_sockets.gears import _2010
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSet',)


class ZerolBevelGearSet(_2194.BevelGearSet):
    '''ZerolBevelGearSet

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_gear_set_design(self) -> '_884.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_884.ZerolBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def zerol_bevel_gear_set_design(self) -> '_884.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ZerolBevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_884.ZerolBevelGearSetDesign)(self.wrapped.ZerolBevelGearSetDesign) if self.wrapped.ZerolBevelGearSetDesign else None

    @property
    def zerol_bevel_gears(self) -> 'List[_2227.ZerolBevelGear]':
        '''List[ZerolBevelGear]: 'ZerolBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGears, constructor.new(_2227.ZerolBevelGear))
        return value

    @property
    def zerol_bevel_meshes(self) -> 'List[_2010.ZerolBevelGearMesh]':
        '''List[ZerolBevelGearMesh]: 'ZerolBevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshes, constructor.new(_2010.ZerolBevelGearMesh))
        return value
