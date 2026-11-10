import json
import os
from pathlib import Path

import bpy
from bpy.types import AddonPreferences, PropertyGroup, bpy_prop_collection
from rna_prop_ui import IDPropertyGroup

from .. import __package__ as base_package

assert base_package


class PrefsFileSaveLoadMixin:
    """Mix-in class that can be used by any add-on to store their preferences in a file,
    so that they don't get lost when the add-on is disabled.
    To use it, copy this file to your add-on, and do this in your code:

    ```
    import bpy
    from .bs_utils.prefs import PrefsFileSaveLoadMixin, update_prefs_on_file

    class MyAddonPrefs(PrefsFileSaveLoadMixin, bpy.types.AddonPreferences):
        some_prop: bpy.props.IntProperty(update=update_prefs_on_file)

    def register():
        bpy.utils.register_class(MyAddonPrefs)
        MyAddonPrefs.register_autoload_from_file()

    def unregister():
        update_prefs_on_file()
    ```

    """

    # List of property names to not write to disk.
    omit_from_disk: list[str] = []

    loading = False

    @staticmethod
    def register_autoload_from_file(delay=1.0):
        # Preferences cannot be modified during add-on registration, so we have to do it with an arbitrary delay.
        # This could still fail if Blender loads too slowly, so it could be better.
        # Ideally, Blender would simply save add-on preferences to disk, and none of this should be needed.
        def timer_func(_scene=None):
            prefs = None
            try:
                prefs = get_addon_prefs()
            except KeyError:
                # Add-on got un-registered in the meantime.
                return
            if prefs:
                prefs.load_and_apply_prefs_from_file()

        bpy.app.timers.register(timer_func, first_interval=delay)

    def apply_prefs_from_dict_recursive(self, propgroup: PropertyGroup, data: dict):
        for key, value in data.items():
            if not hasattr(propgroup, key):
                # Property got removed or renamed in the implementation.
                continue
            if type(value) is list:
                for elem in value:
                    collprop = getattr(propgroup, key)
                    entry = collprop.get(elem["name"])
                    if not entry:
                        entry = collprop.add()
                    self.apply_prefs_from_dict_recursive(entry, elem)
            elif type(value) is dict:
                self.apply_prefs_from_dict_recursive(getattr(propgroup, key), value)
            else:
                try:
                    setattr(propgroup, key, value)
                except TypeError as exc:
                    print("Failed to set add-on preference: ", key, value)
                    print(exc)

    def to_dict(self):
        return props_to_dict_recursive(self, skip=type(self).omit_from_disk)

    def save_prefs_to_file(self):
        filepath = get_prefs_filepath()

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def load_and_apply_prefs_from_file(self) -> dict:
        type(self).loading = True
        addon_data = load_prefs_from_file()
        self.apply_prefs_from_dict_recursive(self, addon_data)
        type(self).loading = False
        return addon_data


def load_prefs_from_file() -> dict:
    filepath = get_prefs_filepath()
    if not filepath.exists():
        return {}

    with open(filepath, "r") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"Failed to load add-on preferences from file: {filepath}")

    return {}


def get_prefs_filepath() -> Path:
    if "." in base_package:
        addon_name = base_package.split(".")[-1]
    else:
        addon_name = base_package
    return Path(bpy.utils.user_resource('CONFIG')) / Path(addon_name + ".json")


def update_prefs_on_file(self=None, context=None):
    prefs = get_addon_prefs(context)
    if prefs:
        if not type(prefs).loading:
            prefs.save_prefs_to_file()
    else:
        print("Couldn't save preferences because the class was already unregistered.")


def props_to_dict_recursive(propgroup: IDPropertyGroup, skip=[]) -> dict:
    """Recursively convert a PropertyGroup or AddonPreferences to a dictionary.
    Note that AddonPreferences don't support PointerProperties,
    so this function doesn't either."""

    ret = {}

    for key in propgroup.bl_rna.properties.keys():
        if key in skip or key in ["rna_type", "bl_idname"]:
            continue
        value = getattr(propgroup, key)
        if isinstance(value, bpy_prop_collection):
            ret[key] = [props_to_dict_recursive(elem) for elem in value]
        elif isinstance(value, IDPropertyGroup) or isinstance(value, PropertyGroup):
            ret[key] = props_to_dict_recursive(value)
        else:
            if hasattr(propgroup.bl_rna.properties[key], "enum_items"):
                # Save enum values as string, not int.
                ret[key] = propgroup.bl_rna.properties[key].enum_items[value].identifier
            else:
                ret[key] = value
    return ret


def get_addon_prefs(context=None) -> AddonPreferences | None:
    if not context:
        context = bpy.context

    addons = context.preferences.addons
    if base_package.startswith("bl_ext"):
        # 4.2 and later
        addon_key = base_package
    else:
        # Pre-4.2
        addon_key = base_package.split(".")[0]

    addon = addons.get(addon_key)
    if addon is None:
        # print("This happens when packaging the extension, due to the registration delay.")
        return

    return addon.preferences
