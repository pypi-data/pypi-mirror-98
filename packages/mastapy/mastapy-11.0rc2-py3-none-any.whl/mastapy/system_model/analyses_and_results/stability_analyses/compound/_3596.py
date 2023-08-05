﻿'''_3596.py

ConnectorCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3637
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ConnectorCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundStabilityAnalysis',)


class ConnectorCompoundStabilityAnalysis(_3637.MountableComponentCompoundStabilityAnalysis):
    '''ConnectorCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
