"""Ep1 Scene 5 — portal flight clip (Cape, clip-local, faces -Y).
Structure @30fps, 125f total:
  0..14   seated hold (sampled from ep1_cape_channel_flip frame 0 pose)
  15..34  procedural stand: slerp seated->stance pose + pelvis rise
  35..94  procedural flight: pelvis accelerates -Y (3.2m) + rises 0.35m,
          body pitches forward to 70deg (superman), arms swept back along body
  95..114 procedural land: pitch back to 0, pelvis descends into a crouch
          (thighs Rx-55deg, shins vertical, feet flat), hold
  115..124 crouch hold (arrival pose; arena stance is the next beat)
Method: pose sampling + parent-first world-orientation solver (same math as
the retarget pipeline: local = (parent_desired @ M_REL)^-1 @ desired_world).
Seated base is mocap (CMU 13_05 via channel-flip clip); stand/flight/land
are procedural (no mocap source exists for being pulled through a TV).
Cape streaming is the cloth lane's job -- this clip moves the BODY only.
Output: clips/cape/ep1_cape_portal_flight.glb (armature-only, idle convention).
"""
import bpy, sys, math, os
from mathutils import Quaternion, Vector
OUT = "/home/hatch/workspace/ep1-fight-anim/clips/cape/ep1_cape_portal_flight.glb"
bpy.context.scene.render.fps = 30
scn = bpy.context.scene
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/scratch/cj-3d/cape-jones-show.glb")
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name == 'CapeJones_Rig')
for b in rig.pose.bones: b.rotation_mode = 'QUATERNION'
for n in ("CapeJones_Body", "CapeJones_Cape"):
    o = bpy.data.objects.get(n)
    if o: o.hide_viewport = True; o.hide_render = True
# load clip actions
def load_action(path):
    before_objs = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new_arms = [o for o in bpy.data.objects if o.type == 'ARMATURE' and o not in before_objs]
    assert new_arms, path
    act0 = new_arms[0].animation_data.action if new_arms[0].animation_data else None
    assert act0 is not None, path
    for o in list(bpy.data.objects):
        if o.type == 'ARMATURE' and o != rig:
            bpy.data.objects.remove(o, do_unlink=True)
    return act0
