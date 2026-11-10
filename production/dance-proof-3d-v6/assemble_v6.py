"""Cape Jones v6 ASSEMBLY: bake the full 1824-frame timeline into ONE
action (DanceV6Full) on the v6 scene:
  frames    1..24   IdleIn (arms-down standing, real mocap lead-in)
  frames   25..1800 DanceV6Loop tiled (the groove, untouched per tile)
  frames 1801..1824 blend from the running loop pose back to the idle
                    stance (the shot returns to arms-down)
Then: attach as the active action (no NLA), save scene_v6.blend, save
the rig-only cape_jones_standing_v6.blend, and trace the final action
(arm angles, toe contact, pelvis, swing) as gate evidence.
Run: blender -b scene_v6_base.blend --python assemble_v6.py
"""
import bpy, math, json, os, time
from mathutils import Vector, Quaternion

W = "/home/hatch/workspace/_cj_v6_work"
LEADF, TOTAL = 24, 1824
t00 = time.time()
def log(*a): print("[v6asm]", *a, round(time.time() - t00, 1), "s", flush=True)

sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
RPB = rig.pose.bones
body = next((o for o in bpy.data.objects if o.type == "MESH" and len(o.data.vertices) > 100000), None)

# append IdleIn from the lead solve output
with bpy.data.libraries.load(os.path.join(W, "rig_lead.blend")) as (df, dt):
    dt.actions = ["IdleIn"]
idle_act = bpy.data.actions["IdleIn"]
loop_act = bpy.data.actions["DanceV6Loop"]
log("actions:", idle_act.name, loop_act.name)

# speed: disable mesh modifier evaluation while recording bone bases
mods_off = []
for ob in bpy.data.objects:
    if ob.type == "MESH":
        for md in ob.modifiers:
            if md.show_viewport:
                md.show_viewport = False
                mods_off.append(md)

def upd(): bpy.context.view_layer.update()

# rest ground reference (identity pose)
rig.animation_data.action = None
for pb in RPB:
    pb.rotation_quaternion = (1, 0, 0, 0); pb.rotation_euler = (0, 0, 0)
    pb.location = (0, 0, 0); pb.scale = (1, 1, 1)
upd()
REST_TOE_Z = min((rig.matrix_world @ RPB[n].matrix).to_translation().z for n in ("toe_L", "toe_R"))
log("REST_TOE_Z:", round(REST_TOE_Z, 4))

def record(act, nframes):
    rig.animation_data.action = act
    rec = {}
    bones = None
    for f in range(1, nframes + 1):
        sc.frame_set(f); upd()
        if bones is None:
            bones = [pb.name for pb in RPB]
        rec[f] = {pb.name: (Vector(pb.location), Quaternion(pb.rotation_quaternion)) for pb in RPB}
    rig.animation_data.action = None
    return rec

idle_rec = record(idle_act, LEADF)
loop_rec = record(loop_act, 96)
# keyed-bone set = every bone whose recorded local base leaves identity
# in either action (constraint-driven deform bones keep identity local
# channels, so they are correctly excluded)
KB = set()
_IDQ = Quaternion((1, 0, 0, 0))
for rec in (idle_rec, loop_rec):
    for f, pose in rec.items():
        for name, (loc, quat) in pose.items():
            if loc.length > 1e-6 or quat.rotation_difference(_IDQ).angle > 1e-4:
                KB.add(name)
log("keyed bones:", len(KB))
log("recorded idle+loop bases")

def sstep(a): return a * a * (3 - 2 * a)

full = {}
for f in range(1, TOTAL + 1):
    if f <= LEADF:
        full[f] = idle_rec[f]
    elif f <= 1800:
        full[f] = loop_rec[(f - LEADF - 1) % 96 + 1]
    else:
        j = f - 1800  # 1..24
        a = sstep(j / LEADF)
        cont = loop_rec[(f - LEADF - 1) % 96 + 1]   # where the loop would be
        idle = idle_rec[LEADF]                       # idle stance (last lead frame)
        mix = {}
        for name in KB:
            l1, q1 = cont[name]; l2, q2 = idle[name]
            mix[name] = (l1.lerp(l2, a), q1.slerp(q2, a))
        full[f] = mix
