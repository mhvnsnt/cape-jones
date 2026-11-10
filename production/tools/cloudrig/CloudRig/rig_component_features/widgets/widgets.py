# SPDX-License-Identifier: GPL-3.0-or-later

import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import bpy
from bpy.types import ID, Context, ImagePreview, Object, Operator, PoseBone, Text
from mathutils import Euler, Vector

from ...bs_utils.prefs import get_addon_prefs
from ...icons import ensure_icon

CLOUDRIG_WIDGETS: dict[str, ImagePreview] = {}
EXTERNAL_WIDGETS: dict[str, ImagePreview] = {}
LOCAL_WIDGETS: dict[str, ImagePreview] = {}


def ensure_widget(wgt_name: str, overwrite=True, clear_asset=True) -> Object:
    """Ensure a singular custom shape. Less performant compared to bulk-loading with `ensure_widgets`."""
    wgt_name = widget_name(wgt_name)
    widgets = ensure_widgets([wgt_name], overwrite=overwrite, clear_asset=clear_asset)
    if wgt_name not in widgets:
        # Widget wasn't found in any of our lists, AND we didn't find one locally... So, we are sad.
        raise ValueError(f"Widget not found: '{wgt_name}'")
    return widgets[wgt_name]


def ensure_widgets(wgt_names: Iterable[str], overwrite=True, clear_asset=True) -> dict[str, Object]:
    """Ensure multiple custom shapes exist, with a single library load per source .blend.
    1. If the widget is in the current .blend file already, return it (unless we want to overwrite or link)
    2. Try to append/link it from the external .blend the user may have specified in the preferences.
    3. If that fails, try to append/link it from the Widgets.blend that ships with the add-on.
    Returns a dict of widget names (without "WGT-" prefix) to objects. Widgets that weren't found are left out.
    """

    refresh_widget_list()

    # Without add-on preferences, fall back to appending, and only from CloudRig's own widget library.
    prefs = get_addon_prefs()
    prefer_linked = bool(prefs) and prefs.widget_import_method == 'LINK'
    external_library = prefs.widget_library if prefs else ""
    widgets, to_load = get_widgets_to_load(
        wgt_names,
        prefer_linked,
        external_library,
        overwrite=overwrite,
        clear_asset=clear_asset,
    )

    # Removing IDs scans the whole file, so do it only once, at the end.
    to_remove: list[ID] = []
    to_rename: list[tuple[Object, str]] = []

    for lib_abs_path, lib_widgets in to_load.items():
        # Append/Link all widget objects of this .blend at once.
        load_path, relative = get_library_load_path(lib_abs_path)
        wgt_obj_names = {"WGT-" + wgt_name for wgt_name in lib_widgets}
        with bpy.data.libraries.load(load_path, link=prefer_linked, relative=relative) as (
            data_from,
            data_to,
        ):
            requested = [obj_name for obj_name in data_from.objects if obj_name in wgt_obj_names]
            # Copy, since Blender replaces the names in this list with the loaded objects.
            data_to.objects = requested.copy()
        # Loaded objects may get a number suffix if an old widget still has their name, so don't look them up by name.
        loaded = dict(zip(requested, data_to.objects))

        for wgt_name, old_wgt_ob in lib_widgets.items():
            new_wgt_ob = loaded.get("WGT-" + wgt_name)
            assert new_wgt_ob, f"Widget failed to import {wgt_name} from {load_path}"

            if new_wgt_ob == old_wgt_ob:
                widgets[wgt_name] = old_wgt_ob
                continue

            if old_wgt_ob and can_swap_widget_data(old_wgt_ob, new_wgt_ob):
                # Overwrite the existing widget's data instead of the object itself, since replacing
                # the object would need a user_remap(), which scans the whole file.
                old_data = old_wgt_ob.data
                old_wgt_ob.data = new_wgt_ob.data
                if old_data.users == 0:
                    to_remove.append(old_data)
                to_remove.append(new_wgt_ob)
                widgets[wgt_name] = old_wgt_ob
                continue

            if old_wgt_ob:
                # Widget already existed, but it must be replaced by what we just imported,
                # eg. when switching between linked and appended widgets.
                old_wgt_ob.user_remap(new_wgt_ob)
                to_remove.append(old_wgt_ob)
                if old_wgt_ob.data and old_wgt_ob.type == 'MESH':
                    to_remove.append(old_wgt_ob.data)
                if new_wgt_ob.library is None:
                    # The old object held the name during loading, so the new one may have a number suffix.
                    to_rename.append((new_wgt_ob, "WGT-" + wgt_name))

            if clear_asset and new_wgt_ob.library is None:
                new_wgt_ob.asset_clear()

            widgets[wgt_name] = new_wgt_ob

    if to_remove:
        bpy.data.batch_remove(to_remove)
    for obj, name in to_rename:
        obj.name = name

    return widgets


