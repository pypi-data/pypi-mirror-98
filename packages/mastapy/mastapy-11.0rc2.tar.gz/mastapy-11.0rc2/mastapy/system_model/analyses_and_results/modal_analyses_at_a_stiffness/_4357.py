﻿'''_4357.py

WormGearMeshModalAnalysisAtAStiffness
'''


from mastapy.system_model.connections_and_sockets.gears import _2008
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6623
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4292
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'WormGearMeshModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshModalAnalysisAtAStiffness',)


class WormGearMeshModalAnalysisAtAStiffness(_4292.GearMeshModalAnalysisAtAStiffness):
    '''WormGearMeshModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2008.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2008.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6623.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6623.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
