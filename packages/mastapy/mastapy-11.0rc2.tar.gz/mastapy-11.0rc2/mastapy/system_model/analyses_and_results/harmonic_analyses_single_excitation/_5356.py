'''_5356.py

ClutchHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2252
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6469
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5372
from mastapy._internal.python_net import python_net_import

_CLUTCH_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ClutchHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHarmonicAnalysisOfSingleExcitation',)


class ClutchHarmonicAnalysisOfSingleExcitation(_5372.CouplingHarmonicAnalysisOfSingleExcitation):
    '''ClutchHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2252.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6469.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6469.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
