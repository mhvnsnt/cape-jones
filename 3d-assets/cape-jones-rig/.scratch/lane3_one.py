"""Lane 3: single fist/rest render per run. Usage: -- SIDE POSE OUTFILE (POSE=rest|fist)"""
import bpy, sys, numpy as np
from mathutils import Vector, Matrix

a = sys.argv[sys.argv.index('--') + 1:]
SIDE, POSE, OUT = a[0], a[1], a[2]
FINGER = a[3] if len(a) > 3 else "all"  # e.g. "index" or "all"

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.update()

cage = bpy.data.objects.get("BlenRigMdefCage")
if cage:
    cage.hide_render = True

for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nt = mat.node_tree
    for out in [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL']:
        for link in list(nt.links):
            if link.to_node == out:
                nt.links.remove(link)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = 1.0
        em.inputs["Color"].default_value = (0.78, 0.78, 0.81, 1.0)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])

w = bpy.data.worlds.new("GrayVoid")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.32, 0.32, 0.35, 1.0)
sc.world = w
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.resolution_x = 640; sc.render.resolution_y = 640
sc.render.image_settings.file_format = "PNG"

cam = bpy.data.objects.new("fcam", bpy.data.cameras.new("fcam"))
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

pts = np.array([pb.head for pb in rig.pose.bones
                if pb.name.startswith("finger_") and pb.name.endswith("_" + SIDE)])
c = Vector(pts.mean(axis=0))
if SIDE == "L":
    # L hand hangs down; low camera looking up at fingers
    eye = Vector((0.38, -0.28, 0.30))
else:
    fbase = {f: np.array(rig.pose.bones[f"finger_{f}_1_{SIDE}"].head) for f in ("index", "pinky")}
    fan = fbase["pinky"] - fbase["index"]; fan = fan / np.linalg.norm(fan)
    pb_idx = rig.pose.bones[f"finger_index_2_{SIDE}"]
    fdir = np.array(pb_idx.tail) - np.array(pb_idx.head); fdir = fdir / np.linalg.norm(fdir)
    viewdir = np.cross(fan, fdir); viewdir = viewdir / np.linalg.norm(viewdir)
    eye = c + Vector(viewdir * 0.26) + Vector((0, -0.06, 0.03))
cam.matrix_world = look_at(eye, c, Vector((0, 0, 1)))
cam.data.lens = 55
bpy.context.view_layer.update()

if POSE == "fist":
    for pb in rig.pose.bones:
        if pb.name.startswith("finger_") and pb.name.endswith("_" + SIDE):
            if FINGER != "all" and not pb.name.startswith(f"finger_{FINGER}_"):
                continue
            pb.rotation_mode = 'XYZ'
            pb.rotation_euler = (-1.0, 0, 0)
    bpy.context.view_layer.update()

sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("RENDERED", OUT, flush=True)
