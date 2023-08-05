﻿'''_4833.py

OilSealModalAnalysis
'''


from mastapy.system_model.part_model import _2142
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6563
from mastapy.system_model.analyses_and_results.system_deflections import _2449
from mastapy.system_model.analyses_and_results.modal_analyses import _4786
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'OilSealModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealModalAnalysis',)


class OilSealModalAnalysis(_4786.ConnectorModalAnalysis):
    '''OilSealModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2142.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6563.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6563.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2449.OilSealSystemDeflection':
        '''OilSealSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2449.OilSealSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
