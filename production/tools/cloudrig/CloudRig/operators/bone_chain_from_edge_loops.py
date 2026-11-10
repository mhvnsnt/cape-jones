# SPDX-License-Identifier: GPL-3.0-or-later

import re
from collections.abc import Iterable

import bmesh
import bpy
import numpy as np
from bmesh.types import BMEdge, BMesh
from bpy.app.translations import pgettext_rpt as rpt_
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import Context, Event, Object, Operator
from mathutils import Vector

_HASH_RUN = re.compile(r"#+")


class MESH_OT_bone_chain_from_edge_loops(Operator):
    """Create a chain of bones connecting the centers of the selected edge loops, then parent the mesh to the armature. Reuses the armature from the mesh's Armature modifier if it has one, otherwise creates a new 'Armature' object"""

    bl_idname = "mesh.bone_chain_from_edge_loops"
    bl_label = "Bone Chain From Edge Loops"
    bl_options = {'REGISTER', 'UNDO'}

    name_pattern: StringProperty(
        name="Bone Name",
        description=(
            "Name pattern for the newly created bones. A run of '#' characters is "
            "replaced with a zero-padded number, e.g. 'Spike_01_####' -> 'Spike_01_0001'"
        ),
        default="Bone_###",
    )
    focus_rig: BoolProperty(
        name="Focus Rig",
        description=(
            "Switch to Pose Mode on the armature after creating the bones. "
            "If disabled, stay in Edit Mode on the mesh instead"
        ),
        default=True,
    )
    automatic_weights: BoolProperty(
        name="Automatic Weights",
        description=(
            "Parent the mesh to the armature with automatically calculated weights. "
            "If disabled, the mesh is parented with empty vertex groups instead"
        ),
        default=True,
    )
    root_end: EnumProperty(
        name="Root End",
        description="Which end of the selected loops becomes the root of the bone chain",
        items=[
            ('THICK', "Thick End", "The thicker (larger circumference) end becomes the root"),
            ('THIN', "Thin End", "The thinner (smaller circumference) end becomes the root"),
        ],
        default='THICK',
    )

    @classmethod
    def poll(cls, context: Context):
        mesh_obj = context.edit_object
        if not mesh_obj or mesh_obj.type != 'MESH':
            cls.poll_message_set("Must be in Edit Mode on a mesh object.")
            return False
        return True

    def invoke(self, context: Context, _event: Event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context: Context):
        mesh_obj = context.edit_object
        bm = bmesh.from_edit_mesh(mesh_obj.data)

        try:
            loop_groups = get_selected_edge_loop_groups(bm)
            if len(loop_groups) < 2:
                raise RuntimeError(
                    rpt_(
                        "Found only {count} connected loop(s). Select at least 2 separate edge loops to form a chain."
                    ).format(count=len(loop_groups))
                )

            # Centers in local space -> world space
            centers_local = [group_center(group) for group in loop_groups]
            mat_world = mesh_obj.matrix_world
            centers_world = [mat_world @ center for center in centers_local]

            order = order_indices_along_main_axis(centers_world)
            centers_world = [centers_world[i] for i in order]
            loop_groups = [loop_groups[i] for i in order]

            # Sanity check for degenerate (coincident) centers
            cleaned_centers = [centers_world[0]]
            cleaned_groups = [loop_groups[0]]
            for center, group in zip(centers_world[1:], loop_groups[1:]):
                if (center - cleaned_centers[-1]).length > 1e-6:
                    cleaned_centers.append(center)
                    cleaned_groups.append(group)
            centers_world = cleaned_centers
            loop_groups = cleaned_groups

            if len(centers_world) < 2:
                raise RuntimeError(rpt_("Loop centers are too close together to form bones."))

            # Chain direction: use loop circumference as a "thickness" heuristic to tell
            # which end is thick vs. thin, then orient the chain per `root_end`.
            first_length = loop_edge_length_sum(loop_groups[0])
            last_length = loop_edge_length_sum(loop_groups[-1])
            first_is_thick_end = first_length >= last_length
            want_thick_root = self.root_end == 'THICK'
            if first_is_thick_end != want_thick_root:
                centers_world.reverse()
        except RuntimeError as error:
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}

        # Leave edit mode on the mesh before creating the armature
        bpy.ops.object.mode_set(mode='OBJECT')

        arm_obj = find_armature_modifier_object(mesh_obj)
        if arm_obj is None:
            arm_data = bpy.data.armatures.new("Armature")
            arm_obj = bpy.data.objects.new("Armature", arm_data)
            context.collection.objects.link(arm_obj)

        bone_names = next_free_bone_names(self.name_pattern, len(centers_world) - 1, arm_obj.data.bones.keys())

        context.view_layer.objects.active = arm_obj
        mesh_obj.select_set(False)
        arm_obj.select_set(True)

        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = arm_obj.data.edit_bones

        prev_bone = None
        for i in range(len(centers_world) - 1):
            bone = edit_bones.new(bone_names[i])
            bone.head = centers_world[i]
            bone.tail = centers_world[i + 1]
            if prev_bone is not None:
                bone.parent = prev_bone
                bone.use_connect = True
            prev_bone = bone

        bpy.ops.object.mode_set(mode='OBJECT')

        # ---- Parent mesh to armature with automatic weights ----
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        arm_obj.select_set(True)
        context.view_layer.objects.active = arm_obj  # active object = armature (required for parenting)

        # Always parent with empty groups first: this sets up the parenting and the
        # Armature modifier (and creates missing vertex groups) without touching any
        # weights that may already exist on other bones of a reused armature.
        bpy.ops.object.parent_set(type='ARMATURE_NAME')

        if self.automatic_weights:
            assign_automatic_weights(context, mesh_obj, arm_obj, bone_names)

        if self.focus_rig:
            # ---- Back to Pose Mode on the armature ----
            bpy.ops.object.select_all(action='DESELECT')
            arm_obj.select_set(True)
            context.view_layer.objects.active = arm_obj
            bpy.ops.object.mode_set(mode='POSE')
        else:
            # ---- Back to Edit Mode on the mesh ----
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            context.view_layer.objects.active = mesh_obj
            bpy.ops.object.mode_set(mode='EDIT')

        self.report(
            {'INFO'},
            rpt_(
                "Created {bone_count} bones from {loop_count} edge loops, and parented '{mesh_name}' {weights_desc}."
            ).format(
                bone_count=len(centers_world) - 1,
                loop_count=len(loop_groups),
                mesh_name=mesh_obj.name,
                weights_desc=rpt_("with automatic weights") if self.automatic_weights else rpt_("with empty groups"),
            ),
        )

        return {'FINISHED'}


