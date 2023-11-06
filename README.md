# Blender ZenGin export Python module

This module can be used to export ZEN files based on the scenes created in Blender.

## Scene preparation

Objects in scene need to follow some conventions in order to be correctly exported as `.zen` file.

- Object name needs to start with type of ZenGin object followed by colon and then followed by object's name.
- Dot (`.`) character in object's name and everything after first dot will be ignored. Thanks to this you can copy objects and `zCVob:NW_CITY_MARKETSTALL_JUNKSHOP_01` will be exported in the same way as `zCVob:NW_CITY_MARKETSTALL_JUNKSHOP_01.001`.
- Object name has different function depending on vob type.

### Supported types and their object name function

#### zCVob
Name of the mesh without `.3ds` extension should be used as object name. E.g. `zCVob:NW_CITY_DECO_SWORDFISH_01` will be exported as `zCVob` that uses `NW_CITY_DECO_SWORDFISH_01.3DS` mesh. 

#### oCItem
Item instance should be used as object name. E.g. `oCItem:ITMI_BROOM` will be exported as instance of `ITMI_BROOM`.

#### zCVobSpot
Name of your object will be used as freepoint name. E.g. `zCVobSpot:FP_STAND_ALCHEMIST_01` will be exported `FP_STAND_ALCHEMIST_01` freepoint that can be used by NPCs during `TA_Stand_*` routines.

#### zCVobLevelCompo
You should use name of your world's mesh, without `.3ds` extension. E.g. if your object is named `zCVobLevelCompo:NewWorld_Part_City_P01.3ds`, then `NewWorld_Part_City_P01.3ds` will be used as your world's mesh.

## How to use this module

- Copy `zen_gin_export` directory to `python\lib` directory of your Blender installation.
- Start Blender, or restart it, if it was already started.
- Open `example_zen_export.py` inside Blender ([check how to run Python script in Blender](https://docs.blender.org/api/current/info_quickstart.html#running-scripts)).
- Adjust `gothic_directory` to match the directory of your **Gothic 2** installation.
- Run the script, it will export `UNCOMPILED_EXPORT.ZEN` into `Plugin` subdirectory of `Work\Data\Worlds` directory of your **Gothic 2** installation.
- Load `.zen` file into Spacer, compile the world and light, save it as compiled `.zen` and use it as you wish.

## Loading Gothic meshes into Blender

Meshes can be loaded into Blender using KrxImpExp plugin. Script for loading Gothic meshes in batch and generating assets with names that are following object's naming convention required by this plugin will be added to this repository in the future.

## Testing this script without Blender

Fake `mathutils` module allows to test this plugin by running `test_zen_export.py` in Python IDE of your choice (tested in PyCharm).

## Plans for future of this project

First of all, I want to rewrite remaining parts of quick prototype that I've created. This includes WayNet support (using geometry nodes to visualise connections between the waypoints) and generating assets from ``Gothic`` scripts (items) and meshes.

Later on I will be using this module for creation of my small ZEN and slowly adding more types of objects that I will need in this ZEN. I definitely need `oCMobInter`, `oCZoneMusicDefault` and `zCVobStartpoint`, maybe also `zCVobLight` and few more.

Later on, after finishing my ZEN I will consider three options:
- Adding possibility to merge scenes created in Blender with other `.zen` files. That way it would be possible to set up most of your objects in Blender, add some less frequently used ones (triggers, camera keyframes) in Spacer and use them together.
- Adding support for all types of objects available in Spacer.
- Leaving the project as it is (maybe someone else would like to continue its development).

First one seems to be more realistic scenario, but we'll see.

### Known issues
- Bounding boxes do not consider size of the object - this can lead to some issues with LOD.