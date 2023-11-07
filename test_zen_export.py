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
        self.modifiers: list[dict[str]] = [{}]

    def link_to_waypoints(self, modifiers):
        self.modifiers = modifiers


wp_1 = DummyBlenderObject("zCWaypoint:WAYPOINT_01")
wp_2 = DummyBlenderObject("zCWaypoint:WAYPOINT_02")
wp_3 = DummyBlenderObject("zCWaypoint:WAYPOINT_03")
wp_4 = DummyBlenderObject("zCWaypoint:WAYPOINT_04")
wp_1.link_to_waypoints([{"Input_2": wp_2, "Input_3": wp_4}])
wp_2.link_to_waypoints([{"Input_2": wp_3}])
zen_gin_export.ZenArchive(
    blender_objects=[
        DummyBlenderObject("zCVob:vob1"),
        DummyBlenderObject("filtering"),
        DummyBlenderObject("oCItem:ITFO_APPLE.001"),
        DummyBlenderObject("zCVobSpot:FP_ALCHEMIST_01"),
        DummyBlenderObject("zCVob:vob1.001"),
        DummyBlenderObject("zCVobSpot:FP_ALCHEMIST_02"),
        DummyBlenderObject("oCItem:ITFO_APPLE"),
        DummyBlenderObject("zCVobLevelCompo:SUKIENNICE_13"),
        wp_1,
        wp_2,
        wp_3,
        wp_4,
    ],
    printer=zen_gin_export.FilePrinter("TEST.ZEN")
).print()
