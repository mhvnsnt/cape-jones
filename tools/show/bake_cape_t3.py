"""Bake T3 JSON fight motion (wh-anim/1) onto the CapeJones_Rig (94 bones) and
export one armature-only clip GLB per move, following the idle.glb convention.
Method: world-space retarget (same family as tools/show-retarget/retarget_idle_cape.py):
  W_t3(f) = product of T3 local quats along the chain (T3 space: X=left, Y=up, Z=forward)
  W_desired = (qG * W_t3 * qG^-1) @ CAPE_REST_WORLD,  qG = Rx(+90deg)
    (maps T3 left->Cape left (+X), T3 up->Cape up (+Z), T3 forward->Cape forward (-Y))
  local = (parent W_desired)^-1 * W_desired, baked onto DEFORM bones only
  COMPOSITION ORDER MATTERS: the idle pipeline's RESTW @ relative form applies
  motion INTRINSICALLY (about the bone's rest axes) -- fine for idle sway, but a
  90-180deg fight rotation then yaws about the bone's forward axis and tips the
  character over (verified in proof: strike_light ended upside-down). The
  EXTRINSIC form (motion @ rest) preserves rigid whole-body motion exactly:
  a pure T3 yaw yields identity locals everywhere, and rest is preserved.
    (mesh is skinned to deform bones; FK/IK layers stay at rest, as in the idle bake).
  pelvis location = Rx90 * (root_t - root_rest) * SCALE, SCALE = 0.409/0.9805
    (Cape pelvis rest height / T3 root rest height).
SOURCE: real decoded T3 motion (owner's disc teardown, wh-anim/1). T3 is the LOGGED
FALLBACK source: T7 .bin fight anims are not in hand on this box (pipeline doc:
Stage 2b/3 "AWAITS FILE PULL"). Swap these clips for T7-sourced ones when pulled.
Usage: blender -b --python bake_cape_t3.py -- <outdir>
"""
import bpy, json, os, sys
from mathutils import Quaternion, Vector

OUTDIR = sys.argv[sys.argv.index("--") + 1]
os.makedirs(OUTDIR, exist_ok=True)
GUN = "/home/hatch/workspace/wh-repo/game/assets/anim/t3/gunjack/"
CLIPS = [
    ("ep1_cape_stance", "t3_stance_b.json"),
    ("ep1_cape_strike_light", "t3_light.json"),
    ("ep1_cape_strike_heavy", "t3_heavy.json"),
    ("ep1_cape_hit", "t3_hit.json"),
    ("ep1_cape_hit_launch", "t3_hit_launch.json"),
    ("ep1_cape_ko", "t3_ko.json"),
]
# T3 source bone -> Cape deform bones (nearest-source mapping; each target bone takes
# the world orientation of its nearest T3 source bone; consecutive targets sharing a
# source keep exact end-effector orientation, bend concentrates at source boundaries)
MAP = {
 "Hips": ["pelvis"],
 "Spine": ["spine_1", "spine_2"],
 "Chest": ["spine_3", "spine_4", "chest"],
 "Neck": ["neck_1", "neck_2"],
 "Head": ["head"],
 "LeftShoulder": ["upperarm_L"], "LeftArm": ["forearm_L"], "LeftForeArm": ["hand_L"],
 "RightShoulder": ["upperarm_R"], "RightArm": ["forearm_R"], "RightForeArm": ["hand_R"],
 "LeftUpLeg": ["thigh_L"], "LeftLeg": ["shin_L"], "LeftFoot": ["foot_L"], "LeftToeBase": ["toe_L"],
 "RightUpLeg": ["thigh_R"], "RightLeg": ["shin_R"], "RightFoot": ["foot_R"], "RightToeBase": ["toe_R"],
}
QG = Quaternion((0.7071067811865476, 0.7071067811865476, 0.0, 0.0))  # Rx(+90deg), wxyz
SCALE = 0.409 / 1.00022  # gunjack bank root_rest_y
ROOT_REST = Vector((0.0, 1.00022, 0.0))

bpy.context.scene.render.fps = 30
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/scratch/cj-3d/cape-jones-show.glb")
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name == 'CapeJones_Rig')
assert len(rig.data.bones) == 94, f"CapeJones_Rig bone count {len(rig.data.bones)}"
for b in rig.pose.bones: b.rotation_mode = 'QUATERNION'
for n in ("CapeJones_Body", "CapeJones_Cape"):
    o = bpy.data.objects.get(n)
    if o: o.hide_viewport = True; o.hide_render = True
