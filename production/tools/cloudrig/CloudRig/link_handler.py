# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from bpy.app.handlers import persistent
from bpy.types import BlendImportContext, Collection, Context, Object, Text

from .bs_utils.prefs import get_addon_prefs
from .generation.cloudrig import is_generated_cloudrig


@persistent
def cloudrig_append_link_handler(lapp_context: BlendImportContext):
    context = bpy.context
    prefs = get_addon_prefs(context)
    if prefs.improve_link_append == 'DISABLED':
        return
    is_link = 'LINK' in lapp_context.options
    is_instance = 'COLLECTION_INSTANCE' in lapp_context.options
    if is_link and not is_instance:
        return

    root_coll = next(
        (
            item.id
            for item in lapp_context.import_items
            if item and item.id and item.id.id_type == 'COLLECTION' and item.import_info == set()
        ),
        None,
    )
    if not root_coll:
        return

    run_all_scripts = prefs.improve_link_append == 'ALL'
    armature_objs = find_armature_objs(root_coll, cloudrig_only=not run_all_scripts)
    if not armature_objs:
        return
    cleanup(context, root_coll, is_link, run_all_scripts)


def find_armature_objs(coll: Collection, cloudrig_only: bool) -> list[Object]:
    """Return the armatures in coll that are relevant for the current Improve Link/Append tier:
    only CloudRig generated rigs (the "CloudRig" tier), or any Armature at all (the "All" tier)."""
    if cloudrig_only:
        return [obj for obj in coll.all_objects if is_generated_cloudrig(obj)]
    return [obj for obj in coll.all_objects if obj.type == 'ARMATURE']


def cleanup(context: Context, root_coll: Collection, is_link: bool, run_all_scripts: bool):
    if not hasattr(context, 'selected_objects'):
        # This happens on Asset Pipeline push, idk what to tell ya.
        return
    if is_link:
        # File->Link creates the instancer before this handler fires.
        # Asset Browser drag creates it after, so it may not exist yet.
        instancer_empty = next(
            (
                obj
                for obj in context.scene.objects
                if obj.instance_type == 'COLLECTION' and obj.instance_collection == root_coll
            ),
            None,
        )
        if instancer_empty:
            bpy.data.objects.remove(instancer_empty)
        else:
            # HACK: instancer_empty doesn't exist yet after asset browser drag&drop.
            # Schedule removal for the next event loop tick, after the asset
            # browser finishes placing the instancer into the scene.
            def recall():
                cleanup(context, root_coll, is_link, run_all_scripts)

            bpy.app.timers.register(recall, first_interval=0.0)
            return

        # Override the root collection and its contents.
        override_root_coll = root_coll.override_hierarchy_create(context.scene, context.view_layer)
        # Mark root collection as editable override, to enable visibility toggles.
        override_root_coll.override_library.is_system_override = False

        target_coll = override_root_coll
    else:
        target_coll = root_coll

    armature_objs = find_armature_objs(target_coll, cloudrig_only=not run_all_scripts)

    for obj in context.selected_objects:
        obj.select_set(False)

    select_armatures(context, armature_objs)
    # The "All" tier also executes scripts unrelated to any armature; the "CloudRig" tier only
    # executes scripts belonging to the CloudRig generated rigs themselves.
    script_scope = list(target_coll.all_objects) if run_all_scripts else armature_objs
    autorun_scripts_of_objects(context, script_scope)


def select_armatures(context: Context, armature_objs: list[Object], set_editable_override=True):
    for arm_ob in armature_objs:
        if arm_ob.override_library:
            arm_ob.override_library.is_system_override = not set_editable_override
        if arm_ob in set(context.view_layer.objects):
            arm_ob.select_set(True)
    if armature_objs and armature_objs[-1] in set(context.view_layer.objects):
        context.view_layer.objects.active = armature_objs[-1]


def autorun_scripts_of_objects(context: Context, objects: list[Object]):
    if not context.preferences.filepaths.use_scripts_auto_execute:
        return
    datablocks = objects + [obj.data for obj in objects if obj.data]
    for datablock in datablocks:
        for value in datablock.values():
            if isinstance(value, Text) and value.use_module:
                value.as_module()


def register():
    bpy.app.handlers.blend_import_post.append(cloudrig_append_link_handler)


def unregister():
    if cloudrig_append_link_handler in bpy.app.handlers.blend_import_post:
        bpy.app.handlers.blend_import_post.remove(cloudrig_append_link_handler)
