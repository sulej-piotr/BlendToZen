from .zen_gin_ocvobtree import OCVobTree
from .printer import Printer


class ZenArchive:

    def __init__(self, blender_objects, printer: Printer):
        self.__vob_tree = OCVobTree(blender_objects, printer)
        self.__printer = printer

    def __print_archive_start_marker(self):
        self.__printer.print("[% oCWorld:zCWorld 36865 0]")

    def __print_archive_end_marker(self):
        self.__printer.print("[]")

    def __print_header_section_end_marker(self):
        self.__printer.print("END")

    def __objects_count(self):
        return self.__vob_tree.nested_objects_count()

    def __print_metadata(self):
        self.__printer.print("ZenGin Archive")
        self.__printer.print("ver 1")
        self.__printer.print("zCArchiverGeneric")
        self.__printer.print("ASCII")
        self.__printer.print("saveGame 0")
        self.__printer.print("date 1.1.1970 12:0:0")
        self.__printer.print("user BlenderZenGinExportPlugin")
        self.__print_header_section_end_marker()

    def __print_objects(self):
        self.__printer.print("objects {objects_count}".format(objects_count=self.__objects_count()))
        self.__print_header_section_end_marker()

    def print(self):
        self.__print_metadata()
        self.__print_objects()
        self.__printer.print()
        self.__print_archive_start_marker()
        self.__vob_tree.print()
        self.__print_archive_end_marker()
