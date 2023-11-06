from .zen_gin_zcvob import ZCVob


class ZCVobLevelCompo(ZCVob):
    _objects_count = 2
    _type_name = "zCVobLevelCompo:zCVob"
    _visual_object_type_2 = "zCMesh"
    _visual_object_triangles_limit = 53505
    _static = False
    _collision = False
    _show_visual = False

    def _printed_vob_name(self):
        return "LEVEL-VOB"
