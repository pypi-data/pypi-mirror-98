'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2285 import ActiveFESubstructureSelection
    from ._2286 import ActiveFESubstructureSelectionGroup
    from ._2287 import ActiveShaftDesignSelection
    from ._2288 import ActiveShaftDesignSelectionGroup
    from ._2289 import BearingDetailConfiguration
    from ._2290 import BearingDetailSelection
    from ._2291 import PartDetailConfiguration
    from ._2292 import PartDetailSelection
