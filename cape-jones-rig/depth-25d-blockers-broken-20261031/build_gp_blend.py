"""Build the Cape Jones Grease Pencil rig (.blend) from gp_frames.json.
EXPERIMENTAL GP rig, Blender 5.2.3. Layer order (front to back, as in the
wire-100 mapping): FaceSnapArm, Head, CowlUpperArm, Neck, ChestSnapArm,
Torso, Collar, NormalArm, Legs, CapeBack. Each stroke is the traced outline
of an existing v7c source piece, placed by the v7c joint math — no new art.
Strokes are outlines only; fills are NOT in this pass (stated limit).
Run inside Blender: blender -b --python build_gp_blend.py
"""
import bpy, json, os
OUT = "/home/hatch/workspace/cape-jones-rig/depth-25d-blockers-broken-20261031"
LAYERS = ["FaceSnapArm", "Head", "CowlUpperArm", "Neck", "ChestSnapArm",
          "Torso", "Collar", "NormalArm", "Legs", "CapeBack"]
COLOURS = {"FaceSnapArm": (1, 0.4, 0.2, 1), "Head": (0.55, 0.2, 0.7, 1),
           "CowlUpperArm": (1, 0.8, 0.2, 1), "Neck": (0.95, 0.7, 0.5, 1),
           "ChestSnapArm": (0.2, 0.8, 1, 1), "Torso": (0.9, 0.9, 0.95, 1),
           "Collar": (0.1, 0.1, 0.15, 1), "NormalArm": (0.85, 0.85, 0.9, 1),
           "Legs": (0.8, 0.85, 0.95, 1), "CapeBack": (0.15, 0.12, 0.2, 1)}
with open(os.path.join(OUT, "gp_frames.json")) as f:
    FRAMES = json.load(f)

bpy.ops.wm.read_factory_settings(use_empty=True)
gp = bpy.data.grease_pencils.new("CapeGP")
obj = bpy.data.objects.new("CapeGP", gp)
bpy.context.collection.objects.link(obj)
for i, name in enumerate(LAYERS):
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
for frame_no in sorted(FRAMES, key=int):
    fn = int(frame_no)
    for name in LAYERS:
        polys = FRAMES[frame_no].get(name, [])
        if not polys:
            continue
        layer = layer_objs[name]
        fr = layer.frames.new(fn)
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
sc.render.film_transparent = False
sc.world = bpy.data.worlds.new("GPWorld"); sc.world.use_nodes = True
sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
bpy.ops.object.camera_add(location=(0, 0, 10))
cam = bpy.context.active_object; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 16
sc.camera = cam
sc.frame_start = 1; sc.frame_end = 4
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "cape-gp-rig-experimental-20261031.blend"))
sc.render.filepath = os.path.join(OUT, "gp-motion-")
bpy.ops.render.render(animation=True)
sc.frame_set(10)
sc.render.filepath = os.path.join(OUT, "gp-jojo03-face-snap-experimental-20261031.png")
bpy.ops.render.render(write_still=True)
print("GP BLEND DONE")
