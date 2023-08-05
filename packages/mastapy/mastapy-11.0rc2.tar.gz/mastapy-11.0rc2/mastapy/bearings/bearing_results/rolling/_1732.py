﻿'''_1732.py

LoadedSelfAligningBallBearingRow
'''


from mastapy.bearings.bearing_results.rolling import _1731, _1698
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_SELF_ALIGNING_BALL_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedSelfAligningBallBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedSelfAligningBallBearingRow',)


class LoadedSelfAligningBallBearingRow(_1698.LoadedBallBearingRow):
    '''LoadedSelfAligningBallBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_SELF_ALIGNING_BALL_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedSelfAligningBallBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1731.LoadedSelfAligningBallBearingResults':
        '''LoadedSelfAligningBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1731.LoadedSelfAligningBallBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
