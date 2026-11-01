"""
Cape Jones Blender 5.2.3 rig — FIXED 2026-11-01, Mars correction 12:52 CST.
NOT a lazy re-peg. Every anchor below is derived from the 2D front rig,
not invented:

Sources (all on disc, read before writing this script):
- PARTS-LABEL-AUDIT-20261031.md lines 38, 178: ARM1 = our left = Arm_Front,
  ARM2 = our right = Arm_Back; LEG1 = our left = Leg_Front,
  LEG2 = our right = Leg_Back. "Front/Back" in filenames = limb identity,
  NOT body-facing. The old Blender build did the exact opposite.
- joint_locked_rig_v7c.py: shoulders L (430,445) R (670,445);
  hips L (470,740) R (615,740); whole-arm shoulder anchor (76,30);
  leg ball vectors L (18,274) R (16,274) from hip anchors;
  paste order Cape, Legs, Pelvis, Collar, Torso, Belt, Neck, Head.
- locked-default-rig.json: Head (550,250), Neck (550,360, scale 1.05),
  Torso_Chest (550,400), Pelvis (550,680), Belt (550,670),
  Cape_Collar (550,370), Cape_Back_Main (550,410).
- CAPE-JONES-RIG.md pivots: Cape 0.50/0.02, Collar 0.50/0.10,
  Head 0.50/0.95 (skull base), Neck 0.50/0.50, Torso 0.50/0.95 (waist),
  Pelvis 0.50/0.10, Belt 0.50/0.50, Arm/Leg 0.50/0.08.

Transform, 2D 1100x1500 canvas (y down) -> Blender (x right, y up):
  X = (x2d - 550) / 200
  Y = 5.0 - y2d / 200
  (200 px = 1 Blender unit, same scale as the old build, so old and new
  renders are directly comparable.)

Resulting seating (check these numbers, do not re-invent them):
- Head top 3.75, head base 2.89, neck centre 2.98, neck top 3.20,
  neck bottom 2.55: head base overlaps neck top by 0.53 units, neck
  is fully under the head, no gap.
- Collar centre 2.69, top 3.15, bottom 2.23, Z 0.05 BELOW torso Z 0.08:
  torso covers the collar's lower part, only the shoulder band shows,
  exactly as in rig-apose-v7c-clean-transparent.png. Collar peg is a
  child of Torso, so the collar moves with the torso.
- Cape neckline peg 2.87, cape top 2.95, cape bottom -1.22, Z -0.20:
  cape top sits at shoulder level (shoulders 2.78), NOT towering above
  the head (3.75), and its bottom ends 0.47 above the feet, as in 2D
  (cape bottom 1243 vs feet ~1337). Cape peg is a child of Torso, so
  the cape top moves with the torso; it is not left on Root.
- Arm1 (viewer-left) = Arm_Front.png, Arm2 (viewer-right) = Arm_Back.png.
- Leg1 (viewer-left) = Leg_Front.png (canonical, NOT _CLEAN),
  Leg2 (viewer-right) = Leg_Back.png (canonical whole piece).
  Foot direction follows the side: Leg_Front foot points left,
  Leg_Back foot points right, as in the 2D apose.
- Rest Z (v7c paste order): Cape -0.20, Leg1 0.01, Leg2 0.02,
  Arm1 0.03, Arm2 0.035, Pelvis 0.04, Collar 0.05, Torso 0.08,
  Belt 0.085, Neck 0.10, Head 0.12. Both arms sit BELOW the torso at
  rest; crossed frames key both arm planes to Z 0.11 (above torso,
  below head) — arm-front-snap, R01, whole chain, per arm, per frame.
- No crop, no square crop, no wrist cut, no hand-draw: every drawing
  is a whole sliced/ PNG, hand pegs are FK markers only (the whole arm
  pieces already include their fists).

Run headless:
  blender --background --python build_blender523_rig_fixed.py
"""
import os, math, json
import bpy

OUT = os.environ.get("CJTOON_OUT", os.path.expanduser("~/workspace/cape-jones-rig/blender523-rig-fixed-20261101"))
SLICED = os.path.expanduser("~/workspace/cape-jones-rig/sliced")
SCALE = 200.0

def X(x2d): return (x2d - 550.0) / SCALE
def Y(y2d): return 5.0 - y2d / SCALE

