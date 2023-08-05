﻿'''_3438.py

BeltDriveStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2250, _2260
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6456, _6489
from mastapy.system_model.analyses_and_results.stability_analyses import _3527
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'BeltDriveStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveStabilityAnalysis',)


class BeltDriveStabilityAnalysis(_3527.SpecialisedAssemblyStabilityAnalysis):
    '''BeltDriveStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2250.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.BeltDrive.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BeltDrive. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6456.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6456.BeltDriveLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to BeltDriveLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
