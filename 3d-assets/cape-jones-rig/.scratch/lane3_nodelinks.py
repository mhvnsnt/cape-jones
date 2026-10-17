"""Lane 3: dump tripo material node links + do a NO-MODIFICATION render for ground truth."""
import bpy, sys
from mathutils import Vector, Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
mat = bpy.data.materials.get("tripo_material_2cad1649-2fab-4c4f-9666-330ccaa37295")
nt = mat.node_tree
for link in nt.links:
    print(f"LINK: {link.from_node.name}.{link.from_socket.name} -> {link.to_node.name}.{link.to_socket.name}")
for n in nt.nodes:
    if n.type == 'BSDF_PRINCIPLED':
        print("PRINCIPLED base color:", tuple(round(v,3) for v in n.inputs['Base Color'].default_value),
              "metallic:", n.inputs['Metallic'].default_value,
              "specular:", n.inputs['Specular'].default_value)
sc = bpy.context.scene
# ground-truth render: NO material changes, white world, cycles CPU
w = bpy.data.worlds.new("WhiteVoid")
w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (1, 1, 1, 1)
sc.world = w
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 8
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.resolution_x = 960; sc.render.resolution_y = 960
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"
cape = bpy.data.objects.get("CapeJones_Cape")
if cape: cape.hide_render = True
cam = bpy.data.objects.new("gtcam", bpy.data.cameras.new("gtcam"))
sc.collection.objects.link(cam); sc.camera = cam
def look_at(eye, target, up):
    z = (eye - target).normalized(); x = up.cross(z).normalized(); y = z.cross(x)
    M = Matrix.Identity(4)
    M[0][0], M[1][0], M[2][0] = x[0], x[1], x[2]
    M[0][1], M[1][1], M[2][1] = y[0], y[1], y[2]
    M[0][2], M[1][2], M[2][2] = z[0], z[1], z[2]
    M[0][3], M[1][3], M[2][3] = eye[0], eye[1], eye[2]
    return M
cam.matrix_world = look_at(Vector((0.0, -2.3, 0.75)), Vector((0.0, 0.0, 0.55)), Vector((0, 0, 1)))
cam.data.lens = 50
bpy.context.view_layer.update()
sc.render.filepath = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/groundtruth.png"
bpy.ops.render.render(write_still=True)
print("RENDERED groundtruth", flush=True)
