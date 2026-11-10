#!/usr/bin/env python3
"""
Integration-lane proof renders. NEVER saves the blend.

    blender -b 3d-assets/living_room.blend --python 3d-assets/living-room/proof_shots.py \
        -- <shot> <out.png> [samples]

Shots: hero | pov | open | red | godray
- hero/pov/open: preset 0 (canon violet), TV ON, frame 48 (title card)
- red: preset 1 (RED gag), TV ON
- godray: vol_density 0.03, volume_bounces 0, WindowShaft view
- open: the linked Recliner collection is unlinked from the scene and APPENDED
  (editable copy); bones are posed directly to recline=1 angles because
  Blender 4.0 headless does not propagate scripted drivers into renders
  (verified by the TV lane). BVH body-vs-open-recliner is reported.

tv_setup.py is re-run first (MANDATORY: the frame-change handler does not
persist in .blend files).
"""

import bpy
import math
import os
import runpy
import sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
SHOT = argv[0]
OUT = argv[1]
SAMPLES = int(argv[2]) if len(argv) > 2 else 64

BLEND = bpy.data.filepath
ASSETS = os.path.dirname(os.path.abspath(BLEND))
LR = os.path.join(ASSETS, "living-room")
sc = bpy.context.scene
vl = bpy.context.view_layer

# ---- mandatory fresh-session TV setup
old_argv = sys.argv
sys.argv = ["blender", "--"]
runpy.run_path(os.path.join(LR, "tv", "tv_setup.py"), run_name="__main__")
sys.argv = old_argv
tv = bpy.data.objects["crt_tv"]
tv["tv_power"] = 1.0
tv.update_tag()          # ID-prop write must tag the depsgraph (driver staleness)
# the committed blend sits at frame 1 (recliner closed default); the TV sequence
# is offset so frame 1 shows the title card (tv_setup rebuilds the node tree,
# so re-apply the integration lane's frame_offset here)
mat0 = bpy.data.materials["tvScreenMat"]
tex0 = next(n for n in mat0.node_tree.nodes if n.type == "TEX_IMAGE")
tex0.image_user.frame_offset = 47
sc.frame_set(1)          # recline=0 (closed); TV title card; handler applies power ON
vl.update()

# ---- lighting state per shot
rig = bpy.data.objects.get("LED_RemoteRig")
assert rig is not None, "LED_RemoteRig missing — integration did not run"
if SHOT == "red":
    sys.argv = ["blender", "--", "1"]
    runpy.run_path(os.path.join(LR, "lighting", "set_led_preset.py"),
                   run_name="__main__")
    sys.argv = old_argv
    print("proof: LED preset 1 (RED)")
else:
    sys.argv = ["blender", "--", "0"]
    runpy.run_path(os.path.join(LR, "lighting", "set_led_preset.py"),
                   run_name="__main__")
    sys.argv = old_argv

vol_density = 0.015
if SHOT == "godray":
    vol_density = 0.03
    vmat = bpy.data.materials.get("VolumeMat_Room")
    if vmat:
        vmat.node_tree.nodes["Principled Volume"].inputs["Density"].default_value = vol_density
    print(f"proof: vol_density={vol_density} (direct write, deterministic)")

# ---- open state: editable appended copy of the recliner
if SHOT == "open":
    rec = bpy.data.collections.get("Recliner")
    if rec and rec.name in [c.name for c in sc.collection.children]:
        sc.collection.children.unlink(rec)   # linked original out of the scene
        print("proof: unlinked the linked Recliner collection")
    with bpy.data.libraries.load(os.path.join(LR, "recliner", "recliner_rigged.blend"),
                                 link=False) as (df, dt):
        dt.collections = ["Recliner"]
    rec2 = bpy.data.collections["Recliner"]
    sc.collection.children.link(rec2)
    arm = next(o for o in rec2.objects if o.type == "ARMATURE")
    OPEN = {"backrest": -0.454, "footrest": -0.873, "footrest_pad": 0.873}
    for bn, ang in OPEN.items():
        pb = arm.pose.bones[bn]
        pb.rotation_euler = (0.0, ang, 0.0)   # stored values render; drivers don't propagate headless
    vl.update()
    # BVH: seated body vs OPEN recliner
    from mathutils.bvhtree import BVHTree
    deps = bpy.context.evaluated_depsgraph_get()
    body = bpy.data.objects["CapeJones_Body"]
    bt = BVHTree.FromObject(body.evaluated_get(deps), deps)
    ov = 0
    for o in rec2.objects:
        if o.type == "MESH":
            ct = BVHTree.FromObject(o.evaluated_get(deps), deps)
            ov += len(ct.overlap(bt))
    print(f"proof: BVH body-vs-OPEN-recliner overlap = {ov} face pairs")
    del bt
    import gc; gc.collect()

# ---- render setup (canon: Cycles CPU, 960x540; OIDN denoise)
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.volume_bounces = 0
sc.render.resolution_x, sc.render.resolution_y = 960, 540
sc.render.film_transparent = False

def aim_cam(pos, target, lens=40.0, name="proof_cam"):
    cd = bpy.data.cameras.new(name)
    co = bpy.data.objects.new(name, cd)
    sc.collection.objects.link(co)
    co.location = Vector(pos)
    d = Vector(target) - Vector(pos)
    co.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cd.lens = lens
    sc.camera = co
    vl.update()
    return co

SCREEN_T = bpy.data.objects["crt_screen"].matrix_world.translation
SCREEN = (SCREEN_T.x, SCREEN_T.y, SCREEN_T.z)   # yawed screen center, measured live
HEAD = (3.10, 2.067, 1.15)         # seated head approx

if SHOT == "hero":
    # on the perpendicular bisector of sitter<->screen (sofa side), wide lens:
    # him front-left 3/4 + TV screen readable
    aim_cam((1.20, -2.34, 1.60), (1.20, 2.25, 0.90), 28.0)
elif SHOT == "pov":
    # from just in front of his eyes toward the screen (sight-line proof)
    aim_cam((2.92, 2.067, 1.20), SCREEN, 32.0)
elif SHOT == "open":
    aim_cam((1.35, 0.95, 1.30), (2.85, 2.10, 0.45), 40.0)
elif SHOT == "red":
    aim_cam((1.20, -2.34, 1.60), (1.20, 2.25, 0.90), 28.0)
elif SHOT == "godray":
    # from the beam's far end looking back toward the window ALONG the shaft:
    # forward-scatter (anisotropy 0.7) makes the beam read brightest this way
    aim_cam((-0.80, 0.00, 0.50), (3.20, 1.50, 1.90), 32.0)
else:
    raise SystemExit(f"unknown shot {SHOT}")

sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("proof render written:", OUT)
