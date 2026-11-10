"""Minimal: check rig pose and body bbox at frame 41."""
import bpy
scn = bpy.context.scene
scn.frame_set(41)
bpy.context.view_layer.update()
rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
root = rig.pose.bones['root']
pb = rig.pose.bones['pelvis']
print(f"root loc: ({root.location.x:.3f},{root.location.y:.3f},{root.location.z:.3f})", flush=True)
print(f"pelvis head world: {(rig.matrix_world @ pb.head).xyz}", flush=True)
print(f"rig action: {rig.animation_data.action.name if rig.animation_data and rig.animation_data.action else None}", flush=True)
# body bbox in world
import mathutils
ws = [body.matrix_world @ Vector(c) for c in body.bound_box]
zs = [v.z for v in ws]
print(f"body bbox z: min={min(zs):.3f} max={max(zs):.3f}", flush=True)
xs = [v.x for v in ws]; ys = [v.y for v in ws]
print(f"body bbox x: {min(xs):.3f}-{max(xs):.3f} y: {min(ys):.3f}-{max(ys):.3f}", flush=True)
print("INFO DONE", flush=True)
