'''_5784.py

AssemblyCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2111, _2150
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5600
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
    _5785, _5787, _5790, _5796,
    _5797, _5798, _5803, _5808,
    _5818, _5820, _5822, _5826,
    _5832, _5833, _5834, _5841,
    _5848, _5851, _5852, _5853,
    _5855, _5857, _5862, _5863,
    _5864, _5873, _5866, _5868,
    _5872, _5878, _5879, _5884,
    _5887, _5890, _5894, _5898,
    _5902, _5905, _5777
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'AssemblyCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundHarmonicAnalysis',)


class AssemblyCompoundHarmonicAnalysis(_5777.AbstractAssemblyCompoundHarmonicAnalysis):
    '''AssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundHarmonicAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5600.AssemblyHarmonicAnalysis]':
        '''List[AssemblyHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5600.AssemblyHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5600.AssemblyHarmonicAnalysis]':
        '''List[AssemblyHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5600.AssemblyHarmonicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5785.BearingCompoundHarmonicAnalysis]':
        '''List[BearingCompoundHarmonicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5785.BearingCompoundHarmonicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5787.BeltDriveCompoundHarmonicAnalysis]':
        '''List[BeltDriveCompoundHarmonicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5787.BeltDriveCompoundHarmonicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5790.BevelDifferentialGearSetCompoundHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetCompoundHarmonicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5790.BevelDifferentialGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5796.BoltCompoundHarmonicAnalysis]':
        '''List[BoltCompoundHarmonicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5796.BoltCompoundHarmonicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5797.BoltedJointCompoundHarmonicAnalysis]':
        '''List[BoltedJointCompoundHarmonicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5797.BoltedJointCompoundHarmonicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5798.ClutchCompoundHarmonicAnalysis]':
        '''List[ClutchCompoundHarmonicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5798.ClutchCompoundHarmonicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5803.ConceptCouplingCompoundHarmonicAnalysis]':
        '''List[ConceptCouplingCompoundHarmonicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5803.ConceptCouplingCompoundHarmonicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5808.ConceptGearSetCompoundHarmonicAnalysis]':
        '''List[ConceptGearSetCompoundHarmonicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5808.ConceptGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5818.CVTCompoundHarmonicAnalysis]':
        '''List[CVTCompoundHarmonicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5818.CVTCompoundHarmonicAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5820.CycloidalAssemblyCompoundHarmonicAnalysis]':
        '''List[CycloidalAssemblyCompoundHarmonicAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5820.CycloidalAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5822.CycloidalDiscCompoundHarmonicAnalysis]':
        '''List[CycloidalDiscCompoundHarmonicAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5822.CycloidalDiscCompoundHarmonicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5826.CylindricalGearSetCompoundHarmonicAnalysis]':
        '''List[CylindricalGearSetCompoundHarmonicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5826.CylindricalGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5832.FaceGearSetCompoundHarmonicAnalysis]':
        '''List[FaceGearSetCompoundHarmonicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5832.FaceGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5833.FEPartCompoundHarmonicAnalysis]':
        '''List[FEPartCompoundHarmonicAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5833.FEPartCompoundHarmonicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5834.FlexiblePinAssemblyCompoundHarmonicAnalysis]':
        '''List[FlexiblePinAssemblyCompoundHarmonicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5834.FlexiblePinAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5841.HypoidGearSetCompoundHarmonicAnalysis]':
        '''List[HypoidGearSetCompoundHarmonicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5841.HypoidGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5848.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5848.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5851.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5851.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5852.MassDiscCompoundHarmonicAnalysis]':
        '''List[MassDiscCompoundHarmonicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5852.MassDiscCompoundHarmonicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5853.MeasurementComponentCompoundHarmonicAnalysis]':
        '''List[MeasurementComponentCompoundHarmonicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5853.MeasurementComponentCompoundHarmonicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5855.OilSealCompoundHarmonicAnalysis]':
        '''List[OilSealCompoundHarmonicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5855.OilSealCompoundHarmonicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5857.PartToPartShearCouplingCompoundHarmonicAnalysis]':
        '''List[PartToPartShearCouplingCompoundHarmonicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5857.PartToPartShearCouplingCompoundHarmonicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5862.PlanetCarrierCompoundHarmonicAnalysis]':
        '''List[PlanetCarrierCompoundHarmonicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5862.PlanetCarrierCompoundHarmonicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5863.PointLoadCompoundHarmonicAnalysis]':
        '''List[PointLoadCompoundHarmonicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5863.PointLoadCompoundHarmonicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5864.PowerLoadCompoundHarmonicAnalysis]':
        '''List[PowerLoadCompoundHarmonicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5864.PowerLoadCompoundHarmonicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5873.ShaftHubConnectionCompoundHarmonicAnalysis]':
        '''List[ShaftHubConnectionCompoundHarmonicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5873.ShaftHubConnectionCompoundHarmonicAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5866.RingPinsCompoundHarmonicAnalysis]':
        '''List[RingPinsCompoundHarmonicAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5866.RingPinsCompoundHarmonicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5868.RollingRingAssemblyCompoundHarmonicAnalysis]':
        '''List[RollingRingAssemblyCompoundHarmonicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5868.RollingRingAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5872.ShaftCompoundHarmonicAnalysis]':
        '''List[ShaftCompoundHarmonicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5872.ShaftCompoundHarmonicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5878.SpiralBevelGearSetCompoundHarmonicAnalysis]':
        '''List[SpiralBevelGearSetCompoundHarmonicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5878.SpiralBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5879.SpringDamperCompoundHarmonicAnalysis]':
        '''List[SpringDamperCompoundHarmonicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5879.SpringDamperCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5884.StraightBevelDiffGearSetCompoundHarmonicAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundHarmonicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5884.StraightBevelDiffGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5887.StraightBevelGearSetCompoundHarmonicAnalysis]':
        '''List[StraightBevelGearSetCompoundHarmonicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5887.StraightBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5890.SynchroniserCompoundHarmonicAnalysis]':
        '''List[SynchroniserCompoundHarmonicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5890.SynchroniserCompoundHarmonicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5894.TorqueConverterCompoundHarmonicAnalysis]':
        '''List[TorqueConverterCompoundHarmonicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5894.TorqueConverterCompoundHarmonicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5898.UnbalancedMassCompoundHarmonicAnalysis]':
        '''List[UnbalancedMassCompoundHarmonicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5898.UnbalancedMassCompoundHarmonicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5902.WormGearSetCompoundHarmonicAnalysis]':
        '''List[WormGearSetCompoundHarmonicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5902.WormGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5905.ZerolBevelGearSetCompoundHarmonicAnalysis]':
        '''List[ZerolBevelGearSetCompoundHarmonicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5905.ZerolBevelGearSetCompoundHarmonicAnalysis))
        return value
