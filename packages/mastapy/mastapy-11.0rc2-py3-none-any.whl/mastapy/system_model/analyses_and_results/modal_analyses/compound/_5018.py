﻿'''_5018.py

SynchroniserPartCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4942
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_PART_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SynchroniserPartCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserPartCompoundModalAnalysis',)


class SynchroniserPartCompoundModalAnalysis(_4942.CouplingHalfCompoundModalAnalysis):
    '''SynchroniserPartCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_PART_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserPartCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
