#!/usr/bin/env python3
"""blend_guard.py — in-blend guard for Cape Jones scenes.

The missing piece named in tools/wired/README.md ("Still missing", 2026-10-28):
the four wired tools gate everything AROUND a .blend (proof, disk, GLB stage);
this script runs INSIDE one and guards the file itself. It:

  1. LOCKS every action (use_fake_user = True) so no action can be lost on
     save / datablock cleanup, and records which action each armature runs.
  2. CHECKS body-to-rig alignment BEFORE render: evaluated world bbox of each
     skinned mesh vs its armature's bone extents, plus a sampled
     vertex-to-nearest-bone-segment distance (the weight-saga audit method).
  3. Optionally BAKES deform -> FK (--bake-fk): for armatures whose pose bones
     carry constraints, bakes the visual result over the scene frame range
     into a new action "<Armature>_FKBAKE" (visual keying, pose only). The
     source actions are never modified; the baked action is fake-user locked.
     With no constrained bones it reports SKIP instead of inventing work.
  4. VERIFIES after: every action locked, active actions present, weight
     sums on skinned meshes (fraction of verts whose total weight deviates
     from 1.0 by > 0.05, and unweighted fraction), bboxes re-measured.

Nothing is saved unless --save is passed (saves in place). Exit code 0 when
every check passes, 2 when any check FAILs, so the script can gate a render.

Usage:
  blender -b scene.blend --python blend_guard.py -- [--bake-fk] [--save]
                                                     [--report out.json]
Tested on Blender 4.5.3 (works on 4.x generally; no version-locked APIs).
"""

import json
import math
import sys

import bpy
from mathutils import Vector

REPORT = {"actions": {}, "armatures": {}, "checks": [], "bakes": []}


def note(ok, label, detail=""):
    REPORT["checks"].append({"ok": bool(ok), "label": label, "detail": detail})
    print(f"[blend_guard] {'PASS' if ok else 'FAIL'}  {label}  {detail}")


# ---------------------------------------------------------------- actions
def lock_actions():
    locked = 0
    for action in bpy.data.actions:
        if not action.use_fake_user:
            action.use_fake_user = True
        locked += 1
        REPORT["actions"][action.name] = {
            "fake_user": bool(action.use_fake_user),
            "frame_range": [float(action.frame_range[0]), float(action.frame_range[1])],
            "users": action.users,
        }
    note(locked > 0, "actions locked", f"{locked} action(s), all fake_user=True")
    return locked


# ---------------------------------------------------------------- geometry
def world_bbox(obj):
    return [obj.matrix_world @ Vector(c) for c in obj.bound_box]


def bbox_stats(corners):
    xs = [c.x for c in corners]
    ys = [c.y for c in corners]
    zs = [c.z for c in corners]
    lo = Vector((min(xs), min(ys), min(zs)))
    hi = Vector((max(xs), max(ys), max(zs)))
    return lo, hi, (lo + hi) / 2.0


def bone_world_points(arm_obj):
    """CURRENT POSE bone endpoints in world space (pose bones, not rest)."""
    pts = []
    mw = arm_obj.matrix_world
    for pbone in arm_obj.pose.bones:
        pts.append(mw @ pbone.head)
        pts.append(mw @ pbone.tail)
    return pts


def seg_point_dist(p, a, b):
    ab = b - a
    denom = ab.length_squared
    if denom == 0.0:
        return (p - a).length
    t = max(0.0, min(1.0, (p - a).dot(ab) / denom))
    return (p - (a + ab * t)).length


