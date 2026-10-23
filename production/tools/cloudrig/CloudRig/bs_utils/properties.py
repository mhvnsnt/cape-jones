# SPDX-FileCopyrightText: 2025-2026 Blender Studio Tools Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

import math
from collections.abc import Iterator
from typing import Any

import bpy
from bpy.types import Object, PropertyGroup, bpy_prop_collection
from bpy.utils import flip_name
from mathutils import Matrix, Vector
from rna_prop_ui import IDPropertyGroup

# Functions to manage runtime properties, which include custom properties and add-on properties.
# These functions aim to abstract away that distinction, and also abstract away whether something is a single value,
# a PropertyGroup, or a CollectionProperty.
# Compatible with the API changes in 5.0, but also older versions.


def copy_all_runtime_properties(src_id: Any, tgt_id: Any, x_mirror=False):
    """Copy add-on and custom properties from source to target.
    Both should be the same type.
    Should support anything that supports custom properties or property registration.
    """
    for prop_name in get_all_runtime_prop_names(src_id):
        copy_runtime_property(src_id, tgt_id, prop_name, x_mirror)


def copy_all_custom_properties(src_id: Any, tgt_id: Any, x_mirror=False):
    """Copy all custom properties (UI-created or dict-syntax) from source to target."""
    for prop_name in get_custom_prop_names(src_id):
        copy_custom_property(src_id, tgt_id, prop_name=prop_name, x_mirror=x_mirror)


def get_all_runtime_prop_names(owner: Any) -> list[str]:
    """Return names of all add-on and custom properties on owner."""
    custom_props = list(owner.keys())
    addon_props = get_addon_prop_names(owner)
    props = custom_props + addon_props
    return props


def get_custom_prop_names(owner: Any) -> Iterator[str]:
    """Yield names of all custom (non-add-on) properties on owner."""
    for prop_name in get_all_runtime_prop_names(owner):
        if is_custom_prop(owner, prop_name):
            yield prop_name


def get_addon_prop_names(owner: Any) -> list[str]:
    """Return names of all add-on registered or system properties on owner."""
    if bpy.app.version >= (5, 0, 0):
        sys_props = owner.bl_system_properties_get()
        if sys_props is None:
            # If there aren't any add-on properties.
            return []
        return list(sys_props.keys())
    else:
        return [prop_name for prop_name in owner.keys() if is_addon_prop(owner, prop_name)]


def rename_custom_prop(owner: Any, from_name: str, to_name: str):
    """Rename a custom property in-place, preserving its value and UI metadata."""
    assert is_custom_prop(owner, from_name), f"Property {from_name} of {owner} is not a Custom Property."
    copy_custom_property(owner, owner, from_name, new_name=to_name, x_mirror=False)
    remove_property(owner, from_name)


def copy_runtime_property(src_id: Any, tgt_id: Any, prop_name: str, x_mirror=False):
    """Copy add-on properties or custom properties."""
    if is_addon_prop(src_id, prop_name):
        if is_registered_addon_prop(src_id, prop_name):
            src_prop = getattr(src_id, prop_name)
            tgt_prop = getattr(tgt_id, prop_name)
            if isinstance(src_prop, bpy_prop_collection):
                copy_coll_prop(src_prop, tgt_prop, x_mirror)
            elif isinstance(src_prop, PropertyGroup):
                copy_property_group(src_prop, tgt_prop, x_mirror)
            else:
                copy_single_addon_prop(src_id, tgt_id, prop_name, x_mirror)
        else:
            if bpy.app.version >= (5, 0, 0):
                # HACK: If we need to copy add-on properties, but the add-on is not present,
                # we have to write to the system properties, which is API abuse that could
                # lose support any moment, but there is no other way to do this atm.
                tgt_props = tgt_id.bl_system_properties_get()
                if not tgt_props:
                    # XXX: not sure why, but this happens in one case in a community CloudRig rig (Hela by a$ap berg).
                    return
                src_props = src_id.bl_system_properties_get()
                # Remove the existing property before assignment to avoid TypeError when copying IDPropertyGroup
                if prop_name in tgt_props:
                    del tgt_props[prop_name]
                tgt_props[prop_name] = src_props[prop_name]
            else:
                tgt_id[prop_name] = src_id[prop_name]
    else:
        copy_custom_property(src_id, tgt_id, prop_name)


def copy_property_group(src_pg: PropertyGroup, tgt_pg: PropertyGroup, x_mirror=False):
    """
    Copy the values from one PropertyGroup into another of the same type.
    Optionally, X-mirror names (e.g., ".L" <-> ".R") in strings and Object references.
    """
    assert isinstance(tgt_pg, PropertyGroup) and isinstance(src_pg, PropertyGroup)
    assert tgt_pg.__class__ == src_pg.__class__

    for prop_name in src_pg.bl_rna.properties.keys():
        if prop_name in ("rna_type", "bl_rna"):
            continue
        if not src_pg.is_property_set(prop_name):
            tgt_pg.property_unset(prop_name)
            continue
        value = getattr(src_pg, prop_name)
        if isinstance(value, bpy_prop_collection):
            tgt_collprop = getattr(tgt_pg, prop_name)
            copy_coll_prop(value, tgt_collprop, x_mirror)
        elif isinstance(value, PropertyGroup):
            copy_property_group(value, getattr(tgt_pg, prop_name), x_mirror)
        else:
            copy_single_addon_prop(src_pg, tgt_pg, prop_name, x_mirror)
    for prop_name in src_pg.keys():
        if is_custom_prop(src_pg, prop_name):
            # PropertyGroups also support custom properties.
            copy_custom_property(src_pg, tgt_pg, prop_name, x_mirror)


