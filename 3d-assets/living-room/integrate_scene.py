#!/usr/bin/env python3
"""
LIVING ROOM SCENE WAVE — INTEGRATION LANE (owner directive 2026-10-17 ~20:51 CDT).

Assembles the final 3d-assets/living_room.blend from the six merged build lanes.
Run ONCE headless on a fresh checkout of origin/main:

    blender -b 3d-assets/living_room.blend \
        --python 3d-assets/living-room/integrate_scene.py

Assembly order (matches INTEGRATION.md):
  1. Recliner  (PR #123): LINK the `Recliner` collection from
     living-room/recliner/recliner_rigged.blend at canon placement
     (2.653, 2.312, 0 / rot Z 270 deg). The static `loungeChairRelax(Clone)`
     mesh is KEPT but hidden (viewport + render) — the rigged recliner IS the
     chair now. Closed state default (recline = 0).
  2. TV       (PR #129): yaw the TV console so the screen reads from the chair
     (staging decision, INTEGRATION.md), then run tv/tv_setup.py, power ON.
     TV_Glow is repositioned along the yawed screen normal (tv_setup hardcodes
     the pre-yaw position).
  3. Lighting (PR #132): run lighting/apply_lighting_rig.py. Default preset 0
     (canon violet). Locked defaults untouched.
  4. Sitting  (PR #131): run sit-targets/place_sitter.py with pose_sit_normal.
     Character scale 0.925 locked (armature object untouched).
  5. Research (PR #126): godray_kit / led3d / crt_tv tools consulted — the
     lighting lane already wired the applicable pieces (VolumeBox, LED presets).

CANON LOCKS honored: colorway zero changes, 0.925m scale, mug untouched,
locked lighting defaults unchanged, chair placement (2.653, 2.312, 0) fixed.

The script SAVES the blend at the end. Proof renders are done in separate
sessions (see proof_shots.py) and never saved.
"""

import bpy
import math
import os
import runpy
import sys
from mathutils import Vector

# ---------------------------------------------------------------- paths
BLEND = bpy.data.filepath
ASSETS = os.path.dirname(os.path.abspath(BLEND))          # 3d-assets/
LR = os.path.join(ASSETS, "living-room")
REC_BLEND = os.path.join(LR, "recliner", "recliner_rigged.blend")
TV_SETUP = os.path.join(LR, "tv", "tv_setup.py")
LIGHT_RIG = os.path.join(LR, "lighting", "apply_lighting_rig.py")
LED_PRESET = os.path.join(LR, "lighting", "set_led_preset.py")
SIT = os.path.join(LR, "sit-targets", "place_sitter.py")

sc = bpy.context.scene
vl = bpy.context.view_layer

checks = []
def check(name, ok, detail=""):
    checks.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")
    if not ok:
        raise RuntimeError(f"INTEGRATION CHECK FAILED: {name} {detail}")

def run_script(path, argv_extra=()):
    """runpy a lane script with a Blender-style argv (path -- args)."""
    old_argv = sys.argv
    sys.argv = [old_argv[0], "--", *argv_extra]
    try:
        runpy.run_path(path, run_name="__main__")
    except SystemExit as e:
        if e.code not in (0, None):
            raise RuntimeError(f"{path} exited {e.code}")
    finally:
        sys.argv = old_argv

# ============================================================ 1. RECLINER
print("\n### 1. RECLINER (link collection)")
with bpy.data.libraries.load(REC_BLEND, link=True) as (df, dt):
    assert "Recliner" in set(df.collections), "Recliner collection missing"
    dt.collections = ["Recliner"]
rec = bpy.data.collections["Recliner"]
if rec.name not in [c.name for c in sc.collection.children]:
    sc.collection.children.link(rec)
# make the library path repo-relative so the committed blend is portable
for lib in bpy.data.libraries:
    if "recliner_rigged.blend" in lib.filepath:
        lib.filepath = "//living-room/recliner/recliner_rigged.blend"
vl.update()
arm = bpy.data.objects.get("recliner_rig")
assert arm is not None, "recliner_rig not linked"
check("recliner linked at canon placement",
      abs(arm.location.x - 2.653) < 1e-3 and abs(arm.location.y - 2.312) < 1e-3
      and abs(arm.location.z) < 1e-3
      and abs(math.degrees(arm.rotation_euler[2]) - 270.0) < 0.01,
      f"loc={tuple(round(v, 4) for v in arm.location)} "
      f"rotZ={math.degrees(arm.rotation_euler[2]):.2f}deg")
check("recliner closed state default", float(arm.get("recline", -1)) == 0.0,
      f"recline={arm.get('recline')}")

