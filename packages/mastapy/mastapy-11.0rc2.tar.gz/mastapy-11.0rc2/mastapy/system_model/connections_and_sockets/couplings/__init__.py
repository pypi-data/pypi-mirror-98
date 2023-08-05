'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2021 import ClutchConnection
    from ._2022 import ClutchSocket
    from ._2023 import ConceptCouplingConnection
    from ._2024 import ConceptCouplingSocket
    from ._2025 import CouplingConnection
    from ._2026 import CouplingSocket
    from ._2027 import PartToPartShearCouplingConnection
    from ._2028 import PartToPartShearCouplingSocket
    from ._2029 import SpringDamperConnection
    from ._2030 import SpringDamperSocket
    from ._2031 import TorqueConverterConnection
    from ._2032 import TorqueConverterPumpSocket
    from ._2033 import TorqueConverterTurbineSocket
