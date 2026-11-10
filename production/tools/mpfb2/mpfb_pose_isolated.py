# Isolated pose proofs: keep ONLY the MPFB reference body + rig, apply
# scripted extreme poses with analytically-verified signs, render.
# Signs verified: thigh +X = swing fwd, knee -X = flex back, elbow +X = flex fwd.
# Usage: blender-4.5 -b cape_jones_mpfb_wired.blend --python mpfb_pose_isolated.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import bpy
from mathutils import Vector, Quaternion

_MPFB_USER = os.path.expanduser("~/.config/mpfb-user-data")
os.makedirs(_MPFB_USER, exist_ok=True)
bpy.utils.extension_path_user = lambda package, **kwargs: _MPFB_USER
import mpfb
mpfb.get_preference = lambda name: None
mpfb.register()

OUT = os.path.join(os.path.dirname(bpy.data.filepath), "mpfb_proofs")
os.makedirs(OUT, exist_ok=True)

rig = bpy.data.objects["MPFB_FullSkeleton"]
body = bpy.data.objects["MPFB_ReferenceBody"]
for o in list(bpy.data.objects):
    if o not in (rig, body):
        bpy.data.objects.remove(o, do_unlink=True)
print("ISOLATED SCENE:", sorted(o.name for o in bpy.data.objects))

X = Vector((1, 0, 0))
Z = Vector((0, 0, 1))


def swing(bone_name, axis_arm, angle):
    # Proven: armature-space rotation -> bone-local via rest matrix, compose.
    pb = rig.pose.bones[bone_name]
    pb.rotation_mode = "QUATERNION"
    q_rest = pb.bone.matrix.to_quaternion()
    q_arm = Quaternion(axis_arm, angle)
    q_local = q_rest.inverted() @ q_arm @ q_rest
    pb.rotation_quaternion = q_local @ pb.rotation_quaternion


def reset_pose():
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = Quaternion()
    bpy.context.view_layer.update()


sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.render.resolution_x = 960
sc.render.resolution_y = 960
bpy.ops.object.camera_add(location=(0, -3.0, 0.7), rotation=(1.35, 0, 0))
sc.camera = bpy.context.active_object


def render(name):
    sc.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("ISOLATED:", name)


# C1: deep knee bend (thighs fwd +X, knees flex back -X)
reset_pose()
swing("upperleg01.L", X, 1.1)
swing("upperleg01.R", X, 1.1)
swing("lowerleg01.L", X, -1.7)
swing("lowerleg01.R", X, -1.7)
bpy.context.view_layer.update()
render("C1_deep_knee_bend.png")

# C2: elbow 90 (upper arm raise +X, elbow flex +X)
reset_pose()
swing("upperarm01.L", X, 0.5)
swing("lowerarm01.L", X, 1.57)
bpy.context.view_layer.update()
render("C2_elbow_90.png")

# C3: spine twist (Z) + bend fwd (+X)
reset_pose()
swing("spine03", Z, 0.5)
swing("spine02", X, 0.3)
bpy.context.view_layer.update()
render("C3_spine_twist_bend.png")

print("ISOLATED_POSES_DONE")
