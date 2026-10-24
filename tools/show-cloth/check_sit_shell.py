#!/usr/bin/env python3
"""Verify the sitting shell sits at the seated back at frame 1 (not
double-transformed). Prints shell bbox + shell x at neck height vs the
seated back surface x."""
import bpy, numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/scratch/cj-cloth-20261024/sit_cloth_setup.blend")
sc = bpy.context.scene
sc.frame_set(1)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()

def world_verts(obj):
    ev = obj.evaluated_get(deps)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    mw = np.array(ev.matrix_world, dtype=np.float64)
    w = (np.concatenate([arr.reshape(-1, 3), np.ones((len(me.vertices), 1))], axis=1) @ mw.T)[:, :3]
    ev.to_mesh_clear()
    return w

shell = world_verts(bpy.data.objects["BackShell_Collider"])
print(f"shell bbox x [{shell[:, 0].min():.3f}, {shell[:, 0].max():.3f}] "
      f"y [{shell[:, 1].min():.3f}, {shell[:, 1].max():.3f}] "
      f"z [{shell[:, 2].min():.3f}, {shell[:, 2].max():.3f}]", flush=True)
band = shell[np.abs(shell[:, 2] - 0.76) < 0.05]
print(f"shell x at neck height (z~0.76): median {np.median(band[:, 0]):.3f}, "
      f"max {band[:, 0].max():.3f} (seated back surface x_p95 was 3.432)", flush=True)
for bn in ("thigh_L", "thigh_R"):
    o = bpy.data.objects.get(bn + "_Collider")
    if o:
        w = world_verts(o)
        print(f"{bn} capsule center: ({w[:, 0].mean():.3f}, {w[:, 1].mean():.3f}, {w[:, 2].mean():.3f})", flush=True)
rig = bpy.data.objects["CapeJones_Rig"]
print("rig rest check: thigh_L head_local:", [round(v, 3) for v in rig.data.bones["thigh_L"].head_local], flush=True)
print("rig pose thigh_L head world:", [round(v, 3) for v in (rig.matrix_world @ rig.pose.bones["thigh_L"].head)], flush=True)