log("timeline composed")

# write DanceV6Full with direct keyframe inserts (values are absolute)
full_act = bpy.data.actions.new("DanceV6Full")
full_act.use_fake_user = True
rig.animation_data.action = full_act
for f in range(1, TOTAL + 1):
    for name in KB:
        pb = RPB[name]
        loc, quat = full[f][name]
        pb.location = loc
        pb.rotation_quaternion = quat
        pb.keyframe_insert("location", frame=f)
        pb.keyframe_insert("rotation_quaternion", frame=f)
    if f % 400 == 0: log("keyed frame", f)
log("DanceV6Full written")

for md in mods_off: md.show_viewport = True
sc.frame_start, sc.frame_end = 1, TOTAL
sc.render.fps = 24
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(W, "scene_v6.blend"))
log("saved scene_v6.blend")

# ---- trace the FINAL action (gate evidence)
DOWN = Vector((0, 0, -1))
def ang(name):
    pb = RPB[name]
    m = rig.matrix_world @ pb.matrix
    h = m.to_translation(); t = m @ Vector((0, pb.length, 0))
    return round(math.degrees((t - h).normalized().angle(DOWN)), 1)
def toe_above():
    return round(min((rig.matrix_world @ RPB[n].matrix).to_translation().z
                     for n in ("toe_L", "toe_R")) - REST_TOE_Z, 4)
def pelvis_z():
    return round((rig.matrix_world @ RPB["pelvis"].matrix).to_translation().z, 4)

trace = {"rest_toe_z": REST_TOE_Z, "samples": []}
check_frames = list(range(1, 31)) + list(range(31, TOTAL + 1, 4))
max_toe = -9; swing = []
for f in check_frames:
    sc.frame_set(f); upd()
    ta = toe_above()
    max_toe = max(max_toe, ta)
    row = dict(f=f, armL=ang("upperarm_fk_L"), armR=ang("upperarm_fk_R"),
               toe=ta, pelvis=pelvis_z())
    trace["samples"].append(row)
    if 1000 <= f <= 1096: swing.append(row)
trace["max_toe_above_contact_sampled"] = max_toe
trace["frame1"] = trace["samples"][0]
trace["frame1824"] = trace["samples"][-1]
if swing:
    al = [r["armL"] for r in swing]; ar = [r["armR"] for r in swing]
    trace["swing_tile_1000_1096"] = dict(
        armL_range=[min(al), max(al)], armR_range=[min(ar), max(ar)],
        pelvis_range=[min(r["pelvis"] for r in swing), max(r["pelvis"] for r in swing)])
with open(os.path.join(W, "gate_out", "trace_v6.json"), "w") as fh:
    json.dump(trace, fh, indent=1)
log("TRACE frame1:", trace["frame1"])
log("TRACE frame1824:", trace["frame1824"])
log("TRACE max toe above contact:", max_toe, "swing:", trace.get("swing_tile_1000_1096"))

# ---- rig-only file: remove the v3 set, keep rig + body + cape + actions
keep = {"CapeJones_Rig", "CapeSheet"}
if body: keep.add(body.name)
for ob in list(bpy.data.objects):
    if ob.name not in keep and ob.type != "MESH":
        bpy.data.objects.remove(ob, do_unlink=True)
    elif ob.type == "MESH" and ob.name not in keep and len(ob.data.vertices) <= 20000:
        bpy.data.objects.remove(ob, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(W, "cape_jones_standing_v6.blend"))
log("saved cape_jones_standing_v6.blend")
print("ASSEMBLE_V6_DONE")
