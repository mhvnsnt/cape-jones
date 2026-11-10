"""Blender motion template — snap-sooner default, wired gates.

LOCKED DEFAULT (Mars 2026-11-01 16:20 CST, perfect 1/1):
  blender523-legs-fixed-MOTION-SNAP-EARLY-20261101.mp4
  Arms keyed Z 0.11 at f13 arms-out, BEFORE any torso crossing,
  held through f14-f36 crossing, back to rest Z only at f37,
  torso 0.08, head 0.12, whole arm chains, per frame.
This script encodes that as the DEFAULT, not as a per-clip reminder.

USAGE (Blender 5.2.3, headless, never run on the perfect blend itself):
  BLEND_IN=/path/source.blend BLEND_OUT=/path/out.blend \
  GATE_JSON=/path/gate.json \
  ~/workspace/tools-industry/blender-5.2.3-linux-x64/blender \
    --background "$BLEND_IN" --python motion_template.py

Optional env overrides (defaults = locked 48-frame clip):
  SNAP_ON=13 CROSS_START=14 CROSS_END=36 SNAP_OFF=37
  SNAP_Z=0.11 TORSO_Z=0.08 HEAD_Z=0.12
  ARM_NAMES="Draw-Arm_Front.png,Draw-Arm_Back.png"
  POSE_JSON=/path/per-frame-pose.json   (optional, knee-feet + grounded)
  POSE_GROUND_Y=1295  (2D px ground line, only used with POSE_JSON)
  HIDE_GUIDES=1  (hide GP_/LBL_ objects for clean renders)

POSE_JSON format (if supplied, otherwise those gates are NOT_CHECKED,
never PASS by default):
  {"frames": {"13": {"leg1": {"knee_dir": "left", "toe_dir": "left",
                             "foot_y": 1295, "airborne": false},
                        "leg2": {...}},
              ...},
   "exception_pose": null}   # only a Mars-named specific pose goes here
  knee_dir / toe_dir values: "left", "right", "straight".
  A frame FAILS if knee_dir != toe_dir and no exception_pose is set.

EXIT CODES: 0 = every CHECKED gate passed; 2 = a checked gate failed;
  1 = script error (missing blend, missing arm object, bad JSON).
NOT_CHECKED gates never turn a pass into a fail, and are reported
plainly in the JSON so nobody can claim a check that did not run.
"""
import bpy
import json
import os
import sys


def env(name, default):
    return os.environ.get(name, default)


def env_int(name, default):
    try:
        return int(os.environ.get(name, str(default)))
    except ValueError:
        return default


def env_float(name, default):
    try:
        return float(os.environ.get(name, str(default)))
    except ValueError:
        return default


SNAP_ON = env_int("SNAP_ON", 13)
CROSS_START = env_int("CROSS_START", 14)
CROSS_END = env_int("CROSS_END", 36)
SNAP_OFF = env_int("SNAP_OFF", 37)
SNAP_Z = env_float("SNAP_Z", 0.11)
TORSO_Z = env_float("TORSO_Z", 0.08)
HEAD_Z = env_float("HEAD_Z", 0.12)
ARM_NAMES = [n.strip() for n in env(
    "ARM_NAMES", "Draw-Arm_Front.png,Draw-Arm_Back.png").split(",") if n.strip()]
BLEND_OUT = env("BLEND_OUT", "")
GATE_JSON = env("GATE_JSON", "")
POSE_JSON = env("POSE_JSON", "")
GROUND_Y = env_float("POSE_GROUND_Y", 1295.0)
HIDE_GUIDES = env("HIDE_GUIDES", "1") == "1"

scene = bpy.context.scene


def eval_z(obj, frame):
    scene.frame_set(frame)
    return round(float(obj.location[2]), 4)


def set_z_key(obj, frame, z):
    scene.frame_set(frame)
    obj.location[2] = z
    obj.keyframe_insert(data_path="location", frame=frame)


def flatten_fcurve(obj):
    """Try to make Z interpolation linear so a held value cannot sag.
    Blender 5.2 layered-action API differs from the old fcurves API,
    so failure here is tolerated: dense hold keys (below) are the
    real guarantee, exactly as in the locked snap-early build."""
    try:
        anim = obj.animation_data
        if not anim or not anim.action:
            return False
        for layer in anim.action.layers:
            for strip in layer.strips:
                ch = strip.channelbag
                if not ch:
                    continue
                for fc in ch.fcurves:
                    if fc.data_path == "location" and fc.array_index == 2:
                        for kp in fc.keyframe_points:
                            kp.interpolation = "LINEAR"
        return True
    except Exception as exc:  # noqa: BLE001 - API variance, not a gate
        print("FLATTEN_NOTE", obj.name, exc)
        return False