flip = load_action("/home/hatch/workspace/ep1-fight-anim/clips/cape/ep1_cape_channel_flip.glb")
stance = load_action("/home/hatch/workspace/ep1-fight-anim/clips/cape/ep1_cape_stance.glb")
M_REL = {}
for b in rig.data.bones:
    M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion() if b.parent is None else (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()
PARENT = {b.name: (b.parent.name if b.parent else None) for b in rig.data.bones}
ORDER = []
seen = set()
def visit(n):
    if n in seen or n is None: return
    p = PARENT[n]
    if p: visit(p)
    seen.add(n); ORDER.append(n)
for b in rig.data.bones: visit(b.name)
def sample(action, frame):
    """Return {bone: (loc_quat, pelvis_loc)} evaluated pose at frame."""
    rig.animation_data_create() if not rig.animation_data else None
    rig.animation_data.action = action
    scn.frame_set(frame); bpy.context.view_layer.update()
    pose = {}
    for pb in rig.pose.bones:
        pose[pb.name] = (pb.rotation_quaternion.copy(), pb.location.copy())
    return pose
def worlds(pose):
    """World orientations from sampled local pose (armature at identity)."""
    W = {}
    for n in ORDER:
        lq, _ = pose[n]; p = PARENT[n]
        W[n] = (W[p] @ M_REL[n] @ lq) if p else (M_REL[n] @ lq)
    return W
seated = sample(flip, 0)
standing = sample(stance, 0)
W_stand = worlds(standing)
act = bpy.data.actions.new("ep1_cape_portal_flight")
rig.animation_data.action = act
def key_pose(pose, frame):
    for bn, (lq, loc) in pose.items():
        pb = rig.pose.bones[bn]
        pb.rotation_quaternion = lq; pb.location = loc
        pb.keyframe_insert(data_path="rotation_quaternion", frame=frame)
        if bn == 'pelvis':
            pb.keyframe_insert(data_path="location", frame=frame)
def blend_pose(a, b, t):
    out = {}
    for bn in a:
        lq = a[bn][0].slerp(b[bn][0], t)
        loc = a[bn][1].lerp(b[bn][1], t)
        out[bn] = (lq, loc)
    return out
def solver_pose(worlds_des, base_pose):
    """Set bones whose world orientation is given; others keep base locals."""
    pose = dict(base_pose)
    Wdes = {}
    for n in ORDER:
        if n in worlds_des:
            p = PARENT[n]
            Wp = Wdes[p] if p in Wdes else (W_stand[p] if p else Quaternion())
            # parent desired world: if parent not in worlds_des, use its base world
            if p and p not in Wdes:
                # compute base world for parent from base pose
                Wp = W_stand[p]
            loc = (Wp @ M_REL[n]).inverted() @ worlds_des[n]
            pose[n] = (loc, base_pose[n][1])
            Wdes[n] = worlds_des[n]
    return pose
def ease(t): return t * t * (3 - 2 * t)
PITCH_BONES = ['pelvis', 'spine_1', 'spine_2', 'spine_3', 'spine_4', 'chest', 'neck_1', 'neck_2', 'head']
# 0..14 seated hold
for f in range(0, 15):
    key_pose(seated, f)
# 15..34 stand blend
for f in range(15, 35):
    t = ease((f - 15) / 19)
    key_pose(blend_pose(seated, standing, t), f)
# 35..94 flight
# Pelvis location is in ROOT-BONE parent space, not armature space. The root
# bone's frame maps armature (dx,dy,dz) -> parent-space (dx,dz,-dy) (measured
# for the T3 converter). The path is designed in armature space (travel -Y,
# rise +Z) and converted here; v1 wrote clip-space values directly as the
# location, which sent the travel DOWN through the floor (pelvis z -2.74).
def to_parent(arm):
    return Vector((arm.x, arm.z, -arm.y))
def to_arm(loc):
    return Vector((loc.x, -loc.z, loc.y))
stand_pelvis_loc = standing['pelvis'][1]
stand_arm = to_arm(stand_pelvis_loc)
for f in range(35, 95):
    t = (f - 35) / 59
    pitch = math.radians(70) * ease(min(t / 0.25, 1.0))
    Rx = Quaternion((1, 0, 0), pitch)
    Wdes = {bn: Rx @ W_stand[bn] for bn in PITCH_BONES}
    # arms sweep back along the (pitched) body, eased in over the first 10f
    # (v1 snapped to full sweep at f35): left +X->+Y is Rz+90, right -X->+Y is Rz-90
    sweep = math.radians(90) * ease(min(t / 0.17, 1.0))
    Wdes['upperarm_L'] = Rx @ Quaternion((0, 0, 1), sweep) @ W_stand['upperarm_L']
    Wdes['upperarm_R'] = Rx @ Quaternion((0, 0, 1), -sweep) @ W_stand['upperarm_R']
    pose = solver_pose(Wdes, standing)
    # pelvis path in armature space: accelerate -Y (t^2), rise 0.35m
    arm = stand_arm.copy()
    arm.y -= 3.2 * t * t
    arm.z += 0.35 * math.sin(math.pi * 0.5 * min(t * 1.4, 1.0))
    pose['pelvis'] = (pose['pelvis'][0], to_parent(arm))
    key_pose(pose, f)
# 95..114 land: pitch->0, pelvis to crouch (armature space, then converted)
flight_end_arm = stand_arm.copy(); flight_end_arm.y -= 3.2; flight_end_arm.z += 0.35
crouch_arm = flight_end_arm.copy(); crouch_arm.z -= 0.55  # pelvis drop into crouch
flight_end_loc = to_parent(flight_end_arm)
crouch_loc = to_parent(crouch_arm)
for f in range(95, 115):
    t = ease((f - 95) / 19)
    pitch = math.radians(70) * (1 - t)
    Rx = Quaternion((1, 0, 0), pitch)
    Wdes = {bn: Rx @ W_stand[bn] for bn in PITCH_BONES}
    # arms come forward/out as he lands (release the sweep)
    Wdes['upperarm_L'] = Rx @ Quaternion((0, 0, 1), math.radians(90 * (1 - t))) @ W_stand['upperarm_L']
    Wdes['upperarm_R'] = Rx @ Quaternion((0, 0, 1), math.radians(-90 * (1 - t))) @ W_stand['upperarm_R']
    # crouch: thighs flex forward (Rx-55), shins stay vertical, feet flat
    flex = math.radians(55) * t
    Wdes['thigh_L'] = Quaternion((1, 0, 0), -flex) @ W_stand['thigh_L']
    Wdes['thigh_R'] = Quaternion((1, 0, 0), -flex) @ W_stand['thigh_R']
    Wdes['shin_L'] = W_stand['shin_L']; Wdes['shin_R'] = W_stand['shin_R']
    Wdes['foot_L'] = W_stand['foot_L']; Wdes['foot_R'] = W_stand['foot_R']
    pose = solver_pose(Wdes, standing)
    loc = flight_end_loc.lerp(crouch_loc, t)
    pose['pelvis'] = (pose['pelvis'][0], loc)
    key_pose(pose, f)
# 115..124 crouch hold (repeat last pose)
for f in range(115, 125):
    key_pose(solver_pose({'thigh_L': Quaternion((1, 0, 0), math.radians(-55)) @ W_stand['thigh_L'],
                          'thigh_R': Quaternion((1, 0, 0), math.radians(-55)) @ W_stand['thigh_R'],
                          'shin_L': W_stand['shin_L'], 'shin_R': W_stand['shin_R'],
                          'foot_L': W_stand['foot_L'], 'foot_R': W_stand['foot_R']}, standing), f)
    # fix pelvis location to crouch (solver_pose kept standing pelvis loc)
    rig.pose.bones['pelvis'].location = crouch_loc
    rig.pose.bones['pelvis'].keyframe_insert(data_path="location", frame=f)
for o in list(bpy.data.objects):
    if o.type == 'ARMATURE' and o != rig:
        bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.actions):
    if a != act:
        bpy.data.actions.remove(a)
scn.frame_start = 0; scn.frame_end = 124
bpy.ops.object.select_all(action='DESELECT')
rig.select_set(True); bpy.context.view_layer.objects.active = rig
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
    export_animations=True, export_frame_range=True, export_anim_single_armature=True,
    export_skins=True, export_morph=False, export_cameras=False, export_lights=False)
print("EXPORTED", OUT, os.path.getsize(OUT), "bytes")
