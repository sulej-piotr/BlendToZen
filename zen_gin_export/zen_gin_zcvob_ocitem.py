from .zen_gin_zcvob_no_visual import NoVisualObjectVob


class OCItem(NoVisualObjectVob):
    _type_name = "oCItem:zCVob"
    _triangles_limit = 0
    _static = False
    _show_visual = False

    def _visual(self):
        return ""

    def _print_additional_data(self):
        self._data_printer.print_string_property("itemInstance", self._vob_name())
