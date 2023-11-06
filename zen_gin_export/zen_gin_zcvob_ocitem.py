from .zen_gin_zcvob import ZCVob


class OCItem(ZCVob):
    _objects_count = 1
    _type_name = "oCItem:zCVob"
    _triangles_limit = 0
    _nested_visual_vob_type = "%"
    _nested_visual_triangles_limit = 0
    _static = False
    _show_visual = False

    def _visual(self):
        return ""

    def _visual_object_index(self, object_index):
        return 0

    def _print_additional_data(self):
        self._data_printer.print_string_property("itemInstance", self._vob_name())