def can_swap_widget_data(old_wgt_ob: Object, new_wgt_ob: Object) -> bool:
    """Whether an existing widget can be overwritten by giving it the data of a newly loaded one."""
    return (
        old_wgt_ob.library is None
        and new_wgt_ob.library is None
        and old_wgt_ob.type == new_wgt_ob.type
        and old_wgt_ob.data is not None
    )


def get_widgets_to_load(
    wgt_names: Iterable[str],
    prefer_linked: bool,
    external_library: str,
    overwrite=True,
    clear_asset=True,
) -> tuple[dict[str, Object], dict[str, dict[str, Object | None]]]:
    """Sort widgets into ones that can be used as they are, and ones that need to be loaded from a library.
    Existing widgets are made local or prepared for being overwritten, as needed.
    Returns a dict of widget names (without "WGT-" prefix) to usable objects, and a dict of
    library absolute paths to {widget name: existing object to replace, if any}.
    Widgets that weren't found are in neither.
    """
    widgets: dict[str, Object] = {}
    to_load: dict[str, dict[str, Object | None]] = {}

    for wgt_name in {widget_name(name) for name in wgt_names}:
        wgt_obj_name = "WGT-" + wgt_name
        old_wgt_ob = bpy.data.objects.get(wgt_obj_name)
        if old_wgt_ob and not overwrite:
            widgets[wgt_name] = old_wgt_ob
            continue

        lib_abs_path = get_widget_library_path(wgt_name, external_library)
        if not lib_abs_path:
            # Not in any library, so there's nothing to load or overwrite from.
            if old_wgt_ob:
                widgets[wgt_name] = old_wgt_ob
            continue

        if old_wgt_ob and old_wgt_ob.library:
            if not prefer_linked:
                # Already linked, but local widgets are wanted. Making it local is equivalent to appending it.
                old_wgt_ob.make_local()
                if old_wgt_ob.data:
                    old_wgt_ob.data.make_local()
                if clear_asset:
                    old_wgt_ob.asset_clear()
                widgets[wgt_name] = old_wgt_ob
                continue
            if old_wgt_ob.library.filepath in {lib_abs_path, get_library_load_path(lib_abs_path)[0]}:
                # Already linked from the right library, so it's up to date.
                widgets[wgt_name] = old_wgt_ob
                continue
        elif old_wgt_ob and old_wgt_ob.data:
            # Local widget will be overwritten. Rename its data, so the loaded data can take its name.
            old_wgt_ob.data.name = old_wgt_ob.data.name + "_temp"

        to_load.setdefault(lib_abs_path, {})[wgt_name] = old_wgt_ob

    return widgets, to_load


def get_widget_library_path(wgt_name: str, external_library: str) -> str:
    """Return the absolute path of the .blend file that a widget should be loaded from, or empty string if none."""
    if wgt_name in EXTERNAL_WIDGETS and external_library:
        return external_library
    if wgt_name in CLOUDRIG_WIDGETS:
        return get_native_widgets_path()
    return ""


def get_library_load_path(lib_abs_path: str) -> tuple[str, bool]:
    """Return the path to load a library .blend file with, and whether that path is relative."""
    assert os.path.exists(lib_abs_path), f"Widgets.blend file not found: {lib_abs_path}"
    if not bpy.data.is_saved:
        return lib_abs_path, False
    try:
        return bpy.path.relpath(lib_abs_path), True
    except ValueError:
        # This can happen when the widgets.blend is on a different drive.
        # In this case, a relative path is not possible.
        return lib_abs_path, False


def get_native_widgets_path() -> str:
    return os.path.realpath(__file__).replace("widgets.py", "Widgets.blend")


