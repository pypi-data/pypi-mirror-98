﻿'''_1939.py

SystemDeflectionViewable
'''


from mastapy.system_model.drawing import _1921
from mastapy._internal.python_net import python_net_import

_SYSTEM_DEFLECTION_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'SystemDeflectionViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemDeflectionViewable',)


class SystemDeflectionViewable(_1921.AbstractSystemDeflectionViewable):
    '''SystemDeflectionViewable

    This is a mastapy class.
    '''

    TYPE = _SYSTEM_DEFLECTION_VIEWABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SystemDeflectionViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
