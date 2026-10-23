# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING, Any

import bpy
from bpy.app.translations import pgettext_iface as iface_
from bpy.app.translations import pgettext_rpt as rpt_
from bpy.props import BoolProperty, StringProperty
from bpy.types import Context, EditBone, Event, Object, Operator, OperatorProperties, PoseBone, UILayout
from bpy.utils import flip_name

from ..bs_utils.hotkeys import register_hotkey
from ..generation.cloudrig import is_cloud_metarig
from ..generation.naming import uniqify

if TYPE_CHECKING:
    from ..properties import RigComponent

# Component parameter RNA paths which store a bone name.
# When using Smart Rename, these params will be kept in sync with their target bone.
# Component types can register their params here, see `register_bone_param()`.
BONE_STRING_REF_PARAMS = [
    'custom_props.props_storage_bone',
    'parenting.root_parent',
    'generator.ensure_root',
    'generator.properties_bone',
]


def register_bone_param(param_path: str):
    BONE_STRING_REF_PARAMS.append(param_path)


class OBJECT_OT_rename_with_symmetry(Operator):
    """Rename active object or bone while accounting for symmetry when possible."""

    bl_idname = "object.rename_with_symmetry"
    bl_label = iface_("Smart Rename")
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = 'new_name'

    def update_new_name(self, context: Context):
        for op_prop_name, _desired_name, new_name in get_future_names(self, context).values():
            setattr(self, op_prop_name, new_name)

    new_name: StringProperty(
        name="Name",
        description="Value to set the name of the active element to.",
        update=update_new_name,
    )
    use_symmetry: BoolProperty(
        name="Use Symmetry",
        description="Rename the symmetrical object/bone, not just the active one",
        default=True,
        options={'SKIP_SAVE'},
    )

    name_display: StringProperty(
        name="Final Name",
        description="Actual name that will be given to the active item, which may be different from the input if the desired name was already taken.",
    )
    name_display_flipped: StringProperty(
        name="Final Name",
        description="Actual name that will be given to the opposite item, which may be different from the input if the desired name was already taken.",
    )

    @property
    def new_name_opposite(self) -> str:
        return flip_name(self.new_name)

    @classmethod
    def poll(cls, context: Context):
        if get_active_item(context) is None:
            cls.poll_message_set("Nothing to rename.")
            return False
        return True

    def invoke(self, context: Context, _event: Event):
        self.rename_map = {}
        item = get_active_item(context)
        self.new_name = item.name
        opposite_item = get_opposite_item(item)
        if not opposite_item:
            self.use_symmetry = False

        return context.window_manager.invoke_props_dialog(self, width=320)

    def draw(self, context: Context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        name_row = layout.row(align=True)
        item = get_active_item(context)
        icon_id = UILayout.icon(item)
        name_row.prop(self, 'new_name', text="", icon_value=icon_id)
        opposite_item = get_opposite_item(item)
        if opposite_item and opposite_item != item:
            toggle_row = name_row.row(align=True)
            toggle_row.enabled = opposite_item is not None
            toggle_row.prop(self, 'use_symmetry', text="", icon='MOD_MIRROR')

        if self.new_name == item.name:
            layout.label(text="Name unchanged.")
            return

        box = layout.box()
        box.label(text="Rename:")

        warning = ""
        future_names = get_future_names(self, context)
        for (
            rename_item,
            (op_prop_name, desired_name, new_name),
        ) in future_names.items():
            icon_id = UILayout.icon(rename_item)
            self.draw_rename_preview(box, rename_item, op_prop_name, icon_value=icon_id)
            if new_name != desired_name:
                warning = rpt_("Names will be incremented.")
            elif len(future_names) > 1 and new_name == flip_name(new_name):
                warning = rpt_("Rename will break symmetry.")
        if warning:
            row = box.row()
            row.alert = True
            row.label(text=warning, icon='ERROR')

    def draw_rename_preview(self, layout: UILayout, item: Any, op_prop_name: str, icon_value: int):
        split = layout.row().split(align=True, factor=0.45)
        split.enabled = False
        row = split.row()
        row.prop(item, 'name', text="", icon_value=icon_value)
        split = split.row().split(factor=0.1)
        split.row().label(text="\u279c")
        split.row().prop(self, op_prop_name, text="", icon_value=icon_value)

    def execute(self, context: Context):
        counter = 0
        name_dict = {}
        for item, (_prop_name, _desired_name, new_name) in get_future_names(self, context).items():
            if item.name != new_name:
                counter += 1
            name_dict[item.name] = new_name
            item.name = new_name

        if context.mode == 'EDIT_ARMATURE' and is_cloud_metarig(context.active_object):
            # Refresh pose bone data, since it doesn't get synced from edit_bones until a
            # mode change. Must happen before the component param fixup below, which reads
            # and writes pose bone data.
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='EDIT')

        if type(item) in (PoseBone, EditBone):
            # Rename bones in component parameters.
            rig = context.pose_object or context.active_object
            for pb in rig.pose.bones:
                comp: RigComponent = pb.cloudrig_component
                if not comp.component_type or not comp.component_module:
                    continue
                bone_comp_name = comp.component_module.__name__.split(".")[-1].replace("cloud_", "")
                for param_path in BONE_STRING_REF_PARAMS:
                    component_name, param_name = param_path.split(".")
                    if component_name == 'generator':
                        param_owner = comp.id_data.cloudrig.generator
                    else:
                        if bone_comp_name != component_name and component_name not in ("custom_props", "parenting"):
                            continue
                        param_owner = getattr(comp.params, component_name)
                    if not param_owner:
                        continue
                    current_bone_name = getattr(param_owner, param_name)
                    if current_bone_name in name_dict:
                        setattr(param_owner, param_name, name_dict[current_bone_name])
                if comp.params.parenting.parent_switching:
                    for parent_slot in comp.params.parenting.parent_slots:
                        if parent_slot.bone in name_dict:
                            if parent_slot.bone == parent_slot.name:
                                parent_slot.name = name_dict[parent_slot.bone]
                            parent_slot.bone = name_dict[parent_slot.bone]

        msg = "Did nothing"
        if counter > 0:
            msg = "Renamed"
        if counter > 1:
            msg += " (Symmetrized)"

        self.report({'INFO'}, msg + "!")
        return {'FINISHED'}


