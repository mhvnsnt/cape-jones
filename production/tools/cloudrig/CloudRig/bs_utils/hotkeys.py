# SPDX-FileCopyrightText: 2016-2026 Blender Foundation
#
# SPDX-License-Identifier: GPL-3.0-or-later

# This file requires (and is made possible by) Blender 5.0 due to the find_match() API call.

import hashlib
import json
from collections.abc import Callable
from typing import Any

import bpy
from bpy.app.translations import pgettext_n as n_
from bpy.app.translations import pgettext_rpt as rpt_
from bpy.types import Context, KeyConfig, KeyMap, KeyMapItem, Operator, Region, UILayout

# Preserve across Reload Scripts (module reload) when possible, but also keep
# names defined for static analyzers.
ADDON_KEYMAPS = locals().get("ADDON_KEYMAPS", [])
KMI_HASHES = locals().get("KMI_HASHES", {})

KEYMAP_ICONS = {
    'Object Mode': 'OBJECT_DATAMODE',
    'Window': 'WINDOW',
    '3D View': 'VIEW3D',
    'Mesh': 'OUTLINER_DATA_MESH',
    'Outliner': 'OUTLINER',
    'Object Non-modal': 'OBJECT_DATAMODE',
    'Sculpt': 'SCULPTMODE_HLT',
    'Armature': 'ARMATURE_DATA',
    'Pose': 'POSE_HLT',
    'Weight Paint': 'WPAINT_HLT',
    'Graph Editor': 'GRAPH',
    'Dopesheet': 'ACTION',
    'Curve': 'CURVE_DATA',
}

KEYMAP_UI_NAMES = {
    'Armature': n_("Armature Edit"),
    'Object Non-modal': n_("Object Mode"),
}

KMI_DEFAULTS = {prop.identifier: prop.default for prop in KeyMapItem.bl_rna.properties if hasattr(prop, 'default')}


def register_hotkey(
    bl_idname: str,
    *,
    op_kwargs: dict | None = None,
    hotkey_kwargs: dict | None = None,
    keymap_name='Window',
):
    """Register an operator hotkey in the add-on keyconfig, avoiding duplicates on Reload Scripts."""
    if op_kwargs is None:
        op_kwargs = {}
    if hotkey_kwargs is None:
        hotkey_kwargs = {'type': "SPACE", 'value': "PRESS"}

    context = bpy.context
    wm = context.window_manager

    kmi_hash = any_to_hash(op_kwargs, hotkey_kwargs, keymap_name)
    if kmi_hash in KMI_HASHES:
        # Avoid re-registering on Reload Scripts.
        return

    space_type = wm.keyconfigs.default.keymaps[keymap_name].space_type

    addon_keyconfig = wm.keyconfigs.addon
    if not addon_keyconfig:
        # This happens when running Blender in background mode.
        return

    addon_keymaps = addon_keyconfig.keymaps
    addon_km = addon_keymaps.get(keymap_name)
    if not addon_km:
        addon_km = addon_keymaps.new(name=keymap_name, space_type=space_type)

    existing_kmi = find_kmi_in_km_by_data(addon_km, hotkey_kwargs, bl_idname, op_kwargs)
    if existing_kmi:
        # NOTE: It is extremely important to not register duplicate add-on keymaps, AND
        # to NOT remove them on add-on unregister, because once an add-on keymap is registered,
        # it is SUPPOSED TO stick around for ever.
        # This allows Blender to store the associated user keymap, meaning the user's modifications
        # will be stored and restored as expected, whenever the add-on is enabled again.
        if (addon_km, existing_kmi) not in ADDON_KEYMAPS:
            ADDON_KEYMAPS.append((addon_km, existing_kmi))
        return
    addon_kmi = addon_km.keymap_items.new(bl_idname, **hotkey_kwargs)
    for key in op_kwargs:
        value = op_kwargs[key]
        setattr(addon_kmi.properties, key, value)

    KMI_HASHES[kmi_hash] = (addon_km, addon_kmi)
    ADDON_KEYMAPS.append((addon_km, addon_kmi))


