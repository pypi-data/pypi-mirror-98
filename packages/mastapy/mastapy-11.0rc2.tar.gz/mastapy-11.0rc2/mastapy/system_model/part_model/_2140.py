'''_2140.py

MountableComponent
'''


from typing import Optional

from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1955, _1945, _1946, _1953,
    _1958, _1959, _1961, _1962,
    _1963, _1964, _1965, _1967,
    _1968, _1969, _1972, _1973,
    _1951, _1944, _1947, _1948,
    _1952, _1960, _1966, _1971,
    _1974
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1989, _1978, _1980, _1982,
    _1984, _1986, _1988, _1990,
    _1992, _1994, _1997, _1998,
    _1999, _2002, _2004, _2006,
    _2008, _2010
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2012, _2013, _2015, _2016,
    _2018, _2019, _2014, _2017,
    _2020
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2022, _2024, _2026, _2028,
    _2030, _2032, _2033, _2021,
    _2023, _2025, _2027, _2029,
    _2031
)
from mastapy.system_model.part_model import _2113, _2122, _2121
from mastapy.system_model.part_model.shaft_model import _2157
from mastapy.system_model.part_model.cycloidal import _2243
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponent',)


class MountableComponent(_2121.Component):
    '''MountableComponent

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rotation_about_axis(self) -> 'float':
        '''float: 'RotationAboutAxis' is the original name of this property.'''

        return self.wrapped.RotationAboutAxis

    @rotation_about_axis.setter
    def rotation_about_axis(self, value: 'float'):
        self.wrapped.RotationAboutAxis = float(value) if value else 0.0

    @property
    def inner_socket(self) -> '_1955.CylindricalSocket':
        '''CylindricalSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1955.CylindricalSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_bearing_inner_socket(self) -> '_1945.BearingInnerSocket':
        '''BearingInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.BearingInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to BearingInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_bearing_outer_socket(self) -> '_1946.BearingOuterSocket':
        '''BearingOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.BearingOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to BearingOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cvt_pulley_socket(self) -> '_1953.CVTPulleySocket':
        '''CVTPulleySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1953.CVTPulleySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_inner_shaft_socket(self) -> '_1958.InnerShaftSocket':
        '''InnerShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1958.InnerShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_inner_shaft_socket_base(self) -> '_1959.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.InnerShaftSocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_mountable_component_inner_socket(self) -> '_1961.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1961.MountableComponentInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_mountable_component_outer_socket(self) -> '_1962.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.MountableComponentOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_mountable_component_socket(self) -> '_1963.MountableComponentSocket':
        '''MountableComponentSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.MountableComponentSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_outer_shaft_socket(self) -> '_1964.OuterShaftSocket':
        '''OuterShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.OuterShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_outer_shaft_socket_base(self) -> '_1965.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.OuterShaftSocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_planetary_socket(self) -> '_1967.PlanetarySocket':
        '''PlanetarySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1967.PlanetarySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_planetary_socket_base(self) -> '_1968.PlanetarySocketBase':
        '''PlanetarySocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1968.PlanetarySocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_pulley_socket(self) -> '_1969.PulleySocket':
        '''PulleySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.PulleySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PulleySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_rolling_ring_socket(self) -> '_1972.RollingRingSocket':
        '''RollingRingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1972.RollingRingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_shaft_socket(self) -> '_1973.ShaftSocket':
        '''ShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.ShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_1989.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.CylindricalGearTeethSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2012.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2013.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cycloidal_disc_inner_socket(self) -> '_2015.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2015.CycloidalDiscInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cycloidal_disc_outer_socket(self) -> '_2016.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.CycloidalDiscOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2018.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_ring_pins_socket(self) -> '_2019.RingPinsSocket':
        '''RingPinsSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.RingPinsSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to RingPinsSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_clutch_socket(self) -> '_2022.ClutchSocket':
        '''ClutchSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.ClutchSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ClutchSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_concept_coupling_socket(self) -> '_2024.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.ConceptCouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_coupling_socket(self) -> '_2026.CouplingSocket':
        '''CouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.CouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2028.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.PartToPartShearCouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_spring_damper_socket(self) -> '_2030.SpringDamperSocket':
        '''SpringDamperSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.SpringDamperSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_torque_converter_pump_socket(self) -> '_2032.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.TorqueConverterPumpSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_socket_of_type_torque_converter_turbine_socket(self) -> '_2033.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.TorqueConverterTurbineSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket else None

    @property
    def inner_connection(self) -> '_1951.Connection':
        '''Connection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1951.Connection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to Connection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1944.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1944.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_belt_connection(self) -> '_1947.BeltConnection':
        '''BeltConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1947.BeltConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BeltConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_coaxial_connection(self) -> '_1948.CoaxialConnection':
        '''CoaxialConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1948.CoaxialConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CoaxialConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_cvt_belt_connection(self) -> '_1952.CVTBeltConnection':
        '''CVTBeltConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1952.CVTBeltConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CVTBeltConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_inter_mountable_component_connection(self) -> '_1960.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1960.InterMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_planetary_connection(self) -> '_1966.PlanetaryConnection':
        '''PlanetaryConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1966.PlanetaryConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to PlanetaryConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_rolling_ring_connection(self) -> '_1971.RollingRingConnection':
        '''RollingRingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1971.RollingRingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to RollingRingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_shaft_to_mountable_component_connection(self) -> '_1974.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.ShaftToMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_1978.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1978.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_bevel_differential_gear_mesh(self) -> '_1980.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1980.BevelDifferentialGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_bevel_gear_mesh(self) -> '_1982.BevelGearMesh':
        '''BevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.BevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_concept_gear_mesh(self) -> '_1984.ConceptGearMesh':
        '''ConceptGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.ConceptGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConceptGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_conical_gear_mesh(self) -> '_1986.ConicalGearMesh':
        '''ConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1986.ConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_cylindrical_gear_mesh(self) -> '_1988.CylindricalGearMesh':
        '''CylindricalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.CylindricalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_face_gear_mesh(self) -> '_1990.FaceGearMesh':
        '''FaceGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.FaceGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to FaceGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_gear_mesh(self) -> '_1992.GearMesh':
        '''GearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.GearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to GearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_hypoid_gear_mesh(self) -> '_1994.HypoidGearMesh':
        '''HypoidGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.HypoidGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to HypoidGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1997.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1998.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1999.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_spiral_bevel_gear_mesh(self) -> '_2002.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.SpiralBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_2004.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.StraightBevelDiffGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_straight_bevel_gear_mesh(self) -> '_2006.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.StraightBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_worm_gear_mesh(self) -> '_2008.WormGearMesh':
        '''WormGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.WormGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to WormGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_zerol_bevel_gear_mesh(self) -> '_2010.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.ZerolBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2014.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2017.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_ring_pins_to_disc_connection(self) -> '_2020.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.RingPinsToDiscConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_clutch_connection(self) -> '_2021.ClutchConnection':
        '''ClutchConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.ClutchConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ClutchConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_concept_coupling_connection(self) -> '_2023.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.ConceptCouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_coupling_connection(self) -> '_2025.CouplingConnection':
        '''CouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.CouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2027.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.PartToPartShearCouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_spring_damper_connection(self) -> '_2029.SpringDamperConnection':
        '''SpringDamperConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.SpringDamperConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to SpringDamperConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def inner_connection_of_type_torque_converter_connection(self) -> '_2031.TorqueConverterConnection':
        '''TorqueConverterConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.TorqueConverterConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection else None

    @property
    def is_mounted(self) -> 'bool':
        '''bool: 'IsMounted' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsMounted

    @property
    def inner_component(self) -> '_2113.AbstractShaft':
        '''AbstractShaft: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2113.AbstractShaft.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to AbstractShaft. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent else None

    @property
    def inner_component_of_type_shaft(self) -> '_2157.Shaft':
        '''Shaft: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2157.Shaft.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to Shaft. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent else None

    @property
    def inner_component_of_type_cycloidal_disc(self) -> '_2243.CycloidalDisc':
        '''CycloidalDisc: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2243.CycloidalDisc.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to CycloidalDisc. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent else None

    def try_mount_on(self, shaft: '_2113.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2122.ComponentsConnectedResult':
        ''' 'TryMountOn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryMountOn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def mount_on(self, shaft: '_2113.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_1948.CoaxialConnection':
        ''' 'MountOn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.CoaxialConnection
        '''

        offset = float(offset)
        method_result = self.wrapped.MountOn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
