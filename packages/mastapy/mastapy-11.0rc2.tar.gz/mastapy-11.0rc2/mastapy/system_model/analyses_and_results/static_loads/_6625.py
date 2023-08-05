'''_6625.py

ZerolBevelGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2227
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6462
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ZerolBevelGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearLoadCase',)


class ZerolBevelGearLoadCase(_6462.BevelGearLoadCase):
    '''ZerolBevelGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2227.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2227.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
