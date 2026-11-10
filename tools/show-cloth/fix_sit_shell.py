#!/usr/bin/env python3
"""Fix the sitting shell: rebuild it STATIC in room coords.

Bug: build_cloth_sit.py measured the back profile in room coords (y~2.16)
but built the shell grid in rig-local x, then added an Armature modifier
-> double transform (shell landed at y~4.1). For the STATIC settle, a
static shell at the seated back is exact. Seated figure faces -X, so
back-out = +X, width axis = Y (centerline 2.067).
"""
import bpy, numpy as np

SRC = "/home/hatch/workspace/scratch/cj-cloth-20261024/sit_cloth_setup.blend"
OUT = "/home/hatch/workspace/scratch/cj-cloth-20261024/sit_cloth_setup_fixed.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene
sc.frame_set(1)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
body = bpy.data.objects["CapeJones_Body"]
shell = bpy.data.objects["BackShell_Collider"]

# seated back profile: per z band, p95 x (back = +X side)
ev = body.evaluated_get(deps)
me = ev.to_mesh()
bco = np.empty(len(me.vertices) * 3, dtype=np.float64)
me.vertices.foreach_get("co", bco)
bco = bco.reshape(-1, 3)
mw = np.array(ev.matrix_world, dtype=np.float64)
world = (np.concatenate([bco, np.ones((len(bco), 1))], axis=1) @ mw.T)[:, :3]
ev.to_mesh_clear()
zs = np.linspace(0.05, 0.85, 17)
prof = []
for i in range(len(zs) - 1):
    sel = world[(world[:, 2] >= zs[i]) & (world[:, 2] < zs[i + 1])]
    x = float(np.percentile(sel[:, 0], 95)) if len(sel) else 3.35
    prof.append(((zs[i] + zs[i + 1]) / 2, x))
print("seated back profile (z, x_p95):", [(round(z, 2), round(x, 3)) for z, x in prof], flush=True)

def back_x(z):
    if z <= prof[0][0]:
        return prof[0][1]
    for (z0, x0), (z1, x1) in zip(prof, prof[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return x0 + t * (x1 - x0)
    return prof[-1][1]

NZ, NX = 40, 20
verts, faces = [], []
for r in range(NZ):
    z = 0.05 + r / (NZ - 1) * 0.80
    for c in range(NX):
        y = 2.067 - 0.26 + c / (NX - 1) * 0.52
        x = back_x(z) - 0.010 - 0.025 * ((y - 2.067) / 0.22) ** 2
        verts.append((x, y, z))
for r in range(NZ - 1):
    for c in range(NX - 1):
        a = r * NX + c; b = a + 1; d = a + NX; e = d + 1
        faces.append((a, d, e, b))
new_mesh = bpy.data.meshes.new("BackShell_Mesh_Fixed")
new_mesh.from_pydata(verts, [], faces)
new_mesh.update()
old_mesh = shell.data
shell.data = new_mesh
if old_mesh.users == 0:
    bpy.data.meshes.remove(old_mesh)
# static shell: NO armature modifier (settle is a static pose)
for m in list(shell.modifiers):
    if m.type == "ARMATURE":
        shell.modifiers.remove(m)
print("shell rebuilt static; modifiers:", [(m.type, m.name) for m in shell.modifiers], flush=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED FIXED", OUT, flush=True)
