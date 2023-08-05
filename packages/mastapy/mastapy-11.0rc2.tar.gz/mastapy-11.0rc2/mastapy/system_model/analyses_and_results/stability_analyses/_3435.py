﻿'''_3435.py

AssemblyStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2111, _2150
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6453, _6585
from mastapy.system_model.analyses_and_results.stability_analyses import (
    _3436, _3438, _3440, _3448,
    _3447, _3451, _3456, _3458,
    _3471, _3472, _3475, _3477,
    _3483, _3485, _3486, _3492,
    _3499, _3502, _3504, _3505,
    _3507, _3511, _3514, _3515,
    _3516, _3524, _3518, _3520,
    _3525, _3529, _3533, _3537,
    _3540, _3547, _3550, _3552,
    _3555, _3558, _3428
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'AssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyStabilityAnalysis',)


class AssemblyStabilityAnalysis(_3428.AbstractAssemblyStabilityAnalysis):
    '''AssemblyStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2111.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6453.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6453.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_3436.BearingStabilityAnalysis]':
        '''List[BearingStabilityAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3436.BearingStabilityAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_3438.BeltDriveStabilityAnalysis]':
        '''List[BeltDriveStabilityAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3438.BeltDriveStabilityAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3440.BevelDifferentialGearSetStabilityAnalysis]':
        '''List[BevelDifferentialGearSetStabilityAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3440.BevelDifferentialGearSetStabilityAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_3448.BoltStabilityAnalysis]':
        '''List[BoltStabilityAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3448.BoltStabilityAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_3447.BoltedJointStabilityAnalysis]':
        '''List[BoltedJointStabilityAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3447.BoltedJointStabilityAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_3451.ClutchStabilityAnalysis]':
        '''List[ClutchStabilityAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3451.ClutchStabilityAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_3456.ConceptCouplingStabilityAnalysis]':
        '''List[ConceptCouplingStabilityAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3456.ConceptCouplingStabilityAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3458.ConceptGearSetStabilityAnalysis]':
        '''List[ConceptGearSetStabilityAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3458.ConceptGearSetStabilityAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_3471.CVTStabilityAnalysis]':
        '''List[CVTStabilityAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3471.CVTStabilityAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3472.CycloidalAssemblyStabilityAnalysis]':
        '''List[CycloidalAssemblyStabilityAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3472.CycloidalAssemblyStabilityAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3475.CycloidalDiscStabilityAnalysis]':
        '''List[CycloidalDiscStabilityAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3475.CycloidalDiscStabilityAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3477.CylindricalGearSetStabilityAnalysis]':
        '''List[CylindricalGearSetStabilityAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3477.CylindricalGearSetStabilityAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3483.FaceGearSetStabilityAnalysis]':
        '''List[FaceGearSetStabilityAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3483.FaceGearSetStabilityAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_3485.FEPartStabilityAnalysis]':
        '''List[FEPartStabilityAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3485.FEPartStabilityAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3486.FlexiblePinAssemblyStabilityAnalysis]':
        '''List[FlexiblePinAssemblyStabilityAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3486.FlexiblePinAssemblyStabilityAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3492.HypoidGearSetStabilityAnalysis]':
        '''List[HypoidGearSetStabilityAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3492.HypoidGearSetStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3499.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3499.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3502.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3502.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_3504.MassDiscStabilityAnalysis]':
        '''List[MassDiscStabilityAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3504.MassDiscStabilityAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_3505.MeasurementComponentStabilityAnalysis]':
        '''List[MeasurementComponentStabilityAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3505.MeasurementComponentStabilityAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_3507.OilSealStabilityAnalysis]':
        '''List[OilSealStabilityAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3507.OilSealStabilityAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3511.PartToPartShearCouplingStabilityAnalysis]':
        '''List[PartToPartShearCouplingStabilityAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3511.PartToPartShearCouplingStabilityAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_3514.PlanetCarrierStabilityAnalysis]':
        '''List[PlanetCarrierStabilityAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3514.PlanetCarrierStabilityAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_3515.PointLoadStabilityAnalysis]':
        '''List[PointLoadStabilityAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3515.PointLoadStabilityAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_3516.PowerLoadStabilityAnalysis]':
        '''List[PowerLoadStabilityAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3516.PowerLoadStabilityAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3524.ShaftHubConnectionStabilityAnalysis]':
        '''List[ShaftHubConnectionStabilityAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3524.ShaftHubConnectionStabilityAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_3518.RingPinsStabilityAnalysis]':
        '''List[RingPinsStabilityAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3518.RingPinsStabilityAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3520.RollingRingAssemblyStabilityAnalysis]':
        '''List[RollingRingAssemblyStabilityAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3520.RollingRingAssemblyStabilityAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_3525.ShaftStabilityAnalysis]':
        '''List[ShaftStabilityAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3525.ShaftStabilityAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3529.SpiralBevelGearSetStabilityAnalysis]':
        '''List[SpiralBevelGearSetStabilityAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3529.SpiralBevelGearSetStabilityAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_3533.SpringDamperStabilityAnalysis]':
        '''List[SpringDamperStabilityAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3533.SpringDamperStabilityAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3537.StraightBevelDiffGearSetStabilityAnalysis]':
        '''List[StraightBevelDiffGearSetStabilityAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3537.StraightBevelDiffGearSetStabilityAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3540.StraightBevelGearSetStabilityAnalysis]':
        '''List[StraightBevelGearSetStabilityAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3540.StraightBevelGearSetStabilityAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_3547.SynchroniserStabilityAnalysis]':
        '''List[SynchroniserStabilityAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3547.SynchroniserStabilityAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_3550.TorqueConverterStabilityAnalysis]':
        '''List[TorqueConverterStabilityAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3550.TorqueConverterStabilityAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3552.UnbalancedMassStabilityAnalysis]':
        '''List[UnbalancedMassStabilityAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3552.UnbalancedMassStabilityAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3555.WormGearSetStabilityAnalysis]':
        '''List[WormGearSetStabilityAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3555.WormGearSetStabilityAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3558.ZerolBevelGearSetStabilityAnalysis]':
        '''List[ZerolBevelGearSetStabilityAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3558.ZerolBevelGearSetStabilityAnalysis))
        return value
