# MPFB -> Cape Jones wiring (run headless in Blender 4.5):
#   blender-4.5 -b cape_jones_rigged_w5r_clean.blend --python mpfb_wire_cj.py
#
# 1. Creates MPFB neutral + 5 semantically-morphed humans (bulk/height/
#    shoulders/belly/limbs), T-poses them via scripted bone alignment.
# 2. Transfers each morph delta field onto CapeJones_Body (910k verts) via
#    KD-tree nearest-surface mapping -> 5 driven shape keys
#    (MPFB_bulk/height/shoulders/belly/limbs) with custom-prop drivers.
# 3. Keeps the 163-bone MPFB default rig in-scene, scaled to CJ, as the
#    full-skeleton base (MPFB_FullSkeleton).
# 4. Saves cape_jones_mpfb_wired.blend next to the source blend.
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import bpy
from mathutils import Vector, Quaternion
from mathutils.kdtree import KDTree

_MPFB_USER = os.path.expanduser("~/.config/mpfb-user-data")
os.makedirs(_MPFB_USER, exist_ok=True)
bpy.utils.extension_path_user = lambda package, **kwargs: _MPFB_USER

import mpfb
mpfb.get_preference = lambda name: None
mpfb.register()

from mpfb.services.humanservice import HumanService
from mpfb.services.targetservice import TargetService
from mpfb.services.locationservice import LocationService
from mpfb.entities.objectproperties import HumanObjectProperties

TARGETS = LocationService.get_mpfb_data("targets")

MORPHS = {
    "bulk": {
        "macro": {"weight": 0.75, "muscle": 0.80},
        "targets": [("torso", "torso-muscle-pectoral-incr.target.gz", 0.9),
                    ("torso", "measure-waist-circ-incr.target.gz", 0.7)]},
    "height": {
        "macro": {"height": 0.65},
        "targets": []},
    "shoulders": {
        "macro": {},
        "targets": [("torso", "measure-shoulder-dist-incr.target.gz", 0.85)]},
    "belly": {
        "macro": {},
        "targets": [("stomach", "stomach-navel-out.target.gz", 0.7),
                    ("torso", "measure-waist-circ-incr.target.gz", 0.8)]},
    "limbs": {
        "macro": {},
        "targets": [("arms", "measure-lowerarm-length-incr.target.gz", 0.6),
                    ("arms", "l-upperarm-scale-vert-incr.target.gz", 0.6),
                    ("arms", "r-upperarm-scale-vert-incr.target.gz", 0.6),
                    ("legs", "l-upperleg-scale-vert-incr.target.gz", 0.6),
                    ("legs", "r-upperleg-scale-vert-incr.target.gz", 0.6),
                    ("legs", "l-lowerleg-scale-vert-incr.target.gz", 0.6),
                    ("legs", "r-lowerleg-scale-vert-incr.target.gz", 0.6)]},
}


def make_human(name, morph):
    h = HumanService.create_human()
    h.name = name
    for k, v in morph["macro"].items():
        HumanObjectProperties.set_value(k, v, entity_reference=h)
    if morph["macro"]:
        TargetService.reapply_macro_details(h)
    for subdir, fname, w in morph["targets"]:
        p = os.path.join(TARGETS, subdir, fname)
        if os.path.exists(p):
            TargetService.load_target(h, p, weight=w)
        else:
            print("WIRE: missing target", p)
    return h


def tpose(rig_obj):
    """Scripted T-pose: rotate shoulder01.L/R so the arm points horizontal."""
    arm = rig_obj.data
    for side, sign in (("L", 1.0), ("R", -1.0)):
        sh = arm.bones.get(f"shoulder01.{side}")
        tip = arm.bones.get(f"lowerarm02.{side}")
        if not sh or not tip:
            print("WIRE: arm bones missing for", side)
            continue
        v_rest = (tip.tail - sh.head).normalized()
        v_target = Vector((sign, 0.0, 0.0))
        q_arm = v_rest.rotation_difference(v_target)
        pb = rig_obj.pose.bones[f"shoulder01.{side}"]
        q_rest = pb.bone.matrix.to_quaternion()
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = q_rest.inverted() @ q_arm @ q_rest
    bpy.context.view_layer.update()


