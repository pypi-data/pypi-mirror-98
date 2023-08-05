﻿'''_5140.py

ShaftHubConnectionMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2272
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6586
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5180, _5182
from mastapy.system_model.analyses_and_results.mbd_analyses import _5071
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ShaftHubConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionMultibodyDynamicsAnalysis',)


class ShaftHubConnectionMultibodyDynamicsAnalysis(_5071.ConnectorMultibodyDynamicsAnalysis):
    '''ShaftHubConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2272.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2272.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6586.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6586.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def peak_dynamic_force(self) -> '_5180.DynamicForceVector3DResult':
        '''DynamicForceVector3DResult: 'PeakDynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5180.DynamicForceVector3DResult)(self.wrapped.PeakDynamicForce) if self.wrapped.PeakDynamicForce else None

    @property
    def peak_dynamic_force_angular(self) -> '_5182.DynamicTorqueVector3DResult':
        '''DynamicTorqueVector3DResult: 'PeakDynamicForceAngular' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5182.DynamicTorqueVector3DResult)(self.wrapped.PeakDynamicForceAngular) if self.wrapped.PeakDynamicForceAngular else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionMultibodyDynamicsAnalysis]':
        '''List[ShaftHubConnectionMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionMultibodyDynamicsAnalysis))
        return value
