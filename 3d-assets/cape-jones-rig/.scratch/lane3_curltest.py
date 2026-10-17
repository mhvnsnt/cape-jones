"""Lane 3: curl-axis empirical test. Rotate finger_index_2_R about local X, render R hand."""
import bpy, numpy as np
from mathutils import Vector, Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.update()

# hide cage for clean renders
cage = bpy.data.objects.get("BlenRigMdefCage")
if cage:
    cage.hide_render = True

# flat clay materials
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
        em.inputs["Color"].default_value = (0.82, 0.82, 0.85, 1.0)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])

w = bpy.data.worlds.new("WhiteVoid")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
sc.world = w
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.resolution_x = 560; sc.render.resolution_y = 560
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

# R hand finger center
pts = [np.array(pb.head) for pb in rig.pose.bones if pb.name.startswith("finger_") and pb.name.endswith("_R")]
c = Vector(np.mean(pts, axis=0))
eye = c + Vector((0.02, -0.16, 0.03))
cam.matrix_world = look_at(eye, c, Vector((0, 0, 1)))
cam.data.lens = 60
bpy.context.view_layer.update()

# BEFORE
sc.render.filepath = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/curltest_before.png"
bpy.ops.render.render(write_still=True)

# curl finger_index_2_R about local X by -1.0
pb = rig.pose.bones["finger_index_2_R"]
pb.rotation_mode = 'XYZ'
pb.rotation_euler = (-1.0, 0, 0)
bpy.context.view_layer.update()
sc.render.filepath = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/curltest_Xneg.png"
bpy.ops.render.render(write_still=True)

# try local Z instead
pb.rotation_euler = (0, 0, 0)
pb2 = rig.pose.bones["finger_index_2_R"]
pb2.rotation_mode = 'XYZ'
pb2.rotation_euler = (0, 0, -1.0)
bpy.context.view_layer.update()
sc.render.filepath = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/curltest_Zneg.png"
bpy.ops.render.render(write_still=True)
print("RENDERED curl tests", flush=True)
