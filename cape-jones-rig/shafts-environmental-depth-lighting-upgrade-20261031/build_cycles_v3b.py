import bpy, math, random
random.seed(31)
OUT='/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/shafts-only-cycles-v3b-20261031.png'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=24; sc.cycles.volume_step_rate=1.0
try:
    sc.cycles.use_denoising=True
    print("DENOISE_ON")
except Exception as e:
    print("DENOISE_FAIL", e)
sc.render.resolution_x=1100; sc.render.resolution_y=1500; sc.render.resolution_percentage=100
sc.render.film_transparent=False; sc.render.filepath=OUT
w=bpy.data.worlds.new("W"); w.use_nodes=True
w.node_tree.nodes["Background"].inputs[0].default_value=(0.01,0.012,0.03,1)
w.node_tree.nodes["Background"].inputs[1].default_value=1.0
sc.world=w
bpy.ops.object.camera_add(location=(0,-14,3.2), rotation=(math.radians(90),0,0))
sc.camera=bpy.context.object
bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,3.0))
vol=bpy.context.object; vol.name="VolumeAir"; vol.scale=(5.0,3.0,4.5)
mat=bpy.data.materials.new("Vol"); mat.use_nodes=True
nt=mat.node_tree; nt.nodes.clear()
pv=nt.nodes.new("ShaderNodeVolumePrincipled")
pv.inputs["Density"].default_value=0.28; pv.inputs["Anisotropy"].default_value=0.7; pv.inputs["Color"].default_value=(1.0,0.85,0.55,1)
outn=nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(pv.outputs[0], outn.inputs["Volume"])
vol.data.materials.append(mat)
bpy.ops.object.light_add(type='SUN', location=(0,0,10))
sun=bpy.context.object; sun.name="SunDown"; sun.data.energy=5.0; sun.data.color=(1.0,0.88,0.60); sun.rotation_euler=(0,0,0)
# NARROWER slats (0.35 vs 0.55) + thinner in Z (0.15 vs 0.25) = wider gaps, less black top
bar_x=[-4.2,-2.25,-0.75,0.75,2.25,4.2]
for i,x in enumerate(bar_x):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x,0,6.8))
    p=bpy.context.object; p.name=f"CeilingSlat_{i}"; p.scale=(0.55,3.0,0.25)
    pm=bpy.data.materials.new("DarkSlat"); pm.use_nodes=True
    pm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(0,0,0,1)
    p.data.materials.append(pm)
bpy.ops.object.empty_add(location=(0,0,-1.5)); target=bpy.context.object
# OUTER spots boosted 12000, inner 6000, centre 8000 — outer columns were too dim in v2
energies=[12000,6000,6000,6000,12000]
for i,gx in enumerate([-3.0,-1.5,0.0,1.5,3.0]):
    bpy.ops.object.light_add(type='SPOT', location=(gx,0,9.0))
    s=bpy.context.object; s.name=f"SpotDown_{i}"; s.data.energy=energies[i]; s.data.color=(1.0,0.88,0.62)
    s.data.spot_size=math.radians(20); s.data.spot_blend=0.5
    c=s.constraints.new('TRACK_TO'); c.target=target; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'
dm=bpy.data.materials.new("Dust"); dm.use_nodes=True
em=dm.node_tree.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value=(1.0,0.9,0.65,1); em.inputs["Strength"].default_value=3.0
dm.node_tree.links.new(em.outputs[0], dm.node_tree.nodes["Material Output"].inputs[0])
for i in range(50):
    gx=random.choice([-3.0,-1.5,0.0,1.5,3.0])
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.015, location=(gx+random.uniform(-0.5,0.5), random.uniform(-2,2), random.uniform(-1,6)))
    bpy.context.object.data.materials.append(dm)
bpy.ops.render.render(write_still=True)
print("SHAFTS_V3B_DONE", OUT)