def copy_coll_prop(src_cp: bpy_prop_collection, tgt_cp: bpy_prop_collection, x_mirror=False):
    """Replace the contents of tgt_cp with a copy of each entry from src_cp."""
    tgt_cp.clear()
    for src_pg in src_cp:
        assert isinstance(src_pg, PropertyGroup)
        tgt_pg = tgt_cp.add()
        copy_property_group(src_pg, tgt_pg, x_mirror)


def copy_custom_property(src_owner: Any, tgt_owner: Any, prop_name: str, new_name="", x_mirror=False) -> Any:
    """Copy a custom property (one that was created via the UI or via Python dictionary syntax)."""
    if not new_name:
        new_name = prop_name
    try:
        src_prop = src_owner.id_properties_ui(prop_name)
    except TypeError:
        # Python dicts don't support UI data.
        tgt_owner[prop_name] = src_owner[prop_name]
        return
    assert src_prop, f'Property "{prop_name}" not found in {src_owner}.'
    value = src_owner[prop_name]
    if x_mirror:
        value = x_mirror_value(value)

    tgt_owner[new_name] = value
    new_prop = tgt_owner.id_properties_ui(new_name)
    new_prop.update_from(src_prop)
    tgt_owner.property_overridable_library_set(
        f'["{new_name}"]', src_owner.is_property_overridable_library(f'["{prop_name}"]')
    )
    return tgt_owner.id_properties_ui(new_name)


def copy_single_addon_prop(src: Any, tgt: Any, prop_name: str, x_mirror=False) -> bool:
    """Copy a single scalar add-on property, optionally X-mirroring the value."""
    if src.is_property_readonly(prop_name):
        # This "early" exit has to come after CollectionProperty & PropertyGroup
        # checks, since they are technically read-only.
        return False

    value = getattr(src, prop_name)
    if x_mirror:
        value = x_mirror_value(value)

    try:
        current_value = getattr(tgt, prop_name)
        if current_value != value:
            setattr(tgt, prop_name, value)
    except TypeError:
        print(f"{__package__}: Copy Addon property failed: \n\tName:{prop_name}\n\tValue:{value}")
    return True


def x_mirror_value(value: Any) -> Any:
    """Return the X-mirrored equivalent of value, flipping string names and Object references."""
    if isinstance(value, str):
        return flip_name(value)
    elif isinstance(value, Object):
        return get_opposite_obj(value)
    else:
        return value


def get_opposite_obj(obj: Object) -> Object:
    """Return the X-mirrored version of a Blender object by name (and library if linked)."""
    flipped_name = flip_name(obj.name)
    lib = obj.library
    return (bpy.data.objects.get((lib, flipped_name)) if lib else bpy.data.objects.get(flipped_name)) or obj


def is_addon_prop(owner: Any, prop_name: str) -> bool:
    """Return whether prop_name is an add-on registered or system property on owner."""
    if bpy.app.version >= (5, 0, 0):
        return prop_name in get_addon_prop_names(owner)
    else:
        # NOTE: I don't think it's possible to detect pre-5.0 non-PropertyGroup/CollectionProperty non-registered add-on properties.
        # They just behave completely as custom properties.
        return prop_name in owner and (
            isinstance(owner[prop_name], IDPropertyGroup) or isinstance(owner[prop_name], list)
        )


def is_registered_addon_prop(owner: Any, prop_name: str) -> bool:
    """Return whether prop_name is an actively registered add-on property on owner."""
    return is_addon_prop(owner, prop_name) and prop_name in owner.bl_rna.properties


def is_custom_prop(owner: Any, prop_name: str) -> bool:
    """Return whether prop_name is a user-created custom property on owner."""
    return prop_name in owner.keys() and not is_addon_prop(owner, prop_name)


def remove_property(owner: Any, prop_name: str):
    """Remove a property from owner, regardless of whether it is custom or an add-on property."""
    if is_custom_prop(owner, prop_name):
        del owner[prop_name]
    elif is_registered_addon_prop(owner, prop_name):
        owner.property_unset(prop_name)
    elif is_addon_prop(owner, prop_name):
        disabled_addon_props = owner.bl_system_properties_get()
        del disabled_addon_props[prop_name]
    else:
        raise KeyError(f"{prop_name} not found in {owner.name}")


def get_property_defaults(bpy_type: type, exclude: list[str] = []) -> dict[str, Any]:
    def get_default(prop: Any) -> Any:
        if not hasattr(prop, "default"):
            return None

        if hasattr(prop, "default_array"):
            default_array = list(prop.default_array)
            if default_array:
                if len(default_array) == 9:
                    return Matrix.Identity(3)
                elif len(default_array) == 16:
                    return Matrix.Identity(4)
                elif len(default_array) == 3 and prop.type == 'FLOAT':
                    default = default_array[0]
                    return Vector((default, default, default))
                else:
                    return default_array

        return prop.default

    return {
        prop.identifier: get_default(prop)
        for prop in bpy_type.bl_rna.properties
        if not prop.is_readonly and prop.identifier not in exclude
    }


def set_if_changed(owner: Any, prop_name: str, value: Any) -> bool:
    """Assign an RNA property only if its value would change, since RNA writes are relatively slow
    (they run update callbacks). Returns whether a write happened."""
    current = getattr(owner, prop_name)
    if current == value:
        return False
    if isinstance(current, float) and isinstance(value, (float, int)):
        # Blender stores floats with single precision.
        if math.isclose(current, value, rel_tol=1e-6):
            return False
    elif hasattr(current, '__len__') and not isinstance(current, str):
        # Arrays, Vectors, Eulers, etc. don't compare equal to other sequence types.
        if tuple(current) == tuple(value):
            return False
    setattr(owner, prop_name, value)
    return True
