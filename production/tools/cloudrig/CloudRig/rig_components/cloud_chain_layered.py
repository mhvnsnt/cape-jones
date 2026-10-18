# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..properties import ComponentParams, RigComponent

from bpy.app.translations import pgettext_iface as iface_
from bpy.app.translations import pgettext_n as n_
from bpy.props import StringProperty
from bpy.types import Context, Object, PoseBone, PropertyGroup, UILayout
from mathutils import Vector

from ..rig_component_features.bone_info import BoneInfo, ConstraintInfo
from ..utils.maths import point_to_segment_dist
from .cloud_base import Component_Base
from .cloud_chain import Component_ToonChain


class Component_LayeredChain(Component_ToonChain):
    """Chain with an additional PCH (parent chain) layer above the regular STR controls.
    STR controls are attached to the DEF bones of a named chain component, or to a
    synthesized bendy bone spanning the full chain (Self Parent mode).
    """

    ui_name = "Chain: Layered"

    forced_params = {'chain.tip_control': True}

    ################################
    # Inherited functions.

    def base__relink_get_target(self, org_i: int, con_info: ConstraintInfo) -> BoneInfo:
        """Return the bone to which a constraint should be moved to."""
        # Ask the Chain: Toon component where it would like the constraint to be moved to.
        to_bone = super().base__relink_get_target(org_i, con_info)

        # If the target is the first or last main STR bone, move it to the PCH bone instead.
        pch_bones = self.bone_sets['Parent Stretch Controls']
        if pch_bones:
            if to_bone is self.main_str_bones[0]:
                to_bone = pch_bones[0]
            elif to_bone is self.main_str_bones[-1]:
                to_bone = pch_bones[-1]

        return to_bone

    def create_bone_infos(self, context: Context):
        super().create_bone_infos(context)
        self._attach_to_parent_chain()

    ################################
    # Layered Chain functions.

    def _attach_to_parent_chain(self):
        """Constrain each main STR bone's parent helper to the closest DEF bone of the
        parent chain component, or synthesize a self-parent bone if no chain is named."""
        chain_name = self.params.chain_layered.parent_chain

        if chain_name:
            parent_chain_comp: Component_ToonChain | None = next(
                (
                    comp
                    for comp in self.generator.all_components
                    if isinstance(comp, Component_ToonChain) and comp.base_bone_name == chain_name
                ),
                None,
            )
            if not parent_chain_comp:
                from bpy.app.translations import pgettext_rpt as rpt_

                self.raise_generation_error(rpt_('Parent Chain component "{name}" not found.').format(name=chain_name))
            parent_def_bones = list(parent_chain_comp.bones_def)
            if not parent_def_bones:
                return
        else:
            parent_def_bones = [self._make_self_parent_bone()]

        for str_bone in self.main_str_bones:
            closest_def = min(parent_def_bones, key=lambda d: point_to_segment_dist(str_bone.head, d.head, d.tail))

            arm_con = str_bone.parent_armature_constraint
            if arm_con:
                arm_con.targets = [closest_def.name]
            else:
                parent_helper = self.create_parent_bone(str_bone, bone_set=self.bones_mch)
                parent_helper.add_constraint('ARMATURE', subtarget=closest_def)
                parent_helper.parent = None

    def _make_self_parent_bone(self) -> BoneInfo:
        """Create a mini chain (2 PCH-STR controls + 1 bendy PCH-DEF bone) spanning the full chain.
        The PCH-STR controls are animator-facing; the PCH-DEF bone is what the main STR bones attach to.
        """
        first_org = self.bones_org[0]
        last_org = self.bones_org[-1]
        root_parent = first_org.parent

        pch_start_head = self.str_chain[0].head.copy()
        pch_end_head = self.str_chain[-1].head.copy()
        chain_direction = (pch_end_head - pch_start_head).normalized()
        str_length = first_org.length / self.params.chain.segments / 3

        pch_str_start = self.bone_sets['Parent Stretch Controls'].new(
            name=self.str_chain[0].name.replace("STR-", "PCH-"),
            source=first_org,
            head=pch_start_head,
            vector=chain_direction,
            length=str_length,
            parent=root_parent,
            custom_shape_name=self.params.chain_layered.shape_layer_ends.shape_name,
            use_custom_shape_bone_size=False,
            custom_shape_scale_xyz=self.main_str_bones[0].custom_shape_scale_xyz.copy() * Vector((1, -1, 1)),
        )
        pch_str_start.custom_shape_scale_xyz.y *= -1
        pch_str_start.roll_align_other(first_org)

        pch_str_end = self.bone_sets['Parent Stretch Controls'].new(
            name=self.str_chain[-1].name.replace("STR-", "PCH-"),
            source=last_org,
            head=pch_end_head,
            vector=chain_direction,
            length=str_length,
            parent=root_parent,
            custom_shape_name=self.params.chain_layered.shape_layer_ends.shape_name,
            use_custom_shape_bone_size=False,
            custom_shape_scale_xyz=self.main_str_bones[-1].custom_shape_scale_xyz.copy(),
        )
        pch_str_end.roll_align_other(last_org)

        pch_str_start.next = pch_str_end
        pch_str_end.prev = pch_str_start

        pch_str_chain = [pch_str_start, pch_str_end]
        self.tangent_helpers = []
        if self.needs_tangent_helpers:
            # Create tangent helpers that will control bendy bone curvature
            self.tangent_helpers = self.chain__make_tangent_helpers(pch_str_chain)

        pch_def = self.bones_mch.new(
            name=self.str_chain[0].name.replace("STR-", "PCH-DEF-"),
            source=first_org,
            head=pch_start_head,
            tail=pch_end_head,
            parent=pch_str_start,
            inherit_scale='NONE',
        )
        pch_def.roll_align_other(first_org)
        self.toon__setup_def_bone(
            def_bone=pch_def,
            org_bone=None,
            str_bone=pch_str_start,
            next_str_bone=pch_str_end,
            bbone_segments_override=32,
            create_def_ctr=False,
        )

        return pch_def

    ##############################
    # Parameters

    @classmethod
    def draw_stretch_control_params(cls, layout: UILayout, context: Context, component: RigComponent):
        super().draw_stretch_control_params(layout, context, component)
        params = component.params

        cls.draw_control_label(layout, iface_("Layer"))

        cls.draw_prop(context, layout, params.chain_layered, 'parent_chain', icon='BONE_DATA')

    @classmethod
    def draw_appearance_params(cls, layout: UILayout, context: Context, component: RigComponent):
        super().draw_appearance_params(layout, context, component)
        layout.separator()
        params = component.params
        cls.draw_prop_custom_shape(context, layout, params.chain_layered, 'shape_layer_stretch')
        cls.draw_prop_custom_shape(context, layout, params.chain_layered, 'shape_layer_ends')

    @classmethod
    def register_bone_pointers(cls):
        cls.register_bone_pointer("chain_layered.parent_chain")

    @classmethod
    def is_bone_set_used(cls, context: Context, rig: Object, params: ComponentParams, set_name: str) -> bool:
        """Return whether the named bone set is used given the current params."""
        if set_name in ["parent_stretch_controls"]:
            return not params.chain_layered.parent_chain
        return super().is_bone_set_used(context, rig, params, set_name)

    @classmethod
    def define_bone_sets(cls):
        """Create parameters for this rig's bone sets."""
        super().define_bone_sets()
        cls.define_bone_set(n_("Parent Stretch Controls"), color_palette='THEME09')


