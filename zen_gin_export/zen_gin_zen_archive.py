from .zen_gin_ocvobtree import OCVobTree
from .zen_gin_waynet import WayNet
from .printer import Printer
from .zen_gin_data_printer import ZenGinDataPrinter


class ZenArchive:

    def __init__(self, blender_objects, printer: Printer):
        self.__printer = printer
        self.__data_printer = ZenGinDataPrinter(printer)
        self.__vob_tree = OCVobTree(blender_objects, printer, self.__data_printer)
        self.__way_net = WayNet(blender_objects, printer, self.__data_printer)

    def __print_header_section_end(self):
        self.__printer.print("END")
        self.__printer.print()

    def __objects_count(self):
        return self.__vob_tree.objects_count()

    def __print_metadata(self):
        self.__printer.print("ZenGin Archive")
        self.__printer.print("ver 1")
        self.__printer.print("zCArchiverGeneric")
        self.__printer.print("ASCII")
        self.__printer.print("saveGame 0")
        self.__printer.print("date 1.1.1970 12:0:0")  # TODO: Use current date
        self.__printer.print("user BlenderZenGinExportPlugin")
        self.__print_header_section_end()

    def print(self):
        self.__print_metadata()
        self.__printer.print("objects {objects_count}".format(objects_count=self.__objects_count()))
        self.__print_header_section_end()
        self.__data_printer.start_object_block(
            type_2="oCWorld:zCWorld",
            triangles_limit=36865,
            object_index=0
        )
        object_index = self.__vob_tree.print(object_index=1)
        self.__way_net.print(object_index=object_index)
        self.__data_printer.start_object_block(type_1="EndMarker")
        self.__data_printer.end_object_block()
        self.__data_printer.end_object_block()
