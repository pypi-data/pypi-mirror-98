﻿'''_3533.py

SpringDamperStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2274
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6596
from mastapy.system_model.analyses_and_results.stability_analyses import _3467
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'SpringDamperStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperStabilityAnalysis',)


class SpringDamperStabilityAnalysis(_3467.CouplingStabilityAnalysis):
    '''SpringDamperStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2274.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2274.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6596.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6596.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
