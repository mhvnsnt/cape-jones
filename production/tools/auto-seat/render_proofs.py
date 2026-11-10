"""Render auto-seat proofs from the fixed blend."""
import bpy, os, time
from mathutils import Vector

WORKTREE = "/home/hatch/workspace/wt-autoseat"
PROOF_DIR = os.path.join(WORKTREE, "production/tools/auto-seat/proofs")
os.makedirs(PROOF_DIR, exist_ok=True)
STAMP = time.strftime("%Y%m%d_%H%M%S")

scn = bpy.context.scene
scn.render.engine='CYCLES'; scn.cycles.samples=24
scn.render.resolution_x=960; scn.render.resolution_y=540; scn.render.resolution_percentage=100
scn.frame_set(41); bpy.context.view_layer.update()
cam=scn.camera
def look_at(eye,target):
    d=Vector(target)-Vector(eye); cam.location=eye
    cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    bpy.context.view_layer.update()
# front: sitter faces -X, camera on -X side
look_at((1.35,2.067,0.85),(3.05,2.067,0.45))
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_front_{STAMP}.png")
bpy.ops.render.render(write_still=True); print("front rendered",flush=True)
# three-quarter
look_at((1.75,1.15,1.15),(3.05,2.067,0.45))
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_threeq_{STAMP}.png")
bpy.ops.render.render(write_still=True); print("threeq rendered",flush=True)
print("DONE",flush=True)
