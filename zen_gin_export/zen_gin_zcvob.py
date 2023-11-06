from mathutils import Quaternion
from mathutils import Vector
import struct
from textwrap import wrap
from .printer import Printer


class ZCVob:
    _nested_objects_count = 2
    _type_name = "zCVob"
    _triangles_limit = 52224
    _nested_visual_vob_type = "zCProgMeshProto"
    _nested_visual_triangles_limit = 53505
    _static = True
    _show_visual = True
    _collision = True
    __3ds_extension = ".3DS"
    __end_block_marker = "[]"

    def __init__(self, blender_object, printer: Printer):
        self.__blender_object = blender_object
        self.__printer = printer

    def nested_objects_count(self, nested_objects_index):
        return nested_objects_index + self._nested_objects_count

    @staticmethod
    def get_object_block_marker_indent(is_nested):
        return "\t\t\t" if is_nested else "\t\t"

    def _start_object_block(self, object_type, vob_type, triangles_limit, nested_objects_index, is_nested):
        indent = self.get_object_block_marker_indent(is_nested=is_nested)
        self.__printer.print(indent + "[{object_type} {vob_type} {triangles_limit} {nested_objects_index}]".format(
            object_type=object_type,
            triangles_limit=triangles_limit,
            vob_type=vob_type,
            nested_objects_index=nested_objects_index
        ))

    def __start_main_object_block(self, nested_objects_index):
        self._start_object_block(
            object_type="%",
            vob_type=self._type_name,
            triangles_limit=self._triangles_limit,
            nested_objects_index=nested_objects_index,
            is_nested=False
        )

    def _end_object_block(self, is_nested):
        indent = self.get_object_block_marker_indent(is_nested=is_nested)
        self.__printer.print(indent + self.__end_block_marker)

    @staticmethod
    def _nested_visual_nested_objects_index(nested_objects_index):
        return nested_objects_index + 1

    def _print_additional_data(self):
        pass

    def __print_nested_visual(self, nested_objects_index):
        self._start_object_block(
            object_type="visual",
            vob_type=self._nested_visual_vob_type,
            triangles_limit=self._nested_visual_triangles_limit,
            nested_objects_index=self._nested_visual_nested_objects_index(nested_objects_index),
            is_nested=True
        )
        self._end_object_block(True)

    def __print_ai(self):
        self._start_object_block(
            object_type="ai",
            vob_type="%",
            triangles_limit=0,
            nested_objects_index=0,
            is_nested=True
        )
        self._end_object_block(True)

    def __print_property(self, name, data_type, value):
        self.__printer.print("\t\t\t{name}={data_type}:{value}".format(
            name=name, data_type=data_type, value=value
        ))

    def _print_vec3_property(self, name, value_vector):
        self.__print_property(name, "vec3", value_vector)

    def _print_raw_rotation_property(self, name, value_quaternion):
        self.__print_property(name, "raw", value_quaternion)

    def _print_raw_float_property(self, name, value):
        self.__print_property(name, "rawFloat", value)

    def _print_float_property(self, name, value_float):
        self.__print_property(name, "float", value_float)

    def _print_enum_property(self, name, value_enum_ordinal):
        self.__print_property(name, "enum", value_enum_ordinal)

    def _print_bool_property(self, name, value_bool):
        self.__print_property(name, "bool", 1 if value_bool else 0)

    def _print_int_property(self, name, value_int):
        self.__print_property(name, "int", value_int)

    def _print_string_property(self, name, value_string):
        self.__print_property(name, "string", value_string)

    def _vob_name(self):
        return self.__blender_object.name.split(":")[-1].split(".")[0]

    def _printed_vob_name(self):
        return self._vob_name()

    def _visual(self):
        return self._vob_name() + self.__3ds_extension

    def __bounding_box(self):
        return "{start} {end}".format(
            start=self.__location(),
            end=self.__location()
        )

    def __location(self):
        return "{x} {z} {y}".format(
            x=self.__blender_object.location.x * -100,
            y=self.__blender_object.location.y * -100,
            z=self.__blender_object.location.z * 100,
        )

    @staticmethod
    def float_to_hex(to_convert: float):
        r = round(to_convert, 6)
        h = hex(struct.unpack('<I', struct.pack('<f', r))[0]).split("0x")[1]
        if h == "0":
            return "00000000"
        h_a = wrap(h, 2)
        return h_a[3] + h_a[2] + h_a[1] + h_a[0]

    @staticmethod
    def convert_vector(vector: Vector):
        return "".join([
            ZCVob.float_to_hex(vector.x),
            ZCVob.float_to_hex(vector.y),
            ZCVob.float_to_hex(vector.z)
        ])

    def __rotation(self):
        qt: Quaternion = self.__blender_object.rotation_quaternion
        new_qt = Quaternion((-qt[3], qt[2], -qt[0], -qt[1]))
        return "".join(map(ZCVob.convert_vector, new_qt.to_matrix()))

    def __print_vob_data(self):
        self._print_int_property(name="pack", value_int=0)
        self._print_string_property(name="presetName", value_string="")
        self._print_raw_float_property(name="bbox3DWS", value=self.__bounding_box())
        self._print_raw_rotation_property(name="trafoOSToWSRot", value_quaternion=self.__rotation())
        self._print_vec3_property(name="trafoOSToWSPos", value_vector=self.__location())
        self._print_string_property(name="vobName", value_string=self._printed_vob_name())
        self._print_string_property(name="visual", value_string=self._visual())
        self._print_bool_property(name="showVisual", value_bool=self._show_visual)
        self._print_enum_property(name="visualCamAlign", value_enum_ordinal=0)
        self._print_enum_property(name="visualAniMode", value_enum_ordinal=0)
        self._print_float_property(name="visualAniModeStrength", value_float=0)
        self._print_float_property(name="vobFarClipZScale", value_float=1)
        self._print_bool_property(name="cdStatic", value_bool=self._collision)
        self._print_bool_property(name="cdDyn", value_bool=self._collision)
        self._print_bool_property(name="staticVob", value_bool=self._static)
        self._print_enum_property(name="dynShadow", value_enum_ordinal=0)
        self._print_int_property(name="zbias", value_int=0)
        self._print_bool_property(name="isAmbient", value_bool=False)

    def print(self, nested_objects_index):
        self.__start_main_object_block(nested_objects_index)
        self.__print_vob_data()
        self.__print_nested_visual(nested_objects_index=nested_objects_index)
        self.__print_ai()
        self._print_additional_data()
        self._end_object_block(False)
        return self.nested_objects_count(nested_objects_index)
