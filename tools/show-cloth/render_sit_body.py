#!/usr/bin/env python3
"""Sitting proof WITH the body: sit baked blend + full cape (surface
deform) + body appended from the room blend, proxy cape hidden.
Shows true show framing (figure + mantle + chair) at frame 60."""
import bpy, math
from mathutils import Vector

BAKED = "/home/hatch/workspace/scratch/cj-cloth-20261024/sit_cloth_proxy_baked.blend"
ROOM = "/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/living_room.blend"
bpy.ops.wm.open_mainfile(filepath=BAKED)
proxy = bpy.data.objects["CapeJones_Cape"]
rig = bpy.data.objects["CapeJones_Rig"]
print("sit proxy baked:", next(m for m in proxy.modifiers if m.type == "CLOTH").point_cache.is_baked, flush=True)

_before = set(bpy.data.objects)
with bpy.data.libraries.load(ROOM, link=False) as (df, dt):
    dt.objects = ["CapeJones_Cape", "CapeJones_Body"]
_new = [o for o in bpy.data.objects if o not in _before]
full = next((o for o in _new if o.name.startswith("CapeJones_Cape")), None)
body = next((o for o in _new if o.name.startswith("CapeJones_Body")), None)
assert full and body, f"append failed: full={full} body={body}"
bpy.context.scene.collection.objects.link(full)
bpy.context.scene.collection.objects.link(body)
for m in list(full.modifiers):
    if m.type == "CORRECTIVE_SMOOTH":
        full.modifiers.remove(m)
full.rotation_mode = "XYZ"
full.rotation_euler = (0, 0, -math.pi / 2)
full.location = (3.344, 2.058, 0.357)
# body armature must target the LOCAL rig (not the room's)
for m in body.modifiers:
    if m.type == "ARMATURE":
        m.object = rig
        print("body armature target:", m.object.name, flush=True)
proxy.hide_render = True
print(f"full cape verts={len(full.data.vertices)} body verts={len(body.data.vertices)}", flush=True)

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
cam = bpy.data.objects.new("sitCamB", bpy.data.cameras.new("sitCamB"))
sc.collection.objects.link(cam)
sc.camera = cam
target = Vector((3.0, 2.067, 0.50))
sc.frame_set(60)
bpy.context.view_layer.update()
for name, pos in (("front", Vector((1.00, 2.067, 1.00))),
                  ("side", Vector((2.99, -0.60, 0.62)))):
    cam.location = pos
    cam.rotation_euler = (target - pos).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = f"/home/hatch/workspace/scratch/cj-cloth-20261024/sitbody_f60_{name}.png"
    bpy.ops.render.render(write_still=True)
    print("rendered", sc.render.filepath, flush=True)
print("RENDER DONE", flush=True)
