'''_3877.py

CylindricalGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.gears.rating.cylindrical import _422
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2200, _2216
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.power_flows.compound import _3875, _3876, _3888
from mastapy.system_model.analyses_and_results.power_flows import _3745
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CylindricalGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundPowerFlow',)


class CylindricalGearSetCompoundPowerFlow(_3888.GearSetCompoundPowerFlow):
    '''CylindricalGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_duty_cycle_rating(self) -> '_422.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_422.CylindricalGearSetDutyCycleRating)(self.wrapped.GearSetDutyCycleRating) if self.wrapped.GearSetDutyCycleRating else None

    @property
    def cylindrical_gear_set_duty_cycle_rating(self) -> '_422.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'CylindricalGearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_422.CylindricalGearSetDutyCycleRating)(self.wrapped.CylindricalGearSetDutyCycleRating) if self.wrapped.CylindricalGearSetDutyCycleRating else None

    @property
    def component_design(self) -> '_2200.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2200.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def ratings_for_all_designs(self) -> 'List[_422.CylindricalGearSetDutyCycleRating]':
        '''List[CylindricalGearSetDutyCycleRating]: 'RatingsForAllDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RatingsForAllDesigns, constructor.new(_422.CylindricalGearSetDutyCycleRating))
        return value

    @property
    def cylindrical_gears_compound_power_flow(self) -> 'List[_3875.CylindricalGearCompoundPowerFlow]':
        '''List[CylindricalGearCompoundPowerFlow]: 'CylindricalGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundPowerFlow, constructor.new(_3875.CylindricalGearCompoundPowerFlow))
        return value

    @property
    def cylindrical_meshes_compound_power_flow(self) -> 'List[_3876.CylindricalGearMeshCompoundPowerFlow]':
        '''List[CylindricalGearMeshCompoundPowerFlow]: 'CylindricalMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundPowerFlow, constructor.new(_3876.CylindricalGearMeshCompoundPowerFlow))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3745.CylindricalGearSetPowerFlow]':
        '''List[CylindricalGearSetPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3745.CylindricalGearSetPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3745.CylindricalGearSetPowerFlow]':
        '''List[CylindricalGearSetPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3745.CylindricalGearSetPowerFlow))
        return value
