"""Lane 3: compare unevaluated vs evaluated pose bone positions; render markers
at EVALUATED positions."""
import bpy, numpy as np
from mathutils import Vector, Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.update()

deps = bpy.context.evaluated_depsgraph_get()
rig_e = rig.evaluated_get(deps)

for bn in ["finger_index_2_R", "finger_pinky_1_R"]:
    pb = rig.pose.bones[bn]
    pbe = rig_e.pose.bones[bn]
    print(f"{bn}:")
    print("  uneval pb.head            :", np.round(np.array(pb.head), 4))
    print("  uneval matrix translation :", np.round(np.array((rig.matrix_world @ pb.matrix).translation), 4))
    print("  EVAL pbe.head             :", np.round(np.array(pbe.head), 4))
    print("  EVAL matrix translation   :", np.round(np.array((rig_e.matrix_world @ pbe.matrix).translation), 4))

# markers at EVALUATED head positions (green)
mgreen = bpy.data.materials.new("MarkerGreen")
mgreen.use_nodes = True
nt = mgreen.node_tree
out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
em = nt.nodes.new("ShaderNodeEmission")
em.inputs["Color"].default_value = (0.1, 1, 0.1, 1.0)
nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
for pb in rig.pose.bones:
    if pb.name.startswith("finger_") and pb.name.endswith("_R"):
        pbe = rig_e.pose.bones[pb.name]
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.002, location=Vector(pbe.head))
        o = bpy.context.active_object
        o.data.materials.append(mgreen)
        o.name = "EMARK_" + pb.name

cage = bpy.data.objects.get("BlenRigMdefCage")
if cage:
    cage.hide_render = True
for mat in bpy.data.materials:
    if mat.name.startswith("Marker"):
        continue
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
cam = bpy.data.objects.new("ecam", bpy.data.cameras.new("ecam"))
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
pts = np.array([rig_e.pose.bones[pb.name].head for pb in rig.pose.bones
                if pb.name.startswith("finger_") and pb.name.endswith("_R")])
c = Vector(pts.mean(axis=0))
fbase = {f: np.array(rig_e.pose.bones[f"finger_{f}_1_R"].head) for f in ("index", "pinky")}
fan = fbase["pinky"] - fbase["index"]; fan = fan / np.linalg.norm(fan)
pbe_idx = rig_e.pose.bones["finger_index_2_R"]
fdir = np.array(pbe_idx.tail) - np.array(pbe_idx.head); fdir = fdir / np.linalg.norm(fdir)
viewdir = np.cross(fan, fdir); viewdir = viewdir / np.linalg.norm(viewdir)
eye = c + Vector(viewdir * 0.26) + Vector((0, -0.06, 0.03))
cam.matrix_world = look_at(eye, c, Vector((0, 0, 1)))
cam.data.lens = 55
bpy.context.view_layer.update()
sc.render.filepath = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/bonemarkers_eval_R.png"
bpy.ops.render.render(write_still=True)
print("RENDERED eval markers", flush=True)