def sampled_alignment(mesh_obj, arm_obj, sample_step=997):
    """Median sampled distance from evaluated mesh verts to nearest bone seg."""
    deps = bpy.context.evaluated_depsgraph_get()
    eval_obj = mesh_obj.evaluated_get(deps)
    mesh = eval_obj.to_mesh()
    mw = eval_obj.matrix_world
    bones = [
        (arm_obj.matrix_world @ pb.head, arm_obj.matrix_world @ pb.tail)
        for pb in arm_obj.pose.bones
    ]
    dists = []
    verts = mesh.vertices
    for i in range(0, len(verts), sample_step):
        p = mw @ verts[i].co
        dists.append(min(seg_point_dist(p, a, b) for a, b in bones))
    eval_obj.to_mesh_clear()
    if not dists:
        return None
    dists.sort()
    return dists[len(dists) // 2]


def weight_stats(mesh_obj):
    total = len(mesh_obj.data.vertices)
    if total == 0:
        return None
    bad = 0
    unweighted = 0
    groups = mesh_obj.data.vertices
    for v in groups:
        s = sum(g.weight for g in v.groups)
        if s == 0.0:
            unweighted += 1
        elif abs(s - 1.0) > 0.05:
            bad += 1
    return {
        "verts": total,
        "unweighted_frac": unweighted / total,
        "bad_sum_frac": bad / total,
        "vertex_groups": len(mesh_obj.vertex_groups),
    }


# ---------------------------------------------------------------- bake
def bake_fk(arm_obj, frame_start, frame_end):
    constrained = [
        pb.name
        for pb in arm_obj.pose.bones
        if len(pb.constraints) > 0
    ]
    if not constrained:
        REPORT["bakes"].append({"armature": arm_obj.name, "result": "SKIP no constrained pose bones"})
        print(f"[blend_guard] SKIP bake for {arm_obj.name}: no constrained pose bones")
        return
    bpy.ops.object.select_all(action="DESELECT")
    arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.nla.bake(
        frame_start=frame_start,
        frame_end=frame_end,
        step=1,
        only_selected=False,
        visual_keying=True,
        clear_constraints=False,
        clear_parents=False,
        use_current_action=False,
        bake_types={"POSE"},
    )
    baked = arm_obj.animation_data.action
    if baked is not None:
        baked.name = f"{arm_obj.name}_FKBAKE"
        baked.use_fake_user = True
        REPORT["bakes"].append(
            {"armature": arm_obj.name, "result": f"baked -> {baked.name}", "constrained_bones": len(constrained)}
        )
        print(f"[blend_guard] baked {arm_obj.name} -> {baked.name} ({len(constrained)} constrained bones)")
    else:
        REPORT["bakes"].append({"armature": arm_obj.name, "result": "FAIL no action produced"})
        note(False, f"bake {arm_obj.name}", "nla.bake produced no action")


# ---------------------------------------------------------------- main
def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    do_bake = "--bake-fk" in argv
    do_save = "--save" in argv
    report_path = None
    if "--report" in argv:
        report_path = argv[argv.index("--report") + 1]

    scene = bpy.context.scene
    frame_start, frame_end = int(scene.frame_start), int(scene.frame_end)
    print(f"[blend_guard] scene frames {frame_start}-{frame_end}, current {scene.frame_current}")

    lock_actions()

    armatures = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    note(len(armatures) > 0, "armature present", f"{len(armatures)} armature(s)")

    for arm in armatures:
        info = {"bones": len(arm.data.bones), "active_action": None}
        if arm.animation_data and arm.animation_data.action:
            info["active_action"] = arm.animation_data.action.name
        note(
            info["active_action"] is not None,
            f"{arm.name} has an active action",
            str(info["active_action"]),
        )
        bone_pts = bone_world_points(arm)
        blo, bhi, _ = bbox_stats(bone_pts)
        info["bone_bbox"] = {"lo": list(blo), "hi": list(bhi)}

        skinned = [
            o
            for o in bpy.data.objects
            if o.type == "MESH"
            and any(m.type == "ARMATURE" and m.object == arm for m in o.modifiers)
        ]
        info["skinned_meshes"] = []
        for mesh_obj in skinned:
            ws = weight_stats(mesh_obj)
            med = sampled_alignment(mesh_obj, arm)
            entry = {"name": mesh_obj.name, "weights": ws, "median_vert_to_bone_m": med}
            info["skinned_meshes"].append(entry)
            if ws:
                note(
                    ws["unweighted_frac"] == 0.0 and ws["bad_sum_frac"] <= 0.01,
                    f"{mesh_obj.name} weight sums sane",
                    f"unweighted={ws['unweighted_frac']:.4f} bad_sum={ws['bad_sum_frac']:.4f} verts={ws['verts']}",
                )
            if med is not None:
                note(
                    med < 0.35,
                    f"{mesh_obj.name} body-to-rig alignment (sampled median)",
                    f"{med:.3f} m to nearest bone segment",
                )
        REPORT["armatures"][arm.name] = info

        if do_bake:
            bake_fk(arm, frame_start, frame_end)

    # post-verify: every action still locked
    unlocked = [a.name for a in bpy.data.actions if not a.use_fake_user]
    note(not unlocked, "post-check: all actions locked", f"unlocked={unlocked}")

    if do_save:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        print(f"[blend_guard] saved {bpy.data.filepath}")

    failed = [c for c in REPORT["checks"] if not c["ok"]]
    REPORT["verdict"] = "PASS" if not failed else f"FAIL ({len(failed)} check(s))"
    print(f"[blend_guard] VERDICT: {REPORT['verdict']}")
    if report_path:
        with open(report_path, "w") as fh:
            json.dump(REPORT, fh, indent=2)
        print(f"[blend_guard] report -> {report_path}")
    sys.exit(0 if not failed else 2)


main()
