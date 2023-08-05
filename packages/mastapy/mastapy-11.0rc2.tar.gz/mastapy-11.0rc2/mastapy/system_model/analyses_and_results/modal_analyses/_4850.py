﻿'''_4850.py

RootAssemblyModalAnalysis
'''


from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _2308, _4757
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _2311
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.system_deflections import _2465
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'RootAssemblyModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyModalAnalysis',)


class RootAssemblyModalAnalysis(_4757.AssemblyModalAnalysis):
    '''RootAssemblyModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2150.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def modal_analysis_inputs(self) -> '_2308.ModalAnalysis':
        '''ModalAnalysis: 'ModalAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2308.ModalAnalysis.TYPE not in self.wrapped.ModalAnalysisInputs.__class__.__mro__:
            raise CastException('Failed to cast modal_analysis_inputs to ModalAnalysis. Expected: {}.'.format(self.wrapped.ModalAnalysisInputs.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ModalAnalysisInputs.__class__)(self.wrapped.ModalAnalysisInputs) if self.wrapped.ModalAnalysisInputs else None

    @property
    def system_deflection_results(self) -> '_2465.RootAssemblySystemDeflection':
        '''RootAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2465.RootAssemblySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
