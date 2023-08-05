'''_5388.py

FaceGearSetHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6521
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5386, _5387, _5393
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'FaceGearSetHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetHarmonicAnalysisOfSingleExcitation',)


class FaceGearSetHarmonicAnalysisOfSingleExcitation(_5393.GearSetHarmonicAnalysisOfSingleExcitation):
    '''FaceGearSetHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2203.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6521.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6521.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_harmonic_analysis_of_single_excitation(self) -> 'List[_5386.FaceGearHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearHarmonicAnalysisOfSingleExcitation]: 'FaceGearsHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsHarmonicAnalysisOfSingleExcitation, constructor.new(_5386.FaceGearHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def face_meshes_harmonic_analysis_of_single_excitation(self) -> 'List[_5387.FaceGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearMeshHarmonicAnalysisOfSingleExcitation]: 'FaceMeshesHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesHarmonicAnalysisOfSingleExcitation, constructor.new(_5387.FaceGearMeshHarmonicAnalysisOfSingleExcitation))
        return value
