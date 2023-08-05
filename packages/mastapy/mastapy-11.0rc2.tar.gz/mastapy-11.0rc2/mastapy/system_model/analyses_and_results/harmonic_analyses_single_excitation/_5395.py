'''_5395.py

HarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses import (
    _5593, _5646, _5647, _5648,
    _5649, _5650, _5651, _5652,
    _5653, _5654, _5655, _5656,
    _5666, _5668, _5669, _5671,
    _5700, _5716, _5741
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.analysis_cases import _7188
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'HarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisOfSingleExcitation',)


class HarmonicAnalysisOfSingleExcitation(_7188.StaticLoadAnalysisCase):
    '''HarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def excitation_detail(self) -> '_5593.AbstractPeriodicExcitationDetail':
        '''AbstractPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5593.AbstractPeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to AbstractPeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_periodic_excitation_detail(self) -> '_5646.ElectricMachinePeriodicExcitationDetail':
        '''ElectricMachinePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5646.ElectricMachinePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachinePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_x_force_periodic_excitation_detail(self) -> '_5647.ElectricMachineRotorXForcePeriodicExcitationDetail':
        '''ElectricMachineRotorXForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5647.ElectricMachineRotorXForcePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorXForcePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_x_moment_periodic_excitation_detail(self) -> '_5648.ElectricMachineRotorXMomentPeriodicExcitationDetail':
        '''ElectricMachineRotorXMomentPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5648.ElectricMachineRotorXMomentPeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorXMomentPeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_y_force_periodic_excitation_detail(self) -> '_5649.ElectricMachineRotorYForcePeriodicExcitationDetail':
        '''ElectricMachineRotorYForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5649.ElectricMachineRotorYForcePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorYForcePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_y_moment_periodic_excitation_detail(self) -> '_5650.ElectricMachineRotorYMomentPeriodicExcitationDetail':
        '''ElectricMachineRotorYMomentPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5650.ElectricMachineRotorYMomentPeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorYMomentPeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_z_force_periodic_excitation_detail(self) -> '_5651.ElectricMachineRotorZForcePeriodicExcitationDetail':
        '''ElectricMachineRotorZForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5651.ElectricMachineRotorZForcePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorZForcePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_axial_loads_excitation_detail(self) -> '_5652.ElectricMachineStatorToothAxialLoadsExcitationDetail':
        '''ElectricMachineStatorToothAxialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5652.ElectricMachineStatorToothAxialLoadsExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothAxialLoadsExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_loads_excitation_detail(self) -> '_5653.ElectricMachineStatorToothLoadsExcitationDetail':
        '''ElectricMachineStatorToothLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5653.ElectricMachineStatorToothLoadsExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothLoadsExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_radial_loads_excitation_detail(self) -> '_5654.ElectricMachineStatorToothRadialLoadsExcitationDetail':
        '''ElectricMachineStatorToothRadialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5654.ElectricMachineStatorToothRadialLoadsExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothRadialLoadsExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_tangential_loads_excitation_detail(self) -> '_5655.ElectricMachineStatorToothTangentialLoadsExcitationDetail':
        '''ElectricMachineStatorToothTangentialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5655.ElectricMachineStatorToothTangentialLoadsExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothTangentialLoadsExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_torque_ripple_periodic_excitation_detail(self) -> '_5656.ElectricMachineTorqueRipplePeriodicExcitationDetail':
        '''ElectricMachineTorqueRipplePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5656.ElectricMachineTorqueRipplePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineTorqueRipplePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_gear_mesh_excitation_detail(self) -> '_5666.GearMeshExcitationDetail':
        '''GearMeshExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5666.GearMeshExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GearMeshExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_gear_mesh_misalignment_excitation_detail(self) -> '_5668.GearMeshMisalignmentExcitationDetail':
        '''GearMeshMisalignmentExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5668.GearMeshMisalignmentExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GearMeshMisalignmentExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_gear_mesh_te_excitation_detail(self) -> '_5669.GearMeshTEExcitationDetail':
        '''GearMeshTEExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5669.GearMeshTEExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GearMeshTEExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_general_periodic_excitation_detail(self) -> '_5671.GeneralPeriodicExcitationDetail':
        '''GeneralPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5671.GeneralPeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GeneralPeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_periodic_excitation_with_reference_shaft(self) -> '_5700.PeriodicExcitationWithReferenceShaft':
        '''PeriodicExcitationWithReferenceShaft: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5700.PeriodicExcitationWithReferenceShaft.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to PeriodicExcitationWithReferenceShaft. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_single_node_periodic_excitation_with_reference_shaft(self) -> '_5716.SingleNodePeriodicExcitationWithReferenceShaft':
        '''SingleNodePeriodicExcitationWithReferenceShaft: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5716.SingleNodePeriodicExcitationWithReferenceShaft.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to SingleNodePeriodicExcitationWithReferenceShaft. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_unbalanced_mass_excitation_detail(self) -> '_5741.UnbalancedMassExcitationDetail':
        '''UnbalancedMassExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5741.UnbalancedMassExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to UnbalancedMassExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ExcitationDetail.__class__)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None
