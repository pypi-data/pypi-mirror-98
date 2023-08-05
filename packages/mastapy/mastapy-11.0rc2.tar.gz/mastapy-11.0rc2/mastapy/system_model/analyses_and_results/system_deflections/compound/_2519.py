'''_2519.py

AbstractShaftToMountableComponentConnectionCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2551
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'AbstractShaftToMountableComponentConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnectionCompoundSystemDeflection',)


class AbstractShaftToMountableComponentConnectionCompoundSystemDeflection(_2551.ConnectionCompoundSystemDeflection):
    '''AbstractShaftToMountableComponentConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
