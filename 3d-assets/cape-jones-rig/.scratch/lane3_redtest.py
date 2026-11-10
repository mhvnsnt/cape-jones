"""Lane 3: nuke materials to RED + render + verify the override actually renders."""
import bpy
from mathutils import Vector, Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene

cape = bpy.data.objects.get("CapeJones_Cape")
if cape:
    cape.hide_render = True
    print("cape hidden:", cape.name)

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
        em.inputs["Color"].default_value = (1.0, 0.0, 0.0, 1.0)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])

body = bpy.data.objects["CapeJones_Body"]
print("body hide_render:", body.hide_render, "visible:", body.visible_get())
print("all mesh objects:", [(o.name, o.hide_render) for o in bpy.data.objects if o.type == 'MESH'])

w = bpy.data.worlds.new("WhiteVoid")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
sc.world = w
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4
sc.cycles.use_denoising = False
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.resolution_x = 640; sc.render.resolution_y = 640
sc.render.image_settings.file_format = "PNG"

cam = bpy.data.objects.new("redcam", bpy.data.cameras.new("redcam"))
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
sc.render.filepath = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/redtest.png"
bpy.ops.render.render(write_still=True)
print("RENDERED redtest", flush=True)
