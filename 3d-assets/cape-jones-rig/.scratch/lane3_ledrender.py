"""Lane 3: render LED press key frames."""
import bpy, sys, numpy as np
from mathutils import Vector, Matrix

FRAMES = [int(x) for x in sys.argv[sys.argv.index('--') + 1:]]
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/led_test.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
rig.animation_data.action = bpy.data.actions["led_press_R"]
bpy.context.view_layer.update()

cage = bpy.data.objects.get("BlenRigMdefCage")
if cage: cage.hide_render = True
for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    if mat.name.startswith("LED"):
        continue
    nt = mat.node_tree
    for out in [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL']:
        for link in list(nt.links):
            if link.to_node == out: nt.links.remove(link)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = 1.0
        em.inputs["Color"].default_value = (0.78, 0.78, 0.81, 1.0)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
# remote = dark gray, button = red
for name, col in (("LED_Remote", (0.25, 0.25, 0.28, 1.0)), ("LED_Button", (0.9, 0.15, 0.15, 1.0))):
    o = bpy.data.objects.get(name)
    if o:
        m = bpy.data.materials.new(name + "_Mat")
        m.use_nodes = True
        nt = m.node_tree
        out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = col
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
        o.data.materials.append(m)

w = bpy.data.worlds.new("GrayVoid"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.32, 0.32, 0.35, 1.0)
sc.world = w
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.resolution_x = 640; sc.render.resolution_y = 640
sc.render.image_settings.file_format = "PNG"
cam = bpy.data.objects.new("lcam2", bpy.data.cameras.new("lcam2"))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.clip_start = 0.01; cam.data.clip_end = 10.0
def look_at(eye, target, up):
    z = (eye - target).normalized(); x = up.cross(z).normalized(); y = z.cross(x)
    M = Matrix.Identity(4)
    M[0][0], M[1][0], M[2][0] = x[0], x[1], x[2]
    M[0][1], M[1][1], M[2][1] = y[0], y[1], y[2]
    M[0][2], M[1][2], M[2][2] = z[0], z[1], z[2]
    M[0][3], M[1][3], M[2][3] = eye[0], eye[1], eye[2]
    return M
# focus on thumb - camera from front-left-above for clear profile
pts = np.array([rig.pose.bones[bn].head for bn in ("finger_thumb_1_R", "finger_thumb_2_R")])
c = Vector(pts.mean(axis=0))
eye = c + Vector((0.12, -0.14, 0.10))
cam.matrix_world = look_at(eye, c, Vector((0, 0, 1)))
cam.data.lens = 70
bpy.context.view_layer.update()
for f in FRAMES:
    sc.frame_set(f)
    bpy.context.view_layer.update()
    sc.render.filepath = f"/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/led_f{f:02d}.png"
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED f{f}", flush=True)
