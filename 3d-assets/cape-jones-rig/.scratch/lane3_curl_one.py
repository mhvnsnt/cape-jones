"""Lane 3: per-finger curl verification renders. Gray bg, clay, proper framing.
Poses ONE finger segment chain at a time with a big curl; renders before/after.
Usage: -- finger_bone_name axis angle outfile
"""
import bpy, sys, numpy as np
from mathutils import Vector, Matrix

a = sys.argv[sys.argv.index('--') + 1:]
BONE, AXIS, ANGLE, OUT = a[0], a[1], float(a[2]), a[3]

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
        em.inputs["Color"].default_value = (0.75, 0.75, 0.78, 1.0)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])

w = bpy.data.worlds.new("GrayVoid")
w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.35, 0.35, 0.38, 1.0)
bg.inputs["Strength"].default_value = 1.0
sc.world = w
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.resolution_x = 560; sc.render.resolution_y = 560
sc.render.image_settings.file_format = "PNG"

cam = bpy.data.objects.new("vcam", bpy.data.cameras.new("vcam"))
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

side = BONE.rsplit("_", 1)[1]
fbase = {}
for f in ("index", "middle", "ring", "pinky"):
    pb = rig.pose.bones[f"finger_{f}_1_{side}"]
    fbase[f] = np.array(pb.head)
pts = [np.array(pb.head) for pb in rig.pose.bones
       if pb.name.startswith("finger_") and pb.name.endswith("_" + side)]
c = Vector(np.mean(pts, axis=0))
# palm normal: fan (index->pinky) x finger direction, oriented to thumb side
pb_idx = rig.pose.bones[f"finger_index_2_{side}"]
fdir = np.array(pb_idx.tail) - np.array(pb_idx.head)
fdir = fdir / np.linalg.norm(fdir)
fan = fbase["pinky"] - fbase["index"]
fan = fan / np.linalg.norm(fan)
n = np.cross(fan, fdir)
thumb = np.array(rig.pose.bones[f"finger_thumb_1_{side}"].head)
mid = np.mean([fbase["index"], fbase["pinky"]], axis=0)
if np.dot(thumb - mid, n) < 0:
    n = -n
n = n / np.linalg.norm(n)
print("palm normal:", np.round(n, 3), flush=True)
eye = c + Vector(n * 0.22) + Vector((0, 0, 0.02))
cam.matrix_world = look_at(eye, c, Vector((0, 0, 1)))
cam.data.lens = 60
bpy.context.view_layer.update()

# pose the finger: whole chain (segments 1..3) curl
fname = BONE.rsplit("_", 2)[0]  # e.g. finger_index
for pb in rig.pose.bones:
    if pb.name.startswith(fname + "_") and pb.name.endswith("_" + side):
        pb.rotation_mode = 'XYZ'
        e = [0, 0, 0]
        e["XYZ".index(AXIS)] = ANGLE
        pb.rotation_euler = e
bpy.context.view_layer.update()

sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("RENDERED", OUT, flush=True)