def _search_parent_chain(self, context: Context, _edit_text: str) -> list[str]:
    """Return ToonChain components that are ancestors of the active bone."""
    if not context.object or not context.object.pose:
        return []

    def parents_recursive(pbone: PoseBone) -> list[PoseBone]:
        parents = []
        parent = pbone.parent
        while parent:
            parents.append(parent)
            parent = parent.parent
        return parents

    active_pbone = context.active_pose_bone
    parents = parents_recursive(active_pbone)

    return [
        pbone.name
        for pbone in context.object.pose.bones
        if pbone.cloudrig_component.component_type
        and issubclass(pbone.cloudrig_component.component_class, Component_ToonChain)
        and pbone != active_pbone
        and pbone in parents
    ]


class Params(PropertyGroup):
    parent_chain: StringProperty(
        name="Parent Chain",
        description="Select a parent Chain Component whose DEF bones this component's STR controls will attach to. Leave empty to auto-generate a self-parent spanning the full chain",
        default="",
        search=_search_parent_chain,
        search_options={'SORT'},
    )

    shape_layer_stretch: Component_Base.make_custom_shape_params(identifier="Stretch Layer", default="Sphere 2")
    shape_layer_ends: Component_Base.make_custom_shape_params(identifier="Stretch Layer Ends", default="Arrow 3")


RIG_COMPONENT_CLASS = Component_LayeredChain
