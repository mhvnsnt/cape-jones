"""Wave-2 before/after proof renders.
Usage: blender -b <blend> --python render_wave2.py -- <outdir> <TAG> <POSE>
POSE keys: shoulderL_side shoulderL_fwd shoulderR_side hipL_flex hipR_flex
           kneeL kneeR wristL_bend ankleL spine_fwd spine_twist
Camera is auto-framed on the joint queried from the rig at runtime.
"""
import bpy, math, os, sys
from mathutils import Quaternion, Vector

OUTDIR = sys.argv[sys.argv.index("--") + 1]
TAG = sys.argv[sys.argv.index("--") + 2]
POSE = sys.argv[sys.argv.index("--") + 3]
os.makedirs(OUTDIR, exist_ok=True)

scn = bpy.context.scene
for name in ["BlenRigMdefCage", "CapeJones_Cape", "CapeJones_Cape_FRAGMENTS_OLD"]:
    o = bpy.data.objects.get(name)
    if o:
        o.hide_viewport = True
        o.hide_render = True

world = bpy.data.worlds.new("StudioGray")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.45, 0.45, 0.45, 1.0)
scn.world = world

bpy.ops.object.empty_add(location=(0, 0, 0.5))
tgt = bpy.context.active_object

def track_to(obj):
    c = obj.constraints.new(type='TRACK_TO')
    c.target = tgt
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'

def area_light(name, loc, power, size):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = power
    ld.size = size
    lo = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(lo)
    lo.location = loc
    track_to(lo)

area_light("KeyLight", (-1.6, -2.0, 2.6), 900, 1.2)
area_light("FillLight", (1.9, -1.4, 1.6), 350, 1.0)
area_light("RimLight", (0.2, 2.2, 2.0), 500, 1.0)

cam_data = bpy.data.cameras.new("C")
cam = bpy.data.objects.new("C", cam_data)
bpy.context.collection.objects.link(cam)
scn.camera = cam
track_to(cam)

rig = bpy.data.objects['CapeJones_Rig']
for prop in ['ik_arm_L', 'ik_arm_R', 'ik_leg_L', 'ik_leg_R']:
    if prop in rig.pose.bones['root']:
        rig.pose.bones['root'][prop] = 0.0
for pb in rig.pose.bones:
    pb.rotation_mode = 'XYZ'
    pb.rotation_euler = (0, 0, 0)
    pb.location = (0, 0, 0)
    pb.scale = (1, 1, 1)

def set_world_rot(pb_name, axis, deg):
    pb = rig.pose.bones[pb_name]
    q_rest = pb.bone.matrix_local.to_quaternion()
    q_delta = Quaternion(Vector(axis), math.radians(deg))
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = q_rest.inverted() @ q_delta @ q_rest

def joint_pos(bone_name):
    b = rig.data.bones[bone_name]
    return tuple(rig.matrix_world @ b.head_local)

# POSE -> (pose spec, joint bone for targeting, camera offset, lens)
POSES = {
    "shoulderL_side": ([("upperarm_fk_L", (0, 1, 0), -80)], "upperarm_L", (-0.5, -1.1, 0.30), 85),
    "shoulderL_fwd":  ([("upperarm_fk_L", (0, 0, 1), -90)], "upperarm_L", (0.7, -1.2, 0.25), 85),
    "shoulderR_side": ([("upperarm_fk_R", (0, 1, 0), 80)], "upperarm_R", (0.5, -1.1, 0.30), 85),
    "hipL_flex":      ([("thigh_fk_L", (1, 0, 0), 90)], "thigh_L", (0.75, -1.1, 0.15), 85),
    "hipR_flex":      ([("thigh_fk_R", (1, 0, 0), 90)], "thigh_R", (-0.75, -1.1, 0.15), 85),
    "kneeL":          ([("shin_fk_L", (1, 0, 0), -120)], "shin_L", (0.6, -0.9, 0.15), 85),
    "kneeR":          ([("shin_fk_R", (1, 0, 0), -120)], "shin_R", (-0.6, -0.9, 0.15), 85),
    "wristL_bend":    ([("hand_fk_L", (0, 0, 1), -60)], "hand_L", (0.7, -0.7, 0.2), 100),
    "wristR_bend":    ([("hand_fk_R", (0, 0, 1), 60)], "hand_R", (-0.7, -0.7, 0.2), 100),
    "ankleL":         ([("foot_fk_L", (1, 0, 0), 30)], "foot_L", (0.6, -0.75, 0.2), 100),
    "ankleR":         ([("foot_fk_R", (1, 0, 0), 30)], "foot_R", (-0.6, -0.75, 0.2), 100),
    "spine_fwd":      ([("spine_1", (1, 0, 0), 35)], "spine_2", (1.5, -0.35, 0.15), 60),
    "spine_twist":    ([("spine_1", (0, 0, 1), 35)], "spine_2", (1.1, -0.9, 0.15), 70),
}

rots, joint, offset, lens = POSES[POSE]
for pb_name, axis, deg in rots:
    set_world_rot(pb_name, axis, deg)
bpy.context.view_layer.update()

jx, jy, jz = joint_pos(joint)
tgt.location = (jx, jy, jz)
cam.location = (jx + offset[0], jy + offset[1], jz + offset[2])
cam_data.lens = lens
bpy.context.view_layer.update()

r = scn.render
r.engine = 'CYCLES'
scn.cycles.device = 'CPU'
scn.cycles.samples = 8
scn.cycles.use_denoising = False
scn.cycles.use_auto_tile = False
scn.cycles.tile_size = 64
r.resolution_x = 720
r.resolution_y = 405
r.filepath = os.path.join(OUTDIR, f"{POSE}_{TAG}.png")
print(f"RENDERING {POSE}_{TAG} target=({jx:.2f},{jy:.2f},{jz:.2f})", flush=True)
bpy.ops.render.render(write_still=True)
print("DONE", flush=True)
