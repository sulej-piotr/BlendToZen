from .zen_gin_zcvob import ZCVob


class ZCVobSpot(ZCVob):
    _nested_objects_count = 1
    _type_name = "zCVobSpot:zCVob"
    _triangles_limit = 52224
    _nested_visual_vob_type = "%"
    _nested_visual_triangles_limit = 0
    _static = False
    _collision = False

    def __init__(self, blender_object, printer):
        super().__init__(blender_object, printer)

    def _visual(self):
        return ""

    def _nested_visual_nested_objects_index(self, nested_objects_index):
        return 0
