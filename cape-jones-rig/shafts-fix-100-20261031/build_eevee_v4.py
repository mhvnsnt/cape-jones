
import bpy, math, random
random.seed(31)
OUT = '/home/hatch/workspace/cape-jones-rig/shafts-fix-100-20261031/shafts-eevee-v4-20261031.png'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
try:
    sc.eevee.use_volumetric_shadows = False
    sc.eevee.volumetric_tile_size = '8'
    sc.eevee.taa_render_samples = 1
    print("EEVEE_SETTINGS_OK")
except Exception as e:
    print("EEVEE_SETTINGS_FAIL", e)
sc.render.resolution_x = 550; sc.render.resolution_y = 750
sc.render.resolution_percentage = 100
sc.render.film_transparent = False; sc.render.filepath = OUT
w = bpy.data.worlds.new("W"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.012, 0.03, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sc.world = w
bpy.ops.object.camera_add(location=(0, -15, 3.2), rotation=(math.radians(90), 0, 0))
sc.camera = bpy.context.object
COLS = [-3.0, -1.5, 0.0, 1.5, 3.0]
for i, gx in enumerate(COLS):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(gx, 0, 3.0))
    vol = bpy.context.object; vol.name = f"VolumeCol_{i}"; vol.scale = (0.55, 3.0, 4.5)
    mat = bpy.data.materials.new(f"VolCol_{i}"); mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    pv = nt.nodes.new("ShaderNodeVolumePrincipled")
    pv.inputs["Density"].default_value = 0.35; pv.inputs["Anisotropy"].default_value = 0.7
    pv.inputs["Color"].default_value = (1.0, 0.85, 0.55, 1)
    outn = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(pv.outputs[0], outn.inputs["Volume"])
    vol.data.materials.append(mat)
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1.5))
floor = bpy.context.object; floor.name = "FloorPools"
fm = bpy.data.materials.new("FloorMat"); fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.25, 0.22, 0.18, 1)
floor.data.materials.append(fm)
for i, gx in enumerate(COLS):
    bpy.ops.object.empty_add(location=(gx, 0, -1.5)); target = bpy.context.object
    bpy.ops.object.light_add(type='SPOT', location=(gx, 0, 9.0))
    s = bpy.context.object; s.data.energy = 10000; s.data.color = (1.0, 0.88, 0.62)
    s.data.spot_size = math.radians(18); s.data.spot_blend = 0.3
    c = s.constraints.new('TRACK_TO'); c.target = target; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
bpy.ops.render.render(write_still=True)
print("EEVEE_V4_DONE", OUT)