print("rig ready:", rig.name)
RESTW = {b.name: (rig.matrix_world @ b.matrix_local).to_3x3().to_quaternion() for b in rig.data.bones}
M_REL = {}
for b in rig.data.bones:
    M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion() if b.parent is None else (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()
PELVIS_HEAD = rig.data.bones['pelvis'].head_local.copy()

def q_xyzw(v):
    q = Quaternion((v[3], v[0], v[1], v[2])); q.normalize(); return -q if q.w < 0 else q

def bake(t3path, action_name):
    TJ = json.load(open(t3path))
    # Standard T3 motion chain (gunjack skeleton.json lists a simplified game rig,
    # not the motion chain; king + gunjack rot streams share this chain).
    PARENTS = {"Root": None, "Hips": "Root", "Spine": "Hips", "Chest": "Spine",
        "Neck": "Chest", "Head": "Neck",
        "LeftShoulder": "Chest", "LeftArm": "LeftShoulder", "LeftForeArm": "LeftArm", "LeftHand": "LeftForeArm",
        "RightShoulder": "Chest", "RightArm": "RightShoulder", "RightForeArm": "RightArm", "RightHand": "RightForeArm",
        "LeftUpLeg": "Hips", "LeftLeg": "LeftUpLeg", "LeftFoot": "LeftLeg", "LeftToeBase": "LeftFoot",
        "RightUpLeg": "Hips", "RightLeg": "RightUpLeg", "RightFoot": "RightLeg", "RightToeBase": "RightFoot"}
    n = len(TJ["root_t"])
    act = bpy.data.actions.new(action_name)
    if not rig.animation_data: rig.animation_data_create()
    rig.animation_data.action = act
    scn = bpy.context.scene
    min_foot_z = 1e9; max_pelvis_z = -1e9
    for i in range(n):
        W = {}
        for bn in TJ["bones"]:
            q = q_xyzw(TJ["rot_xyzw"][bn][i]); p = PARENTS[bn]
            W[bn] = (W[p] @ q) if (p and p in W) else q
        Wdes = {}
        for s, targets in MAP.items():
            if s not in W:
                print(f"  WARN source {s} missing in this clip; targets stay at rest")
                continue
            qw = QG @ W[s] @ QG.inverted()
            for t in targets: Wdes[t] = qw @ RESTW[t]  # EXTRINSIC: motion @ rest
        for s, targets in MAP.items():
            for t in targets:
                pb = rig.pose.bones[t]; par = pb.parent
                Wpar = Quaternion() if par is None else (Wdes[par.name] if par.name in Wdes else RESTW[par.name])
                pb.rotation_quaternion = (Wpar @ M_REL[t]).inverted() @ Wdes[t]
                pb.keyframe_insert(data_path="rotation_quaternion", frame=i)
        rt = Vector(TJ["root_t"][i])
        d = rt - ROOT_REST
        # Rx(+90): (x,y,z) -> (x,-z,y)
        moved = Vector((d.x, -d.z, d.y)) * SCALE  # armature-space offset
        # Pose location is in ROOT-bone parent space: armature (dx,dy,dz) -> L=(dx,dz,-dy)
        # (measured: L=(0,0,0.1)->head -Y; L=(0,0.1,0)->head +Z; L=(0.1,0,0)->head +X)
        pb = rig.pose.bones['pelvis']
        pb.location = Vector((moved.x, moved.z, -moved.y))
        pb.keyframe_insert(data_path="location", frame=i)
        scn.frame_set(i); bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get(); ev = rig.evaluated_get(dg)
        for fb in ("foot_L", "foot_R"):
            min_foot_z = min(min_foot_z, ev.pose.bones[fb].head.z)
        max_pelvis_z = max(max_pelvis_z, ev.pose.bones['pelvis'].head.z)
    print(f"BAKED {action_name}: {n} frames, min_foot_z={min_foot_z:.3f}, max_pelvis_z={max_pelvis_z:.3f}")
    return act

for (name, fn) in CLIPS:
    for a in list(bpy.data.actions):
        if a.name != name: bpy.data.actions.remove(a)
    act = bake(GUN + fn, name)
    bpy.ops.object.select_all(action='DESELECT')
    rig.select_set(True); bpy.context.view_layer.objects.active = rig
    out = os.path.join(OUTDIR, name + ".glb")
    bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True,
        export_animations=True, export_frame_range=True, export_anim_single_armature=True,
        export_skins=True, export_morph=False, export_cameras=False, export_lights=False)
    print("EXPORTED", out, os.path.getsize(out), "bytes")
    bpy.data.actions.remove(act)
print("ALL DONE")
