﻿'''_4778.py

ConceptCouplingModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2255
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6474
from mastapy.system_model.analyses_and_results.system_deflections import _2386
from mastapy.system_model.analyses_and_results.modal_analyses import _4790
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ConceptCouplingModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingModalAnalysis',)


class ConceptCouplingModalAnalysis(_4790.CouplingModalAnalysis):
    '''ConceptCouplingModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2255.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2255.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6474.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6474.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2386.ConceptCouplingSystemDeflection':
        '''ConceptCouplingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2386.ConceptCouplingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
