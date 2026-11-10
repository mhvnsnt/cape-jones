"""Apply corrective shape keys + drivers + smoothed hinge weights. SAVES the blend."""
import bpy, sys, os
import numpy as np

NPZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "correctives.npz")
d = np.load(NPZ)

rig = bpy.data.objects['CapeJones_Rig']
body = bpy.data.objects['CapeJones_Body']

# reset pose to rest before creating keys
for pb in rig.pose.bones:
    pb.rotation_mode = 'XYZ'
    pb.rotation_euler = (0, 0, 0)
    pb.location = (0, 0, 0)
    pb.scale = (1, 1, 1)
bpy.context.view_layer.update()

# --- jaw weight falloff remap: jaw should not drag the midface ---
# Problem: jaw weights reach z=0.93 (forehead) with max 0.58 -> jaw open drags nose/eyes.
# Fix: smooth falloff from full at z<=0.845 to zero at z>=0.885; removed weight -> head.
def sstep(e0, e1, x):
    t = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
    return t * t * (3.0 - 2.0 * t)

jaw_vg = body.vertex_groups['jaw']
head_vg = body.vertex_groups['head']
jaw_idx = jaw_vg.index
head_idx = head_vg.index
mesh = body.data
remap_count = 0
for v in mesh.vertices:
    z = v.co.z
    if z <= 0.845 or z >= 0.905:
        continue
    jw = None
    for g in v.groups:
        if g.group == jaw_idx:
            jw = g.weight
            break
    if not jw or jw < 0.01:
        continue
    f = 1.0 - sstep(0.845, 0.885, z)
    new_jw = jw * f
    removed = jw - new_jw
    if removed < 0.005:
        continue
    groups = [(g.group, g.weight) for g in v.groups]
    total = sum(w for _, w in groups)
    new_groups = []
    has_head = False
    for gi, w in groups:
        if gi == jaw_idx:
            if new_jw >= 0.005:
                new_groups.append((gi, new_jw))
            # else drop jaw entirely
        elif gi == head_idx:
            new_groups.append((gi, w + removed))
            has_head = True
        else:
            new_groups.append((gi, w))
    if not has_head:
        if len(new_groups) < 4:
            new_groups.append((head_idx, removed))
        else:
            # 4 groups and no head: spread removed over others proportionally
            others = sum(w for _, w in new_groups)
            if others > 1e-6:
                new_groups = [(gi, w + removed * w / others) for gi, w in new_groups]
    # renormalize to original total
    new_total = sum(w for _, w in new_groups)
    if new_total > 1e-6:
        s = total / new_total
        new_groups = [(gi, w * s) for gi, w in new_groups]
    # apply
    if new_jw < 0.005:
        jaw_vg.remove([v.index])
    else:
        jaw_vg.add([v.index], new_jw, 'REPLACE')
    for gi, w in new_groups:
        if gi == jaw_idx:
            continue
        body.vertex_groups[gi].add([v.index], w, 'REPLACE')
    remap_count += 1
print(f"jaw remap: {remap_count} verts", flush=True)

# --- shape keys ---
if body.data.shape_keys is None:
    body.shape_key_add(name="Basis")
    print("Basis created", flush=True)

KEYS = [
    ("corr_elbow_L", ("upperarm_L", "forearm_L"), 0.45, 1.55),
    ("corr_elbow_R", ("upperarm_R", "forearm_R"), 0.45, 1.55),
    ("corr_jaw_open", ("head", "jaw"), 0.10, 0.45),
    ("corr_neck_head", ("neck_2", "head"), 0.15, 0.75),
]
for key_name, (b1, b2), start, span in KEYS:
    idx = d[key_name + "_idx"]
    delta = d[key_name + "_delta"].astype(np.float64)
    kb = body.data.shape_keys.key_blocks.get(key_name)
    if kb is None:
        kb = body.shape_key_add(name=key_name)
    n = len(kb.data)
    co = np.empty(n * 3, dtype=np.float32)
    kb.data.foreach_get("co", co)
    co = co.reshape(-1, 3)
    co[idx] += delta
    kb.data.foreach_set("co", co.ravel())
    kb.data.update()
    kb.value = 0.0
    print(f"key {key_name}: {len(idx)} verts", flush=True)

    # driver: rotational difference between the two bones
    q1 = rig.pose.bones[b1].bone.matrix_local.to_quaternion()
    q2 = rig.pose.bones[b2].bone.matrix_local.to_quaternion()
    rest_ang = q1.rotation_difference(q2).angle
    drv = kb.driver_add("value").driver
    drv.type = 'SCRIPTED'
    var = drv.variables.new()
    var.name = "bend"
    var.type = 'ROTATION_DIFF'
    var.targets[0].id = rig
    var.targets[0].bone_target = b1
    var.targets[1].id = rig
    var.targets[1].bone_target = b2
    lo = rest_ang + start
    drv.expression = f"max(0.0, min(1.0, (bend - {lo:.4f}) / {span:.4f}))"
    print(f"  driver: rest_ang={rest_ang:.3f} expr={drv.expression}", flush=True)

# --- smoothed hinge weights ---
for gname in ["upperarm_L", "forearm_L", "upperarm_R", "forearm_R"]:
    k = f"smooth_{gname}_idx"
    if k not in d.files:
        continue
    idx = d[k]
    val = d[f"smooth_{gname}_val"]
    vg = body.vertex_groups[gname]
    q = np.round(val / 0.002).astype(np.int32)
    for uq in np.unique(q):
        ii = idx[q == uq]
        vg.add(ii.tolist(), float(uq) * 0.002, 'REPLACE')
    print(f"weights {gname}: {len(idx)} verts rewritten", flush=True)

bpy.context.view_layer.update()
bpy.ops.wm.save_mainfile()
print("BLEND SAVED", flush=True)
