# SPDX-License-Identifier: GPL-3.0-or-later

from bpy.app.translations import pgettext_rpt as rpt_
from bpy.types import Context, Operator, PoseBone
from bpy.utils import flip_name

from ..bs_utils.properties import copy_property_group
from ..generation.cloudrig import active_rig


class POSE_OT_cloudrig_symmetrize_components(Operator):
    """Mirror rig component type and parameters of selected bones to the opposite side. Names should end in L/R"""

    bl_idname = "pose.cloudrig_symmetrize_components"
    bl_label = "Symmetrize Components"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: Context):
        msg = poll_flippable_bone(context)
        if msg:
            cls.poll_message_set(msg)
            return False

        obj = context.active_object
        sel_bones = context.selected_pose_bones
        for pb in sel_bones:
            mirrored_name = flip_name(pb.name)
            if mirrored_name != pb.name and mirrored_name in obj.pose.bones:
                return True
        cls.poll_message_set("No selected bones have a CloudRig Component assigned. Nothing to symmetrize.")
        return False

    def execute(self, context: Context):
        # First make sure that all selected bones can be mirrored unambiguously.
        for from_pbone in context.selected_pose_bones:
            to_pbone = from_pbone.id_data.pose.bones.get(flip_name(from_pbone.name))
            if not to_pbone:
                # Bones without an opposite will just be ignored.
                continue
            if to_pbone != from_pbone and to_pbone.select:
                self.report(
                    {'ERROR'},
                    rpt_(
                        "Bone {bone} selected on both sides, mirroring would be ambiguous, "
                        "aborting. Only select the left or right side, not both!"
                    ).format(bone=from_pbone.name),
                )
                return {'CANCELLED'}

        # Then mirror the parameters.
        num_mirrored = mirror_cloudrig_components(context.selected_pose_bones)
        self.report({'INFO'}, rpt_("Mirrored parameters of {num_mirrored} bones.").format(num_mirrored=num_mirrored))

        return {'FINISHED'}


class POSE_OT_cloudrig_copy_component(Operator):
    """Copy rig component type and parameters from active to selected bones"""

    bl_idname = "pose.cloudrig_copy_component"
    bl_label = "Copy Component to Selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: Context):
        obj = context.active_object
        if not obj or obj.type != 'ARMATURE' or obj.mode != 'POSE':
            cls.poll_message_set("Active armature must be in pose mode.")
            return False

        active = context.active_pose_bone
        if not active or not active.cloudrig_component.component_type:
            cls.poll_message_set("Active bone has no CloudRig Component assigned.")
            return False

        select = context.selected_pose_bones
        if len(select) < 2:
            cls.poll_message_set("At least two bones must be selected.")
            return False

        if active not in select:
            cls.poll_message_set("Make sure the active bone is also selected.")
            return False

        return True

    def execute(self, context: Context):
        from_bone = context.active_pose_bone

        num_copied = 0
        for to_bone in context.selected_pose_bones:
            if to_bone == from_bone:
                continue
            num_copied += 1
            copy_property_group(from_bone.cloudrig_component, to_bone.cloudrig_component, x_mirror=False)

        self.report(
            {'INFO'},
            rpt_("Copied {component_type} parameters to {num_copied} bones.").format(
                component_type=from_bone.cloudrig_component.component_type, num_copied=num_copied
            ),
        )

        return {'FINISHED'}


def mirror_cloudrig_components(source_pbones: list[PoseBone]) -> int:
    num_mirrored = 0

    for from_pbone in source_pbones:
        to_pbone = from_pbone.id_data.pose.bones.get(flip_name(from_pbone.name))
        if to_pbone == from_pbone or not to_pbone:
            # Bones without an opposite will just be ignored.
            continue
        if to_pbone.cloudrig_component.component_type == 'Component Instance':
            continue

        copy_property_group(from_pbone.cloudrig_component, to_pbone.cloudrig_component, x_mirror=True)

        num_mirrored += 1

    return num_mirrored


def poll_flippable_bone(context: Context) -> str:
    """Return an error message explaining why there is no flippable bone in the active context.
    Otherwise, return an empty string.
    """
    rig = active_rig(context)
    if not rig:
        return "No active armature."

    sel_bones = context.selected_bones or context.selected_pose_bones
    if not sel_bones:
        return "No selected bones."

    for bone in sel_bones:
        if bone.name != flip_name(bone.name):
            return ""

    return "No selected flippable bones."


def draw_copy_mirror_ops(self, context: Context):
    layout = self.layout
    if context.mode == 'POSE':
        layout.separator()
        layout.operator(
            POSE_OT_cloudrig_copy_component.bl_idname,
            icon='DUPLICATE',
            text="Copy Rig Component",
        )
        layout.operator(
            POSE_OT_cloudrig_symmetrize_components.bl_idname,
            icon='MOD_MIRROR',
            text="Symmetrize Rig Component",
        )


# =============================================
# Registration

registry = [POSE_OT_cloudrig_symmetrize_components, POSE_OT_cloudrig_copy_component]
