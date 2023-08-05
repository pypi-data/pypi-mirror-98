﻿'''_4938.py

ConnectionCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7177
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundModalAnalysis',)


class ConnectionCompoundModalAnalysis(_7177.ConnectionCompoundAnalysis):
    '''ConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
