'''_6318.py

AssemblyCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2111, _2150
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6187
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6319, _6321, _6324, _6330,
    _6331, _6332, _6337, _6342,
    _6352, _6354, _6356, _6360,
    _6366, _6367, _6368, _6375,
    _6382, _6385, _6386, _6387,
    _6389, _6391, _6396, _6397,
    _6398, _6407, _6400, _6402,
    _6406, _6412, _6413, _6418,
    _6421, _6424, _6428, _6432,
    _6436, _6439, _6311
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'AssemblyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundCriticalSpeedAnalysis',)


class AssemblyCompoundCriticalSpeedAnalysis(_6311.AbstractAssemblyCompoundCriticalSpeedAnalysis):
    '''AssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundCriticalSpeedAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6187.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6187.AssemblyCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6187.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6187.AssemblyCriticalSpeedAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_6319.BearingCompoundCriticalSpeedAnalysis]':
        '''List[BearingCompoundCriticalSpeedAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6319.BearingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_6321.BeltDriveCompoundCriticalSpeedAnalysis]':
        '''List[BeltDriveCompoundCriticalSpeedAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6321.BeltDriveCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6324.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6324.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_6330.BoltCompoundCriticalSpeedAnalysis]':
        '''List[BoltCompoundCriticalSpeedAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6330.BoltCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_6331.BoltedJointCompoundCriticalSpeedAnalysis]':
        '''List[BoltedJointCompoundCriticalSpeedAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6331.BoltedJointCompoundCriticalSpeedAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_6332.ClutchCompoundCriticalSpeedAnalysis]':
        '''List[ClutchCompoundCriticalSpeedAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6332.ClutchCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_6337.ConceptCouplingCompoundCriticalSpeedAnalysis]':
        '''List[ConceptCouplingCompoundCriticalSpeedAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6337.ConceptCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6342.ConceptGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ConceptGearSetCompoundCriticalSpeedAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6342.ConceptGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_6352.CVTCompoundCriticalSpeedAnalysis]':
        '''List[CVTCompoundCriticalSpeedAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6352.CVTCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6354.CycloidalAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalAssemblyCompoundCriticalSpeedAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6354.CycloidalAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6356.CycloidalDiscCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalDiscCompoundCriticalSpeedAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6356.CycloidalDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6360.CylindricalGearSetCompoundCriticalSpeedAnalysis]':
        '''List[CylindricalGearSetCompoundCriticalSpeedAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6360.CylindricalGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6366.FaceGearSetCompoundCriticalSpeedAnalysis]':
        '''List[FaceGearSetCompoundCriticalSpeedAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6366.FaceGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_6367.FEPartCompoundCriticalSpeedAnalysis]':
        '''List[FEPartCompoundCriticalSpeedAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6367.FEPartCompoundCriticalSpeedAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6368.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6368.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6375.HypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[HypoidGearSetCompoundCriticalSpeedAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6375.HypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6382.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6382.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6385.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6385.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_6386.MassDiscCompoundCriticalSpeedAnalysis]':
        '''List[MassDiscCompoundCriticalSpeedAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6386.MassDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_6387.MeasurementComponentCompoundCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCompoundCriticalSpeedAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6387.MeasurementComponentCompoundCriticalSpeedAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_6389.OilSealCompoundCriticalSpeedAnalysis]':
        '''List[OilSealCompoundCriticalSpeedAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6389.OilSealCompoundCriticalSpeedAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6391.PartToPartShearCouplingCompoundCriticalSpeedAnalysis]':
        '''List[PartToPartShearCouplingCompoundCriticalSpeedAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6391.PartToPartShearCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_6396.PlanetCarrierCompoundCriticalSpeedAnalysis]':
        '''List[PlanetCarrierCompoundCriticalSpeedAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6396.PlanetCarrierCompoundCriticalSpeedAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_6397.PointLoadCompoundCriticalSpeedAnalysis]':
        '''List[PointLoadCompoundCriticalSpeedAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6397.PointLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_6398.PowerLoadCompoundCriticalSpeedAnalysis]':
        '''List[PowerLoadCompoundCriticalSpeedAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6398.PowerLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6407.ShaftHubConnectionCompoundCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCompoundCriticalSpeedAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6407.ShaftHubConnectionCompoundCriticalSpeedAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_6400.RingPinsCompoundCriticalSpeedAnalysis]':
        '''List[RingPinsCompoundCriticalSpeedAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6400.RingPinsCompoundCriticalSpeedAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6402.RollingRingAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[RollingRingAssemblyCompoundCriticalSpeedAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6402.RollingRingAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6406.ShaftCompoundCriticalSpeedAnalysis]':
        '''List[ShaftCompoundCriticalSpeedAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6406.ShaftCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6412.SpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6412.SpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6413.SpringDamperCompoundCriticalSpeedAnalysis]':
        '''List[SpringDamperCompoundCriticalSpeedAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6413.SpringDamperCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6418.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6418.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6421.StraightBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6421.StraightBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6424.SynchroniserCompoundCriticalSpeedAnalysis]':
        '''List[SynchroniserCompoundCriticalSpeedAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6424.SynchroniserCompoundCriticalSpeedAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6428.TorqueConverterCompoundCriticalSpeedAnalysis]':
        '''List[TorqueConverterCompoundCriticalSpeedAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6428.TorqueConverterCompoundCriticalSpeedAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6432.UnbalancedMassCompoundCriticalSpeedAnalysis]':
        '''List[UnbalancedMassCompoundCriticalSpeedAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6432.UnbalancedMassCompoundCriticalSpeedAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6436.WormGearSetCompoundCriticalSpeedAnalysis]':
        '''List[WormGearSetCompoundCriticalSpeedAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6436.WormGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6439.ZerolBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCompoundCriticalSpeedAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6439.ZerolBevelGearSetCompoundCriticalSpeedAnalysis))
        return value
