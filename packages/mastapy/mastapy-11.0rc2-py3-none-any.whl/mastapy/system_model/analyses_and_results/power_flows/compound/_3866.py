'''_3866.py

CouplingConnectionCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3893
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CouplingConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundPowerFlow',)


class CouplingConnectionCompoundPowerFlow(_3893.InterMountableComponentConnectionCompoundPowerFlow):
    '''CouplingConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _COUPLING_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
