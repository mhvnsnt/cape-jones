import bpy
import bmesh
from mathutils import Vector, Matrix
import math

print("=== CREATE CAPE MESH ===")

rig = bpy.data.objects.get("CapeJones_Rig")
bpy.context.view_layer.update()

# Get neck world position and facing
neck_bone = rig.pose.bones.get("neck_1")
neck_pos = rig.matrix_world @ neck_bone.head
print(f"Neck: {tuple(round(v,3) for v in neck_pos)}")

# Facing: rig's local Y axis in world (after placement rotation)
# The placement had -73deg about Z. Original facing was -X (into room).
# Let's compute from the rig matrix
y_axis = (rig.matrix_world @ Vector((0,1,0,0))).xyz  # direction, not position
y_axis.normalize()
print(f"Rig Y (forward) in world: {tuple(round(v,3) for v in y_axis)}")
# Back direction is -forward
back_dir = -y_axis
back_dir.z = 0  # keep horizontal
back_dir.normalize()
print(f"Back direction: {tuple(round(v,3) for v in back_dir)}")

# Cape: plane at shoulders, extending back and down
# Width 0.35m, length 0.55m, subdivided for cloth
shoulder_z = neck_pos.z - 0.02  # just below neck
cape_width = 0.35
cape_length = 0.55

# Create mesh
me = bpy.data.meshes.new("CapeMesh")
ob = bpy.data.objects.new("CapeJones_Cape", me)
bpy.context.scene.collection.objects.link(ob)

# Build grid: width segments x length segments
w_segs, l_segs = 12, 16
verts = []
faces = []
for j in range(l_segs + 1):
    for i in range(w_segs + 1):
        # Position: start at shoulders, go back and down
        # Across width (perpendicular to back_dir)
        across = (i / w_segs - 0.5) * cape_width
        # Along back_dir and down
        t = j / l_segs
        # Curve: starts going back, then drapes down
        back_offset = t * cape_length * 0.4  # backward
        down_offset = t * t * cape_length * 0.9  # downward (accelerating for drape)
        
        # Perpendicular vector (horizontal, 90deg from back_dir)
        perp = Vector((-back_dir.y, back_dir.x, 0))
        
        pos = neck_pos + perp * across + back_dir * back_offset + Vector((0,0,-down_offset))
        # Start slightly below neck
        pos.z -= 0.02
        verts.append(pos)

# Faces
for j in range(l_segs):
    for i in range(w_segs):
        v0 = j * (w_segs+1) + i
        v1 = v0 + 1
        v2 = v0 + w_segs + 1
        v3 = v2 + 1
        faces.append((v0, v1, v3, v2))

me.from_pydata(verts, [], faces)
me.update()

# Pin group: top row (at shoulders)
vg_pin = ob.vertex_groups.new(name="cape_pin")
for i in range(w_segs + 1):
    vg_pin.add([i], 1.0, 'REPLACE')
# Second row partial pin for stability
for i in range(w_segs + 1):
    idx = (w_segs+1) + i
    vg_pin.add([idx], 0.5, 'REPLACE')

print(f"Cape created: {len(verts)} verts, {len(faces)} faces")
print(f"Pin verts: {w_segs+1} full + {w_segs+1} half")

# Black cape material (canon: absolute black #000000)
mat = bpy.data.materials.new("CapeBlack")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0, 0, 0, 1)
    bsdf.inputs['Roughness'].default_value = 0.9
me.materials.append(mat)

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_sit_phys.blend")
print("SAVED")
