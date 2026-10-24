"""retarget_idle_cape.py — rotation-delta retarget of CMU 140_06 ('Idle') BVH
onto the CapeJones_Rig (94-bone show rig, cape-jones repo), clean-scene recipe
adapted from western-heart tools/anim-retarget/retarget_rot.py (proven on the
cyborgx wave clip, PR wh#849).

Math (rotation only, parent-first, scale-safe):
    R_target_pose = (R_src_pose @ R_src_rest^-1) @ R_target_rest
Target bones keep their own rest offsets (lengths never change).
--in-place: no root translation (idle).

Source: CMU mocap 140_06.bvh, commercial-safe per
3d-assets/animation/mocap-cmu/MANIFEST.md ("The data used in this project was
obtained from mocap.cs.cmu.edu. The database was created with funding from
NSF EIA-0196217.")
Target: the show rig inside cape-jones-show.glb (CapeJones_Rig, 94 bones,
0.925 m native, deform bones baked directly so GLB skinning works).

Show context ONLY. No fight movesets.

Usage:
  blender -b --python retarget_idle_cape.py -- --source 140_06.bvh \
    --target cape-jones-show.glb --out clip-idle.glb --clip-name show_idle
"""
import argparse, json, os, sys
import bpy
from mathutils import Matrix

a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
p = argparse.ArgumentParser()
for k in ("--source", "--target", "--out"): p.add_argument(k, required=True)
p.add_argument("--clip-name", default="show_idle")
p.add_argument("--fps", type=int, default=30)
p.add_argument("--step", type=int, default=4)
p.add_argument("--skip", type=int, default=200)
p.add_argument("--max-frames", type=int, default=121)
p.add_argument("--in-place", action="store_true", default=True)
args = p.parse_args(a)

# CMU BVH bone -> CapeJones_Rig DEFORM bone (baked directly; mesh is skinned
# to deform bones, and FK->deform constraints do not survive GLB export)
BONEMAP = {
    "Hips": "pelvis",
    "LowerBack": "spine_1", "Spine": "spine_3", "Spine1": "chest",
    "Neck": "neck_1", "Neck1": "neck_2", "Head": "head",
    "LeftShoulder": "upperarm_L", "LeftArm": "forearm_L", "LeftForeArm": "hand_L",
    "RightShoulder": "upperarm_R", "RightArm": "forearm_R", "RightForeArm": "hand_R",
    "LeftUpLeg": "thigh_L", "LeftLeg": "shin_L",
    "LeftFoot": "foot_L", "LeftToeBase": "toe_L",
    "RightUpLeg": "thigh_R", "RightLeg": "shin_R",
    "RightFoot": "foot_R", "RightToeBase": "toe_R",
    "LThumb": "finger_thumb_1_L", "LeftHandIndex1": "finger_index_1_L",
    "RThumb": "finger_thumb_1_R", "RightHandIndex1": "finger_index_1_R",
}

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = args.fps


def imp(path):
    before = set(bpy.data.objects)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".bvh":
        bpy.ops.import_anim.bvh(filepath=path, rotate_mode="NATIVE")
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=path)
    else:
        bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    return [o for o in new if o.type == "ARMATURE"][0], new


src, _ = imp(args.source)
src_action = src.animation_data.action
tgt, tgt_objs = imp(args.target)
assert len(tgt.data.bones) == 94, f"expected 94-bone CapeJones_Rig, got {len(tgt.data.bones)}"
if tgt.animation_data:
    tgt.animation_data.action = None
for pb in tgt.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
    pb.rotation_mode = "QUATERNION"
bpy.context.view_layer.update()


def wq(arm, M):
    return (arm.matrix_world @ M).to_quaternion()


pairs = []
for s in src.data.bones:
    t = BONEMAP.get(s.name)
    if t and t in tgt.data.bones:
        pairs.append((s.name, t, wq(src, s.matrix_local),
                      wq(tgt, tgt.data.bones[t].matrix_local)))
depth = lambda b: 0 if b.parent is None else 1 + depth(b.parent)
pairs.sort(key=lambda x: depth(tgt.data.bones[x[1]]))
print(f"mapped {len(pairs)} bones: {[q[1] for q in pairs]}")
assert len(pairs) >= 20, "too few bones mapped"

f0, f1 = [int(x) for x in src_action.frame_range]
f0 += args.skip
if args.max_frames:
    f1 = min(f1, f0 + args.max_frames * args.step - 1)

act = bpy.data.actions.new(args.clip_name)
tgt.animation_data_create()
tgt.animation_data.action = act
tw_inv = tgt.matrix_world.to_quaternion().inverted()
# hide heavy meshes during bake (removed before export anyway)
for _o in tgt_objs:
    if _o.type == "MESH":
        _o.hide_viewport = True
        _o.hide_render = True
for fr in range(f0, f1 + 1, args.step):
    sc.frame_set(fr)
    bpy.context.view_layer.update()  # one update: evaluate SOURCE armature
    kf = 1 + (fr - f0) // args.step
    for s_name, t_name, Rs_rest, Rt_rest in pairs:
        sp = src.pose.bones[s_name]
        tp = tgt.pose.bones[t_name]
        Ra = tw_inv @ ((wq(src, sp.matrix) @ Rs_rest.inverted()) @ Rt_rest)
        head = tp.matrix.to_translation()
        tp.matrix = Matrix.LocRotScale(head, Ra, tp.matrix.to_scale())
        tp.keyframe_insert("rotation_quaternion", frame=kf)
sc.frame_start, sc.frame_end = 1, 1 + (f1 - f0) // args.step

# keep ONLY the target armature + the one baked action
for o in list(bpy.data.objects):
    if o not in tgt_objs:
        bpy.data.objects.remove(o, do_unlink=True)
for x in list(bpy.data.actions):
    if x != act:
        bpy.data.actions.remove(x)
for o in list(bpy.data.objects):  # anim-only: drop meshes
    if o.type == "MESH":
        bpy.data.objects.remove(o, do_unlink=True)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(
    filepath=args.out, export_format="GLB", use_selection=True,
    export_animations=True, export_frame_range=True,
    export_anim_single_armature=True,
    export_skins=True, export_morph=False,
    export_cameras=False, export_lights=False)
print(f"WROTE {args.out} frames={sc.frame_end} bones={len(pairs)}")
