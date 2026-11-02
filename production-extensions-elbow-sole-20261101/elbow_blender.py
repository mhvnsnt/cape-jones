#!/usr/bin/env python3
"""STRICT ISOLATED 90-DEGREE ELBOW PASS, BLENDER (2026-11-01).
Run: blender --background --python elbow_blender.py
Fresh scene, built from scratch: NO source blend, NO snap-early motion,
NO torso/head/other limb, NO fcurves except the single elbow rotation
set directly per render (not played back). One arm only per render:
shoulder empty -> upper plane; elbow empty -> lower plane
(forearm+gauntlet+fist whole; wrist never cut) + cap disc above both.
Geometry mirrors the PIL pass and the cutlimbs builder at the same
0.005 units/px scale:
  Front: upper anchor (76,30), ball (60,222); lower ball (60,15).
  Back:  upper anchor (76,30), ball (99,222); lower ball (99,15).
  Elbow world = shoulder + (ball-anchor)*0.005, y flipped (image y
  down -> Blender y up). Lower plane centre = -lower-ball local.
Camera: ortho, 800x1000, ortho_scale 3.0, centred on the arm.
Elbow pixel per render is computed inside Blender with
world_to_camera_view (no hand projection formula) and saved to JSON;
measure_blender.py then scores disc coverage / gap on the renders
with the same definition as the PIL pass (longest transparent run
inside r30, gray-distance >25 from world background).
Cap on/off variants are both rendered so the cap cannot hide a gap.
"""
import bpy, os, json, math
from bpy_extras.object_utils import world_to_camera_view

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
CUT = os.path.join(ROOT, "cut-limbs-v7c")
OUT = "/var/tmp/elbow-sole-20261101/elbow_blender"
os.makedirs(OUT, exist_ok=True)
BL = os.path.join(os.path.expanduser("~/workspace/tools-industry"),
                  "blender-5.2.3-linux-x64/blender")

# --- fresh scene ---
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples = 4
except Exception:
    pass
scene.render.resolution_x = 800
scene.render.resolution_y = 1000
scene.world = bpy.data.worlds.new("WorldGray")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (237 / 255, 237 / 255, 230 / 255, 1.0)
bg.inputs[1].default_value = 1.0

SCALE = 0.005
ARMS = {
    "Front": {"upper": "Arm_Front_Upper.png", "lower": "Arm_Front_Lower.png",
              "cap": "Arm_Front_Cap.png", "ball": (60, 222), "anchor": (76, 30),
              "lower_ball": (60, 15), "lower_size": (153, 289)},
    "Back": {"upper": "Arm_Back_Upper.png", "lower": "Arm_Back_Lower.png",
             "cap": "Arm_Back_Cap.png", "ball": (99, 222), "anchor": (76, 30),
             "lower_ball": (99, 15), "lower_size": (158, 288)},
}
UPPER_SIZE = {"Front": (153, 320), "Back": (158, 320)}

def make_plane(parent, fname, dims, loc, z):
    img = bpy.data.images.load(os.path.join(CUT, fname))
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = "Iso-" + fname
    obj.dimensions = (dims[0], dims[1], 0)
    obj.location = (loc[0], loc[1], z)
    if parent is not None:
        obj.parent = parent
    mat = bpy.data.materials.new(name="Mat-" + fname)
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    nt = mat.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.image = img
    tex.interpolation = 'Closest'
    transp = nt.nodes.new('ShaderNodeBsdfTransparent')
    emit = nt.nodes.new('ShaderNodeEmission')
    emit.inputs['Strength'].default_value = 1.0
    mix = nt.nodes.new('ShaderNodeMixShader')
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(tex.outputs['Color'], emit.inputs['Color'])
    nt.links.new(tex.outputs['Alpha'], mix.inputs['Fac'])
    nt.links.new(transp.outputs['BSDF'], mix.inputs[1])
    nt.links.new(emit.outputs['Emission'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    obj.data.materials.append(mat)
    return obj

def local(px, py, Wpx, Hpx):
    """PNG point (px from top-left, y down) -> plane local (y up)."""
    return ((px - Wpx / 2) * SCALE, (Hpx / 2 - py) * SCALE)

results = {}
for arm, cfg in ARMS.items():
    # wipe previous arm objects (keep camera/world between arms is fine,
    # but rebuild empties/planes per arm for strict isolation)
    for o in list(bpy.data.objects):
        if o.type != 'CAMERA':
            bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.object.empty_add(location=(0, 0, 0))
    shoulder = bpy.context.active_object
    shoulder.name = "Shoulder-P"
    ball, anchor = cfg["ball"], cfg["anchor"]
    vec = ((ball[0] - anchor[0]) * SCALE, -(ball[1] - anchor[1]) * SCALE)
    bpy.ops.object.empty_add(location=(vec[0], vec[1], 0))
    elbow = bpy.context.active_object
    elbow.name = "Elbow-P"
    elbow.parent = shoulder
    UW, UH = UPPER_SIZE[arm]
    ax, ay = local(anchor[0], anchor[1], UW, UH)
    upper = make_plane(shoulder, cfg["upper"], (UW * SCALE, UH * SCALE),
                       (-ax, -ay), 0.030)
    LW, LH = cfg["lower_size"]
    bx, by = local(cfg["lower_ball"][0], cfg["lower_ball"][1], LW, LH)
    lower = make_plane(elbow, cfg["lower"], (LW * SCALE, LH * SCALE),
                       (-bx, -by), 0.032)
    cap = make_plane(elbow, cfg["cap"], (0.33, 0.33), (0, 0), 0.036)
    # camera: centre on arm mid (x ~ vec.x, y ~ -1.15)
    cam_data = bpy.data.cameras.new("CamIso")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 3.0
    cam = bpy.data.objects.new("CameraIso", cam_data)
    scene.collection.objects.link(cam)
    cam.location = (vec[0], -1.15, 5.0)
    cam.rotation_euler = (0, 0, 0)
    scene.camera = cam
    for angle in (0, 45, 90):
        for with_cap in (True, False):
            elbow.rotation_euler[2] = math.radians(angle)
            cap.hide_render = not with_cap
            scene.frame_set(1)
            tag = f"elbow_{arm}_{angle:02d}_{'cap' if with_cap else 'nocap'}"
            scene.render.filepath = os.path.join(OUT, tag + ".png")
            bpy.ops.render.render(write_still=True)
            bpy.context.view_layer.update()
            co = world_to_camera_view(scene, cam, elbow.matrix_world.translation)
            px = (co.x * scene.render.resolution_x,
                  (1 - co.y) * scene.render.resolution_y)
            results[tag] = {"arm": arm, "angle": angle, "with_cap": with_cap,
                            "elbow_world": [round(vec[0], 4), round(vec[1], 4)],
                            "elbow_px": [round(px[0], 1), round(px[1], 1)]}
            print("BLENDER_RENDERED", tag, "elbow_px", results[tag]["elbow_px"],
                  flush=True)
    # keep one blend per arm (isolated scene, elbow at 90 for inspection)
    elbow.rotation_euler[2] = math.radians(90)
    cap.hide_render = False
    bpy.ops.wm.save_mainfile(filepath=os.path.join(OUT, f"elbow_isolated_{arm}.blend"))
json.dump(results, open(os.path.join(OUT, "elbow_blender_joints.json"), "w"), indent=1)
print("BLENDER DONE", len(results))
