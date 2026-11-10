# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from math import pi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..properties import RigComponent

from bpy.props import EnumProperty
from bpy.types import Context, PropertyGroup, UILayout
from mathutils import Vector

from .cloud_fk_chain import Component_Chain_FK


class Component_Shoulder(Component_Chain_FK):
    """A single bone control to connect an arm to a spine."""

    ui_name = "Shoulder Bone"
    forced_params = {
        'chain.segments': 1,
        'fk_chain.display_center': False,
        'fk_chain.create_curl_control': False,
        'fk_chain.counter_rotate_stretch_bones': 0.0,
        'fk_chain.double_first': False,
    }

    max_bones_in_chain = 1

    ##############################
    # Inherited functions.

    def create_bone_infos(self, context: Context):
        """Build the FK chain, then apply shoulder-specific shape rotation and parent override."""
        super().create_bone_infos(context)
        self.__make_shoulder()

    ##############################
    # Shoulder functions.

    def __make_shoulder(self):
        """Rotate the shoulder control's custom shape to match the fwd_axis parameter, then reparent to the ORG bone's parent."""
        shoulder = self.bone_sets['FK Controls'][0]
        shoulder.custom_shape_name = self.params.fk_chain.shape_fk.shape_name
        fwd_axis = self.params.shoulder.fwd_axis
        is_right = self.naming.side_is_left(self.base_bone_name) is False
        shoulder_rot = {
            '+Z': -pi / 2,
            '+X': 0,
            '-Z': pi / 2,
            '-X': pi,
        }[fwd_axis] + pi * is_right

        shoulder.custom_shape_rotation_euler.y += shoulder_rot
        offsets = {
            '+Z': Vector((-1, 0, 0)),
            '+X': Vector((0, 0, 1)),
            '-Z': Vector((1, 0, 0)),
            '-X': Vector((0, 0, -1)),
        }

        shoulder.custom_shape_translation += offsets[fwd_axis] * shoulder.length * (-1 if is_right else 1)
        shoulder.custom_shape_translation.y += shoulder.length

        parent = self.find_bone_info(self.base_bone_name).parent
        if parent:
            shoulder.parent = parent

    ##############################
    # Parameters

    @classmethod
    def draw_appearance_params(cls, layout: UILayout, context: Context, component: RigComponent):
        super().draw_appearance_params(layout, context, component)
        params = component.params

        cls.draw_prop(context, layout, params.shoulder, 'fwd_axis', enabled=component.appearance_enabled)

    @classmethod
    def set_param_defaults(cls, component: RigComponent):
        component.params.fk_chain.shape_fk.name = "Shoulder"


class Params(PropertyGroup):
    fwd_axis: EnumProperty(
        name="Forward Axis",
        description="Rotate the bone shape to align with this axis of the bone",
        items=[
            ("+Z", '+Z', "Align with bone's +Z as forward axis"),
            ("+X", '+X', "Align with bone's +X as forward axis"),
            ("-Z", '-Z', "Align with bone's -Z as forward axis"),
            ("-X", '-X', "Align with bone's +X as forward axis"),
        ],
    )


RIG_COMPONENT_CLASS = Component_Shoulder
