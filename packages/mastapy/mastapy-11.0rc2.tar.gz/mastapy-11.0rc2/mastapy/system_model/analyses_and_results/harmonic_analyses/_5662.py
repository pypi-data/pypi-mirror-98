'''_5662.py

FEPartHarmonicAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4807
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5675, _5595
from mastapy.system_model.part_model import _2129
from mastapy.system_model.analyses_and_results.static_loads import _6522
from mastapy.system_model.analyses_and_results.system_deflections import _2422
from mastapy._internal.python_net import python_net_import

_FE_PART_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'FEPartHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartHarmonicAnalysis',)


class FEPartHarmonicAnalysis(_5595.AbstractShaftOrHousingHarmonicAnalysis):
    '''FEPartHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def export_displacements(self) -> 'str':
        '''str: 'ExportDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportDisplacements

    @property
    def export_velocities(self) -> 'str':
        '''str: 'ExportVelocities' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportVelocities

    @property
    def export_accelerations(self) -> 'str':
        '''str: 'ExportAccelerations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportAccelerations

    @property
    def export_forces(self) -> 'str':
        '''str: 'ExportForces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportForces

    @property
    def coupled_modal_analysis(self) -> '_4807.FEPartModalAnalysis':
        '''FEPartModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4807.FEPartModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def export(self) -> '_5675.HarmonicAnalysisFEExportOptions':
        '''HarmonicAnalysisFEExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5675.HarmonicAnalysisFEExportOptions)(self.wrapped.Export) if self.wrapped.Export else None

    @property
    def component_design(self) -> '_2129.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2129.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6522.FEPartLoadCase':
        '''FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6522.FEPartLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2422.FEPartSystemDeflection':
        '''FEPartSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2422.FEPartSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[FEPartHarmonicAnalysis]':
        '''List[FEPartHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartHarmonicAnalysis))
        return value
