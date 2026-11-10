#!/usr/bin/env python3
"""Measure seated body geometry to anchor the mantle correctly:
- torso back surface (max x) per z band, all y and near-centerline y
- head/hood z range and back surface (verts near centerline, high z)
- chair back front face x per z band
- wall x (WallRight)
Prints the numbers; no decisions made here."""
import bpy, numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/living_room.blend")
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

body = world_verts(bpy.data.objects["CapeJones_Body"])
chair = world_verts(bpy.data.objects["loungeChairRelax(Clone)"])
print("== torso/head back surface (body max x per z band, centerline |y-2.067|<0.15) ==")
for zlo in np.arange(0.40, 0.95, 0.05):
    sel = body[(body[:, 2] >= zlo) & (body[:, 2] < zlo + 0.05) & (np.abs(body[:, 1] - 2.067) < 0.15)]
    if len(sel):
        print(f"z {zlo:.2f}-{zlo+0.05:.2f}: max x {sel[:, 0].max():.3f} p95 {np.percentile(sel[:, 0], 95):.3f} n={len(sel)}")
print("== chair back front face (chair min x per z band = front face, chair faces -X) ==")
for zlo in np.arange(0.35, 0.65, 0.05):
    sel = chair[(chair[:, 2] >= zlo) & (chair[:, 2] < zlo + 0.05)]
    if len(sel):
        print(f"z {zlo:.2f}-{zlo+0.05:.2f}: chair x range [{sel[:, 0].min():.3f}, {sel[:, 0].max():.3f}]")
wall = bpy.data.objects.get("WallRight")
if wall:
    wv = world_verts(wall)
    print(f"WallRight bbox x [{wv[:, 0].min():.3f}, {wv[:, 0].max():.3f}] y [{wv[:, 1].min():.3f}, {wv[:, 1].max():.3f}] z [{wv[:, 2].min():.3f}, {wv[:, 2].max():.3f}]")
rig = bpy.data.objects["CapeJones_Rig"]
for b in ("neck_1", "neck_2", "head", "clavicle_L", "chest"):
    pb = rig.pose.bones[b]
    hw = rig.matrix_world @ pb.head
    print(f"bone {b} head world: ({hw.x:.3f}, {hw.y:.3f}, {hw.z:.3f})")
