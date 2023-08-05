'''_3484.py

FaceGearStabilityAnalysis
'''


from mastapy.system_model.part_model.gears import _2202
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6519
from mastapy.system_model.analyses_and_results.stability_analyses import _3489
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'FaceGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearStabilityAnalysis',)


class FaceGearStabilityAnalysis(_3489.GearStabilityAnalysis):
    '''FaceGearStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2202.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2202.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6519.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6519.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
