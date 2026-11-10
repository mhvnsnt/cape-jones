# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..properties import RigComponent

from math import pi

from bpy.app.translations import pgettext_iface as iface_
from bpy.app.translations import pgettext_n as n_
from bpy.app.translations import pgettext_rpt as rpt_
from bpy.props import BoolProperty, IntProperty
from bpy.types import Context, PropertyGroup, UILayout
from mathutils import Vector

from ..rig_component_features.bone_info import BoneInfo
from ..rig_component_features.overlay_painter import no_overlay
from .cloud_fk_chain import Component_Chain_FK


class Component_Spine_Simple(Component_Chain_FK):
    ui_name = "Spine: Simple"
    forced_params = {
        'chain.segments': 1,
        'fk_chain.root': True,
        'fk_chain.hinge': False,
        'fk_chain.create_curl_control': False,
        'fk_chain.curl_each': False,
        'fk_chain.display_center': True,
        'fk_chain.counter_rotate_stretch_bones': 0.5,
    }
    parent_switch_behaviour = n_("The active parent will own the torso master control.")

    ################################
    # Inherited functions.

    @classmethod
    def set_param_defaults(cls, component: RigComponent):
        """Default to sharp B-bones for FK chains."""
        component.params.chain.sharp = False
        component.params.chain.smooth = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.bone_count < 3:
            self.raise_generation_error(
                rpt_("Spine: Simple component must consist of a chain of at least 3 connected bones!")
            )

        pivot_pos = self.params.spine_simple.pivot_pos
        if not (0 < pivot_pos < self.bone_count):
            self.raise_generation_error(
                rpt_(
                    'Pivot Position must be greater than 0 and less than the number of bones in the chain ("{count}").'
                ).format(count=self.bone_count)
            )

        self.torso_ctr = None
        self.hip_ctr = None
        self.chest_ctr = None

    def fk_chain__make_root_bone(self) -> BoneInfo:
        """Create the torso master control, in place of the usual plain FK root
        socket bone.
        """
        first_org = self.bones_org[0]

        torso_ctr = self.bone_sets['Spine Master'].new(
            name=self.naming.add_prefix(self.base_name, "TORSO"),
            source=first_org,
            parent=first_org.parent,
            custom_shape_name=self.params.spine_simple.shape_torso.shape_name,
        )
        torso_ctr.length *= 1.3
        torso_ctr.put(first_org.center)

        dupli_torso = None
        if self.params.fk_chain.double_first:
            dupli_torso = self.create_child_control(torso_ctr, self.bone_sets['Spine Controls'])

        if self.params.spine_simple.world_align:
            self.create_dsp_bone(torso_ctr)
            torso_ctr.vector = Vector((0, torso_ctr.length, 0))
            torso_ctr.roll = 0
            if dupli_torso:
                self.create_dsp_bone(dupli_torso)
                dupli_torso.vector = Vector((0, dupli_torso.length, 0))
                dupli_torso.roll = 0

        self.torso_ctr = dupli_torso or torso_ctr
        return self.torso_ctr

    def fk_chain__make(self, org_chain: list[BoneInfo]) -> list[BoneInfo]:
        pivot_pos = self.params.spine_simple.pivot_pos
        hip_orgs = org_chain[0:pivot_pos]
        chest_orgs = org_chain[pivot_pos:]

        self.__make_main_controls(hip_orgs, chest_orgs)

        hip_fk = self.__make_fk_and_mch_section(hip_orgs, self.hip_ctr, reverse=True)
        chest_fk = self.__make_fk_and_mch_section(chest_orgs, self.chest_ctr, reverse=False)

        return hip_fk + chest_fk

    @no_overlay
    def fk_chain__attach_org_to_fk(self, org_bones: list[BoneInfo], fk_bones: list[BoneInfo]):
        pivot_pos = self.params.spine_simple.pivot_pos
        for org_bone, fk_bone in zip(org_bones[:pivot_pos], fk_bones[:pivot_pos]):
            org_bone.use_connect = False
            org_bone.parent = fk_bone

        super().fk_chain__attach_org_to_fk(org_bones[pivot_pos:], fk_bones[pivot_pos:])

    @no_overlay
    def fk_chain__counter_rotate_str_bones(
        self, fk_chain: list[BoneInfo], main_str_bones: list[BoneInfo], influence=0.5
    ):
        """Only counter-rotate STR bones in the Chest section."""
        pivot_pos = self.params.spine_simple.pivot_pos
        super().fk_chain__counter_rotate_str_bones(fk_chain[pivot_pos:], main_str_bones[pivot_pos:], influence)

    @no_overlay
    def fk_chain__get_bones_for_test_animation(self) -> list[BoneInfo]:
        return self.bone_sets['Spine Controls']

    ################################
    # Simple Spine functions.

    def __make_main_controls(
        self,
        hip_orgs: list[BoneInfo],
        chest_orgs: list[BoneInfo],
    ):
        """Create the Hips and Chest controls, on either side of the pivot point,
        each acting as the root of its section's FK sub-chain.
        """
        self.hip_ctr = self.__make_main_control(
            "HIP",
            source_org=hip_orgs[-1],
            head=hip_orgs[-1].tail,
            tail=hip_orgs[0].head,
            orgs_section=hip_orgs,
            dsp_source=hip_orgs[0],
            shape_name=self.params.spine_simple.shape_hips.shape_name,
        )
        self.hip_ctr.custom_data['dsp_helper'].roll = -hip_orgs[1].roll
        self.chest_ctr = self.__make_main_control(
            "CHST",
            source_org=chest_orgs[0],
            head=chest_orgs[0].head,
            tail=chest_orgs[-1].tail,
            orgs_section=chest_orgs,
            dsp_source=chest_orgs[-1],
            shape_name=self.params.spine_simple.shape_chest.shape_name,
        )

    def __make_main_control(
        self,
        prefix: str,
        *,
        source_org: BoneInfo,
        head: Vector,
        tail: Vector,
        orgs_section: list[BoneInfo],
        dsp_source: BoneInfo,
        shape_name: str,
    ) -> BoneInfo:
        """Create one end control (Hip or Chest), spanning from the pivot boundary
        (head) out to the tip of its section (tail), with its widget's Override
        Transform following dsp_source so it visually tracks the whole section.
        """
        ctr = self.bone_sets['Spine Controls'].new(
            name=self.naming.add_prefix(self.base_name, prefix),
            source=source_org,
            parent=self.torso_ctr,
            head=head,
            tail=tail,
            custom_shape_name=shape_name,
            custom_shape_along_length=0.25,
            custom_shape_rotation_euler=Vector((0, pi / 2, 0)),
        )
        avg_length = sum(bone.length for bone in orgs_section) / len(orgs_section)
        avg_scale_xyz = sum((bone.custom_shape_scale_xyz for bone in orgs_section), Vector((1, 1, 1))) / len(
            orgs_section
        )
        ctr.custom_shape_scale_xyz = avg_scale_xyz / (ctr.length / avg_length)
        self.create_dsp_bone(ctr).parent = dsp_source
        if self.params.spine_simple.world_align:
            ctr.vector = Vector((0, ctr.length, 0))
            ctr.roll = 0
        return ctr

    def __make_fk_and_mch_section(
        self,
        orgs_section: list[BoneInfo],
        end_ctrl: BoneInfo,
        reverse: bool,
    ) -> list[BoneInfo]:
        fk_list = []
        mch_list = []
        for org_bone in orgs_section:
            fk_bone = self.bone_sets['FK Controls'].new(
                name=self.naming.add_prefix(org_bone, "FK"),
                source=org_bone,
                custom_shape_name=self.params.fk_chain.shape_fk.shape_name,
                inherit_scale=self.params.fk_chain.inherit_scale,
            )
            if reverse:
                fk_bone.reverse()
            if self.params.fk_chain.display_center:
                fk_bone.custom_shape_along_length = 0.5
            org_bone.custom_data['fk_bone'] = fk_bone
            fk_list.append(fk_bone)

            mch_bone = self.bone_sets['Mechanism Bones'].new(
                name=self.naming.add_prefix(org_bone, "MCH"),
                source=fk_bone,
            )
            mch_bone.vector = end_ctrl.y_axis.normalized() * mch_bone.length
            mch_bone.roll = end_ctrl.roll
            mch_list.append(mch_bone)

        # Parent each MCH under the next/previous FK bone,
        # and each FK bone under its own MCH bone.
        # In the Hip section this walks the list back-to-front, since the
        # section's FK bones are reversed.
        order = range(len(orgs_section) - 1, -1, -1) if reverse else range(len(orgs_section))
        parent = self.torso_ctr
        for idx in order:
            mch_list[idx].parent = parent
            fk_list[idx].parent = mch_list[idx]
            parent = fk_list[idx]

        if self.painter:
            return fk_list

        influence = 1 / len(orgs_section)
        for mch_bone in mch_list:
            mch_bone.add_constraint('COPY_TRANSFORMS', subtarget=end_ctrl, space='LOCAL', influence=influence)

        return fk_list

    ##############################
    # Parameters

    @classmethod
    def define_bone_sets(cls):
        """Create parameters for this rig's bone sets."""
        super().define_bone_sets()
        cls.define_bone_set(
            n_("Spine Master"),
            color_palette='THEME12',
            collections=['Spine Controls'],
            wire_width=2.0,
        )
        cls.define_bone_set(
            n_("Spine Controls"),
            color_palette='THEME13',
            collections=['Spine Controls'],
            wire_width=2.0,
        )

    @classmethod
    def draw_control_params(cls, layout: UILayout, context: Context, component: RigComponent):
        super().draw_control_params(layout, context, component)
        params = component.params

        layout.separator()
        cls.draw_control_label(layout, iface_("Spine"))
        cls.draw_prop(context, layout, params.spine_simple, 'pivot_pos')
        cls.draw_prop(context, layout, params.spine_simple, 'world_align')

    @classmethod
    def draw_appearance_params(cls, layout: UILayout, context: Context, component: RigComponent):
        super().draw_appearance_params(layout, context, component)
        params = component.params
        layout.separator()
        cls.draw_prop_custom_shape(context, layout, params.spine_simple, "shape_torso")
        cls.draw_prop_custom_shape(context, layout, params.spine_simple, "shape_hips")
        cls.draw_prop_custom_shape(context, layout, params.spine_simple, "shape_chest")


class Params(PropertyGroup):
    pivot_pos: IntProperty(
        name="Pivot Position",
        description="Number of bones (from the base of the chain) that belong to the Hips section; the rest belong to the Chest section",
        default=2,
        min=1,
    )
    world_align: BoolProperty(
        name="World-Align Controls",
        description="Align the master, hips, and chest controls with the world axes",
        default=True,
    )

    shape_torso: Component_Chain_FK.make_custom_shape_params(
        identifier="Torso",
        default="Torso",
    )
    shape_hips: Component_Chain_FK.make_custom_shape_params(
        identifier="Hips",
        default="Saddle",
    )
    shape_chest: Component_Chain_FK.make_custom_shape_params(
        identifier="Chest",
        default="Saddle",
    )


RIG_COMPONENT_CLASS = Component_Spine_Simple
