﻿'''_6491.py

CycloidalAssemblyLoadCase
'''


from mastapy.system_model.part_model.cycloidal import _2242
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6589
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CycloidalAssemblyLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyLoadCase',)


class CycloidalAssemblyLoadCase(_6589.SpecialisedAssemblyLoadCase):
    '''CycloidalAssemblyLoadCase

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2242.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2242.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
