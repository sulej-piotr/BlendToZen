import zen_gin_export
from mathutils import Quaternion


class DummyBlenderLocation:
    x = 25.0
    y = 15.0
    z = 0.0


class DummyBlenderObject:
    rotation_quaternion = Quaternion((0.0, 0.0, 0.0, 0.0))
    location = DummyBlenderLocation()

    def __init__(self, name):
        self.name = name


zen_gin_export.ZenArchive(
    blender_objects=[
        DummyBlenderObject("zCVob:vob1"),
        DummyBlenderObject("zCVob:vob1.001"),
        DummyBlenderObject("filtering"),
        DummyBlenderObject("oCItem:ITFO_APPLE"),
        DummyBlenderObject("oCItem:ITFO_APPLE.001"),
        DummyBlenderObject("zCVobSpot:FP_ALCHEMIST_01"),
        DummyBlenderObject("zCVobSpot:FP_ALCHEMIST_02"),
    ],
    printer=zen_gin_export.FilePrinter("TEST.ZEN")
).print()
