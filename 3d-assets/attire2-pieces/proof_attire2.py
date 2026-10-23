#!/usr/bin/env python3
"""Proof: Attire-2 pieces turnaround. Viewed with own eyes."""
import bpy
import math
import os

bpy.ops.wm.open_mainfile(filepath="./cj_attire2_pieces.blend")
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 32
sc.render.resolution_x = 1280
sc.render.resolution_y = 1280
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)

bpy.ops.object.light_add(type='SUN', location=(1, 2, 3))
bpy.context.object.data.energy = 3.0
bpy.ops.object.light_add(type='SUN', location=(-2, 1, 1))
bpy.context.object.data.energy = 1.0

bpy.ops.object.empty_add(location=(0, 0, 0.5))
look = bpy.context.active_object
cam_data = bpy.data.cameras.new("A2Cam")
cam = bpy.data.objects.new("A2Cam", cam_data)
sc.collection.objects.link(cam)
cam.location = (0.0, 2.1, 0.55)
tt = cam.constraints.new("TRACK_TO")
tt.target = look
tt.track_axis = "TRACK_NEGATIVE_Z"
tt.up_axis = "UP_Y"
sc.camera = cam

sc.render.filepath = os.path.join(os.path.dirname(bpy.data.filepath),
                                  "proof", "attire2_pieces_proof.png")
os.makedirs(os.path.dirname(sc.render.filepath), exist_ok=True)
bpy.ops.render.render(write_still=True)
print("PROOF SAVED", sc.render.filepath)
