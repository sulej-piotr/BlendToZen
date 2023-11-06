from .zen_gin_zcvob import ZCVob


class NoVisualObjectVob(ZCVob):
    _objects_count = 1
    _visual_object_type_2 = "%"
    _visual_object_triangles_limit = 0

    def _visual_object_index(self, object_index):
        return 0
