import bpy
import mathutils
import os

print("=== RENDER MECH PROOFS ===", flush=True)
OUTDIR = "/home/hatch/workspace/your_files/recliner-mech"
os.makedirs(OUTDIR, exist_ok=True)
rig = bpy.data.objects.get("CapeJones_Rig")
rrig = bpy.data.objects.get("recliner_rig")
scene = bpy.context.scene
scene.frame_set(40)

def eval_update():
    rrig.update_tag(refresh={'DATA'})
    rig.update_tag(refresh={'DATA'})
    bpy.context.view_layer.update()

cam_data = bpy.data.cameras.new("ProofCam")
cam = bpy.data.objects.new("ProofCam", cam_data)
scene.collection.objects.link(cam)
cam.location = (1.1, 0.1, 1.25)
target = mathutils.Vector((2.95, 2.05, 0.5))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam

scene.render.engine = 'CYCLES'
scene.cycles.samples = 4
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 50

for rec, tag in ((0.0, "r0"), (0.5, "r50"), (1.0, "r100")):
    rrig['recline'] = rec
    eval_update()
    eval_update()
    path = os.path.join(OUTDIR, f"mech_{tag}_v1.png")
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED recline={rec} -> {path}", flush=True)

rrig['recline'] = 0.0
print("=== RENDER MECH DONE (file NOT re-saved; on-disk blend keeps recline=0) ===", flush=True)