def draw_hotkey_list(
    context: Context,
    layout: UILayout,
    *,
    compact: bool | None = False,
    debug=False,
    sort_mode='BY_KEYMAP',
    ignore_missing=False,
    button_draw_func: Callable | None = None,
):
    """Draw the list of hotkeys registered by this add-on.
    Will find the corresponding User KeyMapItems, which are safe to modify.
    Supports two sorting modes:
        BY_KEYMAP: Sort by name of containing keymap, then operator name as displayed in the UI.
        Operators with a "name" parameter will use that as the name. No grouping.
        BY_OPERATOR: Sort by operator name as displayed in the UI. Group identical names together.
    """
    if bpy.app.version < (5, 0, 0):
        layout.label(text="Only in Blender 5.0 and later.")
        return

    assert sort_mode in ('BY_KEYMAP', 'BY_OPERATOR')

    if sort_mode == 'BY_OPERATOR':
        layout = layout.column(align=True)

    if compact is None:
        sidebar = get_sidebar(context)
        if sidebar:
            compact = sidebar.width < 600
        elif context.area:
            compact = context.area.width < 600

    if not compact:
        split = layout.row().split(factor=0.75)
        row = split.row()
        row.label(text="Operator", icon='BLANK1')
        row.label(text="Group", icon='BLANK1')
        split.row().label(text="Key Combo")
        layout.separator()

    user_kmis = get_user_kmis_of_addon(context)
    if sort_mode == 'BY_KEYMAP':
        user_kmis = sorted(user_kmis, key=lambda tup: "".join(list(get_kmi_ui_info(*tup)[1:])))
    elif sort_mode == 'BY_OPERATOR':
        user_kmis = sorted(user_kmis, key=lambda tup: "".join(list(get_kmi_ui_info(*tup)[2])))

    for i, (user_km, user_kmi) in enumerate(user_kmis):
        _, _, kmi_name = get_kmi_ui_info(user_km, user_kmi)
        if "Missing" in kmi_name and ignore_missing:
            continue
        if sort_mode == 'BY_OPERATOR' and i > 0:
            prev_km, prev_kmi = user_kmis[i - 1]
            _, _, prev_kmi_name = get_kmi_ui_info(prev_km, prev_kmi)
            if prev_kmi_name != kmi_name:
                layout.separator()

        draw_kmi(user_km, user_kmi, layout, compact=compact, button_draw_func=button_draw_func, debug=debug)


def get_user_kmis_of_addon(context: Context, *, do_update=True) -> list[tuple[KeyMap, KeyMapItem]]:
    """Return a list of (KeyMap, KeyMapItem) tuples of user-shortcuts (the ones that can be modified by user)."""
    ret = []

    assert bpy.app.version >= (5, 0, 0), "This function requires Blender 5.0 or later."

    if do_update:
        context.window_manager.keyconfigs.update()
    for addon_km, addon_kmi in ADDON_KEYMAPS:
        user_km, user_kmi = get_user_kmi_of_addon(context, addon_km, addon_kmi)
        if user_kmi:
            ret.append((user_km, user_kmi))

    return ret


def get_user_kmi_of_addon(
    context: Context, addon_km: KeyMap, addon_kmi: KeyMapItem
) -> tuple[KeyMap | None, KeyMapItem | None]:
    """Return the matching User KeyMap and KeyMapItem for the given add-on KMI pair."""
    user_km = context.window_manager.keyconfigs.user.keymaps.get(addon_km.name)
    if not user_km:
        # This should never happen.
        print("Failed to find User KeyMap: ", addon_km.name)
        return None, None
    user_kmi = user_km.keymap_items.find_match(addon_km, addon_kmi)
    if not user_kmi:
        # This shouldn't really happen, but maybe it can, eg. if user changes idname.
        print("Failed to find User KeyMapItem: ", addon_km.name, addon_kmi.idname)
        return None, None
    return user_km, user_kmi


def get_kmi_ui_info(km: KeyMap, kmi: KeyMapItem) -> tuple[str, str, str]:
    """Return (keymap icon, keymap display name, operator display name) for a KeyMapItem."""
    km_name: str = km.name
    km_icon = KEYMAP_ICONS.get(km_name, 'BLANK1')
    km_name = KEYMAP_UI_NAMES.get(km_name, km_name)
    if kmi.properties and 'name' in kmi.properties:
        name = kmi.properties.name
        if name:
            if hasattr(bpy.types, kmi.properties.name):
                bpy_type = getattr(bpy.types, kmi.properties.name)
                kmi_name = bpy_type.bl_label
            else:
                kmi_name = "Missing (code 1). Try restarting."
        else:
            kmi_name = "Missing (code 2). Try restarting."
    else:
        try:
            parts = kmi.idname.split(".")
            bpy_type = getattr(bpy.ops, parts[0])
            bpy_type = getattr(bpy_type, parts[1])
            kmi_name = bpy_type.get_rna_type().name
        except (AttributeError, IndexError, TypeError):
            kmi_name = "Missing (code 3). Try restarting."

    return km_icon, km_name, kmi_name


