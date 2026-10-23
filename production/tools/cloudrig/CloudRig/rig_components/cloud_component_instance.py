# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..generation.cloud_generator import CloudRig_Generator
    from ..properties import RigComponent

from contextlib import contextmanager

from bpy.app.translations import pgettext_n as n_
from bpy.app.translations import pgettext_rpt as rpt_
from bpy.props import BoolProperty, StringProperty
from bpy.types import Context, PropertyGroup, UILayout
from bpy.utils import flip_name

from ..bs_utils.properties import copy_property_group
from ..bs_utils.ui import aligned_label
from ..generation.naming import side_is_left
from ..properties import ComponentParams
from .cloud_base import Component_Base
from .cloud_curve import Component_Curve_Hooked
from .cloud_curve_ik import Component_Curve_IK_Hooked
from .cloud_lattice import Component_Lattice
from .cloud_physics_chain import Component_PhysicsChain
from .cloud_spline_ik import Component_Curve_SplineIK


def _search_component_bones(self, context: Context, _edit_text: str) -> list[str]:
    """Return bones that have a component type assigned."""
    if not context.object or not context.object.pose:
        return []
    active_pbone = context.active_pose_bone
    return [pb.name for pb in context.object.pose.bones if pb.cloudrig_component.component_type and pb != active_pbone]


class Component_Instance(Component_Base):
    """Treat this bone as an instance of another bone's component, sharing its type and parameters."""

    ui_name = "Component Instance"

    is_component_instance = True

    def create_bone_infos(self, _context: Context):
        raise RuntimeError(
            f"Component_Instance.create_bone_infos() was called for bone '{self.base_bone_name}'. "
            "This should never happen — the instance should have been redirected to its source during instantiation."
        )

    @classmethod
    def do_instantiate(
        cls,
        generator: CloudRig_Generator,
        instance_rna: RigComponent,
        parent_component: Component_Base | None,
    ) -> Component_Base | None:
        """Validate the instancing chain and construct the source component in place of this bone."""
        source_bone_name = instance_rna.params.component_instance.source_bone
        source_pb = instance_rna.id_data.pose.bones.get(source_bone_name)
        if not source_pb:
            generator.raise_generation_error(
                rpt_("Component Instance: Source Not Found"),
                base_bone_name=instance_rna.base_bone_name,
                description=rpt_('Source bone "{bone}" was not found in the metarig.').format(
                    bone=source_bone_name or "(none)"
                ),
            )
            instance_rna.property_unset('params')
            return None
        if not source_pb.cloudrig_component.component_type:
            generator.raise_generation_error(
                rpt_("No Component to Instance"),
                base_bone_name=instance_rna.base_bone_name,
                description=rpt_('Bone "{bone}" has no component type assigned.').format(bone=source_bone_name),
            )
            instance_rna.property_unset('params')
            return None

        final_source = instance_rna.resolved_source
        if getattr(final_source.component_class, 'is_component_instance', False):
            generator.raise_generation_error(
                rpt_("Component Instance: Cycle Detected"),
                base_bone_name=instance_rna.base_bone_name,
                description=rpt_(
                    'A cycle was detected while resolving the source for bone "{bone}". '
                    'Check the source bone assignments for circular references.'
                ).format(bone=instance_rna.base_bone_name),
            )
            instance_rna.property_unset('params')
            return None

        params = instance_rna.params
        protected_params_list = [
            # NOTE: This list is sensitive to order, `source_bone`` has to be before `mirror`,
            # because of the update callback.
            'component_instance.source_bone',
            'component_instance.mirror',
            'lattice.lattice',
            'curve.target',
            'physics_chain.phys_obj',
        ]
        with protect_params(params, protected_params_list):
            copy_property_group(final_source.params, params, x_mirror=params.component_instance.mirror)

        return final_source.component_class(
            generator=generator,
            component_rna=instance_rna,
            parent_component=parent_component,
        )

    ##############################
    # Parameters

    @classmethod
    def set_param_defaults(cls, component: RigComponent):
        pbone = component.owner_pose_bone
        opp_pbone = pbone.id_data.pose.bones.get(flip_name(pbone.name))
        if opp_pbone and pbone != opp_pbone:
            component.params.component_instance.source_bone = opp_pbone.name
            component.params.component_instance.mirror = True

    @classmethod
    def draw_control_params(cls, layout: UILayout, context: Context, component: RigComponent):
        metarig = context.object
        source_bone_name = component.params.component_instance.source_bone
        source_pbone = metarig.pose.bones.get(source_bone_name)

        msg = ""
        if not source_bone_name:
            msg = n_("Source bone not specified!")
        elif not source_pbone:
            msg = n_("Source bone no longer exists!")
        elif not source_pbone.cloudrig_component.component_type:
            msg = n_("Source bone has no component assigned!")

        row = cls.draw_prop(
            context, layout, component.params.component_instance, 'source_bone', alert=bool(msg), icon='BONE_DATA'
        )
        op = row.operator("armature.jump_to_bone", text="", icon='LOOP_FORWARDS')
        op.use_target_rig = False
        op.target_bone = component.params.component_instance.source_bone
        if msg:
            aligned_label(layout, text=msg, alert=True, icon='ERROR')
            return
        cls.draw_prop(context, layout, component.params.component_instance, 'mirror')

        layout.separator()

        match source_pbone.cloudrig_component.component_class.ui_name:
            case Component_Lattice.ui_name:
                cls.draw_prop(context, layout, component.params.lattice, 'lattice')
            case Component_PhysicsChain.ui_name:
                cls.draw_prop(context, layout, component.params.physics_chain, 'phys_obj')
            case Component_Curve_Hooked.ui_name | Component_Curve_IK_Hooked.ui_name | Component_Curve_SplineIK.ui_name:
                cls.draw_prop(context, layout, component.params.curve, 'target')

    @classmethod
    def register_bone_pointers(cls):
        cls.register_bone_pointer("component_instance.source_bone")

    @classmethod
    def poll_draw_parenting_params(cls, _context: Context, _component: RigComponent) -> bool:
        return False

    @classmethod
    def poll_draw_appearance_params(cls, _context: Context, _component: RigComponent) -> bool:
        return False

    @classmethod
    def poll_draw_custom_prop_params(cls, _context: Context, component: RigComponent) -> bool:
        return False


@contextmanager
def protect_params(params: ComponentParams, param_paths: list[str]):
    def resolve(path: str) -> tuple[Any, str]:
        parts = path.split('.')
        obj = params
        for part in parts[:-1]:
            obj = getattr(obj, part)
        return obj, parts[-1]

    saved = [(path, getattr(*resolve(path))) for path in param_paths]
    try:
        yield
    finally:
        for path, value in saved:
            obj, attr = resolve(path)
            setattr(obj, attr, value)


class Params(PropertyGroup):
    def source_bone_update(self, context: Context):
        if not context.active_pose_bone:
            return
        bone_name = context.active_pose_bone.name
        if side_is_left(self.source_bone) is not None:
            self.mirror = side_is_left(self.source_bone) != side_is_left(bone_name)

    source_bone: StringProperty(
        name="Source Bone",
        description="The bone whose component type and parameters this bone will instance",
        search=_search_component_bones,
        search_options={'SORT'},
        update=source_bone_update,
    )
    mirror: BoolProperty(
        name="Mirror",
        description="Flip left/right side names when copying parameters from the source bone",
        default=False,
    )


RIG_COMPONENT_CLASS = Component_Instance
