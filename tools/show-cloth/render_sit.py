#!/usr/bin/env python3
"""Proof renders for the sitting settle: baked proxy drives the full cape
via Surface Deform, in the room, front + side views, frames 1/30/60."""
import bpy, math
from mathutils import Vector

BAKED = "/home/hatch/workspace/scratch/cj-cloth-20261024/sit_cloth_proxy_baked.blend"
ROOM = "/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/living_room.blend"
bpy.ops.wm.open_mainfile(filepath=BAKED)
proxy = bpy.data.objects["CapeJones_Cape"]
print("sit proxy baked:", next(m for m in proxy.modifiers if m.type == "CLOTH").point_cache.is_baked, flush=True)

_before = set(bpy.data.objects)
with bpy.data.libraries.load(ROOM, link=False) as (df, dt):
    dt.objects = ["CapeJones_Cape"] if "CapeJones_Cape" in set(df.objects) else []
_new = [o for o in bpy.data.objects if o not in _before]
full = _new[0] if _new else None
assert full, "full cape append failed"
bpy.context.scene.collection.objects.link(full)
for m in list(full.modifiers):
    if m.type == "CORRECTIVE_SMOOTH":
        full.modifiers.remove(m)
# room-blend cape is QUATERNION mode: force XYZ or the euler is ignored
# (same bug that invalidated the v1 sit bake)
full.rotation_mode = "XYZ"
full.rotation_euler = (0, 0, -math.pi / 2)
full.location = (3.344, 2.058, 0.357)
print(f"full cape verts={len(full.data.vertices)}", flush=True)

sc = bpy.context.scene
sc.frame_set(1)
bpy.context.view_layer.update()
sd = full.modifiers.new("SurfaceDeform", "SURFACE_DEFORM")
sd.target = proxy
bpy.context.view_layer.objects.active = full
bpy.ops.object.surfacedeform_bind(modifier="SurfaceDeform")
print("surface deform bound:", sd.is_bound, flush=True)

sc.render.engine = "CYCLES"
sc.cycles.samples = 16
sc.cycles.device = "CPU"
sc.render.resolution_x, sc.render.resolution_y = 720, 540
sc.render.image_settings.file_format = "PNG"
cam = bpy.data.objects.new("sitCam", bpy.data.cameras.new("sitCam"))
sc.collection.objects.link(cam)
sc.camera = cam
target = Vector((3.0, 2.067, 0.50))
for frame in (1, 30, 60):
    sc.frame_set(frame)
    bpy.context.view_layer.update()
    for name, pos in (("front", Vector((1.00, 2.067, 1.00))),
                      ("side", Vector((2.99, -0.60, 0.62)))):
        cam.location = pos
        cam.rotation_euler = (target - pos).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = f"/home/hatch/workspace/scratch/cj-cloth-20261024/sit_f{frame}_{name}.png"
        bpy.ops.render.render(write_still=True)
        print("rendered", sc.render.filepath, flush=True)
print("RENDER DONE", flush=True)