def find_kmi_in_km_by_data(km: KeyMap, hotkey_kwargs: dict, op_idname: str, op_kwargs: dict) -> KeyMapItem | None:
    """Loop over KeyMapItems of the provided KeyMap, and return the first entry,
    if any, which matches the passed key combo, operator, and operator properties.
    """

    def is_kmi_matching(kmi: KeyMapItem, hotkey_kwargs: dict, op_idname: str, op_kwargs: dict) -> bool:
        if kmi.idname != op_idname:
            return False

        combined_hotkey = KMI_DEFAULTS.copy()
        combined_hotkey.update(hotkey_kwargs)
        for key, value in combined_hotkey.items():
            if value != getattr(kmi, key):
                return False

        # IMPORTANT:
        # `wm.keyconfigs.addon` is shared by *all* add-ons. If we only match on idname+hotkey,
        # we may incorrectly treat another add-on's KeyMapItem as ours and skip registering,
        # which prevents Blender from applying the user's stored overrides on next startup
        # (manifesting as "prefs/hotkeys reset", eg. when used together with Pie Menu Editor).
        #
        # We therefore include operator properties in the match, but do it defensively:
        # - only compare simple scalar types (str/int/float/bool/None)
        # - if anything unexpected is encountered, treat it as a mismatch rather than risking
        #   false positives or Blender RNA edge-case crashes.
        if op_kwargs:
            try:
                if kmi.properties is None:
                    return False
                for key, expected in op_kwargs.items():
                    if key not in kmi.properties:
                        return False
                    actual = getattr(kmi.properties, key, None)

                    # Compare only stable scalar values.
                    scalar_types = (str, int, float, bool, type(None))
                    if isinstance(expected, scalar_types) and isinstance(actual, scalar_types):
                        if actual != expected:
                            return False
                    else:
                        # Unknown/complex value: do not assume a match.
                        return False
            except (AttributeError, KeyError, TypeError, RuntimeError):
                # Be conservative: if Blender throws, don't match.
                return False

        return True

    return next((kmi for kmi in km.keymap_items if is_kmi_matching(kmi, hotkey_kwargs, op_idname, op_kwargs)), None)


def draw_kmi(
    km: KeyMap,
    kmi: KeyMapItem,
    layout: UILayout,
    compact=False,
    button_draw_func: Callable | None = None,
    debug=False,
):
    """Draw a KeyMapItem in the provided UI.
    This function is designed specifically to be used in an add-on's preferences:
    - It does not allow removing the KeyMapItem, since add-on KMIs should never be removed.
    - It does not allow changing the operator name or kwargs for similar reasons.
    - Caller should pass a KeyMap and KeyMapItem pair from keyconfigs.user.
    - Passing data from keyconfigs.addon can be useful for debugging purposes.
    """
    if debug:
        layout = layout.box()

    split = layout.split(factor=0.75)

    row1 = split.row(align=True)
    if debug:
        row1.prop(kmi, "show_expanded", text="", emboss=False)
    row1.prop(kmi, "active", text="", emboss=False)
    km_icon, km_name, kmi_name = get_kmi_ui_info(km, kmi)
    if compact:
        km_name = ""
    row1.label(text=kmi_name)
    row1.label(text=km_name, icon=km_icon or "BLANK1")

    row2 = split.row(align=True)
    sub = row2.row(align=True)
    sub.enabled = kmi.active
    if button_draw_func:
        button_draw_func(layout=sub, km=km, kmi=kmi, compact=compact)
    else:
        sub.prop(kmi, "type", text="", full_event=True)

    if kmi.is_user_modified:
        # Make `context.keymap` available in the drawing code (in this case blender's native code)
        row2.context_pointer_set("keymap", km)
        row2.operator("preferences.keyitem_restore", text="", icon='BACK').item_id = kmi.id

    if debug and kmi.show_expanded:
        layout.template_keymap_item_properties(kmi)


