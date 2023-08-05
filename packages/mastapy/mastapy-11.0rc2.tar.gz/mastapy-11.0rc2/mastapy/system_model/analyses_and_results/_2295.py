'''_2295.py

AdvancedSystemDeflectionAnalysis
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6594, _6612, _6622, _6624,
    _6625, _6627, _6491, _6493,
    _6580, _6568, _6567, _6456,
    _6469, _6468, _6474, _6473,
    _6487, _6486, _6489, _6490,
    _6577, _6586, _6584, _6582,
    _6596, _6595, _6607, _6606,
    _6608, _6609, _6613, _6614,
    _6615, _6588, _6488, _6455,
    _6470, _6483, _6548, _6569,
    _6583, _6444, _6458, _6476,
    _6520, _6599, _6463, _6480,
    _6449, _6497, _6543, _6550,
    _6553, _6556, _6592, _6602,
    _6623, _6626, _6527, _6492,
    _6494, _6581, _6566, _6467,
    _6472, _6485, _6442, _6441,
    _6443, _6454, _6466, _6465,
    _6471, _6484, _6503, _6518,
    _6522, _6523, _6453, _6531,
    _6558, _6559, _6561, _6563,
    _6565, _6572, _6575, _6576,
    _6585, _6589, _6620, _6621,
    _6587, _6475, _6477, _6519,
    _6521, _6448, _6450, _6457,
    _6459, _6460, _6461, _6462,
    _6464, _6478, _6482, _6495,
    _6499, _6500, _6525, _6530,
    _6542, _6544, _6549, _6551,
    _6552, _6554, _6555, _6557,
    _6570, _6591, _6593, _6598,
    _6600, _6601, _6603, _6604,
    _6605
)
from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
    _7017, _7032, _7038, _7040,
    _7041, _7043, _6955, _6956,
    _7003, _6994, _6996, _6921,
    _6932, _6934, _6937, _6939,
    _6949, _6951, _6952, _6954,
    _7002, _7010, _7005, _7006,
    _7016, _7018, _7027, _7028,
    _7029, _7030, _7031, _7033,
    _7034, _7011, _6953, _6920,
    _6935, _6946, _6978, _6997,
    _7007, _6911, _6923, _6941,
    _6967, _7020, _6928, _6944,
    _6916, _6960, _6976, _6980,
    _6983, _6986, _7014, _7023,
    _7039, _7042, _6972, _6957,
    _6958, _7004, _6995, _6933,
    _6938, _6950, _6909, _6908,
    _6910, _6919, _6930, _6931,
    _6936, _6947, _6964, _6965,
    _6969, _6970, _6918, _6974,
    _6989, _6990, _6991, _6992,
    _6993, _6999, _7000, _7001,
    _7008, _7012, _7036, _7037,
    _7009, _6940, _6942, _6966,
    _6968, _6915, _6917, _6922,
    _6924, _6925, _6926, _6927,
    _6929, _6943, _6945, _6959,
    _6961, _6963, _6971, _6973,
    _6975, _6977, _6979, _6981,
    _6982, _6984, _6985, _6987,
    _6998, _7013, _7015, _7019,
    _7021, _7022, _7024, _7025,
    _7026
)
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.couplings import (
    _2031, _2027, _2021, _2023,
    _2025, _2029
)
from mastapy.system_model.part_model.gears import (
    _2226, _2227, _2228, _2195,
    _2196, _2202, _2203, _2187,
    _2188, _2189, _2190, _2191,
    _2192, _2193, _2194, _2197,
    _2198, _2199, _2200, _2201,
    _2204, _2206, _2208, _2209,
    _2210, _2211, _2212, _2213,
    _2214, _2215, _2216, _2217,
    _2218, _2219, _2220, _2221,
    _2222, _2223, _2224, _2225
)
from mastapy.system_model.part_model.cycloidal import _2242, _2243, _2244
from mastapy.system_model.part_model.couplings import (
    _2262, _2263, _2250, _2252,
    _2253, _2255, _2256, _2257,
    _2258, _2260, _2261, _2264,
    _2272, _2270, _2271, _2274,
    _2275, _2276, _2278, _2279,
    _2280, _2281, _2282, _2284
)
from mastapy.system_model.connections_and_sockets import (
    _1974, _1952, _1947, _1948,
    _1951, _1960, _1966, _1971,
    _1944
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1980, _1984, _1990, _2004,
    _1982, _1986, _1978, _1988,
    _1994, _1997, _1998, _1999,
    _2002, _2006, _2008, _2010,
    _1992
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2014, _2017, _2020
from mastapy.system_model.part_model import (
    _2113, _2112, _2114, _2117,
    _2119, _2120, _2121, _2124,
    _2125, _2128, _2129, _2130,
    _2111, _2131, _2138, _2139,
    _2140, _2142, _2144, _2145,
    _2147, _2148, _2150, _2152,
    _2153, _2154
)
from mastapy.system_model.part_model.shaft_model import _2157
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results import _2294

_SPRING_DAMPER_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpringDamperConnectionLoadCase')
_TORQUE_CONVERTER_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueConverterConnectionLoadCase')
_WORM_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'WormGearLoadCase')
_WORM_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'WormGearSetLoadCase')
_ZEROL_BEVEL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ZerolBevelGearLoadCase')
_ZEROL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ZerolBevelGearSetLoadCase')
_CYCLOIDAL_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CycloidalAssemblyLoadCase')
_CYCLOIDAL_DISC_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CycloidalDiscLoadCase')
_RING_PINS_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RingPinsLoadCase')
_PART_TO_PART_SHEAR_COUPLING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PartToPartShearCouplingLoadCase')
_PART_TO_PART_SHEAR_COUPLING_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PartToPartShearCouplingHalfLoadCase')
_BELT_DRIVE_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BeltDriveLoadCase')
_CLUTCH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ClutchLoadCase')
_CLUTCH_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ClutchHalfLoadCase')
_CONCEPT_COUPLING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptCouplingLoadCase')
_CONCEPT_COUPLING_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptCouplingHalfLoadCase')
_COUPLING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CouplingLoadCase')
_COUPLING_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CouplingHalfLoadCase')
_CVT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CVTLoadCase')
_CVT_PULLEY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CVTPulleyLoadCase')
_PULLEY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PulleyLoadCase')
_SHAFT_HUB_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ShaftHubConnectionLoadCase')
_ROLLING_RING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RollingRingLoadCase')
_ROLLING_RING_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RollingRingAssemblyLoadCase')
_SPRING_DAMPER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpringDamperLoadCase')
_SPRING_DAMPER_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpringDamperHalfLoadCase')
_SYNCHRONISER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SynchroniserLoadCase')
_SYNCHRONISER_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SynchroniserHalfLoadCase')
_SYNCHRONISER_PART_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SynchroniserPartLoadCase')
_SYNCHRONISER_SLEEVE_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SynchroniserSleeveLoadCase')
_TORQUE_CONVERTER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueConverterLoadCase')
_TORQUE_CONVERTER_PUMP_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueConverterPumpLoadCase')
_TORQUE_CONVERTER_TURBINE_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueConverterTurbineLoadCase')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ShaftToMountableComponentConnectionLoadCase')
_CVT_BELT_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CVTBeltConnectionLoadCase')
_BELT_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BeltConnectionLoadCase')
_COAXIAL_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CoaxialConnectionLoadCase')
_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConnectionLoadCase')
_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'InterMountableComponentConnectionLoadCase')
_PLANETARY_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PlanetaryConnectionLoadCase')
_ROLLING_RING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RollingRingConnectionLoadCase')
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AbstractShaftToMountableComponentConnectionLoadCase')
_BEVEL_DIFFERENTIAL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelDifferentialGearMeshLoadCase')
_CONCEPT_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptGearMeshLoadCase')
_FACE_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FaceGearMeshLoadCase')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelDiffGearMeshLoadCase')
_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelGearMeshLoadCase')
_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConicalGearMeshLoadCase')
_AGMA_GLEASON_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AGMAGleasonConicalGearMeshLoadCase')
_CYLINDRICAL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalGearMeshLoadCase')
_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HypoidGearMeshLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidConicalGearMeshLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidHypoidGearMeshLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase')
_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpiralBevelGearMeshLoadCase')
_STRAIGHT_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelGearMeshLoadCase')
_WORM_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'WormGearMeshLoadCase')
_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ZerolBevelGearMeshLoadCase')
_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'GearMeshLoadCase')
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CycloidalDiscCentralBearingConnectionLoadCase')
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CycloidalDiscPlanetaryBearingConnectionLoadCase')
_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RingPinsToDiscConnectionLoadCase')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PartToPartShearCouplingConnectionLoadCase')
_CLUTCH_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ClutchConnectionLoadCase')
_CONCEPT_COUPLING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptCouplingConnectionLoadCase')
_COUPLING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CouplingConnectionLoadCase')
_ABSTRACT_SHAFT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AbstractShaftLoadCase')
_ABSTRACT_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AbstractAssemblyLoadCase')
_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AbstractShaftOrHousingLoadCase')
_BEARING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BearingLoadCase')
_BOLT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BoltLoadCase')
_BOLTED_JOINT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BoltedJointLoadCase')
_COMPONENT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ComponentLoadCase')
_CONNECTOR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConnectorLoadCase')
_DATUM_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'DatumLoadCase')
_EXTERNAL_CAD_MODEL_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ExternalCADModelLoadCase')
_FE_PART_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FEPartLoadCase')
_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FlexiblePinAssemblyLoadCase')
_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AssemblyLoadCase')
_GUIDE_DXF_MODEL_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'GuideDxfModelLoadCase')
_MASS_DISC_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'MassDiscLoadCase')
_MEASUREMENT_COMPONENT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'MeasurementComponentLoadCase')
_MOUNTABLE_COMPONENT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'MountableComponentLoadCase')
_OIL_SEAL_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'OilSealLoadCase')
_PART_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PartLoadCase')
_PLANET_CARRIER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PlanetCarrierLoadCase')
_POINT_LOAD_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PointLoadLoadCase')
_POWER_LOAD_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PowerLoadLoadCase')
_ROOT_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RootAssemblyLoadCase')
_SPECIALISED_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpecialisedAssemblyLoadCase')
_UNBALANCED_MASS_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'UnbalancedMassLoadCase')
_VIRTUAL_COMPONENT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'VirtualComponentLoadCase')
_SHAFT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ShaftLoadCase')
_CONCEPT_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptGearLoadCase')
_CONCEPT_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptGearSetLoadCase')
_FACE_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FaceGearLoadCase')
_FACE_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FaceGearSetLoadCase')
_AGMA_GLEASON_CONICAL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AGMAGleasonConicalGearLoadCase')
_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AGMAGleasonConicalGearSetLoadCase')
_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelDifferentialGearLoadCase')
_BEVEL_DIFFERENTIAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelDifferentialGearSetLoadCase')
_BEVEL_DIFFERENTIAL_PLANET_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelDifferentialPlanetGearLoadCase')
_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelDifferentialSunGearLoadCase')
_BEVEL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelGearLoadCase')
_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelGearSetLoadCase')
_CONICAL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConicalGearLoadCase')
_CONICAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConicalGearSetLoadCase')
_CYLINDRICAL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalGearLoadCase')
_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalGearSetLoadCase')
_CYLINDRICAL_PLANET_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalPlanetGearLoadCase')
_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'GearLoadCase')
_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'GearSetLoadCase')
_HYPOID_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HypoidGearLoadCase')
_HYPOID_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HypoidGearSetLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidConicalGearLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidConicalGearSetLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidHypoidGearLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidHypoidGearSetLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidSpiralBevelGearLoadCase')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase')
_PLANETARY_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PlanetaryGearSetLoadCase')
_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpiralBevelGearLoadCase')
_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpiralBevelGearSetLoadCase')
_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelDiffGearLoadCase')
_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelDiffGearSetLoadCase')
_STRAIGHT_BEVEL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelGearLoadCase')
_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelGearSetLoadCase')
_STRAIGHT_BEVEL_PLANET_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelPlanetGearLoadCase')
_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelSunGearLoadCase')
_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_CYCLOIDAL_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalAssembly')
_CYCLOIDAL_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalDisc')
_RING_PINS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'RingPins')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscCentralBearingConnection')
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscPlanetaryBearingConnection')
_RING_PINS_TO_DISC_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'RingPinsToDiscConnection')
_ABSTRACT_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaft')
_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FE_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FEPart')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'AdvancedSystemDeflectionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflectionAnalysis',)


class AdvancedSystemDeflectionAnalysis(_2294.SingleAnalysis):
    '''AdvancedSystemDeflectionAnalysis

    This is a mastapy class.
    '''

    TYPE = _ADVANCED_SYSTEM_DEFLECTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflectionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6594.SpringDamperConnectionLoadCase') -> '_7017.SpringDamperConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_2031.TorqueConverterConnection') -> '_7032.TorqueConverterConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6612.TorqueConverterConnectionLoadCase') -> '_7032.TorqueConverterConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6622.WormGearLoadCase') -> '_7038.WormGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_WORM_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2226.WormGearSet') -> '_7040.WormGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6624.WormGearSetLoadCase') -> '_7040.WormGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_WORM_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2227.ZerolBevelGear') -> '_7041.ZerolBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6625.ZerolBevelGearLoadCase') -> '_7041.ZerolBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2228.ZerolBevelGearSet') -> '_7043.ZerolBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6627.ZerolBevelGearSetLoadCase') -> '_7043.ZerolBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cycloidal_assembly(self, design_entity: '_2242.CycloidalAssembly') -> '_6955.CycloidalAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CycloidalAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cycloidal_assembly_load_case(self, design_entity_analysis: '_6491.CycloidalAssemblyLoadCase') -> '_6955.CycloidalAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CycloidalAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_ASSEMBLY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cycloidal_disc(self, design_entity: '_2243.CycloidalDisc') -> '_6956.CycloidalDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CycloidalDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cycloidal_disc_load_case(self, design_entity_analysis: '_6493.CycloidalDiscLoadCase') -> '_6956.CycloidalDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CycloidalDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_ring_pins(self, design_entity: '_2244.RingPins') -> '_7003.RingPinsAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RingPinsAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_RING_PINS](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_ring_pins_load_case(self, design_entity_analysis: '_6580.RingPinsLoadCase') -> '_7003.RingPinsAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RingPinsAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_RING_PINS_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2262.PartToPartShearCoupling') -> '_6994.PartToPartShearCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6568.PartToPartShearCouplingLoadCase') -> '_6994.PartToPartShearCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2263.PartToPartShearCouplingHalf') -> '_6996.PartToPartShearCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6567.PartToPartShearCouplingHalfLoadCase') -> '_6996.PartToPartShearCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2250.BeltDrive') -> '_6921.BeltDriveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltDriveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6456.BeltDriveLoadCase') -> '_6921.BeltDriveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltDriveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BELT_DRIVE_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2252.Clutch') -> '_6932.ClutchAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6469.ClutchLoadCase') -> '_6932.ClutchAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CLUTCH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2253.ClutchHalf') -> '_6934.ClutchHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6468.ClutchHalfLoadCase') -> '_6934.ClutchHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CLUTCH_HALF_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2255.ConceptCoupling') -> '_6937.ConceptCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6474.ConceptCouplingLoadCase') -> '_6937.ConceptCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2256.ConceptCouplingHalf') -> '_6939.ConceptCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6473.ConceptCouplingHalfLoadCase') -> '_6939.ConceptCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_HALF_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2257.Coupling') -> '_6949.CouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6487.CouplingLoadCase') -> '_6949.CouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COUPLING_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2258.CouplingHalf') -> '_6951.CouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6486.CouplingHalfLoadCase') -> '_6951.CouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COUPLING_HALF_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2260.CVT') -> '_6952.CVTAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6489.CVTLoadCase') -> '_6952.CVTAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CVT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2261.CVTPulley') -> '_6954.CVTPulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTPulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6490.CVTPulleyLoadCase') -> '_6954.CVTPulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTPulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CVT_PULLEY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2264.Pulley') -> '_7002.PulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6577.PulleyLoadCase') -> '_7002.PulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PULLEY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2272.ShaftHubConnection') -> '_7010.ShaftHubConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftHubConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6586.ShaftHubConnectionLoadCase') -> '_7010.ShaftHubConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftHubConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SHAFT_HUB_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2270.RollingRing') -> '_7005.RollingRingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6584.RollingRingLoadCase') -> '_7005.RollingRingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ROLLING_RING_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2271.RollingRingAssembly') -> '_7006.RollingRingAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6582.RollingRingAssemblyLoadCase') -> '_7006.RollingRingAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ROLLING_RING_ASSEMBLY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2274.SpringDamper') -> '_7016.SpringDamperAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6596.SpringDamperLoadCase') -> '_7016.SpringDamperAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2275.SpringDamperHalf') -> '_7018.SpringDamperHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6595.SpringDamperHalfLoadCase') -> '_7018.SpringDamperHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_HALF_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2276.Synchroniser') -> '_7027.SynchroniserAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6607.SynchroniserLoadCase') -> '_7027.SynchroniserAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2278.SynchroniserHalf') -> '_7028.SynchroniserHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6606.SynchroniserHalfLoadCase') -> '_7028.SynchroniserHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_HALF_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2279.SynchroniserPart') -> '_7029.SynchroniserPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6608.SynchroniserPartLoadCase') -> '_7029.SynchroniserPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_PART_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2280.SynchroniserSleeve') -> '_7030.SynchroniserSleeveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserSleeveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6609.SynchroniserSleeveLoadCase') -> '_7030.SynchroniserSleeveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserSleeveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_SLEEVE_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2281.TorqueConverter') -> '_7031.TorqueConverterAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6613.TorqueConverterLoadCase') -> '_7031.TorqueConverterAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2282.TorqueConverterPump') -> '_7033.TorqueConverterPumpAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterPumpAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6614.TorqueConverterPumpLoadCase') -> '_7033.TorqueConverterPumpAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterPumpAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_PUMP_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2284.TorqueConverterTurbine') -> '_7034.TorqueConverterTurbineAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterTurbineAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6615.TorqueConverterTurbineLoadCase') -> '_7034.TorqueConverterTurbineAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterTurbineAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_TURBINE_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1974.ShaftToMountableComponentConnection') -> '_7011.ShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6588.ShaftToMountableComponentConnectionLoadCase') -> '_7011.ShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1952.CVTBeltConnection') -> '_6953.CVTBeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6488.CVTBeltConnectionLoadCase') -> '_6953.CVTBeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CVT_BELT_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1947.BeltConnection') -> '_6920.BeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6455.BeltConnectionLoadCase') -> '_6920.BeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BELT_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1948.CoaxialConnection') -> '_6935.CoaxialConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CoaxialConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6470.CoaxialConnectionLoadCase') -> '_6935.CoaxialConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CoaxialConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COAXIAL_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1951.Connection') -> '_6946.ConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6483.ConnectionLoadCase') -> '_6946.ConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1960.InterMountableComponentConnection') -> '_6978.InterMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6548.InterMountableComponentConnectionLoadCase') -> '_6978.InterMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1966.PlanetaryConnection') -> '_6997.PlanetaryConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6569.PlanetaryConnectionLoadCase') -> '_6997.PlanetaryConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PLANETARY_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1971.RollingRingConnection') -> '_7007.RollingRingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6583.RollingRingConnectionLoadCase') -> '_7007.RollingRingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ROLLING_RING_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_abstract_shaft_to_mountable_component_connection(self, design_entity: '_1944.AbstractShaftToMountableComponentConnection') -> '_6911.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_abstract_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6444.AbstractShaftToMountableComponentConnectionLoadCase') -> '_6911.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1980.BevelDifferentialGearMesh') -> '_6923.BevelDifferentialGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6458.BevelDifferentialGearMeshLoadCase') -> '_6923.BevelDifferentialGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1984.ConceptGearMesh') -> '_6941.ConceptGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6476.ConceptGearMeshLoadCase') -> '_6941.ConceptGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1990.FaceGearMesh') -> '_6967.FaceGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6520.FaceGearMeshLoadCase') -> '_6967.FaceGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FACE_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_2004.StraightBevelDiffGearMesh') -> '_7020.StraightBevelDiffGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6599.StraightBevelDiffGearMeshLoadCase') -> '_7020.StraightBevelDiffGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1982.BevelGearMesh') -> '_6928.BevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6463.BevelGearMeshLoadCase') -> '_6928.BevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1986.ConicalGearMesh') -> '_6944.ConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6480.ConicalGearMeshLoadCase') -> '_6944.ConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1978.AGMAGleasonConicalGearMesh') -> '_6916.AGMAGleasonConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6449.AGMAGleasonConicalGearMeshLoadCase') -> '_6916.AGMAGleasonConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1988.CylindricalGearMesh') -> '_6960.CylindricalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6497.CylindricalGearMeshLoadCase') -> '_6960.CylindricalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1994.HypoidGearMesh') -> '_6976.HypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6543.HypoidGearMeshLoadCase') -> '_6976.HypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1997.KlingelnbergCycloPalloidConicalGearMesh') -> '_6980.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6550.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_6980.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1998.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6983.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6553.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_6983.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1999.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6986.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6556.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_6986.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_2002.SpiralBevelGearMesh') -> '_7014.SpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6592.SpiralBevelGearMeshLoadCase') -> '_7014.SpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_2006.StraightBevelGearMesh') -> '_7023.StraightBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6602.StraightBevelGearMeshLoadCase') -> '_7023.StraightBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_2008.WormGearMesh') -> '_7039.WormGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6623.WormGearMeshLoadCase') -> '_7039.WormGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_WORM_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_2010.ZerolBevelGearMesh') -> '_7042.ZerolBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6626.ZerolBevelGearMeshLoadCase') -> '_7042.ZerolBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1992.GearMesh') -> '_6972.GearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6527.GearMeshLoadCase') -> '_6972.GearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_GEAR_MESH_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cycloidal_disc_central_bearing_connection(self, design_entity: '_2014.CycloidalDiscCentralBearingConnection') -> '_6957.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cycloidal_disc_central_bearing_connection_load_case(self, design_entity_analysis: '_6492.CycloidalDiscCentralBearingConnectionLoadCase') -> '_6957.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscCentralBearingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cycloidal_disc_planetary_bearing_connection(self, design_entity: '_2017.CycloidalDiscPlanetaryBearingConnection') -> '_6958.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cycloidal_disc_planetary_bearing_connection_load_case(self, design_entity_analysis: '_6494.CycloidalDiscPlanetaryBearingConnectionLoadCase') -> '_6958.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_ring_pins_to_disc_connection(self, design_entity: '_2020.RingPinsToDiscConnection') -> '_7004.RingPinsToDiscConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RingPinsToDiscConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_RING_PINS_TO_DISC_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_ring_pins_to_disc_connection_load_case(self, design_entity_analysis: '_6581.RingPinsToDiscConnectionLoadCase') -> '_7004.RingPinsToDiscConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RingPinsToDiscConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_RING_PINS_TO_DISC_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_2027.PartToPartShearCouplingConnection') -> '_6995.PartToPartShearCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6566.PartToPartShearCouplingConnectionLoadCase') -> '_6995.PartToPartShearCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_2021.ClutchConnection') -> '_6933.ClutchConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6467.ClutchConnectionLoadCase') -> '_6933.ClutchConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CLUTCH_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_2023.ConceptCouplingConnection') -> '_6938.ConceptCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6472.ConceptCouplingConnectionLoadCase') -> '_6938.ConceptCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_2025.CouplingConnection') -> '_6950.CouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6485.CouplingConnectionLoadCase') -> '_6950.CouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COUPLING_CONNECTION_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_2029.SpringDamperConnection') -> '_7017.SpringDamperConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_abstract_shaft(self, design_entity: '_2113.AbstractShaft') -> '_6909.AbstractShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_abstract_shaft_load_case(self, design_entity_analysis: '_6442.AbstractShaftLoadCase') -> '_6909.AbstractShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_2112.AbstractAssembly') -> '_6908.AbstractAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6441.AbstractAssemblyLoadCase') -> '_6908.AbstractAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ABSTRACT_ASSEMBLY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2114.AbstractShaftOrHousing') -> '_6910.AbstractShaftOrHousingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftOrHousingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6443.AbstractShaftOrHousingLoadCase') -> '_6910.AbstractShaftOrHousingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftOrHousingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_2117.Bearing') -> '_6919.BearingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BearingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6454.BearingLoadCase') -> '_6919.BearingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BearingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEARING_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_2119.Bolt') -> '_6930.BoltAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6466.BoltLoadCase') -> '_6930.BoltAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BOLT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_2120.BoltedJoint') -> '_6931.BoltedJointAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltedJointAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6465.BoltedJointLoadCase') -> '_6931.BoltedJointAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltedJointAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BOLTED_JOINT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_2121.Component') -> '_6936.ComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6471.ComponentLoadCase') -> '_6936.ComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_COMPONENT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_2124.Connector') -> '_6947.ConnectorAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6484.ConnectorLoadCase') -> '_6947.ConnectorAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONNECTOR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_2125.Datum') -> '_6964.DatumAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.DatumAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6503.DatumLoadCase') -> '_6964.DatumAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.DatumAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_DATUM_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_2128.ExternalCADModel') -> '_6965.ExternalCADModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ExternalCADModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6518.ExternalCADModelLoadCase') -> '_6965.ExternalCADModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ExternalCADModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_EXTERNAL_CAD_MODEL_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_fe_part(self, design_entity: '_2129.FEPart') -> '_6969.FEPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FEPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FE_PART](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_fe_part_load_case(self, design_entity_analysis: '_6522.FEPartLoadCase') -> '_6969.FEPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FEPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FE_PART_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_2130.FlexiblePinAssembly') -> '_6970.FlexiblePinAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FlexiblePinAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6523.FlexiblePinAssemblyLoadCase') -> '_6970.FlexiblePinAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FlexiblePinAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_2111.Assembly') -> '_6918.AssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6453.AssemblyLoadCase') -> '_6918.AssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ASSEMBLY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_2131.GuideDxfModel') -> '_6974.GuideDxfModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GuideDxfModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6531.GuideDxfModelLoadCase') -> '_6974.GuideDxfModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GuideDxfModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_GUIDE_DXF_MODEL_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_2138.MassDisc') -> '_6989.MassDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MassDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6558.MassDiscLoadCase') -> '_6989.MassDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MassDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_MASS_DISC_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_2139.MeasurementComponent') -> '_6990.MeasurementComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MeasurementComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6559.MeasurementComponentLoadCase') -> '_6990.MeasurementComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MeasurementComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_MEASUREMENT_COMPONENT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_2140.MountableComponent') -> '_6991.MountableComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6561.MountableComponentLoadCase') -> '_6991.MountableComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_MOUNTABLE_COMPONENT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_2142.OilSeal') -> '_6992.OilSealAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.OilSealAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6563.OilSealLoadCase') -> '_6992.OilSealAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.OilSealAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_OIL_SEAL_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_2144.Part') -> '_6993.PartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PART](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6565.PartLoadCase') -> '_6993.PartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PART_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_2145.PlanetCarrier') -> '_6999.PlanetCarrierAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetCarrierAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6572.PlanetCarrierLoadCase') -> '_6999.PlanetCarrierAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetCarrierAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PLANET_CARRIER_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_2147.PointLoad') -> '_7000.PointLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PointLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6575.PointLoadLoadCase') -> '_7000.PointLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PointLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_POINT_LOAD_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_2148.PowerLoad') -> '_7001.PowerLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PowerLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6576.PowerLoadLoadCase') -> '_7001.PowerLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PowerLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_POWER_LOAD_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_2150.RootAssembly') -> '_7008.RootAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RootAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6585.RootAssemblyLoadCase') -> '_7008.RootAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RootAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_ROOT_ASSEMBLY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_2152.SpecialisedAssembly') -> '_7012.SpecialisedAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpecialisedAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6589.SpecialisedAssemblyLoadCase') -> '_7012.SpecialisedAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpecialisedAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPECIALISED_ASSEMBLY_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_2153.UnbalancedMass') -> '_7036.UnbalancedMassAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.UnbalancedMassAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6620.UnbalancedMassLoadCase') -> '_7036.UnbalancedMassAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.UnbalancedMassAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_UNBALANCED_MASS_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_2154.VirtualComponent') -> '_7037.VirtualComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.VirtualComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6621.VirtualComponentLoadCase') -> '_7037.VirtualComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.VirtualComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_VIRTUAL_COMPONENT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_2157.Shaft') -> '_7009.ShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6587.ShaftLoadCase') -> '_7009.ShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SHAFT_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2195.ConceptGear') -> '_6940.ConceptGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6475.ConceptGearLoadCase') -> '_6940.ConceptGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2196.ConceptGearSet') -> '_6942.ConceptGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6477.ConceptGearSetLoadCase') -> '_6942.ConceptGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2202.FaceGear') -> '_6966.FaceGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6519.FaceGearLoadCase') -> '_6966.FaceGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FACE_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2203.FaceGearSet') -> '_6968.FaceGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6521.FaceGearSetLoadCase') -> '_6968.FaceGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_FACE_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2187.AGMAGleasonConicalGear') -> '_6915.AGMAGleasonConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6448.AGMAGleasonConicalGearLoadCase') -> '_6915.AGMAGleasonConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2188.AGMAGleasonConicalGearSet') -> '_6917.AGMAGleasonConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6450.AGMAGleasonConicalGearSetLoadCase') -> '_6917.AGMAGleasonConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2189.BevelDifferentialGear') -> '_6922.BevelDifferentialGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6457.BevelDifferentialGearLoadCase') -> '_6922.BevelDifferentialGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2190.BevelDifferentialGearSet') -> '_6924.BevelDifferentialGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6459.BevelDifferentialGearSetLoadCase') -> '_6924.BevelDifferentialGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2191.BevelDifferentialPlanetGear') -> '_6925.BevelDifferentialPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6460.BevelDifferentialPlanetGearLoadCase') -> '_6925.BevelDifferentialPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2192.BevelDifferentialSunGear') -> '_6926.BevelDifferentialSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6461.BevelDifferentialSunGearLoadCase') -> '_6926.BevelDifferentialSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2193.BevelGear') -> '_6927.BevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6462.BevelGearLoadCase') -> '_6927.BevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2194.BevelGearSet') -> '_6929.BevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6464.BevelGearSetLoadCase') -> '_6929.BevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2197.ConicalGear') -> '_6943.ConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6478.ConicalGearLoadCase') -> '_6943.ConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2198.ConicalGearSet') -> '_6945.ConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6482.ConicalGearSetLoadCase') -> '_6945.ConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2199.CylindricalGear') -> '_6959.CylindricalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6495.CylindricalGearLoadCase') -> '_6959.CylindricalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2200.CylindricalGearSet') -> '_6961.CylindricalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6499.CylindricalGearSetLoadCase') -> '_6961.CylindricalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2201.CylindricalPlanetGear') -> '_6963.CylindricalPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6500.CylindricalPlanetGearLoadCase') -> '_6963.CylindricalPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_PLANET_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2204.Gear') -> '_6971.GearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6525.GearLoadCase') -> '_6971.GearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2206.GearSet') -> '_6973.GearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6530.GearSetLoadCase') -> '_6973.GearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2208.HypoidGear') -> '_6975.HypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6542.HypoidGearLoadCase') -> '_6975.HypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2209.HypoidGearSet') -> '_6977.HypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6544.HypoidGearSetLoadCase') -> '_6977.HypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2210.KlingelnbergCycloPalloidConicalGear') -> '_6979.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6549.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_6979.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2211.KlingelnbergCycloPalloidConicalGearSet') -> '_6981.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6551.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_6981.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2212.KlingelnbergCycloPalloidHypoidGear') -> '_6982.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6552.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_6982.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2213.KlingelnbergCycloPalloidHypoidGearSet') -> '_6984.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6554.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_6984.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2214.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6985.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6555.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_6985.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2215.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6987.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6557.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_6987.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2216.PlanetaryGearSet') -> '_6998.PlanetaryGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6570.PlanetaryGearSetLoadCase') -> '_6998.PlanetaryGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_PLANETARY_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2217.SpiralBevelGear') -> '_7013.SpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6591.SpiralBevelGearLoadCase') -> '_7013.SpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2218.SpiralBevelGearSet') -> '_7015.SpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6593.SpiralBevelGearSetLoadCase') -> '_7015.SpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2219.StraightBevelDiffGear') -> '_7019.StraightBevelDiffGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6598.StraightBevelDiffGearLoadCase') -> '_7019.StraightBevelDiffGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2220.StraightBevelDiffGearSet') -> '_7021.StraightBevelDiffGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6600.StraightBevelDiffGearSetLoadCase') -> '_7021.StraightBevelDiffGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2221.StraightBevelGear') -> '_7022.StraightBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6601.StraightBevelGearLoadCase') -> '_7022.StraightBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2222.StraightBevelGearSet') -> '_7024.StraightBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6603.StraightBevelGearSetLoadCase') -> '_7024.StraightBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2223.StraightBevelPlanetGear') -> '_7025.StraightBevelPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6604.StraightBevelPlanetGearLoadCase') -> '_7025.StraightBevelPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2224.StraightBevelSunGear') -> '_7026.StraightBevelSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6605.StraightBevelSunGearLoadCase') -> '_7026.StraightBevelSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE](design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2225.WormGear') -> '_7038.WormGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
