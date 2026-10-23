"""Proof stills: mocap sitting in the living room. Dedicated camera on the chair.
Usage: blender -b proof/sitting_mocap.blend --python proof_render.py -- <outdir>"""
import bpy, sys, math
outdir = sys.argv[-1]
scn = bpy.context.scene
scn.render.resolution_x, scn.render.resolution_y = 960, 540
scn.render.resolution_percentage = 100
scn.render.film_transparent = False
# camera on the chair
cam_data = bpy.data.cameras.new("SitProofCam")
cam = bpy.data.objects.new("SitProofCam", cam_data)
scn.collection.objects.link(cam)
cam.location = (1.4, 2.067, 1.1)
# aim at chair center
from mathutils import Vector
tgt = Vector((3.05, 2.067, 0.45))
d = tgt - cam.location
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
cam_data.lens = 40
scn.camera = cam
FRAMES = [1, 40, 81]
for i, f in enumerate(FRAMES):
    scn.frame_set(f)
    scn.render.filepath = f"{outdir}/mocap_sit_f{f:03d}.png"
    bpy.ops.render.render(write_still=True)
    print("rendered", f)
# three-quarter: move camera
cam.location = (1.6, 0.6, 1.2)
d = tgt - cam.location
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
for i, f in enumerate(FRAMES):
    scn.frame_set(f)
    scn.render.filepath = f"{outdir}/mocap_sit_f{f:03d}_34.png"
    bpy.ops.render.render(write_still=True)
    print("rendered 3/4", f)
