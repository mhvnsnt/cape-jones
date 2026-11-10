"""SPINE LANE — Workbench proof renders for the flexible spine.
Usage: blender -b cape_jones_rigged_w5r.blend --python spine_proof_render.py -- <outdir>
Renders front + side (960x720 Workbench) for 7 poses:
  rest, bend_fwd, arch_back, side_bend, twist, hunch, ik_bend
"""
import bpy, sys, os
from math import radians

outdir = sys.argv[sys.argv.index("--") + 1:]
outdir = outdir[0] if outdir else "/tmp/spine_proofs"
os.makedirs(outdir, exist_ok=True)

RIG = "CapeJones_Rig"
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.resolution_x = 960
sc.render.resolution_y = 720
sc.render.film_transparent = False
sc.render.image_settings.file_format = 'PNG'

cage = bpy.data.objects.get('BlenRigMdefCage')
if cage:
    cage.hide_render = True

rig = bpy.data.objects[RIG]


def reset():
    for pb in rig.pose.bones:
        pb.rotation_mode = "XYZ"
        pb.location = (0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
        pb.scale = (1, 1, 1)
    rig.pose.bones["root"]["ik_spine"] = 0.0


def fk_spine(x=0.0, z=0.0):
    for i in range(1, 5):
        rig.pose.bones[f"spine_fk_{i}"].rotation_euler = (x, 0, z)
    rig.pose.bones["chest_fk"].rotation_euler = (x, 0, z)


def p_rest():
    pass


def p_bend_fwd():
    fk_spine(x=radians(12))


def p_arch_back():
    fk_spine(x=radians(-8))


def p_side_bend():
    fk_spine(z=radians(8))


def p_twist():
    e = rig.pose.bones["spine_twist"].rotation_euler
    rig.pose.bones["spine_twist"].rotation_euler = (e[0], radians(45), e[2])


def p_hunch():
    rig.pose.bones["pelvis"].rotation_euler = (radians(7), 0, 0)
    fk_spine(x=radians(10))
    rig.pose.bones["neck_1"].rotation_euler = (radians(14), 0, 0)
    rig.pose.bones["head"].rotation_euler = (radians(8), 0, 0)


def p_ik_bend():
    # NOTE: chest_ik points +Z, so its .location is in bone-local space:
    # local (0,-0.06,+0.10) == world/armature (0,-0.10,-0.06) (forward+down).
    rig.pose.bones["root"]["ik_spine"] = 1.0
    rig.pose.bones["chest_ik"].location = (0, -0.06, 0.10)
    rig.pose.bones["chest_fk"].rotation_euler = (radians(14), 0, 0)


POSES = {
    "rest": p_rest,
    "bend_fwd": p_bend_fwd,
    "arch_back": p_arch_back,
    "side_bend": p_side_bend,
    "twist": p_twist,
    "hunch": p_hunch,
    "ik_bend": p_ik_bend,
}


def setup_cams():
    aim = bpy.data.objects.new('spine_aim', None)
    sc.collection.objects.link(aim)
    aim.location = (0, -0.02, 0.50)
    cams = {}
    for vname, vloc in {'front': (0, -2.2, 0.55), 'side': (2.2, 0, 0.55)}.items():
        cd = bpy.data.cameras.new(f'spine_{vname}')
        cam = bpy.data.objects.new(f'spine_{vname}', cd)
        sc.collection.objects.link(cam)
        cam.location = vloc
        con = cam.constraints.new('TRACK_TO')
        con.target = aim
        con.track_axis = 'TRACK_NEGATIVE_Z'
        con.up_axis = 'UP_Y'
        cd.lens = 45
        cams[vname] = cam
    return cams


cams = setup_cams()
for pname, apply in POSES.items():
    reset()
    apply()
    bpy.context.view_layer.update()
    for vname, cam in cams.items():
        sc.camera = cam
        bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(outdir, f'spine_{pname}_{vname}.png')
        bpy.ops.render.render(write_still=True)
        print(f"RENDERED {sc.render.filepath}", flush=True)
print("DONE", flush=True)
