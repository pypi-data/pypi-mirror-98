﻿'''_3469.py

CVTBeltConnectionStabilityAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1952
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3437
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'CVTBeltConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionStabilityAnalysis',)


class CVTBeltConnectionStabilityAnalysis(_3437.BeltConnectionStabilityAnalysis):
    '''CVTBeltConnectionStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1952.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1952.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
