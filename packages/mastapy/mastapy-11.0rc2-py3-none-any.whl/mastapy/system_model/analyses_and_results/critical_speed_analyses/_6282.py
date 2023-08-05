﻿'''_6282.py

SpiralBevelGearMeshCriticalSpeedAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _2002
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6592
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6197
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'SpiralBevelGearMeshCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshCriticalSpeedAnalysis',)


class SpiralBevelGearMeshCriticalSpeedAnalysis(_6197.BevelGearMeshCriticalSpeedAnalysis):
    '''SpiralBevelGearMeshCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2002.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2002.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6592.SpiralBevelGearMeshLoadCase':
        '''SpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6592.SpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
