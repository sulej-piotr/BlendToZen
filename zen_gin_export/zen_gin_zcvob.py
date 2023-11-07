from mathutils import Quaternion
from mathutils import Vector
import struct
from textwrap import wrap
from .printer import Printer


class ZCVob:
    _objects_count = 2
    _type_name = "zCVob"
    _triangles_limit = 52224
    _visual_object_type_2 = "zCProgMeshProto"
    _visual_object_triangles_limit = 53505
    _static = True
    _show_visual = True
    _collision = True
    __3ds_extension = ".3DS"

    def __init__(self, blender_object, printer: Printer, data_printer):
        self.__blender_object = blender_object
        self.__printer = printer
        self._data_printer = data_printer

    def updated_object_index(self, object_index):
        return object_index + self._objects_count

    def __start_main_object_block(self, object_index):
        self._data_printer.start_object_block(
            type_2=self._type_name,
            triangles_limit=self._triangles_limit,
            object_index=object_index
        )

    @staticmethod
    def _visual_object_index(object_index):
        return object_index + 1

    def _print_additional_data(self):
        pass

    def __print_visual_block(self, object_index):
        self._data_printer.start_object_block(
            type_1="visual",
            type_2=self._visual_object_type_2,
            triangles_limit=self._visual_object_triangles_limit,
            object_index=self._visual_object_index(object_index)
        )
        self._data_printer.end_object_block()

    def __print_ai(self):
        self._data_printer.start_object_block(type_1="ai")
        self._data_printer.end_object_block()

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
        self._data_printer.print_int_property(name="pack", value_int=0)
        self._data_printer.print_string_property(name="presetName", value_string="")
        self._data_printer.print_raw_float_property(name="bbox3DWS", value=self.__bounding_box())
        self._data_printer.print_raw_rotation_property(name="trafoOSToWSRot", value_quaternion=self.__rotation())
        self._data_printer.print_vec3_property(name="trafoOSToWSPos", value_vector=self.__location())
        self._data_printer.print_string_property(name="vobName", value_string=self._printed_vob_name())
        self._data_printer.print_string_property(name="visual", value_string=self._visual())
        self._data_printer.print_bool_property(name="showVisual", value_bool=self._show_visual)
        self._data_printer.print_enum_property(name="visualCamAlign", value_enum_ordinal=0)
        self._data_printer.print_enum_property(name="visualAniMode", value_enum_ordinal=0)
        self._data_printer.print_float_property(name="visualAniModeStrength", value_float=0)
        self._data_printer.print_float_property(name="vobFarClipZScale", value_float=1)
        self._data_printer.print_bool_property(name="cdStatic", value_bool=self._collision)
        self._data_printer.print_bool_property(name="cdDyn", value_bool=self._collision)
        self._data_printer.print_bool_property(name="staticVob", value_bool=self._static)
        self._data_printer.print_enum_property(name="dynShadow", value_enum_ordinal=0)
        self._data_printer.print_int_property(name="zbias", value_int=0)
        self._data_printer.print_bool_property(name="isAmbient", value_bool=False)

    def print(self, object_index):
        self.__start_main_object_block(object_index)
        self.__print_vob_data()
        self.__print_visual_block(object_index=object_index)
        self.__print_ai()
        self._print_additional_data()
        self._data_printer.end_object_block()
        return self.updated_object_index(object_index)
