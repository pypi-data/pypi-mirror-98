﻿'''_4943.py

CVTBeltConnectionCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4912
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CVTBeltConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionCompoundModalAnalysis',)


class CVTBeltConnectionCompoundModalAnalysis(_4912.BeltConnectionCompoundModalAnalysis):
    '''CVTBeltConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
