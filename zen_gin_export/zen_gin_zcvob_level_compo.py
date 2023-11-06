from .zen_gin_zcvob import ZCVob


class ZCVobLevelCompo(ZCVob):
    _nested_objects_count = 2
    _type_name = "zCVobLevelCompo:zCVob"
    _nested_visual_vob_type = "zCMesh"
    _nested_visual_triangles_limit = 53505
    _static = False
    _collision = False
    _show_visual = False

    def __init__(self, blender_object, printer):
        super().__init__(blender_object, printer)

    def _printed_vob_name(self):
        return "LEVEL-VOB"
