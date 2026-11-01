"""Build a CapeGP .blend from a frames JSON, for one preset only.

Adapted from capegp-presets-20261031/build_capegp.py (same 10 layers,
same colours, same radius 0.035, same ortho camera 16, 550x750,
film_transparent=True). Difference: frames file and preset name are
arguments, so ANY CapeGP pose frame can be built as a single-preset blend
with no holdover from other frames (see the CapeGP README: a multi-frame
GP object holds a layer's previous frame when that layer has no keyframe
at the new frame, so proof renders must come from single-preset blends).

Usage inside Blender 5.2.3:
  blender -b --python blender_build.py -- --frames FRAMES.json --preset NAME OUT.blend
"""
import bpy, json, os, sys, argparse
LAYERS = ["FaceSnapArm", "Head", "CowlUpperArm", "Neck", "ChestSnapArm",
          "Torso", "Collar", "NormalArm", "Legs", "CapeBack"]
COLOURS = {"FaceSnapArm": (1, 0.4, 0.2, 1), "Head": (0.55, 0.2, 0.7, 1),
           "CowlUpperArm": (1, 0.8, 0.2, 1), "Neck": (0.95, 0.7, 0.5, 1),
           "ChestSnapArm": (0.2, 0.8, 1, 1), "Torso": (0.9, 0.9, 0.95, 1),
           "Collar": (0.1, 0.1, 0.15, 1), "NormalArm": (0.85, 0.85, 0.9, 1),
           "Legs": (0.8, 0.85, 0.95, 1), "CapeBack": (0.15, 0.12, 0.2, 1)}

def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", required=True)
    ap.add_argument("--preset", required=True)
    ap.add_argument("out")
    args = ap.parse_args(argv)
    with open(args.frames) as f:
        FRAMES = json.load(f)
    frame = FRAMES[args.preset]
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
    for name in LAYERS:
        polys = frame.get(name, [])
        if not polys:
            continue
        fr = layer_objs[name].frames.new(1)
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
    sc.frame_start = 1; sc.frame_end = 1
    bpy.ops.wm.save_as_mainfile(filepath=args.out)
    print("COLORED INVISIBLE BLEND DONE", args.out, args.preset,
          {k: len(v) for k, v in frame.items() if v})

main()