def get_wgt_names_in_blend(blend_path: str) -> list[str]:
    if blend_path == bpy.data.filepath:
        wgt_names = [widget_name(o.name) for o in bpy.data.objects if o.name.startswith("WGT-")]
        return wgt_names

    if not (os.path.exists(blend_path) and os.path.isfile(blend_path)):
        return []

    wgt_names: list[str] = []
    try:
        with bpy.data.libraries.load(blend_path) as (data_from, _data_to):
            for obj_name in data_from.objects:
                if obj_name.startswith("WGT-"):
                    wgt_names.append(widget_name(obj_name))
    except (OSError, ValueError) as exc:
        print(exc)

    return wgt_names


def load_widgets_of_blend(blend_path: str) -> dict[str, ImagePreview]:
    thumb_dir = Path(blend_path).parent / Path("thumbnails")
    wgt_names = get_wgt_names_in_blend(blend_path)
    icons = {}
    for wgt_name in wgt_names:
        icons[wgt_name] = ensure_icon(
            wgt_name.replace("WGT-", ""), dir_path=thumb_dir, icon_map_name="Widget Thumbnails"
        )

    return icons


def widget_name(name: str) -> str:
    return name.replace("WGT-", "")


def refresh_cloudrig_widgets():
    """Build a list of custom shapes found in the Widgets.blend that ships with CloudRig.
    This should only be refreshed on Blender restart or Reload Scripts, otherwise it's unnecessary.
    """

    global CLOUDRIG_WIDGETS
    wgt_blend_path = get_native_widgets_path()
    CLOUDRIG_WIDGETS = load_widgets_of_blend(wgt_blend_path)


def refresh_external_widgets(context=None):
    """Build a list of custom shapes found in the .blend that the user may or may not have browsed in the preferences.
    This should only be refreshed when that filepath changes, or on operators like Generate/Assign Custom Shape.
    """
    global EXTERNAL_WIDGETS
    prefs = get_addon_prefs(context)
    if not prefs or not prefs.widget_library or not os.path.isfile(prefs.widget_library):
        return []
    wgt_blend_path = prefs.widget_library
    if wgt_blend_path == get_native_widgets_path():
        # If the user has CloudRig's native .blend browsed in the preferences, ignore it.
        return []
    EXTERNAL_WIDGETS = load_widgets_of_blend(wgt_blend_path)


def refresh_local_widgets():
    global LOCAL_WIDGETS
    LOCAL_WIDGETS = load_widgets_of_blend(bpy.data.filepath)


def refresh_widget_list(force_cloudrig=False, force_external=False):
    """This is the `items` callback function for a widget selector EnumProperty.
    Widgets local to this .blend shall mask widgets found in the .blend provided by the user.
    And widgets found in the .blend provided by the user shall mask widgets found in the Widgets.blend that ships with the add-on.
    """
    # First time this is called (per script reload), populate the widget lists.
    if EXTERNAL_WIDGETS == {} or force_external:
        refresh_external_widgets()
    if CLOUDRIG_WIDGETS == {} or force_cloudrig:
        refresh_cloudrig_widgets()

    refresh_local_widgets()

    all_widgets = CLOUDRIG_WIDGETS.copy()
    all_widgets.update(EXTERNAL_WIDGETS)
    all_widgets.update(LOCAL_WIDGETS)

    prefs = get_addon_prefs()
    if not prefs:
        return all_widgets
    prefs.widget_names.clear()
    used_names = set()
    for wgt_name in all_widgets:
        ui_name = wgt_name.replace("WGT-", "").replace("_", " ")
        if ui_name in used_names:
            # For name overlaps, priority is local > external > cloudrig.
            # Duplicate widget names across these 3 widget sources are not allowed.
            continue
        used_names.add(ui_name)

        widget_entry = prefs.widget_names.add()
        widget_entry.name = ui_name

    return all_widgets


def widgets_enum_items(_operator=None, context=None) -> list[tuple[str, str, str, str, int]]:
    enum_items: list[tuple[str, str, str]] = []

    all_widgets = CLOUDRIG_WIDGETS.copy()
    all_widgets.update(EXTERNAL_WIDGETS)
    all_widgets.update(LOCAL_WIDGETS)

    for i, (name, icon) in enumerate(sorted(all_widgets.items(), key=lambda w: w[0])):
        enum_items.append((name, name, name, icon.icon_id, i))

    return enum_items


