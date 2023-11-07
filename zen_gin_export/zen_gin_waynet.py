from .printer import Printer
from .zen_gin_data_printer import ZenGinDataPrinter


class WayNet:

    def __init__(self, blender_objects, printer: Printer, data_printer: ZenGinDataPrinter):
        self.__printer = printer
        self.__data_printer = data_printer

    def print(self, object_index):
        self.__data_printer.start_object_block(type_1="WayNet")
        self.__data_printer.start_object_block(
            type_1="%",
            type_2="zCWayNet",
            object_index=object_index  # TODO: pass index
        )
        object_index += 1
        self.__data_printer.print_int_property("waynetVersion", 1)
        self.__data_printer.print_int_property("numWaypoints", 0)
        self.__data_printer.print_int_property("numWays", 0)
        self.__data_printer.end_object_block()
        self.__data_printer.end_object_block()
        return object_index

