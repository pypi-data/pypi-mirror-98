﻿'''_5500.py

CouplingCompoundHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5561
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'CouplingCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundHarmonicAnalysisOfSingleExcitation',)


class CouplingCompoundHarmonicAnalysisOfSingleExcitation(_5561.SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation):
    '''CouplingCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
