'''_5241.py

FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5092
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5282
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis',)


class FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis(_5282.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis):
    '''FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2130.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.FlexiblePinAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2130.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5092.FlexiblePinAssemblyMultibodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5092.FlexiblePinAssemblyMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_multibody_dynamics_analysis_load_cases(self) -> 'List[_5092.FlexiblePinAssemblyMultibodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyMultibodyDynamicsAnalysis]: 'AssemblyMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultibodyDynamicsAnalysisLoadCases, constructor.new(_5092.FlexiblePinAssemblyMultibodyDynamicsAnalysis))
        return value
