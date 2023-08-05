﻿'''_6347.py

ConnectorCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6388
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'ConnectorCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundCriticalSpeedAnalysis',)


class ConnectorCompoundCriticalSpeedAnalysis(_6388.MountableComponentCompoundCriticalSpeedAnalysis):
    '''ConnectorCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
