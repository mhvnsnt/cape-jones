"""Lane 3: BEFORE close-ups of both hands. Cycles CPU + emission override (flat look)."""
import bpy, numpy as np
from mathutils import Vector, Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.update()

# --- flat unlit look: emission override on all materials ---
for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nt = mat.node_tree
    out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if out is None:
        continue
    img_node = None
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is not None:
        for link in nt.links:
            if link.to_node == bsdf and link.to_socket.name == "Base Color" \
               and link.from_node.type == "TEX_IMAGE":
                img_node = link.from_node
                break
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = 1.0
    if img_node is not None and img_node.image is not None:
        nt.links.new(img_node.outputs["Color"], em.inputs["Color"])
    else:
        em.inputs["Color"].default_value = (0.9, 0.9, 0.9, 1.0)
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])

# --- white world, Cycles CPU ---
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
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGB"

cam = bpy.data.objects.new("handcam", bpy.data.cameras.new("handcam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.clip_start = 0.01
cam.data.clip_end = 10.0

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

def hand_center(side):
    pts = []
    for pb in rig.pose.bones:
        if pb.name.startswith("finger_") and pb.name.endswith("_" + side):
            pts.append(np.array((rig.matrix_world @ pb.matrix).translation))
    return Vector(np.mean(pts, axis=0))

UP = Vector((0, 0, 1))
for side in ("R", "L"):
    c = hand_center(side)
    eye = c + Vector((0.0, -0.20, 0.05))  # character faces -Y; camera in front
    cam.matrix_world = look_at(eye, c, UP)
    cam.data.lens = 70
    bpy.context.view_layer.update()
    sc.render.filepath = f"/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/before_hand_{side}.png"
    bpy.ops.render.render(write_still=True)
    print("RENDERED", side, flush=True)
