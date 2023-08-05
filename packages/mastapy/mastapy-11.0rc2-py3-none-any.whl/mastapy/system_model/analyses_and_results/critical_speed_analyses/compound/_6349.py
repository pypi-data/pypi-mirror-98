﻿'''_6349.py

CouplingConnectionCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6376
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CouplingConnectionCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundCriticalSpeedAnalysis',)


class CouplingConnectionCompoundCriticalSpeedAnalysis(_6376.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis):
    '''CouplingConnectionCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
