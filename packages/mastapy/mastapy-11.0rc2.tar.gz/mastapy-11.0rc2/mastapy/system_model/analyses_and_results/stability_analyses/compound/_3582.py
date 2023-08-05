﻿'''_3582.py

ClutchConnectionCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2021
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3449
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3598
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ClutchConnectionCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundStabilityAnalysis',)


class ClutchConnectionCompoundStabilityAnalysis(_3598.CouplingConnectionCompoundStabilityAnalysis):
    '''ClutchConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2021.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2021.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2021.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2021.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3449.ClutchConnectionStabilityAnalysis]':
        '''List[ClutchConnectionStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3449.ClutchConnectionStabilityAnalysis))
        return value

    @property
    def connection_stability_analysis_load_cases(self) -> 'List[_3449.ClutchConnectionStabilityAnalysis]':
        '''List[ClutchConnectionStabilityAnalysis]: 'ConnectionStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionStabilityAnalysisLoadCases, constructor.new(_3449.ClutchConnectionStabilityAnalysis))
        return value
