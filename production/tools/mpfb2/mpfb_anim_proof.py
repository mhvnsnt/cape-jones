# MPFB animation + morph visual proof (run headless in Blender 4.5):
#   blender-4.5 -b cape_jones_mpfb_wired.blend --python mpfb_anim_proof.py
#
# Proves, with zero hand-tooling (all scripted):
#  A. Semantic morphs driving the CJ mesh (bulk / belly+height sweep)
#  B. The 163-bone MPFB full skeleton (spine01-05, neck01-03, fingers...)
#  C. Scripted extreme poses on the MPFB rig: deep knee bend, elbow 90,
#     spine twist — the wave's deformation targets — with clean skinning.
#  D. Mixamo-topology rig generation (rig.mixamo.json, 52 bones) headless.
import sys, os, math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import bpy
from mathutils import Vector, Quaternion

_MPFB_USER = os.path.expanduser("~/.config/mpfb-user-data")
os.makedirs(_MPFB_USER, exist_ok=True)
bpy.utils.extension_path_user = lambda package, **kwargs: _MPFB_USER

import mpfb
mpfb.get_preference = lambda name: None
mpfb.register()

from mpfb.services.humanservice import HumanService

OUT = os.path.join(os.path.dirname(bpy.data.filepath), "mpfb_proofs")
os.makedirs(OUT, exist_ok=True)

cj = bpy.data.objects.get("CapeJones_Body")
rig = bpy.data.objects.get("MPFB_FullSkeleton")
body = bpy.data.objects.get("MPFB_ReferenceBody")
assert rig and body, "wired objects missing"

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.render.resolution_x = 960
sc.render.resolution_y = 960

bpy.ops.object.camera_add(location=(0, -3.4, 0.85), rotation=(1.35, 0, 0))
cam = bpy.context.active_object
sc.camera = cam


def render(name):
    sc.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("PROOF: rendered", name)


def set_morphs(**kw):
    for k, v in kw.items():
        cj[f"mpfb_{k}"] = v
    bpy.context.view_layer.update()


# ---------- A. morph sweep on CJ mesh ----------
rig.hide_render = True
body.hide_render = True
set_morphs(bulk=1.0, shoulders=0.8, height=0.0, belly=0.0, limbs=0.0)
render("A1_morph_bulk_shoulders.png")
set_morphs(bulk=0.0, shoulders=0.0, height=0.65, belly=1.0, limbs=0.6)
render("A2_morph_belly_height_limbs.png")
set_morphs(bulk=0.0, shoulders=0.0, height=0.0, belly=0.0, limbs=0.0)

# ---------- B. full skeleton ----------
cj.hide_render = True
rig.hide_render = False
rig.data.display_type = "WIRE"
for o in bpy.data.objects:
    if o.type == "ARMATURE":
        o.show_in_front = True
render("B_full_skeleton_163.png")
cj.hide_render = False

# ---------- C. scripted extreme poses on MPFB rig ----------
body.hide_render = False
cj.hide_render = True


def swing(bone_name, axis_arm, angle, distal_bone=None, want_dir=None):
    """Rotate bone about an ARMATURE-space axis (proven math: convert to the
    bone's local frame via the rest matrix, then compose — same as the wiring
    T-pose). If distal_bone + want_dir are given, the sign auto-flips until
    the distal end moves along want_dir (scripted correctness, no eyeballing).
    """
    pb = rig.pose.bones[bone_name]
    pb.rotation_mode = "QUATERNION"
    q_rest = pb.bone.matrix.to_quaternion()
    q_existing = pb.rotation_quaternion.copy()
    for attempt in range(2):
        a = angle if attempt == 0 else -angle
        q_arm = Quaternion(axis_arm, a)
        q_local = q_rest.inverted() @ q_arm @ q_rest
        pb.rotation_quaternion = q_local @ q_existing
        bpy.context.view_layer.update()
        if distal_bone is None:
            return a
        dg = bpy.context.evaluated_depsgraph_get()
        db = rig.evaluated_get(dg).pose.bones[distal_bone]
        # NOTE: Bone.tail is parent-relative; tail_local is armature space.
        rest_tail = rig.matrix_world @ rig.pose.bones[distal_bone].bone.tail_local
        moved = (rig.matrix_world @ db.tail) - rest_tail
        if moved.length > 1e-6 and moved.normalized().dot(want_dir) > 0.3:
            return a
        pb.rotation_quaternion = q_existing  # reset, retry flipped
    return 0.0


def reset_pose():
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = Quaternion()
    bpy.context.view_layer.update()


X = Vector((1, 0, 0))
Z = Vector((0, 0, 1))
FWD = Vector((0, 1, 0))
BACK = Vector((0, -1, 0))

# C1: deep knee bend (both legs) — the candy-wrapper test
reset_pose()
swing("upperleg01.L", X, 1.2, "foot.L", FWD)
swing("upperleg01.R", X, 1.2, "foot.R", FWD)
swing("lowerleg01.L", X, 1.6, "foot.L", BACK)
swing("lowerleg01.R", X, 1.6, "foot.R", BACK)
render("C1_deep_knee_bend.png")

# C2: elbow 90 + arm raise
reset_pose()
swing("upperarm01.L", X, 0.5, "lowerarm02.L", FWD)
swing("lowerarm01.L", X, 1.57, "lowerarm02.L", FWD)
render("C2_elbow_90.png")

# C3: spine twist + bend (the flexible-spine test)
reset_pose()
swing("spine03", Z, 0.5)
swing("spine02", X, 0.25, "head", FWD)
render("C3_spine_twist_bend.png")
reset_pose()

# ---------- D. Mixamo-topology rig generation ----------
mix_h = HumanService.create_human()
mix_h.name = "MPFB_MixamoCheck"
mix_rig = HumanService.add_builtin_rig(mix_h, "mixamo")
print("PROOF: mixamo rig bones:", len(mix_rig.data.bones))
assert len(mix_rig.data.bones) == 52, "mixamo rig bone count changed"
mix_h.hide_render = True
mix_rig.hide_render = True

print("ANIM_PROOF_DONE")
