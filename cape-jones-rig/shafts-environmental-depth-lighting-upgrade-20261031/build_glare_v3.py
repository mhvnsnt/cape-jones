import bpy, os
INP='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/shafts-only-cycles-v2-20261031.png'
OUTDIR='/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.use_nodes=True
nt=bpy.data.node_groups.new('Comp','CompositorNodeTree'); sc.compositing_node_group=nt
img=nt.nodes.new('CompositorNodeImage'); img.image=bpy.data.images.load(INP)
gl=nt.nodes.new('CompositorNodeGlare')
for name,val in [('Type','Fog Glow'),('Quality','High'),('Threshold',0.6),('Strength',0.5),('Size',6.0)]:
    gl.inputs[name].default_value=val
fo=nt.nodes.new('CompositorNodeOutputFile')
it=fo.file_output_items.new('RGBA','Image')
print("item:", it.name)
try: it.format.file_format='PNG'; print("item format PNG ok")
except Exception as e: print("item format fail", e)
fo.directory=OUTDIR
try: fo.file_name='shafts-glare-blender'
except Exception as e: print("file_name fail", e)
nt.links.new(img.outputs[0], gl.inputs[0])
nt.links.new(gl.outputs[0], fo.inputs['Image'])
sc.render.resolution_x=1100; sc.render.resolution_y=1500
sc.render.filepath='/tmp/_glare_scene_tmp.png'
bpy.ops.render.render(write_still=True)
print("GLARE_V3_DONE")
