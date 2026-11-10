#!/usr/bin/env python3
"""Idle cloth setup v2: 82k shared-vert cape (same mesh as the 224k GLB cape,
unsplit verts) from living_room.blend, reusing the shell/capsule colliders
from cloth_idle_setup.blend. The 224k-vert bake died at solver init
(probable OOM); the 82k mesh is the same cape and bakes on this VM.
"""
import bpy, numpy as np

SRC = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_setup.blend"
ROOM = "/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/living_room.blend"
OUT = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_setup82.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)

# drop the 224k GLB cape + its cloth
old = bpy.data.objects.get("CapeJones_Cape")
if old:
    me = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if me.users == 0:
        bpy.data.meshes.remove(me)

# append the room's cape (82k verts, same mesh, shared verts)
with bpy.data.libraries.load(ROOM, link=False) as (df, dt):
    dt.objects = ["CapeJones_Cape"] if "CapeJones_Cape" in set(df.objects) else []
cape = bpy.data.objects.get("CapeJones_Cape")
assert cape, "room cape append failed"
bpy.context.scene.collection.objects.link(cape)
print(f"appended cape verts={len(cape.data.vertices)} polys={len(cape.data.polygons)}", flush=True)
# strip CorrectiveSmooth (cloth does not need it; saves evaluation cost)
for m in list(cape.modifiers):
    if m.type == "CORRECTIVE_SMOOTH":
        cape.modifiers.remove(m)
# verify authored bbox matches the GLB cape slab
import numpy as np
co = np.empty(len(cape.data.vertices) * 3, dtype=np.float64)
cape.data.vertices.foreach_get("co", co)
co = co.reshape(-1, 3)
print("cape authored bbox x", [round(co[:, 0].min(), 3), round(co[:, 0].max(), 3)],
      "y", [round(co[:, 1].min(), 3), round(co[:, 1].max(), 3)],
      "z", [round(co[:, 2].min(), 3), round(co[:, 2].max(), 3)], flush=True)

# place + pin + cloth (same values as v1)
cape.location = (0.01, 0.04, 0.377)
vg = cape.vertex_groups.new(name="cape_pin")
w = np.clip((co[:, 2] - 0.36) / 0.04, 0.0, 1.0)
for i in np.nonzero(w > 0)[0]:
    vg.add([int(i)], float(w[i]), "REPLACE")
print(f"pin verts>0: {int((w > 0).sum())}, full pin: {int((w >= 0.999).sum())}", flush=True)

cloth = cape.modifiers.new("Cloth", "CLOTH")
cs = cloth.settings
# quality 8 (not stage2's 12): this VM OOM-kills the bake at quality 10+
cs.quality = 8
cs.mass = 0.35
cs.tension_stiffness = 15.0
cs.compression_stiffness = 15.0
cs.shear_stiffness = 8.0
cs.bending_stiffness = 0.8
cs.tension_damping = 5.0
cs.compression_damping = 5.0
cs.shear_damping = 5.0
cs.bending_damping = 0.5
cs.air_damping = 1.0
cs.vertex_group_mass = "cape_pin"
try:
    cs.pin_stiffness = 1.0
except Exception:
    pass
col = cloth.collision_settings
col.use_collision = True
col.collision_quality = 3
col.distance_min = 0.010
col.use_self_collision = True
col.self_distance_min = 0.006
pc = cloth.point_cache
pc.frame_start, pc.frame_end = 0, 96
pc.use_disk_cache = True
print("cloth set on 82k cape", flush=True)

sc = bpy.context.scene
sc.frame_start, sc.frame_end = 0, 96
sc.frame_set(0)
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, flush=True)
