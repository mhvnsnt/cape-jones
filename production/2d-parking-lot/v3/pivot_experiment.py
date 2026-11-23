#!/usr/bin/env python3
"""PIVOT EXPERIMENT — decisive test of bone-parent inverse formulas.
Bone: head (0,10,0), tail (0,5,0) (points down, like armR).
Plane: 1x2 units, centre (0,7.5,0) — i.e. 2.5 units below the bone HEAD.
Rotate the bone -90 deg about Z in pose mode and read the plane centre.

Expected if the pivot is the bone HEAD (correct, anatomical):
  rel point (0,-2.5) rotated -90deg -> (-2.5,0) -> world (-2.5, 10)
Expected if the pivot is the bone TAIL (the V2 rig's parent_keep):
  rel point (0,+2.5) rotated -90deg -> (+2.5,0) -> world (2.5, 5)
Expected if the pivot is the plane centre (no parenting effect):
  (0, 7.5)

Formulas tested:
  A canonical: mpi = (arm_mw @ pb.matrix).inverted() @ ob.matrix_world
  B V2 tail:   mpi = (arm_mw @ m).inverted() where m = pb.matrix with
               translation replaced by pb.tail (no @ ob.matrix_world term)
  C head-only: mpi = (arm_mw @ m).inverted() where m = pb.matrix with
               translation replaced by pb.head (no @ ob.matrix_world term)
"""
import bpy
import math
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

def build(tag, mpi_fn):
    arm_data = bpy.data.armatures.new("Arm_" + tag)
    arm_ob = bpy.data.objects.new("Arm_" + tag, arm_data)
    bpy.context.collection.objects.link(arm_ob)
    bpy.context.view_layer.objects.active = arm_ob
    bpy.ops.object.mode_set(mode="EDIT")
    b = arm_data.edit_bones.new("bone")
    b.head = (0, 10, 0)
    b.tail = (0, 5, 0)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 7.5, 0))
    ob = bpy.context.active_object
    ob.name = "Plane_" + tag
    ob.scale = (1, 2, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.parent = arm_ob
    ob.parent_type = "BONE"
    ob.parent_bone = "bone"
    pb = arm_ob.pose.bones["bone"]
    ob.matrix_parent_inverse = mpi_fn(arm_ob, pb, ob)
    return arm_ob, ob

def f_canonical(arm_ob, pb, ob):
    return (arm_ob.matrix_world @ pb.matrix).inverted() @ ob.matrix_world

def f_tail(arm_ob, pb, ob):
    m = pb.matrix.copy()
    m.translation = pb.tail
    return (arm_ob.matrix_world @ m).inverted()

def f_head(arm_ob, pb, ob):
    m = pb.matrix.copy()
    m.translation = pb.head
    return (arm_ob.matrix_world @ m).inverted()

results = {}
for tag, fn in (("A_canonical", f_canonical), ("B_tail_V2", f_tail), ("C_head", f_head)):
    arm_ob, ob = build(tag, fn)
    # rest position first
    bpy.context.view_layer.update()
    rest = tuple(round(v, 3) for v in ob.matrix_world.translation)
    bpy.context.view_layer.objects.active = arm_ob
    bpy.ops.object.mode_set(mode="POSE")
    pb = arm_ob.pose.bones["bone"]
    pb.rotation_mode = "XYZ"
    pb.rotation_euler = (0, 0, math.radians(-90))
    bpy.context.view_layer.update()
    rot = tuple(round(v, 3) for v in ob.matrix_world.translation)
    bpy.ops.object.mode_set(mode="OBJECT")
    results[tag] = (rest, rot)
    print(tag, "rest centre:", rest, "after -90deg rot:", rot)

print("EXPECTED: head-pivot (-2.5, 10) | tail-pivot (2.5, 5) | centre-pivot (0, 7.5)")
for tag, (rest, rot) in results.items():
    print(tag, "->", rot)
