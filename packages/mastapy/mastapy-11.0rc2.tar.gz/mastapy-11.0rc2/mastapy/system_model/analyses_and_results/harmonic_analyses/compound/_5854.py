﻿'''_5854.py

MountableComponentCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5802
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'MountableComponentCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundHarmonicAnalysis',)


class MountableComponentCompoundHarmonicAnalysis(_5802.ComponentCompoundHarmonicAnalysis):
    '''MountableComponentCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
