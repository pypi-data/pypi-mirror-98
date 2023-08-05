﻿'''_6580.py

RingPinsLoadCase
'''


from mastapy.system_model.analyses_and_results.static_loads import _6451, _6561
from mastapy._internal import constructor
from mastapy.system_model.part_model.cycloidal import _2244
from mastapy._internal.python_net import python_net_import

_RING_PINS_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RingPinsLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsLoadCase',)


class RingPinsLoadCase(_6561.MountableComponentLoadCase):
    '''RingPinsLoadCase

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def all_ring_pins_manufacturing_error(self) -> '_6451.AllRingPinsManufacturingError':
        '''AllRingPinsManufacturingError: 'AllRingPinsManufacturingError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6451.AllRingPinsManufacturingError)(self.wrapped.AllRingPinsManufacturingError) if self.wrapped.AllRingPinsManufacturingError else None

    @property
    def component_design(self) -> '_2244.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
