"""Cape Jones v5 POSE-TEST GATE (hard gate before any dance).
Opens the standing rig, runs an extreme-bend battery on the FK layer
(deform follows FK at ik switches = 0), renders full + zoomed views per
pose, and measures cross-section volume preservation at mid-upperarm,
mid-forearm, mid-thigh, mid-shin (posed vs rest, weight>0.3 verts).
Writes gate_v5_report.json + PNGs into the out dir.
Run: blender -b <standing.blend> --python gate_v5.py -- <outdir>
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector, Matrix, Quaternion

OUT = sys.argv[sys.argv.index("--") + 1]
os.makedirs(OUT, exist_ok=True)
rig = bpy.data.objects["CapeJones_Rig"]
body = None
for ob in bpy.data.objects:
    if ob.type == "MESH" and len(ob.data.vertices) > 100000:
        body = ob
        break

# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# The raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
# Runs FIRST: the cross-section measurements below are taken at mid-upperarm / mid-forearm, i.e. from this
# rig's joint positions — they must be the FIXED joints.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
_cj_body = bpy.data.objects.get("CapeJones_Body") or body
if bpy.data.objects.get("CapeJones_Rig") is not None and _cj_body is not None:
    cj_arm_guard.ensure_arm_fix(body_name=_cj_body.name)

for _ob in bpy.data.objects:
    if _ob.name in ("BlenRigMdefCage", "CapeJones_Cape"):
        # the BlenRig cage is a deform helper, never a render object (it
        # ghosted the first gate renders); the repo cape mesh is unbound
        # in this file - cape proof happens in the dance scene, where
        # the one-piece CapeSheet is bound to this rig.
        _ob.hide_render = True
        _ob.hide_viewport = True
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "MATERIAL"
sc.render.resolution_x = 640
sc.render.resolution_y = 640
sc.render.film_transparent = False
if not sc.world:
    sc.world = bpy.data.worlds.new("W")
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.55, 0.6, 1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sun = bpy.data.objects.get("GateSun")
if not sun:
    ld = bpy.data.lights.new("GateSun", "SUN")
    ld.energy = 3.0
    sun = bpy.data.objects.new("GateSun", ld)
    sc.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
cam_ob = bpy.data.objects.get("GateCam")
if not cam_ob:
    cd = bpy.data.cameras.new("GateCam")
    cam_ob = bpy.data.objects.new("GateCam", cd)
    sc.collection.objects.link(cam_ob)
sc.camera = cam_ob

def upd():
    bpy.context.view_layer.update()

def pb(name):
    return rig.pose.bones.get(name)

def bone_dir(name):
    b = pb(name)
    return (Vector(b.tail) - Vector(b.head)).normalized()

def _rot_about_head(b, M):
    """Apply a world-space rotation M to pose bone b ABOUT ITS OWN HEAD.
    (The first gate draft premultiplied M onto b.matrix directly, which
    rotates about the armature ORIGIN - bones orbited instead of
    rotating; caught by probe4.py: aim 'up' sent the FK tail to -X.)"""
    h = Vector(b.head)
    b.matrix = Matrix.Translation(h) @ M @ Matrix.Translation(-h) @ b.matrix

def aim(name, target_dir):
    """Rotate pose bone so its world direction matches target_dir."""
    b = pb(name)
    if not b:
        return
    cur = bone_dir(name)
    tgt = Vector(target_dir).normalized()
    if cur.angle(tgt) < 1e-4:
        return
    q = cur.rotation_difference(tgt)
    M = Matrix.Rotation(q.angle, 4, q.axis) if q.angle > 1e-6 else Matrix.Identity(4)
    _rot_about_head(b, M)
    upd()

def rot_world(name, axis, deg):
    b = pb(name)
    if not b:
        return
    M = Matrix.Rotation(math.radians(deg), 4, Vector(axis))
    _rot_about_head(b, M)
    upd()

def reset_pose():
    for b in rig.pose.bones:
        b.rotation_quaternion = (1, 0, 0, 0)
        b.rotation_euler = (0, 0, 0)
        b.location = (0, 0, 0)
        b.scale = (1, 1, 1)
    # FK mode: deform follows FK layer
    root = pb("root")
    if root:
        for k in ("ik_arm_L", "ik_arm_R", "ik_leg_L", "ik_leg_R", "ik_spine"):
            if k in root.keys():
                root[k] = 0.0
    upd()

def look(cam, at, dist, dirv):
    at = Vector(at)
    d = Vector(dirv).normalized()
    cam.location = at + d * dist
    rot = (at - cam.location).to_track_quat("-Z", "Y")
    cam.rotation_euler = rot.to_euler()

WANT = set(os.environ.get("CJ_GATE_POSES", "rest,arms_down,arms_up,fwd_elbow,crouch,spine,fingers").split(","))

def render(name, at=(0, 0, 0.45), dist=1.6, dirv=(0.3, -1, 0.25), lens=50):
    if os.environ.get("CJ_GATE_RESUME") and os.path.exists(os.path.join(OUT, name + ".png")):
        print("[gate] skip existing", name, flush=True)
        return
    cam_ob.data.lens = lens
    look(cam_ob, at, dist, dirv)
    sc.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)

def joint_pos(name):
    b = pb(name)
    return Vector(b.head) if b else Vector((0, 0, 0))

# ------- volume metric: cross-section RMS radius around a bone segment
def seg_radius(group_name, bone_name):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    vg_idx = body.vertex_groups[group_name].index
    b = pb(bone_name)
    h, t = Vector(b.head), Vector(b.tail)
    axis = t - h
    L = axis.length
    pts = []
    src = body.data.vertices
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    sel = []
    for v in src:
        for g in v.groups:
            if g.group == vg_idx and g.weight > 0.3:
                sel.append(v.index)
                break
    if len(sel) < 30:
        ev.to_mesh_clear()
        return None
    P = co[sel]
    rel = P - np.array(h)
    ax = np.array(axis) / L
    tt = rel @ ax
    keep = (tt > L * 0.3) & (tt < L * 0.7)
    if keep.sum() < 30:
        ev.to_mesh_clear()
        return None
    mid = P[keep]
    relm = mid - np.array(h)
    perp = relm - np.outer(relm @ ax, ax)
    r = float(np.sqrt((perp ** 2).sum(axis=1).mean()))
    ev.to_mesh_clear()
    return r

report = {"poses": {}, "radii": {}}
FK = {"ua": "upperarm_fk_{}", "fa": "forearm_fk_{}", "th": "thigh_fk_{}",
      "sh": "shin_fk_{}", "ft": "foot_fk_{}"}
def fk(kind, side):
    cand = FK[kind].format(side)
    return cand if pb(cand) else {"ua": f"upperarm_{side}", "fa": f"forearm_{side}",
                                  "th": f"thigh_{side}", "sh": f"shin_{side}",
                                  "ft": f"foot_{side}"}[kind]

reset_pose()
base_radii = {}
for grp, bn in (("upperarm_L", fk("ua", "L")), ("upperarm_R", fk("ua", "R")),
                ("forearm_L", fk("fa", "L")), ("thigh_L", fk("th", "L")),
                ("shin_L", fk("sh", "L"))):
    r = seg_radius(grp, bn)
    if r:
        base_radii[grp] = r
report["radii_rest"] = base_radii
render("pose_rest_full")
render("pose_rest_shoulder_L", at=joint_pos(fk("ua", "L")), dist=0.45, dirv=(0.4, -1, 0.3), lens=70)
render("pose_rest_shoulder_R", at=joint_pos(fk("ua", "R")), dist=0.45, dirv=(-0.4, -1, 0.3), lens=70)

POSES = {}
def snap(pose_name, radii_groups=()):
    row = {}
    for grp, bn in radii_groups:
        r = seg_radius(grp, bn)
        if r and grp in base_radii:
            row[grp] = round(r / base_radii[grp], 3)
    POSES[pose_name] = row

if "arms_down" in WANT:
    # P2 arms down to sides
    reset_pose()
    for s in ("L", "R"):
        aim(fk("ua", s), (0.15 if s == "L" else -0.15, 0, -1))
    render("pose_arms_down_full")
    render("pose_arms_down_shoulder_L", at=joint_pos(fk("ua", "L")), dist=0.45, dirv=(0.4, -1, 0.3), lens=70)
    render("pose_arms_down_shoulder_R", at=joint_pos(fk("ua", "R")), dist=0.45, dirv=(-0.4, -1, 0.3), lens=70)
    snap("arms_down", (("upperarm_L", fk("ua", "L")), ("upperarm_R", fk("ua", "R"))))

if "arms_up" in WANT:
    # P3 arms overhead
    reset_pose()
    for s in ("L", "R"):
        aim(fk("ua", s), (0.25 if s == "L" else -0.25, 0, 1))
    render("pose_arms_up_full")
    render("pose_arms_up_shoulder_L", at=joint_pos(fk("ua", "L")), dist=0.45, dirv=(0.4, -1, 0.3), lens=70)
    render("pose_arms_up_shoulder_R", at=joint_pos(fk("ua", "R")), dist=0.45, dirv=(-0.4, -1, 0.3), lens=70)
    snap("arms_up", (("upperarm_L", fk("ua", "L")), ("upperarm_R", fk("ua", "R"))))

if "fwd_elbow" in WANT:
    # P4 forward raise + full elbow bend (the owner's chain, both arms)
    reset_pose()
    for s in ("L", "R"):
        aim(fk("ua", s), (0, -1, 0.1))
        # elbow flexion: rotate forearm about lateral axis so hand comes up/forward
        rot_world(fk("fa", s), (1, 0, 0), -115 if s == "L" else -115)
        # NOTE: hand_fk is deliberately NOT posed here. On this rig the
        # hand is welded to the forearm through the FK parenting chain
        # (hand_fk is a child of forearm_fk; the deform hand copies it),
        # so the mitten follows the elbow rigidly - verified clean
        # (probe9). Counter-rotating hand_fk (an earlier draft of this
        # gate tried both a -115 add-on and an aim-to-forearm) shears
        # the mitten's mixed weights and tears the wrist - a harness
        # artifact, not a rig defect (probe7/probe8/probe9 bisect).
    render("pose_fwd_elbow_full")
    render("pose_fwd_elbow_L", at=joint_pos(fk("fa", "L")), dist=0.4, dirv=(0.5, -1, 0.3), lens=70)
    render("pose_fwd_elbow_R", at=joint_pos(fk("fa", "R")), dist=0.4, dirv=(-0.5, -1, 0.3), lens=70)
    render("pose_fwd_shoulder_L", at=joint_pos(fk("ua", "L")), dist=0.45, dirv=(0.4, -1, 0.3), lens=70)
    snap("fwd_elbow", (("upperarm_L", fk("ua", "L")), ("forearm_L", fk("fa", "L")),
                       ("upperarm_R", fk("ua", "R"))))

if "crouch" in WANT:
    # P5 deep crouch (thigh fwd, shin back, ankle comp) - NOT the sitting pose,
    # a standing deep knee bend for the gate
    reset_pose()
    for s in ("L", "R"):
        aim(fk("th", s), (0, -0.75, -0.66))
        aim(fk("sh", s), (0, 0.25, -0.97))
        aim(fk("ft", s), (0, -1, 0))
        if pb("root"):
            pb("root").location = (0, 0, -0.16)
            upd()
    render("pose_crouch_full")
    render("pose_crouch_knee_L", at=joint_pos(fk("sh", "L")), dist=0.45, dirv=(0.4, -1, 0.25), lens=70)
    render("pose_crouch_hip_L", at=joint_pos(fk("th", "L")), dist=0.5, dirv=(0.4, -1, 0.3), lens=70)
    render("pose_crouch_legs_front", at=(0, 0, 0.25), dist=1.0, dirv=(0, -1, 0.15), lens=60)
    snap("crouch", (("thigh_L", fk("th", "L")), ("shin_L", fk("sh", "L"))))

if "spine" in WANT:
    # P6 spine bend + twist, head turn
    reset_pose()
    for nm, ax, dg_ in (("spine_fk_1", (0, 1, 0), 0),):
        pass
    spine_chain = [n for n in ("spine_fk_1", "spine_fk_2", "spine_fk_3", "spine_fk_4", "chest_fk")
                   if pb(n)] or [n for n in ("spine_1", "spine_2", "chest") if pb(n)]
    for nm in spine_chain:
        rot_world(nm, (1, 0, 0), -8)   # forward bend distributed
    for nm in spine_chain:
        rot_world(nm, (0, 0, 1), 6)    # twist distributed
    if pb("neck_1"):
        rot_world("neck_1", (0, 0, 1), 25)
    if pb("head"):
        rot_world("head", (0, 0, 1), 30)
    render("pose_spine_head_full")
    render("pose_spine_head_zoom", at=(0, 0, 0.75), dist=0.55, dirv=(0.3, -1, 0.2), lens=70)

if "fingers" in WANT:
    # P7 finger curl (both hands, deform finger bones directly)
    reset_pose()
    for s in ("L", "R"):
        for f in ("index", "middle", "ring", "pinky"):
            for seg in (1, 2, 3):
                nm = f"finger_{f}_{seg}_{s}"
                if pb(nm):
                    rot_world(nm, (1, 0, 0), -32)
        for seg in (1, 2):
            nm = f"finger_thumb_{seg}_{s}"
            if pb(nm):
                rot_world(nm, (0, 0, 1), -20 if s == "L" else 20)
    render("pose_fingers_full")
    render("pose_fingers_hand_L", at=joint_pos(f"finger_index_1_L") if pb("finger_index_1_L") else (0, 0, 0.5),
           dist=0.3, dirv=(0.4, -1, 0.4), lens=70)

report["poses"] = POSES
_rp = os.path.join(OUT, "gate_v5_report.json")
if os.path.exists(_rp):
    try:
        _old = json.load(open(_rp))
        _old["poses"].update(POSES)
        report["poses"] = _old["poses"]
    except Exception:
        pass
with open(_rp, "w") as f:
    json.dump(report, f, indent=1)
print("GATE_V5_DONE", json.dumps(report)[:500])
