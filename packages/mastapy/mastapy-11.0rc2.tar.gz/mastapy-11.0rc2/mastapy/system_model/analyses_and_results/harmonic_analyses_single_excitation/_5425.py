'''_5425.py

RollingRingAssemblyHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2271
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6582
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5432
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'RollingRingAssemblyHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyHarmonicAnalysisOfSingleExcitation',)


class RollingRingAssemblyHarmonicAnalysisOfSingleExcitation(_5432.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation):
    '''RollingRingAssemblyHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2271.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2271.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6582.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6582.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
