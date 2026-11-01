# Blender 5.2.3 compositor, REAL node run. In 5.2 there is no Composite node type;
# output is via File Output node. Glare inputs are socket-driven, enum strings are 'Fog Glow'/'High'.
import bpy
INP='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/shafts-only-cycles-v2-20261031.png'
OUTDIR='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.use_nodes=True
nt=bpy.data.node_groups.new('Comp','CompositorNodeTree'); sc.compositing_node_group=nt
img=nt.nodes.new('CompositorNodeImage'); img.image=bpy.data.images.load(INP)
gl=nt.nodes.new('CompositorNodeGlare')
gl.inputs['Type'].default_value='Fog Glow'
gl.inputs['Quality'].default_value='High'
gl.inputs['Threshold'].default_value=0.6
gl.inputs['Strength'].default_value=0.5
gl.inputs['Size'].default_value=6
fo=nt.nodes.new('CompositorNodeOutputFile')
fo.base_path=OUTDIR
fo.file_slots[0].path='shafts-glare-blender-20261031'
fo.format.file_format='PNG'
nt.links.new(img.outputs[0], gl.inputs[0]); nt.links.new(gl.outputs[0], fo.inputs[0])
sc.render.resolution_x=1100; sc.render.resolution_y=1500; sc.render.filepath=OUTDIR+'shafts-glare-blender-20261031.png'
bpy.ops.render.render(write_still=True)
print("GLARE_DONE")
