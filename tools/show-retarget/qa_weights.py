"""Weight QA: audit head/face-region skin weights for the face-stretch bug
(face verts weighted to spine/pelvis instead of head).
Usage: blender -b --python qa_weights.py -- <model.glb|blend> [report.json]
For a .blend, uses its first armature+mesh pair as-is."""
import bpy, sys, json, math
from mathutils import Vector

a = sys.argv[sys.argv.index("--")+1:]
path = a[0]
out = a[1] if len(a) > 1 else None

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

arm = None
if path.endswith(".blend"):
    bpy.ops.wm.open_mainfile(filepath=path)
    arms = [o for o in bpy.data.objects if o.type == 'ARMATURE']
    arm = arms[0] if arms else None
else:
    bpy.ops.import_scene.gltf(filepath=path)
    arms = [o for o in bpy.data.objects if o.type == 'ARMATURE']
    arm = arms[0] if arms else None

if not arm:
    print("QA FAIL: no armature found")
    sys.exit(2)

bones = {b.name for b in arm.data.bones}
print("armature:", arm.name, "bones:", len(bones))

# pick the skinned mesh bound to this armature (largest)
cands = []
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    mods = [m for m in o.modifiers if m.type == 'ARMATURE' and m.object == arm]
    if mods or any(g in o.vertex_groups for g in bones):
        cands.append((len(o.data.vertices), o))
cands.sort(reverse=True)
if not cands:
    print("QA FAIL: no skinned mesh")
    sys.exit(2)
mesh = cands[0][1]
print("mesh:", mesh.name, "verts:", len(mesh.data.vertices))

dg = bpy.context.evaluated_depsgraph_get()
eo = mesh.evaluated_get(dg)
me = eo.to_mesh()
vco = [mesh.matrix_world @ v.co for v in me.vertices]
zs = [c.z for c in vco]
zmin, zmax = min(zs), max(zs)
h = zmax - zmin
head_cut = zmax - 0.16 * h   # top ~16% = head region
neck_cut = zmax - 0.30 * h

vg = mesh.vertex_groups
bad = {"spine", "pelvis", "thigh", "shin", "hips", "root"}
report = {"mesh": mesh.name, "zmin": zmin, "zmax": zmax,
          "head_verts": 0, "head_dominant": {}, "suspect": []}

def vgroups_of(vi):
    v = me.vertices[vi]
    out = []
    for g in v.groups:
        try:
            out.append((vg[g.group].name, g.weight))
        except Exception:
            pass
    return out

for i, c in enumerate(vco):
    if c.z < head_cut:
        continue
    report["head_verts"] += 1
    gs = vgroups_of(i)
    if not gs:
        continue
    gs.sort(key=lambda x: -x[1])
    dom = gs[0][0]
    key = dom.lower()
    report["head_dominant"][dom] = report["head_dominant"].get(dom, 0) + 1
    if any(k in key for k in bad):
        report["suspect"].append({"vert": i, "bone": dom, "w": round(gs[0][1], 3),
                                  "z": round(c.z, 3)})

eo.to_mesh_clear()
n_sus = len(report["suspect"])
sus_frac = n_sus / max(report["head_verts"], 1)
report["suspect_fraction"] = round(sus_frac, 4)
report["verdict"] = ("FAIL-FACE-STRETCH-RISK" if sus_frac > 0.05
                     else "PASS")
print(json.dumps(report, indent=1)[:3000])
print("VERDICT:", report["verdict"], f"({n_sus}/{report['head_verts']} head verts dominated by spine/pelvis/lower)")
if out:
    json.dump(report, open(out, "w"), indent=1)
    print("report:", out)
