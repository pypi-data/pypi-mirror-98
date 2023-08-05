﻿'''_6353.py

CVTPulleyCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6399
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CVTPulleyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundCriticalSpeedAnalysis',)


class CVTPulleyCompoundCriticalSpeedAnalysis(_6399.PulleyCompoundCriticalSpeedAnalysis):
    '''CVTPulleyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
