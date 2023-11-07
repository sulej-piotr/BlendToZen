from .printer import Printer


class ZenGinDataPrinter:

    def __init__(self, printer: Printer):
        self.__printer = printer
        self.__indent_level = 0
        self.__indent = ""

    def __increment_indent(self):
        self.__indent_level += 1
        self.__indent = "\t" * self.__indent_level

    def __decrement_indent(self):
        self.__indent_level -= 1
        self.__indent = "\t" * self.__indent_level

    def start_object_block(self, type_1="%", type_2="%", triangles_limit=0, object_index=0):
        self.__printer.print(self.__indent + "[{type_1} {type_2} {triangles_limit} {object_index}]".format(
            type_1=type_1,
            type_2=type_2,
            triangles_limit=triangles_limit,
            object_index=object_index
        ))
        self.__increment_indent()

    def end_object_block(self):
        self.__decrement_indent()
        self.__printer.print(self.__indent + "[]")

    def __print_property(self, name, data_type, value):
        self.__printer.print(self.__indent + "{name}={data_type}:{value}".format(
            name=name, data_type=data_type, value=value
        ))

    def print_vec3_property(self, name, value_vector):
        self.__print_property(name, "vec3", value_vector)

    def print_raw_rotation_property(self, name, value_quaternion):
        self.__print_property(name, "raw", value_quaternion)

    def print_raw_float_property(self, name, value):
        self.__print_property(name, "rawFloat", value)

    def print_float_property(self, name, value_float):
        self.__print_property(name, "float", value_float)

    def print_enum_property(self, name, value_enum_ordinal):
        self.__print_property(name, "enum", value_enum_ordinal)

    def print_bool_property(self, name, value_bool):
        self.__print_property(name, "bool", 1 if value_bool else 0)

    def print_int_property(self, name, value_int):
        self.__print_property(name, "int", value_int)

    def print_string_property(self, name, value_string):
        self.__print_property(name, "string", value_string)
