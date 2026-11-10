"""Lane 3: wide shot to confirm hand positions + framing. Cycles CPU."""
import bpy, sys
from mathutils import Vector, Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
bpy.context.view_layer.update()

MODE = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else "wide"

# hide cape for clarity
cape = bpy.data.objects.get("CapeJones_Cape")
if cape:
    cape.hide_render = True

# flat materials: nuke to plain emission white/gray
for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nt = mat.node_tree
    out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if out is None:
        continue
    for link in list(nt.links):
        if link.to_node == out:
            nt.links.remove(link)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = 1.0
    em.inputs["Color"].default_value = (0.85, 0.85, 0.88, 1.0)
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])

w = bpy.data.worlds.new("WhiteVoid")
w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (1, 1, 1, 1)
bg.inputs["Strength"].default_value = 1.0
sc.world = w
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 4
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.render.resolution_x = 960
sc.render.resolution_y = 960
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGB"

cam = bpy.data.objects.new("widecam", bpy.data.cameras.new("widecam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.clip_start = 0.01
cam.data.clip_end = 20.0

def look_at(eye, target, up):
    z = (eye - target).normalized()
    x = up.cross(z).normalized()
    y = z.cross(x)
    M = Matrix.Identity(4)
    M[0][0], M[1][0], M[2][0] = x[0], x[1], x[2]
    M[0][1], M[1][1], M[2][1] = y[0], y[1], y[2]
    M[0][2], M[1][2], M[2][2] = z[0], z[1], z[2]
    M[0][3], M[1][3], M[2][3] = eye[0], eye[1], eye[2]
    return M

UP = Vector((0, 0, 1))
eye = Vector((0.0, -2.3, 0.75))
target = Vector((0.0, 0.0, 0.55))
cam.matrix_world = look_at(eye, target, UP)
cam.data.type = "PERSP"
cam.data.lens = 50
bpy.context.view_layer.update()
sc.render.filepath = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/wide_idle.png"
bpy.ops.render.render(write_still=True)
print("RENDERED wide", flush=True)