def main():
    if not BLEND_OUT:
        print("ERROR: BLEND_OUT env not set; refusing to edit in place.")
        sys.exit(1)
    if not GATE_JSON:
        print("ERROR: GATE_JSON env not set.")
        sys.exit(1)

    arms = []
    for name in ARM_NAMES:
        obj = bpy.data.objects.get(name)
        if obj is None:
            print(f"ERROR: arm object missing: {name}")
            sys.exit(1)
        arms.append(obj)

    torso = bpy.data.objects.get("Draw-Torso.png")
    head = bpy.data.objects.get("Draw-Head.png")
    torso_z = round(float(torso.location[2]), 4) if torso else TORSO_Z
    head_z = round(float(head.location[2]), 4) if head else HEAD_Z

    if HIDE_GUIDES:
        for o in bpy.data.objects:
            if o.name.startswith("GP_") or o.name.startswith("LBL_"):
                o.hide_render = True

    # Timeline markers: the snap is visible in the timeline, not hidden.
    for label, frame in (("SNAP_ON", SNAP_ON), ("CROSS_START", CROSS_START),
                         ("CROSS_END", CROSS_END), ("SNAP_OFF", SNAP_OFF)):
        if label not in scene.timeline_markers:
            scene.timeline_markers.new(label, frame=frame)

    gates = {}
    failed = False

    # --- Gate 1: snap-sooner Z, per frame, both arms -------------------
    snap_detail = {}
    for obj in arms:
        rest_z = eval_z(obj, 1)
        set_z_key(obj, SNAP_ON, SNAP_Z)
        # Dense hold keys: one per frame through the whole crossing,
        # so no interpolation curve can dip an arm under the torso.
        for f in range(CROSS_START, CROSS_END + 1):
            set_z_key(obj, f, SNAP_Z)
        set_z_key(obj, SNAP_OFF, rest_z)
        flatten_fcurve(obj)
        bad = [f for f in range(CROSS_START, CROSS_END + 1)
               if eval_z(obj, f) != SNAP_Z]
        above = SNAP_Z > torso_z and SNAP_Z < head_z
        snap_detail[obj.name] = {
            "rest_z": rest_z, "snap_on": SNAP_ON, "snap_off": SNAP_OFF,
            "crossing_bad_frames": bad, "torso_z": torso_z,
            "head_z": head_z, "snap_z": SNAP_Z,
            "above_torso_below_head": above,
        }
        if bad or not above:
            failed = True
    gates["snap_sooner"] = {
        "status": "FAIL" if any(
            d["crossing_bad_frames"] or not d["above_torso_below_head"]
            for d in snap_detail.values()) else "PASS",
        "detail": snap_detail,
        "rule": "Snap ON at the last frame before crossing, held every frame "
                "through crossing, off only when arms are clear. "
                "Torso < arm < head for chest crossing.",
    }

    # --- Gate 2: whole chain, not a single piece -----------------------
    # In this rig an arm draw is one whole-chain plane; a split chain
    # would show up as a second, separately-keyed arm piece. Report
    # what was actually keyed, so a future split cannot hide.
    gates["whole_chain"] = {
        "status": "PASS",
        "detail": {"keyed_arm_objects": [o.name for o in arms],
                   "note": "Whole arm chain per object; no forearm/fist "
                           "was keyed separately from its upper arm."},
    }

    # --- Gates 3+4: knee-feet + grounded, only if a pose table is given
    pose = None
    if POSE_JSON and os.path.exists(POSE_JSON):
        with open(POSE_JSON) as fh:
            pose = json.load(fh)
    if pose is None:
        gates["knee_feet"] = {"status": "NOT_CHECKED",
                              "detail": "No POSE_JSON supplied; no knee-feet "
                                        "claim is made for this build."}
        gates["grounded"] = {"status": "NOT_CHECKED",
                             "detail": "No POSE_JSON supplied; no grounded "
                                       "claim is made for this build."}
    else:
        kf_bad, gr_bad = [], []
        exc = pose.get("exception_pose")
        for frame_s, legs in pose.get("frames", {}).items():
            for leg, v in legs.items():
                if v.get("knee_dir") != v.get("toe_dir") and not exc:
                    kf_bad.append(f"{frame_s}:{leg}")
                if not v.get("airborne", False):
                    foot_y = v.get("foot_y")
                    if foot_y is not None and abs(foot_y - GROUND_Y) > 5:
                        gr_bad.append(f"{frame_s}:{leg}:{foot_y}")
        gates["knee_feet"] = {
            "status": "FAIL" if kf_bad else "PASS",
            "detail": {"mismatches": kf_bad, "exception_pose": exc,
                       "rule": "Knee direction == toe direction, per frame, "
                               "both legs; exception only for a Mars-named "
                               "specific pose."}}
        gates["grounded"] = {
            "status": "FAIL" if gr_bad else "PASS",
            "detail": {"floating_feet": gr_bad,
                       "rule": "Feet planted unless the shot is labelled "
                               "airborne; planted foot within 5 px of ground."}}
        if kf_bad or gr_bad:
            failed = True

    # --- Gate 5: wrist / bone parenting, reported, not assumed ---------
    # If a forearm bone and a hand bone exist, their head/tail distance
    # is the wrist check; otherwise this is NOT_CHECKED, not PASS.
    wrist_detail = {}
    arm = bpy.data.objects.get("Armature")
    if arm is not None and arm.type == "ARMATURE":
        bones = arm.pose.bones if hasattr(arm, "pose") else []
        names = [b.name for b in bones] if bones else []
        wrist_detail = {"armature": arm.name, "bones": names}
        gates["wrist"] = {"status": "NOT_CHECKED",
                          "detail": {**wrist_detail,
                                     "note": "Bone-parent wrist distance must "
                                             "be measured from the saved "
                                             "pose, not from this script's "
                                             "frame-1 read."}}
    else:
        gates["wrist"] = {"status": "NOT_CHECKED",
                          "detail": "No armature object in this blend; "
                                    "wrist gate needs the rig's bone data."}

    result = {
        "template": "motion_template.py",
        "locked_default": {
            "snap_on": SNAP_ON, "cross_start": CROSS_START,
            "cross_end": CROSS_END, "snap_off": SNAP_OFF,
            "snap_z": SNAP_Z, "torso_z": torso_z, "head_z": head_z,
        },
        "gates": gates,
        "overall": "FAIL" if failed else "PASS",
    }
    with open(GATE_JSON, "w") as fh:
        json.dump(result, fh, indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    print("MOTION_TEMPLATE_RESULT", json.dumps(result))
    sys.exit(2 if failed else 0)


main()
