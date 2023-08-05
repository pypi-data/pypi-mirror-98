'''_3594.py

ConicalGearSetCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3620
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ConicalGearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearSetCompoundStabilityAnalysis',)


class ConicalGearSetCompoundStabilityAnalysis(_3620.GearSetCompoundStabilityAnalysis):
    '''ConicalGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearSetCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
