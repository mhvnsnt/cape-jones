#!/usr/bin/env python3
"""Proof renders: baked PROXY cape drives the full 82k cape via Surface
Deform, plus the GLB body for context, lights added (temporary, not saved).
Run AFTER the proxy bake completes."""
import bpy
from mathutils import Vector

PROXY_BAKED = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_v3_baked.blend"
BASE = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_base.blend"
ROOM = "/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/living_room.blend"
bpy.ops.wm.open_mainfile(filepath=PROXY_BAKED)
proxy = bpy.data.objects["CapeJones_Cape"]
print("proxy cloth baked:", next(m for m in proxy.modifiers if m.type == "CLOTH").point_cache.is_baked, flush=True)

# append the full 82k cape from the room blend, place it identically
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
full.location = (0.01, 0.04, 0.377)
print(f"full cape verts={len(full.data.vertices)}", flush=True)

# surface deform: bind at frame 0 (proxy base position == full cape position)
sc = bpy.context.scene
sc.frame_set(0)
bpy.context.view_layer.update()
sd = full.modifiers.new("SurfaceDeform", "SURFACE_DEFORM")
sd.target = proxy
bpy.context.view_layer.objects.active = full
bpy.ops.object.surfacedeform_bind(modifier="SurfaceDeform")
print("surface deform bound:", sd.is_bound, flush=True)

# append GLB body for context
_before = set(bpy.data.objects)
with bpy.data.libraries.load(BASE, link=False) as (df, dt):
    dt.objects = ["CapeJones_Body"] if "CapeJones_Body" in set(df.objects) else []
_new = [o for o in bpy.data.objects if o not in _before]
body = _new[0] if _new else None
assert body, "body append failed"
bpy.context.scene.collection.objects.link(body)
arm_mod = next((m for m in body.modifiers if m.type == "ARMATURE"), None)
print("body armature target:", arm_mod.object.name if arm_mod and arm_mod.object else None, flush=True)
for o in bpy.data.objects:
    if o.name in ("Cube", "Icosphere"):
        o.hide_render = True

# lights (temporary)
sun_data = bpy.data.lights.new("proof_sun", "SUN")
sun_data.energy = 3.0
sun = bpy.data.objects.new("proof_sun", sun_data)
sc.collection.objects.link(sun)
sun.location = (2.0, 2.0, 3.0)
fill_data = bpy.data.lights.new("proof_fill", "AREA")
fill_data.energy = 200
fill_data.size = 2.0
fill = bpy.data.objects.new("proof_fill", fill_data)
sc.collection.objects.link(fill)
fill.location = (0, -2.0, 1.5)

sc.render.engine = "CYCLES"
sc.cycles.samples = 16
sc.cycles.device = "CPU"
sc.render.resolution_x, sc.render.resolution_y = 720, 540
sc.render.image_settings.file_format = "PNG"
cam = bpy.data.objects.new("bakedCam", bpy.data.cameras.new("bakedCam"))
sc.collection.objects.link(cam)
sc.camera = cam
target = Vector((0, 0, 0.55))
for frame in (0, 48, 96):
    sc.frame_set(frame)
    bpy.context.view_layer.update()
    cam.location = Vector((0, 2.0, 0.6))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = f"/home/hatch/workspace/scratch/cj-cloth-20261024/baked_idle_v3_f{frame}_back.png"
    bpy.ops.render.render(write_still=True)
    print("rendered", sc.render.filepath, flush=True)
print("RENDER DONE", flush=True)
