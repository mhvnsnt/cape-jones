import bpy, math, os
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
outdir = "/home/hatch/workspace/cape-jones-rig/mixed-media-2d-3d-bridge-20261031/frames_3d"
os.makedirs(outdir, exist_ok=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.device = 'CPU'
scene.render.resolution_x = 476
scene.render.resolution_y = 688
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
world = bpy.data.worlds.new("W2")
world.use_nodes = True
scene.world = world
bpy.ops.object.camera_add(location=(0, 0, 6), rotation=(0, 0, 0))
cam = bpy.context.active_object
scene.camera = cam
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 3.6
bpy.ops.object.light_add(type='SUN', location=(2, 2, 5))
bpy.context.active_object.data.energy = 3.0
bpy.ops.object.light_add(type='AREA', location=(-2, -1, 4))
def mat(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.8
    return m
skin = mat("Skin2", (0.95, 0.75, 0.60))
purple = mat("Cowl2", (0.45, 0.15, 0.65))
dark = mat("Dark2", (0.08, 0.08, 0.12))
muscle_mat = mat("Muscle2", (0.75, 0.25, 0.25))
white = mat("White2", (1, 1, 1))
# Head: single sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0.1, 0), segments=48, ring_count=32)
head = bpy.context.active_object
head.name = "Head"
head.scale = (0.9, 1.15, 0.6)
bpy.ops.object.transform_apply(scale=True)
head.data.materials.append(skin)
# Cowl cap: slightly larger sphere, shifted up, purple — reads as a cap over the top half
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.02, location=(0, 0.45, 0), segments=48, ring_count=32)
cowl = bpy.context.active_object
cowl.name = "CowlCap"
cowl.scale = (0.92, 0.85, 0.62)
bpy.ops.object.transform_apply(scale=True)
cowl.data.materials.append(purple)
# Eyes on front
for x in (-0.35, 0.35):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(x, 0.35, 0.55))
    e = bpy.context.active_object
    e.scale = (1.4, 0.6, 0.3)
    bpy.ops.object.transform_apply(scale=True)
    e.data.materials.append(white)
# Hinge + jaw (bevelled box)
bpy.ops.object.empty_add(location=(0, -0.35, 0))
hinge = bpy.context.active_object
hinge.name = "TMJ_Hinge"
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.95, 0.05))
jaw = bpy.context.active_object
jaw.name = "Mandible"
jaw.scale = (0.78, 0.32, 0.45)
bpy.ops.object.transform_apply(scale=True)
bev = jaw.modifiers.new("Bevel", 'BEVEL')
bev.width = 0.12
bev.segments = 3
jaw.data.materials.append(skin)
jaw.parent = hinge
jaw.matrix_parent_inverse = hinge.matrix_world.inverted()
# Mouth cavity on jaw front
bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, -0.78, 0.48))
cav = bpy.context.active_object
cav.name = "MouthCavity"
cav.scale = (1.0, 0.22, 0.1)
bpy.ops.object.transform_apply(scale=True)
cav.data.materials.append(dark)
cav.parent = hinge
cav.matrix_parent_inverse = hinge.matrix_world.inverted()
# Muscle strands BEHIND the jaw (z=-0.3), stretch-to jaw attaches
for side, x in (("L", -0.62), ("R", 0.62)):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.8, location=(x, -0.45, -0.3))
    mus = bpy.context.active_object
    mus.name = f"Masseter_{side}"
    mus.data.materials.append(muscle_mat)
    bpy.ops.object.empty_add(location=(x, -0.95, -0.3))
    tgt = bpy.context.active_object
    tgt.name = f"JawAttach_{side}"
    tgt.parent = hinge
    tgt.matrix_parent_inverse = hinge.matrix_world.inverted()
    con = mus.constraints.new('STRETCH_TO')
    con.target = tgt
    con.volume = 'NO_VOLUME'
angles = [0, 12, 24, 32, 32, 24, 12, 0]
for i, deg in enumerate(angles, start=1):
    scene.frame_set(i)
    hinge.rotation_euler[0] = math.radians(deg)
    hinge.keyframe_insert(data_path="rotation_euler", frame=i)
for i, deg in enumerate(angles, start=1):
    scene.frame_set(i)
    scene.render.filepath = os.path.join(outdir, f"jaw3d_f{i:02d}_{deg}deg.png")
    bpy.ops.render.render(write_still=True)
print("DONE v2 angles:", angles)
