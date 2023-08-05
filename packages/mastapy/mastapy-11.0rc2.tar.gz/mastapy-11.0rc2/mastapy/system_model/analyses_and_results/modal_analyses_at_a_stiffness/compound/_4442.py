﻿'''_4442.py

PartCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7184
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'PartCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundModalAnalysisAtAStiffness',)


class PartCompoundModalAnalysisAtAStiffness(_7184.PartCompoundAnalysis):
    '''PartCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