def get_sidebar(context: Context) -> Region | None:
    """Return the N-panel (sidebar) region of the 3D Viewport, or None if not in a 3D Viewport."""
    if not context.area or context.area.type != 'VIEW_3D':
        return None
    for region in context.area.regions:
        if region.type == 'UI':
            return region


def find_matching_km_and_kmi(
    context: Context, target_kc: KeyConfig, src_km: KeyMap, src_kmi: KeyMapItem
) -> tuple[KeyMap | None, KeyMapItem | None]:
    """Find the matching KeyMap and KeyMapItem in target_kc corresponding to the given src_km/src_kmi."""
    target_km = find_matching_keymap(context, target_kc, src_km)
    if not target_km:
        raise RuntimeError(f"Failed to find KeyMap '{src_km.name}' in KeyConfig '{target_kc.name}'")
    kc_user = context.window_manager.keyconfigs.user
    # If we want to find a matching User KeyMapItem, that's easy, because that's what the API was meant for.
    if target_kc == kc_user:
        return target_km, target_km.keymap_items.find_match(src_km, src_kmi)

    user_km = src_km
    # If we want to find any other type of KeyMapItem, we have to do it indirectly, since we can only directly check for matches in the User KeyConfig.
    # So eg. if we want to find an Addon KeyMapItem based on a User KeyMapItem, we have to loop over all Addon KeyMapItems, and find which one matches with the given User KeyMapItem.
    for target_kmi in target_km.keymap_items:
        try:
            match = user_km.keymap_items.find_match(target_km, target_kmi)
            if match == src_kmi:
                return target_km, target_kmi
        except RuntimeError:
            print("Failed to find matching KeyMapItem for: ", target_km.name, target_kmi.to_string())

    # raise Exception(f"Failed to find KeyMapItem '{src_kmi.idname}' ({src_kmi.to_string()}) in KeyConfig '{target_kc.name}', KeyMap '{target_km.name}'")
    # We will return here eg. when looking for an add-on keymap in the default keyconfig.
    return None, None


def find_matching_keymap(context: Context, target_kc: KeyConfig, src_km: KeyMap) -> KeyMap | None:
    """Find the equivalent keymap in another keyconfig."""

    kc_user = context.window_manager.keyconfigs.user

    # If we want to find a matching User KeyMap, that's easy, because that's what the API was meant for.
    if target_kc == kc_user:
        match = target_kc.keymaps.find_match(src_km)
        assert match != src_km, "This is the same exact keymap already."
        return match

    # If we want to find any other type of KeyMap, we have to do it indirectly, since we can only directly check for matches in the User KeyConfig.
    # So eg. if we want to find an Addon KeyMap based on a User KeyMap, we have to loop over all Addon KeyMaps, and find which one matches with the given User KeyMap.
    for km in target_kc.keymaps:
        match = kc_user.keymaps.find_match(km)
        if match == src_km:
            return km


class WINDOW_OT_restore_deleted_hotkeys(Operator):
    bl_idname = "window.restore_deleted_hotkeys"
    bl_description = "Restore any missing built-in or add-on hotkeys.\n(These should be disabled instead of being deleted.)\nThis operation cannot be undone!"
    # Undo flag is omitted, because this operation cannot be un-done.
    bl_options = {'REGISTER'}
    bl_label = "Restore Deleted Hotkeys"

    def execute(self, context: Context):
        num_restored = restore_deleted_keymap_items_global(context)
        self.report({'INFO'}, rpt_("Restored {num_restored} deleted keymaps.").format(num_restored=num_restored))
        return {'FINISHED'}


def restore_deleted_keymap_items_global(context: Context) -> int:
    """Deleting built-in or add-on KeyMapItems should never be done by users, as there's no way to recover them.
    Changing the operator name also shouldn't be done, since that makes it impossible to track modifications.
    Blender shouldn't even allow either of these things. You can disable instead of delete, and you can disable and add new entry instead of modifying idname.
    This function tries to bring them back, by restoring all KeyMaps to their default state, then re-applying any modifications that were there before
    (Except these deletions.)
    """

    keyconfigs = context.window_manager.keyconfigs
    user_kc = keyconfigs.user
    total_restored = 0
    keymap_names = [km.name for km in user_kc.keymaps]
    for km_name in keymap_names:
        num_restored = restore_deleted_keymap_items(context, km_name)
        user_km = user_kc.keymaps[km_name]
        if num_restored != 0:
            user_km = user_kc.keymaps[km_name]
            print(f"{user_km.name}: Restored {num_restored}")
        total_restored += num_restored
    return total_restored


