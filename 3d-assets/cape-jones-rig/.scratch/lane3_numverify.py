"""Lane 3 NUMERICAL verification: for each finger bone, rotate about curl axis,
check verts move rigidly with the bone (depsgraph, no render).
Also auto-discovers the curl axis per hand."""
import bpy
import numpy as np
from mathutils import Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
bpy.context.view_layer.update()
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
n = len(me.vertices)
vg_names = [v.name for v in mesh.vertex_groups]

def eval_positions():
    deps = bpy.context.evaluated_depsgraph_get()
    ev = deps.objects.get(mesh.name).data
    co = np.empty(len(ev.vertices) * 3, dtype=np.float64)
    ev.vertices.foreach_get("co", co)
    return co.reshape(len(ev.vertices), 3)

def bone_verts(bn, thr=0.5):
    gid = vg_names.index(bn)
    idx = []
    for v in me.vertices:
        for g in v.groups:
            if g.group == gid and g.weight >= thr:
                idx.append(v.index)
                break
    return np.array(idx, dtype=np.int64)

def set_bone_rot(bn, axis, angle):
    pb = rig.pose.bones[bn]
    pb.rotation_mode = 'XYZ'
    e = [0.0, 0.0, 0.0]
    e["XYZ".index(axis)] = angle
    pb.rotation_euler = e

def clear_bone_rot(bn):
    pb = rig.pose.bones[bn]
    pb.rotation_mode = 'XYZ'
    pb.rotation_euler = (0, 0, 0)

# --- discover curl axis on index_2_R ---
test_bone = "finger_index_2_R"
idx = bone_verts(test_bone)
print(f"{test_bone}: {len(idx)} verts w>=0.5")
P0 = eval_positions()
head0 = np.array(rig.pose.bones[test_bone].head)
# palm dir: from finger centroid toward wrist (hand bone head)
hand_head = np.array(rig.pose.bones["hand_R"].head)
palm_dir = hand_head - P0[idx].mean(axis=0)
palm_dir = palm_dir / np.linalg.norm(palm_dir)
tip_idx = idx[np.argmax(np.linalg.norm(P0[idx] - head0, axis=1))]
print("tip vert:", tip_idx)
best = None
for ax in "XYZ":
    for sgn in (1.0, -1.0):
        set_bone_rot(test_bone, ax, sgn * 0.5)
        bpy.context.view_layer.update()
        P1 = eval_positions()
        disp = P1[tip_idx] - P0[tip_idx]
        score = float(np.dot(disp, palm_dir))
        print(f"  axis {ax} sign {sgn:+.0f}: tip disp toward palm = {score:.4f}")
        if best is None or score > best[0]:
            best = (score, ax, sgn)
        clear_bone_rot(test_bone)
        bpy.context.view_layer.update()
print("CURL AXIS:", best[1], "sign:", best[2], flush=True)
CURL_AX, CURL_SGN = best[1], best[2]

# --- verify all 28 finger bones ---
print("== per-bone rigid verification (rotate 0.6 about curl axis) ==")
results = {}
for pb in sorted(rig.pose.bones, key=lambda b: b.name):
    bn = pb.name
    if not bn.startswith("finger_"):
        continue
    idx = bone_verts(bn, thr=0.5)
    if len(idx) == 0:
        print(f"DEAD {bn}: no verts w>=0.5")
        results[bn] = "DEAD"
        continue
    P0 = eval_positions()
    head = np.array(pb.head)
    # expected: rigid rotation about bone-local axis through head
    # bone local axis in world = (pose matrix rotation) @ axis
    R = np.array((rig.matrix_world @ pb.matrix).to_3x3(), dtype=np.float64)
    laxis = {"X": np.array([1, 0, 0]), "Y": np.array([0, 1, 0]), "Z": np.array([0, 0, 1])}[CURL_AX]
    waxis = R @ laxis
    ang = CURL_SGN * 0.6
    # rotation matrix about waxis
    K = np.array([[0, -waxis[2], waxis[1]], [waxis[2], 0, -waxis[0]], [-waxis[1], waxis[0], 0]])
    Rm = np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)
    set_bone_rot(bn, CURL_AX, ang)
    bpy.context.view_layer.update()
    P1 = eval_positions()
    pred = head + (P0[idx] - head) @ Rm.T
    err = np.linalg.norm(P1[idx] - pred, axis=1)
    mean_err = float(err.mean())
    max_err = float(err.max())
    # movement magnitude
    move = float(np.linalg.norm((P1[idx] - P0[idx]), axis=1).mean())
    ok = mean_err < 0.002 and move > 0.003
    print(f"{'OK  ' if ok else 'FAIL'} {bn}: n={len(idx)} mean_move={move:.4f} mean_rigid_err={mean_err:.5f} max_err={max_err:.5f}")
    results[bn] = "OK" if ok else "FAIL"
    clear_bone_rot(bn)
    bpy.context.view_layer.update()

n_ok = sum(1 for v in results.values() if v == "OK")
print(f"RESULT: {n_ok}/28 OK", flush=True)
