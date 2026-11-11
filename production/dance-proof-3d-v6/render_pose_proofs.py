"""Render zoomed idle proofs from a rig file (session-only scene dressing;
the file itself is never saved). For each sitting pose action + the
breathe idle: assign, evaluate, frame the character's bounding box,
render a front three-quarter still.
Args: <out_dir>
Run: blender -b <file.blend> --python render_pose_proofs.py -- <out_dir>
"""
import bpy, sys, math
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]

# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# The raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
# The proofs render the rig's posed mesh, so they must show the FIXED arms.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
cj_arm_guard.ensure_arm_fix()

sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["CapeJones_Body"]
cape = bpy.data.objects["CapeJones_Cape"]

# ---- session-only studio: world, sun, key light, camera, floor
w = bpy.data.worlds.new("ProofWorld"); sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.58, 0.62, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sun_d = bpy.data.lights.new("Sun", 'SUN'); sun_d.energy = 3.0
sun = bpy.data.objects.new("Sun", sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), 0, math.radians(30))
key_d = bpy.data.lights.new("Key", 'POINT'); key_d.energy = 300.0
key = bpy.data.objects.new("Key", key_d); sc.collection.objects.link(key)
cam_d = bpy.data.cameras.new("ProofCam"); cam_d.lens = 50
cam = bpy.data.objects.new("ProofCam", cam_d); sc.collection.objects.link(cam)
sc.camera = cam
mat = bpy.data.materials.new("FloorMat")
mat.diffuse_color = (0.35, 0.37, 0.4, 1)
floor = None

# WORKBENCH, not EEVEE: these are pose/silhouette gate proofs, and a
# second EEVEE instance OOM-kills alongside the dance render on this
# box (proven twice). Workbench studio lighting reads the arm pose
# clearly at a fraction of the memory.
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.light = 'STUDIO'
sh.color_type = 'TEXTURE'
sh.show_cavity = True
sh.cavity_type = 'WORLD'
sc.render.resolution_x = 560; sc.render.resolution_y = 560
sc.render.film_transparent = False

# The cape in this file carries no Armature modifier (pre-existing;
# the sitting lane's own proofs hid it for the same reason) and the
# BlenRig mdef cage is a working cage, not the character - hide both
# session-only and frame on the body alone.
cape.hide_render = True
cage = bpy.data.objects.get("BlenRigMdefCage")
if cage: cage.hide_render = True

def bbox_world():
    # Frame from EVALUATED POSE-BONE positions (ob.bound_box is the
    # UNDEFORMED rest box - standing height - and frames seated poses
    # wrong; to_mesh on the evaluated body errors in this build).
    RPB_ = rig.pose.bones
    pts = []
    for n in ("head", "pelvis", "chest", "toe_L", "toe_R", "hand_fk_L",
              "hand_fk_R", "foot_L", "foot_R", "shin_L", "shin_R"):
        if n in RPB_:
            pb = RPB_[n]
            m = rig.matrix_world @ pb.matrix
            pts.append(m.to_translation())
            pts.append(m @ Vector((0, pb.length, 0)))
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    return Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2)), \
           Vector((max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))), min(zs)

def look_at(obj, pt):
    obj.rotation_euler = (pt - obj.location).to_track_quat('-Z', 'Y').to_euler()

ITEMS = [("pose_sit_normal", 1), ("pose_sit_leg_folded", 1),
         ("pose_sit_lean_forward", 1), ("pose_sit_recline", 1),
         ("pose_sit_shrug", 1), ("idle_heroic_breathe", 12)]
import os
os.makedirs(OUT, exist_ok=True)
if len(argv) > 1:
    ITEMS = [ITEMS[int(argv[1])]]
for name, fr in ITEMS:
    if name not in bpy.data.actions:
        print("missing action", name); continue
    rig.animation_data_create()
    rig.animation_data.action = bpy.data.actions[name]
    if name == "idle_heroic_breathe":
        # the breathe keys only 8 bones - start it from a neutral
        # standing base or it inherits the previous pose's root/legs
        for pb in rig.pose.bones:
            pb.rotation_quaternion = (1, 0, 0, 0); pb.rotation_euler = (0, 0, 0)
            pb.location = (0, 0, 0); pb.scale = (1, 1, 1)
    sc.frame_set(fr); bpy.context.view_layer.update()
    cen, size, zmin = bbox_world()
    # evaluated facing from the posed feet (toe - ankle, world, z=0)
    RPBf = rig.pose.bones
    _tf = (rig.matrix_world @ RPBf["toe_L"].matrix).to_translation()
    _af = (rig.matrix_world @ RPBf["foot_L"].matrix).to_translation()
    fw0 = Vector((_tf.x - _af.x, _tf.y - _af.y, 0))
    fw0 = fw0.normalized() if fw0.length > 1e-6 else Vector((0, -1, 0))
    if floor is None:
        bpy.ops.mesh.primitive_plane_add(size=30)
        floor = bpy.context.active_object
        floor.data.materials.append(mat)
    floor.location = (cen.x, cen.y, zmin - 0.01)
    # session-only seat block: the poses sit at the canon seat height
    # (top z=0.37) but the library file carries no chair - a plain
    # block under the pelvis makes the sit read instantly in proofs.
    for ob in list(bpy.data.objects):
        if ob.name.startswith("ProofSeat"):
            bpy.data.objects.remove(ob, do_unlink=True)
    if name != "idle_heroic_breathe":
        # seat block under the PELVIS (not the bone-span centre, which
        # is toe-biased and swallows the shins), top just below pelvis
        _pv = (rig.matrix_world @ rig.pose.bones["pelvis"].matrix).to_translation()
        bpy.ops.mesh.primitive_cube_add(size=1)
        seat = bpy.context.active_object
        seat.name = "ProofSeat"
        _top = max(_pv.z - 0.02, 0.08)
        seat.scale = (0.55, 0.30, _top)
        _ctr = Vector((_pv.x, _pv.y, 0)) - fw0 * 0.08
        seat.rotation_euler = (0, 0, math.atan2(fw0.y, fw0.x) - math.pi / 2)
        seat.location = (_ctr.x, _ctr.y, _top / 2)
        seat.data.materials.append(mat)
    # evaluated facing from the posed feet (toe - ankle, world, z=0)
    RPB = rig.pose.bones
    _t = (rig.matrix_world @ RPB["toe_L"].matrix).to_translation()
    _a = (rig.matrix_world @ RPB["foot_L"].matrix).to_translation()
    fw = Vector((_t.x - _a.x, _t.y - _a.y, 0))
    fw = fw.normalized() if fw.length > 1e-6 else Vector((0, -1, 0))
    side = Vector((-fw.y, fw.x, 0))
    span = max(size.x, size.y, size.z)
    dist = span * 2.1
    cam.location = cen + fw * dist + side * dist * 0.38 + Vector((0, 0, size.z * 0.22))
    look_at(cam, cen + Vector((0, 0, size.z * 0.02)))
    key.location = cen + fw * 2.0 + side * 1.5 + Vector((0, 0, 2.5))
    sc.render.filepath = os.path.join(OUT, f"proof_{name}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name, "center", [round(v, 2) for v in cen], "size", [round(v, 2) for v in size])
print("POSE_PROOFS_DONE")
