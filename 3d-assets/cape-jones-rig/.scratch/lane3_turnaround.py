"""Lane 3: R hand turnaround (4 angles), slight relaxed curl pose."""
import bpy, numpy as np
from mathutils import Vector, Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.update()
cage = bpy.data.objects.get("BlenRigMdefCage")
if cage: cage.hide_render = True
# hide remote for clean turnaround
for oname in ("LED_Remote", "LED_Button"):
    o = bpy.data.objects.get(oname)
    if o: o.hide_render = True

for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    nt = mat.node_tree
    for out in [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL']:
        for link in list(nt.links):
            if link.to_node == out: nt.links.remove(link)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = 1.0
        em.inputs["Color"].default_value = (0.80, 0.80, 0.83, 1.0)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
w = bpy.data.worlds.new("GrayVoid"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.30, 0.30, 0.33, 1.0)
sc.world = w
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 5
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.resolution_x = 700; sc.render.resolution_y = 700
sc.render.image_settings.file_format = "PNG"
cam = bpy.data.objects.new("tcam", bpy.data.cameras.new("tcam"))
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

# relaxed curl pose (shows articulation, not flat)
for pb in rig.pose.bones:
    if pb.name.startswith("finger_") and pb.name.endswith("_R"):
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (-0.35, 0, 0)
bpy.context.view_layer.update()

pts = np.array([pb.head for pb in rig.pose.bones if pb.name.startswith("finger_") and pb.name.endswith("_R")])
c = Vector(pts.mean(axis=0))
views = {
    "front": c + Vector((0.00, -0.24, 0.04)),
    "threequarter": c + Vector((0.16, -0.18, 0.05)),
    "side": c + Vector((0.24, -0.02, 0.03)),
    "back": c + Vector((0.00, 0.24, 0.04)),
}
for vname, eye in views.items():
    cam.matrix_world = look_at(eye, c, Vector((0, 0, 1)))
    cam.data.lens = 60
    bpy.context.view_layer.update()
    sc.render.filepath = f"/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/turn_R_{vname}.png"
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {vname}", flush=True)
