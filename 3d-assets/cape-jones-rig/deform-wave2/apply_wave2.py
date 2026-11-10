"""Apply wave-2 corrective shape keys + rotation-diff drivers + smoothed hinge weights.
Procedural: reads scratch/wave2_correctives.npz + wave2_keys.json. SAVES output blend.
Usage: blender -b <in.blend> --python apply_wave2.py -- <out.blend>
"""
import bpy, sys, os, json
import numpy as np

args = sys.argv[sys.argv.index("--") + 1:]
OUT_BLEND = args[0]
HERE = os.path.dirname(os.path.abspath(__file__))
NPZ = os.path.join(HERE, "scratch", "wave2_correctives.npz")
CFG = os.path.join(HERE, "wave2_keys.json")

d = np.load(NPZ)
with open(CFG) as f:
    cfg = json.load(f)

rig = bpy.data.objects['CapeJones_Rig']
body = bpy.data.objects['CapeJones_Body']

for pb in rig.pose.bones:
    pb.rotation_mode = 'XYZ'
    pb.rotation_euler = (0, 0, 0)
    pb.location = (0, 0, 0)
    pb.scale = (1, 1, 1)
bpy.context.view_layer.update()

if body.data.shape_keys is None:
    body.shape_key_add(name="Basis")
    print("Basis created", flush=True)

for key in cfg["keys"]:
    name = key["name"]
    idx = d[name + "_idx"]
    delta = d[name + "_delta"].astype(np.float64)
    kb = body.data.shape_keys.key_blocks.get(name)
    if kb is None:
        kb = body.shape_key_add(name=name)
    n = len(kb.data)
    co = np.empty(n * 3, dtype=np.float32)
    kb.data.foreach_get("co", co)
    co = co.reshape(-1, 3)
    co[idx] += delta
    kb.data.foreach_set("co", co.ravel())
    kb.data.update()
    kb.value = 0.0
    ad = body.data.shape_keys.animation_data
    if ad:
        for fc in list(ad.drivers):
            if fc.data_path == f'key_blocks["{name}"].value':
                ad.drivers.remove(fc)
    drv = kb.driver_add("value").driver
    drv.type = 'SCRIPTED'
    var = drv.variables.new()
    dt = key.get("driver", {"type": "ROTATION_DIFF"})
    if dt["type"] == "TRANSFORMS":
        var.name = dt.get("var", "a")
        var.type = 'TRANSFORMS'
        var.targets[0].id = rig
        var.targets[0].bone_target = dt["bone"]
        var.targets[0].transform_type = dt["chan"]   # e.g. ROT_X
        var.targets[0].transform_space = dt.get("space", "LOCAL_SPACE")
    else:
        b1, b2 = key["bone1"], key["bone2"]
        var.name = "bend"
        var.type = 'ROTATION_DIFF'
        var.targets[0].id = rig
        var.targets[0].bone_target = b1
        var.targets[1].id = rig
        var.targets[1].bone_target = b2
    drv.expression = key["expr"]
    print(f"key {name}: {len(idx)} verts expr={key['expr']}", flush=True)

# smoothed hinge weights: apply every smooth_w2_<zone>_<group> entry in the npz
import re
for k in d.files:
    mch = re.match(r"smooth_w2_([^_]+)_(.+)_idx$", k)
    if not mch:
        continue
    zone, gname = mch.group(1), mch.group(2)
    idx = d[k]
    val = d[f"smooth_w2_{zone}_{gname}_val"]
    vg = body.vertex_groups.get(gname)
    if vg is None:
        print(f"  WARN no vertex group {gname}", flush=True)
        continue
    q = np.round(val / 0.002).astype(np.int32)
    for uq in np.unique(q):
        ii = idx[q == uq]
        vg.add(ii.tolist(), float(uq) * 0.002, 'REPLACE')
    print(f"weights {zone}/{gname}: {len(idx)} verts rewritten", flush=True)

bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", OUT_BLEND, flush=True)
