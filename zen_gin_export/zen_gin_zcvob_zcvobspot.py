from .zen_gin_zcvob import ZCVob


class ZCVobSpot(ZCVob):
    _objects_count = 1
    _type_name = "zCVobSpot:zCVob"
    _triangles_limit = 52224
    _nested_visual_vob_type = "%"
    _nested_visual_triangles_limit = 0
    _static = False
    _collision = False

    def _visual(self):
        return ""

    def _visual_object_index(self, object_index):
        return 0
