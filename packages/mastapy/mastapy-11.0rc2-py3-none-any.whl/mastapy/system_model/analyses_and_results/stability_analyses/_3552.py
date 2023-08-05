﻿'''_3552.py

UnbalancedMassStabilityAnalysis
'''


from mastapy.system_model.part_model import _2153
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6620
from mastapy.system_model.analyses_and_results.stability_analyses import _3553
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'UnbalancedMassStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassStabilityAnalysis',)


class UnbalancedMassStabilityAnalysis(_3553.VirtualComponentStabilityAnalysis):
    '''UnbalancedMassStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2153.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2153.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6620.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6620.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