def get_collprop(item: Any):
    """Return the collection property that contains the given item (objects, pose bones, or edit bones)."""
    if isinstance(item, Object):
        return bpy.data.objects
    elif isinstance(item, PoseBone):
        return item.id_data.pose.bones
    elif isinstance(item, EditBone):
        return item.id_data.edit_bones
    else:
        raise NotImplementedError(f"Data type not yet supported: {type(item)}")


def get_future_names(operator: OperatorProperties, context: Context) -> dict[Any, tuple[str, str, str]]:
    """Return a mapping of items to their (prop_name, desired_name, actual_new_name) rename tuples."""
    rename_dict = {}
    item = get_active_item(context)
    collprop = get_collprop(item)
    rename_dict[item] = (
        'name_display',
        operator.new_name,
        uniqify(operator.new_name, collprop, datablock=item, strip_first=False),
    )

    if not operator.use_symmetry:
        return rename_dict

    opposite_item = collprop.get(flip_name(item.name))
    if opposite_item and opposite_item != item:
        flipped_name = flip_name(operator.new_name)
        if flipped_name == operator.new_name:
            flipped_name = opposite_item.name
        rename_dict[opposite_item] = (
            'name_display_flipped',
            flipped_name,
            uniqify(flipped_name, collprop, datablock=opposite_item, strip_first=False),
        )

    return rename_dict


def get_active_item(context: Context) -> Any | None:
    """Return the currently active renameable item: an Object, PoseBone, or EditBone."""
    if context.mode == 'OBJECT' and context.object:
        return context.object
    elif context.mode in ('POSE', 'PAINT_WEIGHT') and context.active_pose_bone:
        return context.active_pose_bone
    elif context.mode == 'EDIT_ARMATURE':
        return context.active_bone


def get_opposite_item(item: Any) -> Any | None:
    """Return the symmetrical counterpart of item by flipping its name, or None if no counterpart exists."""
    collprop = get_collprop(item)
    return collprop.get(flip_name(item.name))


registry = [OBJECT_OT_rename_with_symmetry]


def register():
    register_hotkey(
        OBJECT_OT_rename_with_symmetry.bl_idname,
        hotkey_kwargs={'type': "F2", 'value': "PRESS"},
        keymap_name='3D View',
    )
