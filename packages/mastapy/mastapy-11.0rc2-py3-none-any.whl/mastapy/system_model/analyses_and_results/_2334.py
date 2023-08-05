﻿'''_2334.py

CompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results import _2293
from mastapy._internal.python_net import python_net_import

_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundCriticalSpeedAnalysis',)


class CompoundCriticalSpeedAnalysis(_2293.CompoundAnalysis):
    '''CompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