def restore_deleted_keymap_items(context: Context, user_km_name: str) -> int:
    """Restore deleted KeyMapItems in user_km_name, preserving any user modifications that were present."""
    keyconfigs = context.window_manager.keyconfigs
    user_kc = keyconfigs.user
    default_kc = keyconfigs.default
    addon_kc = keyconfigs.addon

    user_km = user_kc.keymaps[user_km_name]

    # Step 1: Store modified and added KeyMapItems in a temp keymap.
    temp_km_name = "temp_" + user_km_name
    temp_km = user_kc.keymaps.new(temp_km_name)
    kmis_user_modified = []
    kmis_user_defined = []
    for user_kmi in user_km.keymap_items:
        if user_kmi.is_user_defined:
            temp_kmi = temp_km.keymap_items.new_from_item(user_kmi)
            kmis_user_defined.append(temp_kmi)
            continue
        if user_kmi.is_user_modified:
            temp_kmi = temp_km.keymap_items.new_from_item(user_kmi)
            # Find the original keymap in either the Blender default or Addon KeyConfigs.
            # Not sure if this works with presets like Industry Compatible keymap,
            # but I assume they change the contents of the "default" keyconfig, so it would work.
            default_km, default_kmi = find_matching_km_and_kmi(context, default_kc, user_km, user_kmi)
            if not default_kmi:
                default_km, default_kmi = find_matching_km_and_kmi(context, addon_kc, user_km, user_kmi)
            kmis_user_modified.append(((default_km, default_kmi), (temp_km, temp_kmi)))

    # Step 2: Restore User KeyMap to default.
    num_kmis = len(user_km.keymap_items)
    user_km.restore_to_default()
    # NOTE: restore_to_default() will shuffle the memory addresses, so we need to re-reference user_km.
    # I don't think this was the case pre-Blender 5.0!!
    user_km = user_kc.keymaps[user_km_name]
    temp_km = user_kc.keymaps[temp_km_name]

    # Step 3: Restore modified and added KeyMapItems.
    for temp_def_kmi in kmis_user_defined:
        user_km.keymap_items.new_from_item(temp_def_kmi)

    for (default_km, default_kmi), (temp_km, temp_kmi) in kmis_user_modified:
        _user_km, user_kmi = find_matching_km_and_kmi(context, user_kc, default_km, default_kmi)
        for key in (
            'active',
            'alt',
            'any',
            'ctrl',
            'hyper',
            'key_modifier',
            'map_type',
            'oskey',
            'shift',
            'repeat',
            'type',
            'value',
        ):
            setattr(user_kmi, key, getattr(temp_kmi, key))
        if temp_kmi.properties:
            for key in temp_kmi.properties.keys():
                temp_value = getattr(temp_kmi.properties, key)
                if hasattr(temp_value, 'keys'):
                    # Operator properties can be PropertyGroups, and this is the case for some node wrangler ops.
                    temp_propgroup = temp_value
                    real_propgroup = getattr(user_kmi.properties, key)
                    for pg_key in temp_propgroup.keys():
                        pg_val = getattr(temp_propgroup, pg_key)
                        real_propgroup[pg_key] = pg_val
                    continue
                setattr(user_kmi.properties, key, temp_value)

    # Nuke the temp keymap.
    user_kc.keymaps.remove(temp_km)

    return len(user_km.keymap_items) - num_kmis


def any_to_hash(*args: Any) -> str:
    """Hash whatever."""

    def stable(obj: Any) -> Any:
        # Make hashing deterministic across runs and independent of dict insertion order.
        # Keep it conservative to avoid surprises with Blender RNA objects.
        if isinstance(obj, dict):
            return {str(k): stable(v) for k, v in sorted(obj.items(), key=lambda kv: str(kv[0]))}
        if isinstance(obj, (list, tuple)):
            return [stable(v) for v in obj]
        return obj

    try:
        stringified = json.dumps([stable(a) for a in args], sort_keys=True, separators=(",", ":"), default=str)
    except (TypeError, ValueError):
        # Fallback: last resort stringification
        stringified = ";".join([str(arg) for arg in args])
    return hashlib.sha256(stringified.encode("utf-8")).hexdigest()


registry = [WINDOW_OT_restore_deleted_hotkeys]