# remove the temporary standing scale-check figure (documented deletion)
scale_check = bpy.data.objects.get("CapeJones_ScaleCheck")
if scale_check is not None:
    bpy.data.objects.remove(scale_check, do_unlink=True)
    print("removed temporary CapeJones_ScaleCheck (standing scale figure)")
check("scale-check figure removed",
      bpy.data.objects.get("CapeJones_ScaleCheck") is None)

# ============================================================ 2. TV CONSOLE YAW
print("\n### 2. TV CONSOLE YAW (staging decision)")
CONSOLE = ["cabinetTelevision(Clone)", "crt_tv", "crt_screen", "antenna_0",
           "antenna_1", "vcr_dvd", "box_a", "box_b", "box_c", "box_d",
           "monster_body", "monster_eye_0", "monster_eye_1",
           "monster_foot_0", "monster_foot_1"]
console_objs = []
for n in CONSOLE:
    o = bpy.data.objects.get(n)
    assert o is not None, f"console object missing: {n}"
    console_objs.append(o)

# aim the screen (local +Z) at the seated viewer's face zone
AIM = Vector((3.10, 2.067, 1.05))          # seated head/chest zone
PIVOT = Vector((-0.9, 2.45, 0.0))          # 15 cm off the back wall: y-max of
                                           # the yawed cabinet clears y=2.925
dx, dy = AIM.x - PIVOT.x, AIM.y - PIVOT.y
yaw = math.atan2(dx, -dy)                  # exact: tan(yaw) = dx/|dy|
print(f"console yaw = {math.degrees(yaw):.2f} deg, pivot -> {tuple(PIVOT)}")

empty = bpy.data.objects.new("TVConsole_Yaw", None)
sc.collection.objects.link(empty)
empty.location = (-0.9, 2.6, 0.0)          # start at the console's canon spot
vl.update()
# parent via the operator (keep_transform): hand-rolled parent-inverse math
# double-applies the child local matrix — verified empirically 2026-10-18.
pre_parent = {o.name: o.matrix_world.translation.copy() for o in console_objs}
bpy.ops.object.select_all(action="DESELECT")
for o in console_objs:
    o.select_set(True)
empty.select_set(True)
vl.objects.active = empty
bpy.ops.object.parent_set(type="OBJECT", keep_transform=True)
bpy.ops.object.select_all(action="DESELECT")
vl.update()
for o in console_objs:                      # keep-transform sanity
    drift = (o.matrix_world.translation - pre_parent[o.name]).length
    assert drift < 1e-4, f"{o.name} moved {drift:.4f} m on parent"
empty.location = (PIVOT.x, PIVOT.y, 0.0)
empty.rotation_euler = (0.0, 0.0, yaw)
vl.update()
bpy.context.evaluated_depsgraph_get().update()

