# SPDX-License-Identifier: GPL-3.0-or-later

from bpy.app.translations import pgettext_rpt as rpt_
from bpy.types import Context, Object, Operator

from ..bs_utils.properties import copy_property_group
from ..generation.cloudrig import is_cloud_metarig, read_rig_panels, write_rig_panels
from ..rig_component_features.mechanism import copy_driver


class OBJECT_OT_copy_bone_collections(Operator):
    "Copy bone collections, bone set assignments of components with matching bone names, and the Bone Collections UI panel if it exists, from active to selected metarigs."

    bl_idname = "object.cloudrig_copy_bone_collections"
    bl_label = "Copy Bone Collections"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: Context):
        if not is_cloud_metarig(context.active_object):
            cls.poll_message_set("Active object must be a CloudRig metarig.")
            return False
        if not get_target_metarigs(context):
            cls.poll_message_set("Select at least one other CloudRig metarig besides the active one.")
            return False
        return True

    def execute(self, context: Context):
        source = context.active_object
        targets = get_target_metarigs(context)

        for target in targets:
            copy_cloudrig_bonecolls(source, target)

        self.report(
            {'INFO'},
            rpt_("Copied bone collections to {num_targets} armature(s).").format(num_targets=len(targets)),
        )

        return {'FINISHED'}


def get_target_metarigs(context: Context) -> list[Object]:
    """Return the selected CloudRig metarigs, excluding the active object."""
    active = context.active_object
    return [obj for obj in context.selected_objects if obj is not active and is_cloud_metarig(obj)]


def copy_cloudrig_bonecolls(source: Object, target: Object):
    """Clear target's bone collections and replace them with a copy of source's.
    Bones with matching names in both armatures are assigned to the same collections, and the Bone
    Sets of their cloudrig components (which decide collection assignment at generation time) are copied too.
    If source has a "Bone Collections" UI panel, it is copied over too, overwriting target's.
    """
    for coll in target.data.collections_all[:]:
        if coll.is_editable:
            target.data.collections.remove(coll)

    # Collections are created first, and parented in a second pass below,
    # since `collections_all` is not guaranteed to be in hierarchy order.
    for src_coll in source.data.collections_all:
        tgt_coll = target.data.collections.new(src_coll.name)
        tgt_coll.is_visible = src_coll.is_visible
        tgt_coll.is_solo = src_coll.is_solo
        copy_property_group(
            src_coll.cloudrig_info,
            tgt_coll.cloudrig_info,
        )

    for src_coll in source.data.collections_all:
        if not src_coll.parent:
            continue
        tgt_coll = target.data.collections_all.get(src_coll.name)
        tgt_coll.parent = target.data.collections_all.get(src_coll.parent.name)

    copy_bone_collection_visibility_drivers(source, target)

    for src_pbone in source.pose.bones:
        tgt_pbone = target.pose.bones.get(src_pbone.name)
        if not tgt_pbone:
            continue

        for src_coll in src_pbone.bone.collections:
            tgt_coll = target.data.collections_all.get(src_coll.name)
            if tgt_coll:
                tgt_coll.assign(tgt_pbone)

        if src_pbone.cloudrig_component.component_type:
            copy_property_group(
                src_pbone.cloudrig_component.params.bone_sets,
                tgt_pbone.cloudrig_component.params.bone_sets,
            )

    source_panels = read_rig_panels(source)
    if "Bone Collections" in source_panels:
        target_panels = read_rig_panels(target)
        target_panels["Bone Collections"] = source_panels["Bone Collections"]
        write_rig_panels(target, target_panels)


def copy_bone_collection_visibility_drivers(source: Object, target: Object):
    """Copy drivers on bone collections' `is_visible` property from source to target.
    Any driver variable that targets the source metarig (its object or its armature data)
    is repointed to target instead, so the copied drivers keep working.
    """
    if not source.data.animation_data:
        return

    for fcurve in source.data.animation_data.drivers:
        if not (fcurve.data_path.startswith('collections_all["') and fcurve.data_path.endswith('"].is_visible')):
            continue

        new_fcurve = copy_driver(fcurve, target.data)
        for variable in new_fcurve.driver.variables:
            for var_target in variable.targets:
                if var_target.id == source:
                    var_target.id = target
                elif var_target.id == source.data:
                    var_target.id = target.data


registry = [
    OBJECT_OT_copy_bone_collections,
]
