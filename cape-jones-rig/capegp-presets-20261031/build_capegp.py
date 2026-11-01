"""Build a CapeGP .blend from capegp_presets_frames.json (or a single preset).

CapeGP — Cape Jones Grease Pencil Layer Rig. One object, 10 layers
front-to-back: FaceSnapArm, Head, CowlUpperArm, Neck, ChestSnapArm, Torso,
Collar, NormalArm, Legs, CapeBack. One colour-coded material per layer.
Strokes are traced outlines only, no fills yet.
PIL/v7c remains DEFAULT for approved clean plates; CapeGP is for
layer-order proofs, Blender motion tests, and layer-tree deliverables.

Usage inside Blender 5.2.3:
  blender -b --python build_capegp.py -- --all capegp_all_presets.blend
  blender -b --python build_capegp.py -- --preset FACE_SNAP capegp_face_snap.blend
Rendered with Eevee under xvfb-run (bare headless aborts on missing libEGL),
film_transparent=True so the figure background is transparent, ortho camera
scale 16, 550x750 (same framing as the original GP rig: figure x -5.5..5.5,
y -7.5..7.5 in Blender units, so no crop window clips the figure).
API note (Blender 5.2): gpencil_add does NOT exist; use
bpy.data.grease_pencils.new() + drawing.add_strokes().
"""
import bpy, json, os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
LAYERS = ["FaceSnapArm", "Head", "CowlUpperArm", "Neck", "ChestSnapArm",
          "Torso", "Collar", "NormalArm", "Legs", "CapeBack"]
COLOURS = {"FaceSnapArm": (1, 0.4, 0.2, 1), "Head": (0.55, 0.2, 0.7, 1),
           "CowlUpperArm": (1, 0.8, 0.2, 1), "Neck": (0.95, 0.7, 0.5, 1),
           "ChestSnapArm": (0.2, 0.8, 1, 1), "Torso": (0.9, 0.9, 0.95, 1),
           "Collar": (0.1, 0.1, 0.15, 1), "NormalArm": (0.85, 0.85, 0.9, 1),
           "Legs": (0.8, 0.85, 0.95, 1), "CapeBack": (0.15, 0.12, 0.2, 1)}
ORDER = ["NORMAL", "APOSE_FLEX", "FACE_SNAP", "COWL_SNAP", "CHEST_SNAP", "JOINT_SMOOTH"]

def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("out")
    args = ap.parse_args(argv)
    with open(os.path.join(HERE, "capegp_presets_frames.json")) as f:
        FRAMES = json.load(f)
    names = ORDER if args.all else [args.preset]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    gp = bpy.data.grease_pencils.new("CapeGP")
    obj = bpy.data.objects.new("CapeGP", gp)
    bpy.context.collection.objects.link(obj)
    for name in LAYERS:
        mat = bpy.data.materials.new("GP_" + name)
        bpy.data.materials.create_gpencil_data(mat)
        mat.grease_pencil.color = COLOURS[name]
        mat.grease_pencil.stroke_style = 'SOLID'
        gp.materials.append(mat)
    layer_objs = {}
    for name in LAYERS:
        layer = gp.layers.new(name)
        layer.use_lights = False
        layer_objs[name] = layer
    for i, pname in enumerate(names):
        fn = i + 1
        for name in LAYERS:
            polys = FRAMES[pname].get(name, [])
            if not polys:
                continue
            fr = layer_objs[name].frames.new(fn)
            d = fr.drawing
            d.add_strokes([len(p) for p in polys])
            for si, poly in enumerate(polys):
                st = d.strokes[si]
                st.material_index = LAYERS.index(name)
                st.cyclic = True
                for pi, (x, y) in enumerate(poly):
                    pt = st.points[pi]
                    pt.position = (x, y, 0)
                    pt.radius = 0.035
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE'
    sc.render.resolution_x = 550; sc.render.resolution_y = 750
    sc.render.film_transparent = True
    bpy.ops.object.camera_add(location=(0, 0, 10))
    cam = bpy.context.active_object; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 16
    sc.camera = cam
    sc.frame_start = 1; sc.frame_end = len(names)
    outpath = args.out if os.path.isabs(args.out) else os.path.join(HERE, args.out)
    bpy.ops.wm.save_as_mainfile(filepath=outpath)
    print("CAPEGP BLEND DONE", outpath, names)

main()
