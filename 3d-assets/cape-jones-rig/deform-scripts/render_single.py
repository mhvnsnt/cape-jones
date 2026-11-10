"""Streamlined before/after render. Usage: -- blend outdir tag posename
Renders a single pose from a single blend file."""
import bpy, math, os, sys
from mathutils import Quaternion, Vector

BLEND = sys.argv[sys.argv.index("--") + 1]  # not used, file already open
OUTDIR = sys.argv[sys.argv.index("--") + 2]
TAG = sys.argv[sys.argv.index("--") + 3]
POSE = sys.argv[sys.argv.index("--") + 4]
os.makedirs(OUTDIR, exist_ok=True)

scn = bpy.context.scene
for name in ["BlenRigMdefCage", "CapeJones_Cape"]:
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

POSES = {
    "elbow_topdown": ([("forearm_fk_L", (0,0,1), -130)], ((0.32,-0.05,0.72), (0.32,-0.05,1.6), 50)),
    "elbow_crease":  ([("forearm_fk_L", (0,0,1), -130)], ((0.345,-0.06,0.735), (0.42,-0.52,0.86), 80)),
    "jaw_side":      ([("jaw", (1,0,0), 32)], ((0.0,-0.055,0.815), (0.48,-0.10,0.86), 85)),
    "jaw_front":     ([("jaw", (1,0,0), 32)], ((0.0,-0.06,0.82), (0.10,-0.50,0.90), 85)),
    "head_turn":     ([("head", (0,0,1), 60)], ((0.0,-0.02,0.85), (0.45,-0.62,0.95), 70)),
    "overhead":      ([("upperarm_fk_L", (0,1,0), -95)], ((0.30,-0.05,0.80), (1.05,-1.10,0.60), 50)),
}

rots, (target, pos, lens) = POSES[POSE]
for pb_name, axis, deg in rots:
    set_world_rot(pb_name, axis, deg)
bpy.context.view_layer.update()
tgt.location = target
cam.location = pos
cam_data.lens = lens
bpy.context.view_layer.update()

r = scn.render
r.engine = 'CYCLES'
scn.cycles.device = 'CPU'
scn.cycles.samples = 12
scn.cycles.use_denoising = True
r.resolution_x = 960
r.resolution_y = 540
r.filepath = os.path.join(OUTDIR, f"{POSE}_{TAG}.png")
print(f"RENDERING {POSE}_{TAG}", flush=True)
bpy.ops.render.render(write_still=True)
print("DONE", flush=True)
