﻿'''_4944.py

CVTCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4913
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CVTCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundModalAnalysis',)


class CVTCompoundModalAnalysis(_4913.BeltDriveCompoundModalAnalysis):
    '''CVTCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
