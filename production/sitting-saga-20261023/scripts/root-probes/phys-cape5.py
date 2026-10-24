import bpy
import bmesh
from mathutils import Vector
import math

print("=== CREATE CAPE IN LIGHTWEIGHT SCENE ===")

# Clear default objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Cape parameters (from earlier: neck at (3.007, 2.07, 0.586))
# Facing: -73deg about Z from -X. Let's compute back direction.
# Original facing -X (into room). Rotated -73deg about Z.
# Rotation about Z by -73deg: (x,y) -> (x cos + y sin, -x sin + y cos) for -73deg
# Actually, let's just use the known values from the placement.
# The rig Y axis after placement: we computed it earlier, but let's approximate.
# From the widget: ry=-73deg. In Blender, that's -73deg about Z.
# If original forward was -X (i.e., vector (-1, 0, 0)), after -73deg about Z:
# (x,y) -> (x cos(-73) - y sin(-73), x sin(-73) + y cos(-73))
# cos(-73)=0.292, sin(-73)=-0.956
# (-1, 0) -> (-1*0.292 - 0*(-0.956), -1*(-0.956) + 0*0.292) = (-0.292, 0.956)
# So forward = (-0.292, 0.956, 0), back = (0.292, -0.956, 0)

neck_pos = Vector((3.007, 2.07, 0.586))
back_dir = Vector((0.292, -0.956, 0))
back_dir.normalize()
print(f"Back direction: {tuple(round(v,3) for v in back_dir)}")

# Cape: width 0.35, length 0.55, 12x16 segs
w_segs, l_segs = 12, 16
cape_width = 0.35
cape_length = 0.55

me = bpy.data.meshes.new("CapeMesh")
ob = bpy.data.objects.new("CapeJones_Cape", me)
bpy.context.scene.collection.objects.link(ob)

verts = []
faces = []
perp = Vector((-back_dir.y, back_dir.x, 0))  # horizontal perpendicular

for j in range(l_segs + 1):
    for i in range(w_segs + 1):
        across = (i / w_segs - 0.5) * cape_width
        t = j / l_segs
        back_offset = t * cape_length * 0.4
        down_offset = t * t * cape_length * 0.9
        pos = neck_pos + perp * across + back_dir * back_offset + Vector((0, 0, -down_offset))
        pos.z -= 0.02
        verts.append(pos)

for j in range(l_segs):
    for i in range(w_segs):
        v0 = j * (w_segs+1) + i
        v1 = v0 + 1
        v2 = v0 + w_segs + 1
        v3 = v2 + 1
        faces.append((v0, v1, v3, v2))

me.from_pydata(verts, [], faces)
me.update()

# Pin group
vg_pin = ob.vertex_groups.new(name="cape_pin")
for i in range(w_segs + 1):
    vg_pin.add([i], 1.0, 'REPLACE')
for i in range(w_segs + 1):
    idx = (w_segs+1) + i
    vg_pin.add([idx], 0.5, 'REPLACE')

# Black material
mat = bpy.data.materials.new("CapeBlack")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0, 0, 0, 1)
    bsdf.inputs['Roughness'].default_value = 0.9
me.materials.append(mat)

print(f"Cape: {len(verts)} verts, {len(faces)} faces")

bpy.ops.wm.save_as_mainfile(filepath="/tmp/cape_only.blend")
print("SAVED /tmp/cape_only.blend")