def get_selected_edge_loop_groups(bm: BMesh) -> list[list[BMEdge]]:
    """Split the current edge selection into connected components (individual loops)."""
    selected_edges = [edge for edge in bm.edges if edge.select]
    if not selected_edges:
        raise RuntimeError(rpt_("No edges selected. Select one or more edge loops in Edit Mode."))

    visited = set()
    groups = []

    for start_edge in selected_edges:
        if start_edge in visited:
            continue
        stack = [start_edge]
        visited.add(start_edge)
        component = []

        while stack:
            edge = stack.pop()
            component.append(edge)
            for vert in edge.verts:
                for other_edge in vert.link_edges:
                    if other_edge.select and other_edge not in visited:
                        visited.add(other_edge)
                        stack.append(other_edge)

        groups.append(component)

    return groups


def group_center(edges: list[BMEdge]) -> Vector:
    """Average vertex position of a connected edge group (loop)."""
    verts = set()
    for edge in edges:
        verts.add(edge.verts[0])
        verts.add(edge.verts[1])
    total = Vector((0, 0, 0))
    for vert in verts:
        total += vert.co
    return total / len(verts)


def order_indices_along_main_axis(centers: list[Vector]) -> list[int]:
    """Return the permutation of indices that sorts `centers` along the mesh's
    principal axis (PCA), so bones chain correctly along the 'cylinder' even
    if loop spacing is irregular."""
    pts = np.array([tuple(c) for c in centers])
    centroid = pts.mean(axis=0)
    centered = pts - centroid

    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    main_axis = eigvecs[:, np.argmax(eigvals)]

    proj = centered @ main_axis
    return list(np.argsort(proj))


def loop_edge_length_sum(edges: list[BMEdge]) -> float:
    """Total edge length of a loop. Used as a 'thickness' heuristic to guess
    which end of the chain is the base vs. the tip."""
    return sum(edge.calc_length() for edge in edges)


def assign_automatic_weights(context: Context, mesh_obj: Object, arm_obj: Object, bone_names: Iterable[str]):
    """Recalculate heat-map automatic weights for only `bone_names`, leaving the
    vertex groups of every other bone in the armature untouched.
    """
    bone_name_set = set(bone_names)
    for pose_bone in arm_obj.pose.bones:
        pose_bone.select = pose_bone.name in bone_name_set

    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    context.view_layer.objects.active = mesh_obj
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    bpy.ops.paint.weight_from_bones(type='AUTOMATIC')
    bpy.ops.object.mode_set(mode='OBJECT')


def find_armature_modifier_object(mesh_obj: Object) -> Object | None:
    """Return the armature object referenced by the mesh's first Armature
    modifier, or None if it has none."""
    for mod in mesh_obj.modifiers:
        if mod.type == 'ARMATURE' and mod.object:
            return mod.object
    return None


def bone_name_from_pattern(pattern: str, index: int) -> str:
    """Fill a run of '#' characters in `pattern` with a zero-padded `index`,
    e.g. bone_name_from_pattern("Spike_01_####", 1) -> "Spike_01_0001".
    If `pattern` has no '#' run, falls back to a simple numbered suffix."""
    match = _HASH_RUN.search(pattern)
    if not match:
        return f"{pattern}_{index:02d}"
    padding = len(match.group(0))
    return f"{pattern[: match.start()]}{index:0{padding}d}{pattern[match.end() :]}"


def next_free_bone_names(pattern: str, count: int, existing_names: Iterable[str]) -> list[str]:
    """Generate `count` bone names from `pattern`, skipping over any names
    already present in `existing_names` by incrementing the number until a
    free one is found. Lets the operator be re-run on the same armature
    without colliding with bones from a previous run."""
    used = set(existing_names)
    names = []
    index = 1
    while len(names) < count:
        name = bone_name_from_pattern(pattern, index)
        if name not in used:
            names.append(name)
            used.add(name)
        index += 1
    return names


def draw_menu_entry(self, _context: Context):
    self.layout.operator(MESH_OT_bone_chain_from_edge_loops.bl_idname, icon='BONE_DATA')


registry = [MESH_OT_bone_chain_from_edge_loops]


def register():
    bpy.types.VIEW3D_MT_mesh_add.append(draw_menu_entry)


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_menu_entry)
