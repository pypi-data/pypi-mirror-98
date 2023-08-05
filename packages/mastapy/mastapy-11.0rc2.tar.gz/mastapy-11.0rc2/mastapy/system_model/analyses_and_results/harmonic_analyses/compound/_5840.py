﻿'''_5840.py

HypoidGearMeshCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1994
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5680
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5782
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'HypoidGearMeshCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshCompoundHarmonicAnalysis',)


class HypoidGearMeshCompoundHarmonicAnalysis(_5782.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis):
    '''HypoidGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1994.HypoidGearMesh':
        '''HypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1994.HypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1994.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1994.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5680.HypoidGearMeshHarmonicAnalysis]':
        '''List[HypoidGearMeshHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5680.HypoidGearMeshHarmonicAnalysis))
        return value

    @property
    def connection_harmonic_analysis_load_cases(self) -> 'List[_5680.HypoidGearMeshHarmonicAnalysis]':
        '''List[HypoidGearMeshHarmonicAnalysis]: 'ConnectionHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisLoadCases, constructor.new(_5680.HypoidGearMeshHarmonicAnalysis))
        return value