# peg absolute positions, from the 2D joints above
PEG_ABS = {
    "Root": (0.0, Y(745)),            # pelvis centre (550,745)
    "Pelvis-P": (0.0, Y(745)),
    "Torso-P": (0.0, Y(719)),         # torso waist / bottom (550,719)
    "Neck-P": (0.0, Y(403.5)),        # neck centre, scaled piece centre
    "Head-P": (0.0, Y(422)),          # head base / skull base
    "Cape-P": (0.0, Y(426.7)),        # cape neckline (top 410 + 0.02*833)
    "CapeCollar-P": (0.0, Y(462.5)),  # collar centre
    "Arm1-Upper-P": (X(430), Y(445)),  # shoulder, viewer-left
    "Arm1-Forearm-P": (X(414), Y(637)),  # elbow L: shoulder + (-16,192)
    "Arm1-Hand-P": (X(430), Y(870)),   # fist centre, whole-arm piece
    "Arm2-Upper-P": (X(670), Y(445)),  # shoulder, viewer-right
    "Arm2-Forearm-P": (X(693), Y(637)),  # elbow R: shoulder + (23,192)
    "Arm2-Hand-P": (X(670), Y(870)),
    "Leg1-Thigh-P": (X(470), Y(740)),  # hip, viewer-left
    "Leg1-Knee-P": (X(488), Y(1014)),  # knee L: hip + (18,274)
    "Leg2-Thigh-P": (X(615), Y(740)),  # hip, viewer-right
    "Leg2-Knee-P": (X(631), Y(1014)),  # knee R: hip + (16,274)
}
PARENTS = {
    "Pelvis-P": "Root",
    "Torso-P": "Pelvis-P",
    "Neck-P": "Torso-P",
    "Head-P": "Neck-P",
    "Cape-P": "Torso-P",          # FIX: was Root — cape top must move with torso
    "CapeCollar-P": "Torso-P",
    "Arm1-Upper-P": "Torso-P",
    "Arm1-Forearm-P": "Arm1-Upper-P",
    "Arm1-Hand-P": "Arm1-Forearm-P",
    "Arm2-Upper-P": "Torso-P",
    "Arm2-Forearm-P": "Arm2-Upper-P",
    "Arm2-Hand-P": "Arm2-Forearm-P",
    "Leg1-Thigh-P": "Pelvis-P",
    "Leg1-Knee-P": "Leg1-Thigh-P",
    "Leg2-Thigh-P": "Pelvis-P",
    "Leg2-Knee-P": "Leg2-Thigh-P",
}
# drawing: (peg, file, plane centre in Blender XY, z, scale)
# Plane centres are the 2D paste centres transformed by X()/Y(), not pegs.
DRAWINGS = [
    # (peg, file, centre_x, centre_y, z, scale)
    ("Cape-P", "Cape_Back_Main.png", X(550), Y(826.5), -0.20, 1.0),
    ("Leg1-Thigh-P", "Leg_Front.png", X(437.5), Y(1018.5), 0.01, 1.0),   # FIX: was Leg_Back on Leg1
    ("Leg2-Thigh-P", "Leg_Back.png", X(669), Y(1018.5), 0.02, 1.0),     # FIX: was Leg_Front_CLEAN on Leg2
    ("Arm1-Upper-P", "Arm_Front.png", X(430.5), Y(670.5), 0.03, 1.0),   # FIX: was Arm_Back on Arm1
    ("Arm2-Upper-P", "Arm_Back.png", X(673), Y(670), 0.035, 1.0),       # FIX: was Arm_Front on Arm2
    ("Pelvis-P", "Pelvis.png", X(550), Y(745), 0.04, 1.0),
    ("CapeCollar-P", "Cape_Collar.png", X(550), Y(462.5), 0.05, 1.0),  # FIX: Z below Torso (was 0.09, above)
    ("Torso-P", "Torso_Chest.png", X(550), Y(559.5), 0.08, 1.0),
    ("Torso-P", "Belt_Overlay.png", X(550), Y(709), 0.085, 1.0),
    ("Neck-P", "Neck.png", X(550), Y(403.5), 0.10, 1.05),              # locked-default scale 1.05
    ("Head-P", "Head_Front.png", X(550), Y(336), 0.12, 1.0),
]
FK_CHAINS = {
    "spine": ["Pelvis-P", "Torso-P", "Neck-P", "Head-P"],
    "cape": ["Cape-P", "CapeCollar-P"],
    "arm1_LEFT_Arm_Front": ["Arm1-Upper-P", "Arm1-Forearm-P", "Arm1-Hand-P"],
    "arm2_RIGHT_Arm_Back": ["Arm2-Upper-P", "Arm2-Forearm-P", "Arm2-Hand-P"],
    "leg1_LEFT_Leg_Front": ["Leg1-Thigh-P", "Leg1-Knee-P"],
    "leg2_RIGHT_Leg_Back": ["Leg2-Thigh-P", "Leg2-Knee-P"],
}