def posed_verts(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    eo = obj.evaluated_get(dg)
    m = eo.to_mesh()
    cos = [obj.matrix_world @ v.co for v in m.vertices]
    eo.to_mesh_clear()
    return cos


def world_bbox(obj):
    ws = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    xs = [c.x for c in ws]; ys = [c.y for c in ws]; zs = [c.z for c in ws]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


# --- locate CJ body ---
cj = bpy.data.objects.get("CapeJones_Body")
assert cj is not None, "CapeJones_Body not found"
cj_bb = world_bbox(cj)
cj_height = cj_bb[5] - cj_bb[4]
cj_cx = (cj_bb[0] + cj_bb[1]) / 2
cj_cy = (cj_bb[2] + cj_bb[3]) / 2
print(f"WIRE: CJ height={cj_height:.3f}m verts={len(cj.data.vertices)}")

# --- build MPFB humans ---
neutral = make_human("MPFB_neutral", {"macro": {}, "targets": []})
rig_n = HumanService.add_builtin_rig(neutral, "default")
tpose(rig_n)
print("WIRE: neutral bones:", len(rig_n.data.bones))

variants = {}
for mname, mdef in MORPHS.items():
    h = make_human("MPFB_" + mname, mdef)
    r = HumanService.add_builtin_rig(h, "default")
    tpose(r)
    variants[mname] = h

# --- scale/align MPFB set to CJ ---
mpfb_bb = world_bbox(neutral)
mpfb_height = mpfb_bb[5] - mpfb_bb[4]
s = cj_height / mpfb_height
print(f"WIRE: MPFB height={mpfb_height:.3f} scale={s:.4f}")
for o in [neutral, rig_n] + list(variants.values()):
    o.scale = (s, s, s)
for o in bpy.data.objects:
    if o.name.startswith("MPFB_") and o.type == "ARMATURE" and o is not rig_n:
        o.scale = (s, s, s)
bpy.context.view_layer.update()
# re-align: feet to z=0, center x/y on CJ
mpfb_bb = world_bbox(neutral)
dx = cj_cx - (mpfb_bb[0] + mpfb_bb[1]) / 2
dy = cj_cy - (mpfb_bb[2] + mpfb_bb[3]) / 2
dz = -mpfb_bb[4]
for o in bpy.data.objects:
    if o.name.startswith("MPFB_"):
        o.location.x += dx; o.location.y += dy; o.location.z += dz
bpy.context.view_layer.update()

# --- posed vertex fields ---
print("WIRE: evaluating posed meshes...")
n_co = posed_verts(neutral)
deltas = {}
for mname, h in variants.items():
    m_co = posed_verts(h)
    deltas[mname] = [(m_co[i] - n_co[i]) for i in range(len(n_co))]
    dmax = max((d.length for d in deltas[mname]), default=0.0)
    print(f"WIRE: morph {mname}: max delta {dmax*1000:.1f}mm")

# --- KD-tree transfer to CJ shape keys ---
print("WIRE: building KD-tree...")
kd = KDTree(len(n_co))
for i, co in enumerate(n_co):
    kd.insert(co, i)
kd.balance()

mesh = cj.data
if not mesh.shape_keys:
    cj.shape_key_add(name="Basis", from_mix=False)
cj_cos = [v.co.copy() for v in mesh.vertices]
sks = {}
for mname in MORPHS:
    sks[mname] = cj.shape_key_add(name="MPFB_" + mname, from_mix=False)

print(f"WIRE: transferring {len(cj_cos)} verts x {len(MORPHS)} morphs...")
dnames = list(MORPHS.keys())
for i, co in enumerate(cj_cos):
    wco = cj.matrix_world @ co
    _, idx, _ = kd.find(wco)
    for mname in dnames:
        sks[mname].data[i].co = co + deltas[mname][idx]
    if i % 200000 == 0:
        print(f"WIRE: {i}/{len(cj_cos)}")

# --- custom props + drivers ---
for mname in MORPHS:
    cj[f"mpfb_{mname}"] = 0.0
    sk = sks[mname]
    fcu = sk.driver_add("value").driver
    fcu.type = "AVERAGE"
    var = fcu.variables.new()
    var.type = "SINGLE_PROP"
    var.targets[0].id = cj
    var.targets[0].data_path = f'["mpfb_{mname}"]'
print("WIRE: drivers added")

# --- keep reference full skeleton ---
neutral.name = "MPFB_ReferenceBody"
rig_n.name = "MPFB_FullSkeleton"
for o in list(bpy.data.objects):
    if o.name.startswith("MPFB_") and o not in (neutral, rig_n):
        bpy.data.objects.remove(o, do_unlink=True)
print("WIRE: kept", rig_n.name, "bones:", len(rig_n.data.bones))

# --- save ---
src = bpy.data.filepath
dst = os.path.join(os.path.dirname(src), "cape_jones_mpfb_wired.blend")
bpy.ops.wm.save_as_mainfile(filepath=dst)
print("WIRE: saved", dst)
print("WIRE_DONE")
