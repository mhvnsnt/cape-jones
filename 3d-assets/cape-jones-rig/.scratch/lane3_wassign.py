"""Lane 3: visualize finger weight assignment as vertex colors, render both hands."""
import bpy, numpy as np
from mathutils import Vector, Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
bpy.context.view_layer.update()

cage = bpy.data.objects.get("BlenRigMdefCage")
if cage:
    cage.hide_render = True

# vertex color by dominant finger bone (or gray if none)
if "finger_id" not in me.color_attributes:
    me.color_attributes.new("finger_id", 'FLOAT_COLOR', 'POINT')
ca = me.color_attributes["finger_id"]
vg_names = [v.name for v in mesh.vertex_groups]
finger_bones = sorted([pb.name for pb in rig.pose.bones if pb.name.startswith("finger_")])
# distinct colors per finger (index=red, middle=green, ring=blue, pinky=yellow, thumb=magenta)
fcol = {"index": (1, 0.2, 0.2, 1), "middle": (0.2, 1, 0.2, 1), "ring": (0.2, 0.4, 1, 1),
        "pinky": (1, 1, 0.2, 1), "thumb": (1, 0.2, 1, 1)}
for v in me.vertices:
    best = None
    for g in v.groups:
        gn = vg_names[g.group]
        if gn.startswith("finger_") and g.weight >= 0.5:
            best = gn
            break
    if best:
        fname = best.split("_")[1]
        ca.data[v.index].color = fcol.get(fname, (1, 1, 1, 1))
    else:
        ca.data[v.index].color = (0.75, 0.75, 0.78, 1.0)

# material using vertex colors
mat = bpy.data.materials.new("VColMat")
mat.use_nodes = True
nt = mat.node_tree
out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
for link in list(nt.links):
    nt.links.remove(link)
vc = nt.nodes.new("ShaderNodeVertexColor")
vc.layer_name = "finger_id"
em = nt.nodes.new("ShaderNodeEmission")
em.inputs["Strength"].default_value = 1.0
nt.links.new(vc.outputs["Color"], em.inputs["Color"])
nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
me.materials.clear()
me.materials.append(mat)

w = bpy.data.worlds.new("GrayVoid")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.25, 0.25, 0.28, 1.0)
sc.world = w
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.resolution_x = 640; sc.render.resolution_y = 640
sc.render.image_settings.file_format = "PNG"
cam = bpy.data.objects.new("wcam", bpy.data.cameras.new("wcam"))
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

import sys
SIDE = sys.argv[sys.argv.index('--') + 1]
pts = np.array([pb.head for pb in rig.pose.bones
                if pb.name.startswith("finger_") and pb.name.endswith("_" + SIDE)])
c = Vector(pts.mean(axis=0))
fbase = {f: np.array(rig.pose.bones[f"finger_{f}_1_{SIDE}"].head) for f in ("index", "pinky")}
fan = fbase["pinky"] - fbase["index"]; fan = fan / np.linalg.norm(fan)
pb_idx = rig.pose.bones[f"finger_index_2_{SIDE}"]
fdir = np.array(pb_idx.tail) - np.array(pb_idx.head); fdir = fdir / np.linalg.norm(fdir)
viewdir = np.cross(fan, fdir); viewdir = viewdir / np.linalg.norm(viewdir)
eye = c + Vector(viewdir * 0.24) + Vector((0, -0.05, 0.02))
cam.matrix_world = look_at(eye, c, Vector((0, 0, 1)))
cam.data.lens = 55
bpy.context.view_layer.update()
sc.render.filepath = f"/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/wassign_{SIDE}.png"
bpy.ops.render.render(write_still=True)
print("RENDERED wassign", SIDE, flush=True)
