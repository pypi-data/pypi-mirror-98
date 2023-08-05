﻿'''_6130.py

PlanetCarrierCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2145
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6001
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6122
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'PlanetCarrierCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundDynamicAnalysis',)


class PlanetCarrierCompoundDynamicAnalysis(_6122.MountableComponentCompoundDynamicAnalysis):
    '''PlanetCarrierCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2145.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6001.PlanetCarrierDynamicAnalysis]':
        '''List[PlanetCarrierDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6001.PlanetCarrierDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_6001.PlanetCarrierDynamicAnalysis]':
        '''List[PlanetCarrierDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_6001.PlanetCarrierDynamicAnalysis))
        return value
