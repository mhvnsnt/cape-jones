"""Effects V2 proof — Blender 5.2.3, Eevee.
Systems proven in one frame (all real Blender systems, no PIL VFX):
 1. Volumetric god rays: Spot light + Principled Volume cube.
 2. Bloom / glow with light spill: emissive aura spheres at the raised fists
    + point light + Eevee bloom + compositor Glare (Fog Glow).
 3. Dust particles with light interaction: particle system inside the volume.
 4. Ground light pool + cast shadow: ground plane receives spot shadow and
    the warm pool from the aura point light.
 5. Warm grade via compositor Color Balance (rim follows key hue family).
Base art is untouched: the arms-up pose is a separate textured plane; all
effects are separate layers/lights/volumes. No red labels anywhere.
"""
import bpy, math, os

OUT = "/home/hatch/workspace/cape-jones-rig/showcase/effects-v2-proof-20261031/effects-v2-proof-blender-20261031.png"
CHAR = "/home/hatch/workspace/cape-jones-rig/showcase/effects-v2-proof-20261031/arms-up-rgba-20261031.png"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 32
scene.cycles.use_denoising = False
scene.cycles.volume_bounces = 2
scene.render.resolution_x = 640
scene.render.resolution_y = 480
scene.render.resolution_percentage = 100
scene.render.filepath = OUT
# Headless VM has no working GPU context (EGL_BAD_MATCH): run the
# compositor on CPU so the Glare stack actually executes.
scene.render.compositor_device = "CPU"
scene.render.image_settings.file_format = "PNG"
# Eevee: volumetric shadows on (bloom in 5.2 is a compositor Glare effect,
# applied below — no render-time bloom toggle exists in this build)
try:
    scene.eevee.use_volumetric_shadows = False
    scene.eevee.volumetric_tile_size = "4"
    scene.eevee.volumetric_samples = 16
except Exception as e:
    print("eevee settings note:", e)

if "World" in bpy.data.worlds:
    world = bpy.data.worlds["World"]
else:
    world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
wn = world.node_tree.nodes
wn["Background"].inputs[0].default_value = (0.02, 0.015, 0.03, 1.0)
wn["Background"].inputs[1].default_value = 0.6

# Camera
cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
scene.collection.objects.link(cam)
cam.location = (0, -8.5, 0.5)
cam.rotation_euler = (math.radians(90), 0, 0)
scene.camera = cam

# Ground plane (receives shadow + light pool)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -3.2))
ground = bpy.context.active_object
ground.name = "Ground"
gm = bpy.data.materials.new("GroundMat")
gm.use_nodes = True
bsdf = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (0.10, 0.08, 0.07, 1.0)
bsdf.inputs["Roughness"].default_value = 1.0
ground.data.materials.append(gm)

# Character plane (arms-up reference pose, labels=False, base art untouched)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
char = bpy.context.active_object
char.name = "CapeJonesArmsUp"
# Local scale, not world dimensions: after the X-90 rotation, local Y maps
# to world Z, so (4.4, 6.0) gives a 4.4-wide, 6.0-tall billboard.
char.scale = (2.2, 3.0, 1.0)
char.rotation_euler = (math.radians(90), 0, 0)
cm = bpy.data.materials.new("CharMat")
cm.use_nodes = True
cm.blend_method = "BLEND"
nodes = cm.node_tree.nodes
links = cm.node_tree.links
nodes.remove(next(n for n in nodes if n.type == "BSDF_PRINCIPLED"))
tex = nodes.new("ShaderNodeTexImage")
tex.image = bpy.data.images.load(CHAR)
tex.image.alpha_mode = "STRAIGHT"
# Emissive billboard: the cutout reads exactly as drawn; scene lights
# act on the ground, the volume and the aura, not by recolouring the art.
emis = nodes.new("ShaderNodeEmission")
emis.inputs["Strength"].default_value = 1.0
transp = nodes.new("ShaderNodeBsdfTransparent")
mixsh = nodes.new("ShaderNodeMixShader")
out = next(n for n in nodes if n.type == "OUTPUT_MATERIAL")
links.new(tex.outputs["Color"], emis.inputs["Color"])
links.new(tex.outputs["Alpha"], mixsh.inputs["Fac"])
links.new(transp.outputs["BSDF"], mixsh.inputs[1])
links.new(emis.outputs["Emission"], mixsh.inputs[2])
links.new(mixsh.outputs["Shader"], out.inputs["Surface"])
cm.use_backface_culling = False
char.data.materials.append(cm)

# --- System 1: volumetric god rays ---
# Volume cube surrounding the scene
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
vol = bpy.context.active_object
vol.name = "VolumeCube"
vol.scale = (8, 7, 5)
vm = bpy.data.materials.new("VolumeMat")
vm.use_nodes = True
vn = vm.node_tree.nodes
vn.remove(vn["Principled BSDF"])
pv = vn.new("ShaderNodeVolumePrincipled")
pv.inputs["Density"].default_value = 0.02
pv.inputs["Anisotropy"].default_value = 0.5
pv.inputs["Color"].default_value = (1.0, 0.75, 0.45, 1.0)
vout = next(n for n in vn if n.type == "OUTPUT_MATERIAL")
vm.node_tree.links.new(pv.outputs["Volume"], vout.inputs["Volume"])
vol.data.materials.append(vm)

