'''_6918.py

AssemblyAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2111, _2150
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6453, _6585
from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
    _6919, _6921, _6924, _6930,
    _6931, _6932, _6937, _6942,
    _6952, _6955, _6956, _6961,
    _6968, _6969, _6970, _6977,
    _6984, _6987, _6989, _6990,
    _6992, _6994, _6999, _7000,
    _7001, _7010, _7003, _7006,
    _7009, _7015, _7016, _7021,
    _7024, _7027, _7031, _7036,
    _7040, _7043, _6908
)
from mastapy.system_model.analyses_and_results.system_deflections import _2364
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'AssemblyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyAdvancedSystemDeflection',)


class AssemblyAdvancedSystemDeflection(_6908.AbstractAssemblyAdvancedSystemDeflection):
    '''AssemblyAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyAdvancedSystemDeflection.TYPE'):
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
    def bearings(self) -> 'List[_6919.BearingAdvancedSystemDeflection]':
        '''List[BearingAdvancedSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6919.BearingAdvancedSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_6921.BeltDriveAdvancedSystemDeflection]':
        '''List[BeltDriveAdvancedSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6921.BeltDriveAdvancedSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6924.BevelDifferentialGearSetAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearSetAdvancedSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6924.BevelDifferentialGearSetAdvancedSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_6930.BoltAdvancedSystemDeflection]':
        '''List[BoltAdvancedSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6930.BoltAdvancedSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_6931.BoltedJointAdvancedSystemDeflection]':
        '''List[BoltedJointAdvancedSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6931.BoltedJointAdvancedSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_6932.ClutchAdvancedSystemDeflection]':
        '''List[ClutchAdvancedSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6932.ClutchAdvancedSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_6937.ConceptCouplingAdvancedSystemDeflection]':
        '''List[ConceptCouplingAdvancedSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6937.ConceptCouplingAdvancedSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6942.ConceptGearSetAdvancedSystemDeflection]':
        '''List[ConceptGearSetAdvancedSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6942.ConceptGearSetAdvancedSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_6952.CVTAdvancedSystemDeflection]':
        '''List[CVTAdvancedSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6952.CVTAdvancedSystemDeflection))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6955.CycloidalAssemblyAdvancedSystemDeflection]':
        '''List[CycloidalAssemblyAdvancedSystemDeflection]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6955.CycloidalAssemblyAdvancedSystemDeflection))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6956.CycloidalDiscAdvancedSystemDeflection]':
        '''List[CycloidalDiscAdvancedSystemDeflection]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6956.CycloidalDiscAdvancedSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6961.CylindricalGearSetAdvancedSystemDeflection]':
        '''List[CylindricalGearSetAdvancedSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6961.CylindricalGearSetAdvancedSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6968.FaceGearSetAdvancedSystemDeflection]':
        '''List[FaceGearSetAdvancedSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6968.FaceGearSetAdvancedSystemDeflection))
        return value

    @property
    def fe_parts(self) -> 'List[_6969.FEPartAdvancedSystemDeflection]':
        '''List[FEPartAdvancedSystemDeflection]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6969.FEPartAdvancedSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6970.FlexiblePinAssemblyAdvancedSystemDeflection]':
        '''List[FlexiblePinAssemblyAdvancedSystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6970.FlexiblePinAssemblyAdvancedSystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6977.HypoidGearSetAdvancedSystemDeflection]':
        '''List[HypoidGearSetAdvancedSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6977.HypoidGearSetAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6984.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6984.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6987.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6987.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_6989.MassDiscAdvancedSystemDeflection]':
        '''List[MassDiscAdvancedSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6989.MassDiscAdvancedSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_6990.MeasurementComponentAdvancedSystemDeflection]':
        '''List[MeasurementComponentAdvancedSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6990.MeasurementComponentAdvancedSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_6992.OilSealAdvancedSystemDeflection]':
        '''List[OilSealAdvancedSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6992.OilSealAdvancedSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6994.PartToPartShearCouplingAdvancedSystemDeflection]':
        '''List[PartToPartShearCouplingAdvancedSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6994.PartToPartShearCouplingAdvancedSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_6999.PlanetCarrierAdvancedSystemDeflection]':
        '''List[PlanetCarrierAdvancedSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6999.PlanetCarrierAdvancedSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_7000.PointLoadAdvancedSystemDeflection]':
        '''List[PointLoadAdvancedSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_7000.PointLoadAdvancedSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_7001.PowerLoadAdvancedSystemDeflection]':
        '''List[PowerLoadAdvancedSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_7001.PowerLoadAdvancedSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_7010.ShaftHubConnectionAdvancedSystemDeflection]':
        '''List[ShaftHubConnectionAdvancedSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_7010.ShaftHubConnectionAdvancedSystemDeflection))
        return value

    @property
    def ring_pins(self) -> 'List[_7003.RingPinsAdvancedSystemDeflection]':
        '''List[RingPinsAdvancedSystemDeflection]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_7003.RingPinsAdvancedSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_7006.RollingRingAssemblyAdvancedSystemDeflection]':
        '''List[RollingRingAssemblyAdvancedSystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_7006.RollingRingAssemblyAdvancedSystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_7009.ShaftAdvancedSystemDeflection]':
        '''List[ShaftAdvancedSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_7009.ShaftAdvancedSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_7015.SpiralBevelGearSetAdvancedSystemDeflection]':
        '''List[SpiralBevelGearSetAdvancedSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_7015.SpiralBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_7016.SpringDamperAdvancedSystemDeflection]':
        '''List[SpringDamperAdvancedSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_7016.SpringDamperAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_7021.StraightBevelDiffGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearSetAdvancedSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_7021.StraightBevelDiffGearSetAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_7024.StraightBevelGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelGearSetAdvancedSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_7024.StraightBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_7027.SynchroniserAdvancedSystemDeflection]':
        '''List[SynchroniserAdvancedSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_7027.SynchroniserAdvancedSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_7031.TorqueConverterAdvancedSystemDeflection]':
        '''List[TorqueConverterAdvancedSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_7031.TorqueConverterAdvancedSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_7036.UnbalancedMassAdvancedSystemDeflection]':
        '''List[UnbalancedMassAdvancedSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_7036.UnbalancedMassAdvancedSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_7040.WormGearSetAdvancedSystemDeflection]':
        '''List[WormGearSetAdvancedSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_7040.WormGearSetAdvancedSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_7043.ZerolBevelGearSetAdvancedSystemDeflection]':
        '''List[ZerolBevelGearSetAdvancedSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_7043.ZerolBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2364.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2364.AssemblySystemDeflection))
        return value
