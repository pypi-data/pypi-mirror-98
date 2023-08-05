﻿'''_6080.py

ConnectionCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7177
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ConnectionCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundDynamicAnalysis',)


class ConnectionCompoundDynamicAnalysis(_7177.ConnectionCompoundAnalysis):
    '''ConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