def get_nonlocal_widgets():
    ret = CLOUDRIG_WIDGETS.copy()
    ret.update(EXTERNAL_WIDGETS)
    return ret


def get_pbone_custom_shape_data(pose_bone: PoseBone) -> dict[str, Any]:
    """
    Saves all custom shape properties of a pose bone.
    Returns a dictionary with the object and its settings.
    """
    return {
        "custom_shape": pose_bone.custom_shape,
        "custom_shape_scale_xyz": pose_bone.custom_shape_scale_xyz.copy(),
        "custom_shape_translation": pose_bone.custom_shape_translation.copy(),
        "custom_shape_rotation_euler": pose_bone.custom_shape_rotation_euler.copy(),
        "use_custom_shape_bone_size": pose_bone.use_custom_shape_bone_size,
        "custom_shape_wire_width": pose_bone.custom_shape_wire_width,
        "show_wire": pose_bone.bone.show_wire,
    }


def set_pbone_custom_shape_data(
    pose_bone: PoseBone,
    custom_shape: Object = None,
    custom_shape_translation: Vector = None,
    custom_shape_rotation_euler: Euler = None,
    custom_shape_scale_xyz: Vector = None,
    use_custom_shape_bone_size: bool | None = None,
    show_wire: bool | None = None,
    custom_shape_wire_width: float | None = None,
):
    """Applies the passed custom shape settings to the pose bone."""
    if custom_shape:
        pose_bone.custom_shape = custom_shape
    if custom_shape_translation:
        pose_bone.custom_shape_translation = custom_shape_translation
    if custom_shape_rotation_euler:
        pose_bone.custom_shape_rotation_euler = custom_shape_rotation_euler
    if custom_shape_scale_xyz:
        pose_bone.custom_shape_scale_xyz = custom_shape_scale_xyz
    if use_custom_shape_bone_size is not None:
        pose_bone.use_custom_shape_bone_size = use_custom_shape_bone_size
    if show_wire is not None:
        pose_bone.bone.show_wire = show_wire
    if custom_shape_wire_width:
        pose_bone.custom_shape_wire_width = custom_shape_wire_width


def get_custom_shape_rig_data(rig: Object) -> dict[str, dict]:
    return {pb.name: get_pbone_custom_shape_data(pb) for pb in rig.pose.bones}


def apply_custom_shape_rig_data(rig: Object, custom_shape_data: dict) -> None:
    if not (rig and rig.pose):
        return
    for pb in rig.pose.bones:
        if pb.name in custom_shape_data:
            set_pbone_custom_shape_data(
                pb,
                **custom_shape_data[pb.name],
            )


class CLOUDRIG_OT_refresh_widget_list(Operator):
    """Click this if you're not seeing a widget that you should be seeing."""

    bl_idname = "pose.cloudrig_refresh_widget_list"
    bl_label = "Refresh Widget List"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _context: Context):
        refresh_widget_list(force_cloudrig=True, force_external=True)
        self.report({'INFO'}, 'Refreshed all widgets and icons.')
        return {'FINISHED'}


class CLOUDRIG_OT_ensure_shape_housekeeping_scripts(Operator):
    """Ensure custom shape housekeeping scripts are loaded and registered."""

    bl_idname = "scene.cloudrig_ensure_shape_housekeeping_scripts"
    bl_label = "Ensure Custom Shape Scripts"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context: Context):
        def ensure_script(filename: str) -> Text:
            filename = filename + ".py"
            existing = bpy.data.texts.get(filename)
            if existing:
                bpy.data.texts.remove(existing)
            text_id = bpy.data.texts.new(filename)
            text_id.filepath = (Path(__file__).parent / Path(f"scripts/{filename}")).as_posix()
            with open(bpy.path.abspath(text_id.filepath), encoding='utf-8') as f:
                content = f.read()
            text_id.indentation = 'SPACES'
            text_id.from_string(content)
            return text_id

        gen_thumbs = ensure_script("generate_thumbnails")
        housekeeping = ensure_script("widgets_housekeeping")
        housekeeping.as_module()

        return {'FINISHED'}


registry = [CLOUDRIG_OT_refresh_widget_list, CLOUDRIG_OT_ensure_shape_housekeeping_scripts]