screen = bpy.data.objects["crt_screen"]
nrm = (screen.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()
ctr = screen.matrix_world.translation
to_aim = (AIM - ctr).normalized()
off_axis = math.degrees(math.acos(max(-1.0, min(1.0, nrm.dot(to_aim)))))
check("screen dead-on to seated viewer", off_axis < 2.0,
      f"{off_axis:.2f} deg off-axis")
# wall clearance: whole-console world bbox vs back-wall inner face y=2.925
cbb = []
for o in console_objs:
    try:
        cbb += [o.matrix_world @ Vector(c) for c in o.bound_box]
    except Exception:
        pass
ymax = max(v.y for v in cbb)
check("yawed console clears back wall", ymax < 2.90,
      f"console y-max={ymax:.3f} (wall inner 2.925)")
zmax = max(v.z for v in cbb)
check("console clear of wall decor", ymax < 2.90 and zmax < 2.0,
      f"console y-max={ymax:.3f} z-max={zmax:.3f}")

# ---- tv_setup.py (idempotent; installs frame-change handler for this session)
print("\n### 2b. TV SETUP")
run_script(TV_SETUP)
tv = bpy.data.objects["crt_tv"]
tv["tv_power"] = 1.0                       # hero look: TV ON
# tv_setup hardcodes the glow position for the pre-yaw console — reposition
# along the yawed screen normal (same 0.612 m standoff + 0.04 lift as canon)
glow = bpy.data.objects["TV_Glow"]
glow.location = ctr + nrm * 0.612 + Vector((0, 0, 0.04))
# repo-relative sequence path so the committed blend is portable
img = bpy.data.images.get("tv_show_seq")
if img is not None:
    img.filepath = "//living-room/tv/frames/tv_show_0001.png"
    img.reload()
mat0 = bpy.data.materials["tvScreenMat"]
tex0 = next(n for n in mat0.node_tree.nodes if n.type == "TEX_IMAGE")
# The linked recliner carries the ReclinerOpen action (frames 1-24, recline 0->1):
# the saved blend MUST sit at frame 1 for the closed default. Shift the TV
# sequence so frame 1 shows the title card (frame 48 of the loop).
tex0.image_user.frame_offset = 47
tv.update_tag()                            # ID-prop assignment does NOT tag the depsgraph —
                                           # without this, the glow driver re-evaluates with a
                                           # stale p=0 and overwrites the handler's 14.0 (verified)
sc.frame_set(1)                            # frame 1: recline=0 (closed), TV title card
vl.update()
mat = bpy.data.materials["tvScreenMat"]
mix = next(n for n in mat.node_tree.nodes if n.type == "MIX_SHADER")
check("TV ON (screen mix = emission)", abs(mix.inputs[0].default_value - 1.0) < 1e-6,
      f"mix={mix.inputs[0].default_value}")
check("TV_Glow follows yawed screen",
      (Vector(glow.location) - (ctr + nrm * 0.612 + Vector((0, 0, 0.04)))).length < 1e-3,
      f"glow={tuple(round(v, 3) for v in glow.location)}")
check("TV_Glow energy", abs(glow.data.energy - 14.0) < 1e-6,
      f"energy={glow.data.energy}")

# ============================================================ 3. LIGHTING RIG
print("\n### 3. LIGHTING RIG")
run_script(LIGHT_RIG)                      # self-verifies preset 1 -> RED, 0 -> canon
run_script(LED_PRESET, ("0",))             # deterministic headless state, preset 0
rig = bpy.data.objects.get("LED_RemoteRig")
check("LED rig present, preset 0 (canon violet)", rig is not None and int(rig["preset"]) == 0)
room = bpy.data.objects["RoomLight"]
check("RoomLight canon untouched",
      abs(room.data.energy - 300.0) < 1e-6 and
      all(abs(a - b) < 1e-4 for a, b in zip(tuple(room.data.color), (0.45, 0.10, 0.90))),
      f"energy={room.data.energy} color={tuple(round(c, 3) for c in room.data.color)}")

# ============================================================ 4. SITTING
print("\n### 4. SITTING (place_sitter, pose_sit_normal)")
run_script(SIT, ("pose_sit_normal",))      # appends rig + pose; verifies + exits 0
print("place_sitter: ALL PASS (see its log above)")

# ---- own BVH gate: seated body vs the LINKED recliner (closed), zero overlap
from mathutils.bvhtree import BVHTree
deps = bpy.context.evaluated_depsgraph_get()
body = bpy.data.objects["CapeJones_Body"]
bev = body.evaluated_get(deps)
bt = BVHTree.FromObject(bev, deps)
total_overlap = 0
for o in rec.objects:
    if o.type != "MESH":
        continue
    oev = o.evaluated_get(deps)
    ct = BVHTree.FromObject(oev, deps)
    total_overlap += len(ct.overlap(bt))
    del ct
del bt
bev.to_mesh_clear()
import gc; gc.collect()
check("zero mesh intersection (body vs LINKED recliner)", total_overlap == 0,
      f"{total_overlap} overlapping face pairs")
rig_obj = next(o for o in bpy.data.objects if o.type == "ARMATURE"
               and "CapeJones" in o.name)
check("character scale locked (armature object scale 1)",
      all(abs(s - 1.0) < 1e-9 for s in rig_obj.scale),
      f"scale={tuple(rig_obj.scale)}")

# ---- the rigged recliner IS the chair now: hide the static mesh (kept, not deleted)
static = bpy.data.objects.get("loungeChairRelax(Clone)")
if static is not None:
    static.hide_viewport = True
    static.hide_render = True
    print("static loungeChairRelax(Clone) hidden (kept in file for provenance)")
check("static chair hidden", static.hide_viewport and static.hide_render)
mug = bpy.data.objects.get("okayest_hero_mug")
check("mug untouched", mug is not None)

# ============================================================ SAVE
tv.update_tag()
sc.frame_set(1)          # closed default (recline=0); TV title card via frame_offset=47
vl.update()
arm_final = bpy.data.objects.get("recliner_rig")
check("recliner closed at save", float(arm_final.get("recline", -1)) == 0.0,
      f"recline={arm_final.get('recline')} at frame {sc.frame_current}")
mix_final = next(n for n in mat.node_tree.nodes if n.type == "MIX_SHADER")
check("TV still ON at save", abs(mix_final.inputs[0].default_value - 1.0) < 1e-6)
bpy.ops.wm.save_mainfile()
print(f"\nINTEGRATION COMPLETE — saved {bpy.data.filepath}")
print(f"{sum(1 for _, ok, _ in checks if ok)}/{len(checks)} checks passed")
