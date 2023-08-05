﻿'''_2555.py

CouplingHalfCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2594
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CouplingHalfCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundSystemDeflection',)


class CouplingHalfCompoundSystemDeflection(_2594.MountableComponentCompoundSystemDeflection):
    '''CouplingHalfCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
