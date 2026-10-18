# MPFB2 headless proof — run inside Blender 4.5:
#   blender -b --python mpfb_proof.py
# Creates a MakeHuman, applies semantic body morphs, adds the full default
# rig (163 bones), saves the .blend and renders proof images.
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import bpy

# Headless: MPFB's LocationService calls bpy.utils.extension_path_user() which
# requires a registered extension repo. Mock it to a plain user-data dir.
_MPFB_USER = os.path.expanduser("~/.config/mpfb-user-data")
os.makedirs(_MPFB_USER, exist_ok=True)
bpy.utils.extension_path_user = lambda package, **kwargs: _MPFB_USER

import mpfb
# Headless: MPFB is not a registered addon here, so preferences don't exist.
# Patch before register() — services bind get_preference at import time.
mpfb.get_preference = lambda name: None
mpfb.register()
from mpfb.services.humanservice import HumanService
from mpfb.services.targetservice import TargetService
from mpfb.services.locationservice import LocationService
from mpfb.entities.objectproperties import HumanObjectProperties

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proof")
os.makedirs(OUT, exist_ok=True)

# --- clean scene ---
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# --- 1. neutral human ---
human = HumanService.create_human()
human.name = "MPFB_Neutral"
print("PROOF: created human", human.name, "verts:", len(human.data.vertices))

# --- 2. semantic morphs on a second human (bulk/height/shoulders/belly/limbs) ---
morphed = HumanService.create_human()
morphed.name = "MPFB_Morphed"
morphed.location = (2.2, 0, 0)

# macro: gender (0=male,1=female), weight, height, muscle
HumanObjectProperties.set_value("gender", 0.15, entity_reference=morphed)
HumanObjectProperties.set_value("weight", 0.75, entity_reference=morphed)   # bulk
HumanObjectProperties.set_value("height", 0.60, entity_reference=morphed)
HumanObjectProperties.set_value("muscle", 0.80, entity_reference=morphed)
TargetService.reapply_macro_details(morphed)

targets_root = LocationService.get_mpfb_data("targets")
morph_targets = [
    ("torso", "measure-shoulder-dist-incr.target.gz", 0.8),      # shoulders
    ("stomach", "stomach-tone-incr.target.gz", 0.6),              # belly tone
    ("torso", "measure-waist-circ-incr.target.gz", 0.7),         # belly bulk
    ("arms", "l-upperarm-muscle-incr.target.gz", 0.9),           # limbs
    ("arms", "measure-lowerarm-length-incr.target.gz", 0.5),      # limbs
]
for subdir, fname, weight in morph_targets:
    p = os.path.join(targets_root, subdir, fname)
    if os.path.exists(p):
        TargetService.load_target(morphed, p, weight=weight)
        print("PROOF: applied target", fname, weight)
    else:
        print("PROOF: MISSING target", p)

# --- 3. full default rig (163 bones incl. 5-spine, 3-neck) ---
rig = HumanService.add_builtin_rig(morphed, "default")
nbones = len(rig.data.bones)
print("PROOF: rig bones:", nbones)
assert nbones >= 150, "expected full skeleton, got %d" % nbones

# --- 4. save + render ---
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "mpfb_proof.blend"))

bpy.context.scene.render.engine = "BLENDER_WORKBENCH"
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.film_transparent = False
bpy.ops.object.camera_add(location=(0, -6.5, 1.2), rotation=(1.35, 0, 0))
cam = bpy.context.active_object
bpy.context.scene.camera = cam
bpy.context.scene.render.filepath = os.path.join(OUT, "mpfb_proof.png")
bpy.ops.render.render(write_still=True)
print("PROOF: render written")
print("PROOF_DONE")
