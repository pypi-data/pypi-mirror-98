'''_3044.py

AssemblyCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2111, _2150
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2914
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _3045, _3047, _3050, _3056,
    _3057, _3058, _3063, _3068,
    _3078, _3080, _3082, _3086,
    _3092, _3093, _3094, _3101,
    _3108, _3111, _3112, _3113,
    _3115, _3117, _3122, _3123,
    _3124, _3133, _3126, _3128,
    _3132, _3138, _3139, _3144,
    _3147, _3150, _3154, _3158,
    _3162, _3165, _3037
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'AssemblyCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponseAtASpeed',)


class AssemblyCompoundSteadyStateSynchronousResponseAtASpeed(_3037.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed):
    '''AssemblyCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2111.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

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
    def load_case_analyses_ready(self) -> 'List[_2914.AssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[AssemblySteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2914.AssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2914.AssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[AssemblySteadyStateSynchronousResponseAtASpeed]: 'AssemblySteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2914.AssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bearings(self) -> 'List[_3045.BearingCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BearingCompoundSteadyStateSynchronousResponseAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3045.BearingCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def belt_drives(self) -> 'List[_3047.BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3047.BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3050.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3050.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bolts(self) -> 'List[_3056.BoltCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BoltCompoundSteadyStateSynchronousResponseAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3056.BoltCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bolted_joints(self) -> 'List[_3057.BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3057.BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def clutches(self) -> 'List[_3058.ClutchCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ClutchCompoundSteadyStateSynchronousResponseAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3058.ClutchCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def concept_couplings(self) -> 'List[_3063.ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3063.ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3068.ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3068.ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cv_ts(self) -> 'List[_3078.CVTCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[CVTCompoundSteadyStateSynchronousResponseAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3078.CVTCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3080.CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3080.CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3082.CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3082.CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3086.CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3086.CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3092.FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3092.FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def fe_parts(self) -> 'List[_3093.FEPartCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[FEPartCompoundSteadyStateSynchronousResponseAtASpeed]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3093.FEPartCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3094.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3094.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3101.HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3101.HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3108.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3108.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3111.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3111.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def mass_discs(self) -> 'List[_3112.MassDiscCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponseAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3112.MassDiscCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def measurement_components(self) -> 'List[_3113.MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3113.MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def oil_seals(self) -> 'List[_3115.OilSealCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[OilSealCompoundSteadyStateSynchronousResponseAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3115.OilSealCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3117.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3117.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def planet_carriers(self) -> 'List[_3122.PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3122.PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def point_loads(self) -> 'List[_3123.PointLoadCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponseAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3123.PointLoadCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def power_loads(self) -> 'List[_3124.PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3124.PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3133.ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3133.ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def ring_pins(self) -> 'List[_3126.RingPinsCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[RingPinsCompoundSteadyStateSynchronousResponseAtASpeed]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3126.RingPinsCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3128.RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3128.RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def shafts(self) -> 'List[_3132.ShaftCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftCompoundSteadyStateSynchronousResponseAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3132.ShaftCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3138.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3138.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spring_dampers(self) -> 'List[_3139.SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3139.SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3144.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3144.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3147.StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3147.StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def synchronisers(self) -> 'List[_3150.SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3150.SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def torque_converters(self) -> 'List[_3154.TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3154.TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3158.UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3158.UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3162.WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3162.WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3165.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3165.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value