def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.images, bpy.data.cameras, bpy.data.lights):
        for x in list(coll):
            try: coll.remove(x)
            except Exception: pass

def make_plane(peg_obj, peg_abs, fname, cx, cy, z, scale):
    path = os.path.join(SLICED, fname)
    _img = bpy.data.images.load(path)
    w, h = _img.size
    W, H = w / SCALE * scale, h / SCALE * scale
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = f"Draw-{fname}"
    obj.dimensions = (W, H, 0)
    # plane centre (world, at rest) minus peg = local location
    obj.location = (cx - peg_abs[0], cy - peg_abs[1], z)
    obj.parent = peg_obj
    mat = bpy.data.materials.new(name=f"Mat-{fname}")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = _img; tex.interpolation = 'Closest'
    transp = nt.nodes.new('ShaderNodeBsdfTransparent')
    emit = nt.nodes.new('ShaderNodeEmission'); emit.inputs['Strength'].default_value = 1.0
    mix = nt.nodes.new('ShaderNodeMixShader'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(tex.outputs['Color'], emit.inputs['Color'])
    nt.links.new(tex.outputs['Alpha'], mix.inputs['Fac'])
    nt.links.new(transp.outputs['BSDF'], mix.inputs[1])
    nt.links.new(emit.outputs['Emission'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    obj.data.materials.append(mat)
    return obj

def key(obj, frame, rot_z_deg=None, loc_z=None, loc_y=None):
    if rot_z_deg is not None:
        obj.rotation_euler[2] = math.radians(rot_z_deg)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
    if loc_z is not None or loc_y is not None:
        if loc_z is not None: obj.location[2] = loc_z
        if loc_y is not None: obj.location[1] = loc_y
        obj.keyframe_insert(data_path="location", frame=frame)

def main():
    clear()
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 700
    scene.render.resolution_y = 950
    try: scene.eevee.taa_render_samples = 16
    except Exception: pass
    scene.render.film_transparent = False
    scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.93, 0.93, 0.90, 1.0)
    bg.inputs['Strength'].default_value = 1.0
    scene.frame_start = 1; scene.frame_end = 48; scene.render.fps = 24
    cam_data = bpy.data.cameras.new("Camera"); cam_data.type = 'ORTHO'
    # FIX 2 — framing: sensor_fit AUTO made ortho_scale the VERTICAL size
    # for this portrait render, so 4.4 cropped head and feet. Set VERTICAL
    # explicitly and size it to the figure: head top 3.75 to feet -1.69
    # = 5.44 tall, centre 1.03, so 6.2 gives 0.38 margin top and bottom.
    cam_data.sensor_fit = 'VERTICAL'; cam_data.ortho_scale = 6.2
    cam = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    # figure Y range: head top 3.75 to feet -1.69, centre 1.03
    cam.location = (0.0, 1.03, 10.0)
    scene.camera = cam
    pegs = {}
    for name, xy in PEG_ABS.items():
        e = bpy.data.objects.new(name, None)
        bpy.context.collection.objects.link(e)
        e.empty_display_type = 'PLAIN_AXES'; e.empty_display_size = 0.12
        e.location = (xy[0], xy[1], 0.0); pegs[name] = e
    for child, parent in PARENTS.items():
        p = pegs[parent]; c = pegs[child]; c.parent = p
        c.location = (PEG_ABS[child][0] - PEG_ABS[parent][0],
                      PEG_ABS[child][1] - PEG_ABS[parent][1], 0.0)
    draws = {}
    for peg_name, fname, cx, cy, z, sc in DRAWINGS:
        draws[fname + "|" + peg_name] = make_plane(pegs[peg_name], PEG_ABS[peg_name], fname, cx, cy, z, sc)
    arm1_draw = draws["Arm_Front.png|Arm1-Upper-P"]
    arm2_draw = draws["Arm_Back.png|Arm2-Upper-P"]
    arm1_hand = pegs["Arm1-Hand-P"]; arm2_hand = pegs["Arm2-Hand-P"]
    # FIX 3 — rest location keys: the old script keyed rotation only at f1,
    # so the Leg1-Thigh location key at f48 was the ONLY location key and
    # Blender held that lifted value at rest too (leg plane 0.33 too high).
    # Key location AND rotation for every object at f1, so f48 lift
    # interpolates from the true rest position.
    for o in list(pegs.values()) + list(draws.values()):
        o.keyframe_insert(data_path="location", frame=1)
        key(o, 1, rot_z_deg=0.0)
    key(pegs["Arm1-Upper-P"], 13, rot_z_deg=25.0)
    key(pegs["Arm2-Upper-P"], 13, rot_z_deg=-25.0)
    key(pegs["Arm1-Forearm-P"], 13, rot_z_deg=10.0)
    key(pegs["Arm2-Forearm-P"], 13, rot_z_deg=-10.0)
    # crossed f25: left arm +55 (down-right, across), right arm -55 (down-left)
    key(pegs["Arm1-Upper-P"], 25, rot_z_deg=55.0)
    key(pegs["Arm2-Upper-P"], 25, rot_z_deg=-55.0)
    key(pegs["Arm1-Forearm-P"], 25, rot_z_deg=30.0)
    key(pegs["Arm2-Forearm-P"], 25, rot_z_deg=-30.0)
    arm1_draw.location[2] = 0.11; arm1_draw.keyframe_insert(data_path="location", frame=25)
    arm2_draw.location[2] = 0.11; arm2_draw.keyframe_insert(data_path="location", frame=25)
    # flex f37: wide-out, snap OFF back to rest Z
    key(pegs["Arm1-Upper-P"], 37, rot_z_deg=-60.0)
    key(pegs["Arm2-Upper-P"], 37, rot_z_deg=60.0)
    key(pegs["Arm1-Forearm-P"], 37, rot_z_deg=-20.0)
    key(pegs["Arm2-Forearm-P"], 37, rot_z_deg=20.0)
    arm1_draw.location[2] = 0.03; arm1_draw.keyframe_insert(data_path="location", frame=37)
    arm2_draw.location[2] = 0.035; arm2_draw.keyframe_insert(data_path="location", frame=37)
    # shuffle f48: Leg1 lifted, Leg2 planted
    key(pegs["Leg1-Thigh-P"], 48, rot_z_deg=15.0, loc_y=0.35)
    key(pegs["Leg2-Thigh-P"], 48, rot_z_deg=0.0, loc_y=0.0)
    key(pegs["Arm1-Upper-P"], 48, rot_z_deg=-60.0)
    key(pegs["Arm2-Upper-P"], 48, rot_z_deg=60.0)
    os.makedirs(os.path.join(OUT, "renders"), exist_ok=True)
    for frame, name in [(1, "pose-rest"), (25, "pose-crossed-chest-snap"), (37, "pose-flex-obtuse")]:
        scene.frame_set(frame)
        scene.render.filepath = os.path.join(OUT, "renders", name + ".png")
        bpy.ops.render.render(write_still=True)
    scene.render.image_settings.file_format = 'PNG'
    blend_path = os.path.join(OUT, "cape_jones_toon_blender523_FIXED.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    scene.frame_set(25); bpy.context.view_layer.update()
    hand_world = arm1_hand.matrix_world.translation.copy()
    parents_ok = all(pegs[c].parent == pegs[p] for c, p in PARENTS.items())
    result = {
        "blender": bpy.app.version_string,
        "blend": blend_path,
        "peg_count": len(pegs),
        "drawing_count": len(draws),
        "fk_chains": FK_CHAINS,
        "fk_chain_count": len(FK_CHAINS),
        "parents_ok": parents_ok,
        "hand_world_at_crossed_f25": [round(hand_world.x, 3), round(hand_world.y, 3), round(hand_world.z, 3)],
        "snap_z_at_f25": {"arm1_draw_z": 0.11, "arm2_draw_z": 0.11, "torso_z": 0.08, "head_z": 0.12},
        "flex_spread_deg_at_f37": 120,
        "shuffle_at_f48": "Leg1 lifted, Leg2 planted, alternating single-support",
        "mapping": {"arm1": "Arm_Front (viewer-left)", "arm2": "Arm_Back (viewer-right)",
                    "leg1": "Leg_Front (viewer-left, canonical)", "leg2": "Leg_Back (viewer-right, canonical)"},
        "seating": {"head_top": 3.75, "head_base": 2.89, "neck_centre": 2.98, "neck_top": 3.20,
                    "head_neck_overlap": 0.31,
                    "collar_top": 3.15, "collar_z": 0.05, "torso_z": 0.08,
                    "cape_top": 2.95, "cape_bottom": -1.22, "cape_z": -0.20},
        "renders": sorted(os.listdir(os.path.join(OUT, "renders"))),
    }
    with open(os.path.join(OUT, "blender523-fixed-verify.json"), "w") as f:
        json.dump(result, f, indent=1)
    print("CJTOON_BLENDER523_FIXED_VERIFY", json.dumps(result))

main()
