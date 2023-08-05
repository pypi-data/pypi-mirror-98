﻿'''_6948.py

ContactChartPerToothPass
'''


from mastapy.scripting import _7200
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONTACT_CHART_PER_TOOTH_PASS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ContactChartPerToothPass')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactChartPerToothPass',)


class ContactChartPerToothPass(_0.APIBase):
    '''ContactChartPerToothPass

    This is a mastapy class.
    '''

    TYPE = _CONTACT_CHART_PER_TOOTH_PASS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ContactChartPerToothPass.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def max_pressure(self) -> '_7200.SMTBitmap':
        '''SMTBitmap: 'MaxPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7200.SMTBitmap)(self.wrapped.MaxPressure) if self.wrapped.MaxPressure else None

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
