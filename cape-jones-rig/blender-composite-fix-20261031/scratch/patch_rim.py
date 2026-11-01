import pathlib
p=pathlib.Path('/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/blender_composite_final.py')
t=p.read_text()
old="""rim = nodes.new("ShaderNodeMixRGB"); rim.name = "CyanBackRim_Add"; rim.location = (500, -200)
rim.blend_type = 'ADD'
links.new(sub.outputs['Value'], rim.inputs['Factor'])
links.new(over.outputs['Image'], rim.inputs['Color1'])
rim.inputs['Color2'].default_value = (0.0, 0.784, 1.0, 1.0)  # cyan (0,200,255)

out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (800, 0)
links.new(rim.outputs['Color'], out.inputs['Image'])"""
new="""# Rim via AlphaOver (NOT MixRGB Add): MixRGB in 5.2 crops its output to
# the Factor image's canvas, which produced black bars in the first
# final render. AlphaOver keeps the background canvas.
cyan = nodes.new("CompositorNodeImage"); cyan.name = "SolidCyan_FullCanvas"; cyan.location = (250, -750)
cyan.image = bpy.data.images.load('/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/scratch/solid-cyan-640x360.png')
seta = nodes.new("CompositorNodeSetAlpha"); seta.name = "Rim_SetAlpha"; seta.location = (500, -550)
links.new(cyan.outputs['Image'], seta.inputs['Image'])
links.new(sub.outputs['Value'], seta.inputs['Alpha'])
rim = nodes.new("CompositorNodeAlphaOver"); rim.name = "CyanBackRim_AlphaOver"; rim.location = (500, -200)
links.new(over.outputs['Image'], rim.inputs['Background'])
links.new(seta.outputs['Image'], rim.inputs['Foreground'])

out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (800, 0)
links.new(rim.outputs['Image'], out.inputs['Image'])"""
assert old in t
t=t.replace(old,new)
pathlib.Path('/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/blender_composite_final.py').write_text(t)
print("patched rim to AlphaOver")
