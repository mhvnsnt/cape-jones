"""Proof renders from the baked scene + cache verification."""
import bpy
import mathutils

SRC = "/home/hatch/workspace/capebake-work/scene_capebaked.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
scene = bpy.context.scene
cape = bpy.data.objects["CapeJones_Cape"]
cloth = [m for m in cape.modifiers if m.type == 'CLOTH'][0]
pc = cloth.point_cache
print(f"VERIFY: is_baked={pc.is_baked} cache frames {pc.frame_start}-{pc.frame_end} scene frames {scene.frame_start}-{scene.frame_end} cloth verts={len(cape.data.vertices)}")
scene.frame_set(40)

def shot(name, loc, tgt):
    cam_data = bpy.data.cameras.new(name)
    cam = bpy.data.objects.new(name, cam_data)
    scene.collection.objects.link(cam)
    cam.location = loc
    tv = mathutils.Vector(tgt)
    cam.rotation_euler = (tv - cam.location).to_track_quat('-Z', 'Y').to_euler()
    scene.camera = cam
    scene.render.filepath = f"/home/hatch/workspace/your_files/cape-bake/{name}.png"
    bpy.ops.render.render(write_still=True)
    print("RENDERED", scene.render.filepath, flush=True)
    bpy.data.objects.remove(cam, do_unlink=True)

scene.render.engine = 'CYCLES'
scene.cycles.samples = 4
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 50

shot("capebake_front_f40_v1", (1.1, 0.1, 1.25), (2.95, 2.05, 0.5))
shot("capebake_closeup_f40_v1", (2.15, 1.15, 0.85), (2.92, 2.08, 0.55))
print("PROOFS DONE", flush=True)
