#!/usr/bin/env python3
"""Debug: replicate render_sit.py setup, print full cape evaluated bbox +
material, render one front frame."""
import bpy, math, numpy as np
from mathutils import Vector

BAKED = "/home/hatch/workspace/scratch/cj-cloth-20261024/sit_cloth_proxy_baked.blend"
ROOM = "/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/living_room.blend"
bpy.ops.wm.open_mainfile(filepath=BAKED)
proxy = bpy.data.objects["CapeJones_Cape"]
_before = set(bpy.data.objects)
with bpy.data.libraries.load(ROOM, link=False) as (df, dt):
    dt.objects = ["CapeJones_Cape"] if "CapeJones_Cape" in set(df.objects) else []
_new = [o for o in bpy.data.objects if o not in _before]
full = _new[0]
bpy.context.scene.collection.objects.link(full)
for m in list(full.modifiers):
    if m.type == "CORRECTIVE_SMOOTH":
        full.modifiers.remove(m)
full.rotation_mode = "XYZ"
full.rotation_euler = (0, 0, -math.pi / 2)
full.location = (3.344, 2.058, 0.357)
print("full hide_render:", full.hide_render, "visible:", full.visible_get(), flush=True)
print("full materials:", [m.name if m else None for m in full.data.materials], flush=True)
sc = bpy.context.scene
sc.frame_set(1)
bpy.context.view_layer.update()
sd = full.modifiers.new("SurfaceDeform", "SURFACE_DEFORM")
sd.target = proxy
bpy.context.view_layer.objects.active = full
bpy.ops.object.surfacedeform_bind(modifier="SurfaceDeform")
print("bound:", sd.is_bound, flush=True)
sc.frame_set(60)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
for obj, label in ((full, "full"), (proxy, "proxy")):
    ev = obj.evaluated_get(deps)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    mw = np.array(ev.matrix_world, dtype=np.float64)
    w = (np.concatenate([arr.reshape(-1, 3), np.ones((len(me.vertices), 1))], axis=1) @ mw.T)[:, :3]
    ev.to_mesh_clear()
    print(f"{label} frame60 world bbox x [{w[:,0].min():.3f}, {w[:,0].max():.3f}] "
          f"y [{w[:,1].min():.3f}, {w[:,1].max():.3f}] z [{w[:,2].min():.3f}, {w[:,2].max():.3f}]", flush=True)
# render one frame with BOTH capes, plus a control with only the proxy
sc.render.engine = "CYCLES"
sc.cycles.samples = 16
sc.cycles.device = "CPU"
sc.render.resolution_x, sc.render.resolution_y = 720, 540
sc.render.image_settings.file_format = "PNG"
cam = bpy.data.objects.new("dbgCam", bpy.data.cameras.new("dbgCam"))
sc.collection.objects.link(cam)
sc.camera = cam
target = Vector((3.0, 2.067, 0.50))
cam.location = Vector((1.00, 2.067, 1.00))
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.render.filepath = "/home/hatch/workspace/scratch/cj-cloth-20261024/dbg_both.png"
bpy.ops.render.render(write_still=True)
print("rendered dbg_both", flush=True)
full.hide_render = True
sc.render.filepath = "/home/hatch/workspace/scratch/cj-cloth-20261024/dbg_proxyonly.png"
bpy.ops.render.render(write_still=True)
print("rendered dbg_proxyonly", flush=True)
