import bpy
import zen_gin_export

gothic_directory = "C:\\Program Files (x86)\\GOG Galaxy\\Games\\Gothic II\\"
worlds_directory = gothic_directory + "_Work\\Data\\Worlds\\"
zen_gin_export.ZenArchive(
    blender_objects=bpy.data.objects,
    printer=zen_gin_export.FilePrinter(worlds_directory + "Plugin\\UNCOMPILED_EXPORT.ZEN")
).print()
