﻿'''_5660.py

FaceGearMeshHarmonicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1990
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6520
from mastapy.system_model.analyses_and_results.system_deflections import _2419
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5667
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'FaceGearMeshHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshHarmonicAnalysis',)


class FaceGearMeshHarmonicAnalysis(_5667.GearMeshHarmonicAnalysis):
    '''FaceGearMeshHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1990.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6520.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6520.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2419.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2419.FaceGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
