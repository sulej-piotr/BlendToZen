from .zen_gin_zcvob_ocitem import OCItem
from .zen_gin_zcvob_zcvobspot import ZCVobSpot
from .zen_gin_zcvob import ZCVob
from .zen_gin_zcvob_level_compo import ZCVobLevelCompo
from .printer import Printer


class OCVobTree:

    @staticmethod
    def __vob_order(vob):
        if isinstance(vob, ZCVobLevelCompo):
            return 0
        elif isinstance(vob, ZCVob):
            return 1
        elif isinstance(vob, OCItem):
            return 2
        elif isinstance(vob, ZCVobSpot):
            return 3

    def __create_vob(self, blender_object):
        if blender_object.name.startswith("zCVob:"):
            return ZCVob(blender_object, self.__printer)
        elif blender_object.name.startswith("oCItem:"):
            return OCItem(blender_object, self.__printer)
        elif blender_object.name.startswith("zCVobSpot:"):
            return ZCVobSpot(blender_object, self.__printer)
        elif blender_object.name.startswith("zCVobLevelCompo:"):
            return ZCVobLevelCompo(blender_object, self.__printer)

    def __init__(self, blender_objects, printer: Printer):
        self.__printer = printer
        mapped_vobs = list(map(self.__create_vob, blender_objects))
        filtered_vobs = [i for i in mapped_vobs if i is not None]
        filtered_vobs.sort(key=OCVobTree.__vob_order)
        self.__vob_tree = filtered_vobs

    def nested_objects_count(self):
        nested_objects_index = 0
        for index, vob in enumerate(self.__vob_tree):
            vob: ZCVob = vob
            nested_objects_index = vob.nested_objects_count(nested_objects_index)
        return nested_objects_index

    def __print_vob_tree_block_start(self):
        self.__printer.print("\t[VobTree % 0 0]")

    def __print_vob_tree_block_end(self):
        self.__print_children_count(index=len(self.__vob_tree))
        self.__printer.print("\t[]")

    def __print_end_marker(self):
        self.__printer.print("\t[EndMarker % 0 0]")
        self.__printer.print("\t[]")

    def __print_children_count(self, index):
        children_count = len(self.__vob_tree) if index == 0 else 0
        self.__printer.print("\t\tchilds{index}=int:{children_count}".format(index=index, children_count=children_count))

    def __print_way_net(self):
        self.__printer.print("\t[WayNet % 0 0]")
        self.__printer.print("\t[]")

    def __print_vob(self, vob: ZCVob, index, nested_objects_index):
        self.__print_children_count(index)
        return vob.print(nested_objects_index)

    def __print_vobs(self):
        nested_objects_index = 1
        for index, vob in enumerate(self.__vob_tree):
            nested_objects_index = self.__print_vob(vob, index, nested_objects_index)

    def print(self):
        self.__print_vob_tree_block_start()
        self.__print_vobs()
        self.__print_vob_tree_block_end()
        self.__print_way_net()
        self.__print_end_marker()