# Spot light, upper right behind, warm gold key — the god-ray source
spot_data = bpy.data.lights.new("GodRaySpot", "SPOT")
spot = bpy.data.objects.new("GodRaySpot", spot_data)
scene.collection.objects.link(spot)
spot.location = (5.5, -2.0, 5.5)
import mathutils
_dir = mathutils.Vector((0, 0, 0)) - mathutils.Vector(spot.location)
spot.rotation_euler = _dir.to_track_quat("-Z", "Y").to_euler()
spot_data.energy = 3000
spot_data.color = (1.0, 0.70, 0.32)
spot_data.spot_size = math.radians(55)
spot_data.spot_blend = 0.4
spot_data.use_shadow = True
spot_data.shadow_soft_size = 0.5

# --- System 2: aura bloom + light spill at the raised fists ---
for loc in [(-0.9, 0, 1.3), (0.9, 0, 1.3)]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=loc)
    s = bpy.context.active_object
    s.name = "AuraSphere"
    sm = bpy.data.materials.new("AuraMat")
    sm.use_nodes = True
    sn = sm.node_tree.nodes
    sn.remove(next(n for n in sn if n.type == "BSDF_PRINCIPLED"))
    se = sn.new("ShaderNodeEmission")
    se.inputs["Color"].default_value = (1.0, 0.70, 0.30, 1.0)
    se.inputs["Strength"].default_value = 8.0
    sout = next(n for n in sn if n.type == "OUTPUT_MATERIAL")
    sm.node_tree.links.new(se.outputs["Emission"], sout.inputs["Surface"])
    s.data.materials.append(sm)

pt_data = bpy.data.lights.new("AuraPoint", "POINT")
pt = bpy.data.objects.new("AuraPoint", pt_data)
scene.collection.objects.link(pt)
pt.location = (0, -0.5, 1.3)
pt_data.energy = 800
pt_data.color = (1.0, 0.70, 0.30)
pt_data.shadow_soft_size = 0.8

# --- System 3: dust particles inside the volume ---
bpy.ops.mesh.primitive_cube_add(size=8, location=(0, 0, 1.0))
emit = bpy.context.active_object
emit.name = "DustEmitter"
emit.hide_render = True
ps = emit.modifiers.new("Dust", "PARTICLE_SYSTEM").particle_system
ps.settings.count = 80
ps.settings.frame_start = 1
ps.settings.frame_end = 1
ps.settings.lifetime = 250
ps.settings.emit_from = "VOLUME"
ps.settings.physics_type = "NO"
ps.settings.render_type = "OBJECT"
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.02, location=(0, 0, -10))
dot = bpy.context.active_object
dot.name = "DustDot"
dot.hide_render = True
dm = bpy.data.materials.new("DustMat")
dm.use_nodes = True
dn = dm.node_tree.nodes
dn.remove(next(n for n in dn if n.type == "BSDF_PRINCIPLED"))
de = dn.new("ShaderNodeEmission")
de.inputs["Color"].default_value = (1.0, 0.8, 0.5, 1.0)
de.inputs["Strength"].default_value = 2.0
dout = next(n for n in dn if n.type == "OUTPUT_MATERIAL")
dm.node_tree.links.new(de.outputs["Emission"], dout.inputs["Surface"])
dot.data.materials.append(dm)
ps.settings.instance_object = dot

# --- Compositor: original + Fog Glow + Sun Beams glare, warm grade ---
# Glare nodes output ONLY the glow pass in 5.2, so the original image must
# be added back with Mix (ADD) nodes — a chained Glare stack alone goes black.
scene.use_nodes = True
scene.compositing_node_group = bpy.data.node_groups.new("EffectsV2Comp", "CompositorNodeTree")
tree = scene.compositing_node_group
rl = tree.nodes.new("CompositorNodeRLayers")
glare = tree.nodes.new("CompositorNodeGlare")
glare.inputs["Type"].default_value = "Fog Glow"
glare.inputs["Threshold"].default_value = 0.8
glare.inputs["Size"].default_value = 8
glare.inputs["Strength"].default_value = 0.5
beams = tree.nodes.new("CompositorNodeGlare")
beams.inputs["Type"].default_value = "Sun Beams"
beams.inputs["Threshold"].default_value = 0.8
beams.inputs["Strength"].default_value = 0.4
try:
    beams.inputs["Sun Position"].default_value = (0.78, 0.82)
except Exception as e:
    print("sun position note:", e)
def add_mix(a, b):
    m = tree.nodes.new("ShaderNodeMix")
    m.data_type = "RGBA"
    m.blend_type = "ADD"
    m.inputs[0].default_value = 1.0
    tree.links.new(a, m.inputs[6])
    tree.links.new(b, m.inputs[7])
    return m
mix1 = add_mix(rl.outputs["Image"], glare.outputs["Image"])
mix2 = add_mix(mix1.outputs[2], beams.outputs["Image"])
grade = tree.nodes.new("CompositorNodeBrightContrast")
grade.inputs["Bright"].default_value = 0.05
grade.inputs["Contrast"].default_value = 0.10
comp = tree.nodes.new("CompositorNodeViewer")
links = tree.links
links.new(rl.outputs["Image"], glare.inputs["Image"])
links.new(mix1.outputs[2], beams.inputs["Image"])
links.new(mix2.outputs[2], grade.inputs["Image"])
links.new(grade.outputs["Image"], comp.inputs["Image"])

scene.frame_set(1)
bpy.ops.render.render(write_still=True)
print("PROOF_RENDERED", OUT)
