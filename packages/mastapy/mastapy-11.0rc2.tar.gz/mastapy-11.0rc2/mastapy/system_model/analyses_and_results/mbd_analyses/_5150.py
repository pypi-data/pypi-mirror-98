'''_5150.py

SpringDamperMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2274
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6596
from mastapy.system_model.analyses_and_results.mbd_analyses import _5074
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SpringDamperMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperMultibodyDynamicsAnalysis',)


class SpringDamperMultibodyDynamicsAnalysis(_5074.CouplingMultibodyDynamicsAnalysis):
    '''SpringDamperMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperMultibodyDynamicsAnalysis.TYPE'):
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
