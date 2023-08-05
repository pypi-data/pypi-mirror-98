'''_5301.py

TorqueConverterCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2281
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5165
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5221
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'TorqueConverterCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundMultibodyDynamicsAnalysis',)


class TorqueConverterCompoundMultibodyDynamicsAnalysis(_5221.CouplingCompoundMultibodyDynamicsAnalysis):
    '''TorqueConverterCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2281.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2281.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5165.TorqueConverterMultibodyDynamicsAnalysis]':
        '''List[TorqueConverterMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5165.TorqueConverterMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_multibody_dynamics_analysis_load_cases(self) -> 'List[_5165.TorqueConverterMultibodyDynamicsAnalysis]':
        '''List[TorqueConverterMultibodyDynamicsAnalysis]: 'AssemblyMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultibodyDynamicsAnalysisLoadCases, constructor.new(_5165.TorqueConverterMultibodyDynamicsAnalysis))
        return value
