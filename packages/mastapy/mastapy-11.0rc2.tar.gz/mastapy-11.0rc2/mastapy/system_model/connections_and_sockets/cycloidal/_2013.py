'''_2013.py

CycloidalDiscAxialRightSocket
'''


from mastapy.system_model.connections_and_sockets import _1965
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_AXIAL_RIGHT_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscAxialRightSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscAxialRightSocket',)


class CycloidalDiscAxialRightSocket(_1965.OuterShaftSocketBase):
    '''CycloidalDiscAxialRightSocket

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_AXIAL_RIGHT_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscAxialRightSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
