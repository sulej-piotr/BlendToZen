from .printer import Printer
from mathutils import Quaternion
from .zen_gin_data_printer import ZenGinDataPrinter


class WayNet:

    def __init__(self, blender_objects, printer: Printer, data_printer: ZenGinDataPrinter):
        self.__printer = printer
        self.__data_printer = data_printer
        self.__way_net = []
        self.objects_count = 1
        for blender_object in blender_objects:
            if blender_object.name.startswith("zCWaypoint:"):
                self.objects_count += 1
                if blender_object.modifiers[0].get("Input_2"):
                    self.__way_net.append((blender_object, blender_object.modifiers[0].get("Input_2")))
                if blender_object.modifiers[0].get("Input_3"):
                    self.__way_net.append((blender_object, blender_object.modifiers[0].get("Input_3")))
                if blender_object.modifiers[0].get("Input_4"):
                    self.__way_net.append((blender_object, blender_object.modifiers[0].get("Input_4")))

    @staticmethod
    def __waypoint_location(waypoint):
        return "{x} {z} {y}".format(
            x=waypoint.location.x * -100,
            y=waypoint.location.y * -100,
            z=waypoint.location.z * 100,
        )

    @staticmethod
    def __waypoint_rotation_vec3(waypoint):
        qt: Quaternion = waypoint.rotation_quaternion
        new_qt = Quaternion((-qt[3], qt[2], -qt[0], -qt[1]))
        vector = new_qt.to_matrix()[2]
        return "{x} {y} {z}".format(x=-vector.x, y=vector.y, z=vector.z)

    def __print_waypoint(self, waypoint, side, way_index, object_index, defined_waypoints):
        waypoint_definition = None
        for defined_waypoint in defined_waypoints:
            if defined_waypoint[0] == waypoint.name:
                waypoint_definition = defined_waypoint
                break
        if waypoint_definition:
            self.__data_printer.start_object_block(
                type_1="way{side}{way_index}".format(way_index=way_index, side=side),
                type_2="§",
                object_index=waypoint_definition[1]
            )
            self.__data_printer.end_object_block()
            return object_index
        else:
            self.__data_printer.start_object_block(
                type_1="way{side}{way_index}".format(way_index=way_index, side=side),
                type_2="zCWaypoint",
                object_index=object_index
            )
            self.__data_printer.print_string_property("wpName", waypoint.name.removeprefix("zCWaypoint:"))
            self.__data_printer.print_int_property("waterDepth", 0)
            self.__data_printer.print_int_property("underWater", 0)
            self.__data_printer.print_vec3_property("position", self.__waypoint_location(waypoint))
            self.__data_printer.print_vec3_property("direction", self.__waypoint_rotation_vec3(waypoint))
            self.__data_printer.end_object_block()
            defined_waypoints.append((waypoint.name, object_index))
            return object_index + 1

    def print(self, object_index):
        self.__data_printer.start_object_block(type_1="WayNet")
        self.__data_printer.start_object_block(
            type_1="%",
            type_2="zCWayNet",
            object_index=object_index
        )
        object_index += 1
        self.__data_printer.print_int_property("waynetVersion", 1)
        self.__data_printer.print_int_property("numWaypoints", 0)
        self.__data_printer.print_int_property("numWays", len(self.__way_net))
        defined_waypoints = []
        for way_index, way in enumerate(self.__way_net):
            object_index = self.__print_waypoint(
                waypoint=way[0], side="l", way_index=way_index, object_index=object_index,
                defined_waypoints=defined_waypoints
            )
            object_index = self.__print_waypoint(
                waypoint=way[1], side="r", way_index=way_index, object_index=object_index,
                defined_waypoints=defined_waypoints
            )
        self.__data_printer.end_object_block()
        self.__data_printer.end_object_block()
        return object_index

