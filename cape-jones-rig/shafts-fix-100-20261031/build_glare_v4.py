import bpy
INP = '/home/hatch/workspace/cape-jones-rig/shafts-fix-100-20261031/shafts-eevee-v4-fullres-20261031.png'
OUTDIR = '/home/hatch/workspace/cape-jones-rig/shafts-fix-100-20261031/methods/'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x = 1100; sc.render.resolution_y = 1500
sc.render.resolution_percentage = 100
tree = bpy.data.node_groups.new('Comp', 'CompositorNodeTree')
sc.compositing_node_group = tree
inp = tree.nodes.new('CompositorNodeImage')
inp.image = bpy.data.images.load(INP)
glare = tree.nodes.new('CompositorNodeGlare')
for name, val in [('Type', 'Fog Glow'), ('Quality', 'High'), ('Threshold', 0.6), ('Strength', 0.5), ('Size', 6.0)]:
    try:
        glare.inputs[name].default_value = val
        print('GLARE_INPUT_OK', name, val)
    except Exception as e:
        print('GLARE_INPUT_FAIL', name, e)
fo = tree.nodes.new('CompositorNodeOutputFile')
it = fo.file_output_items.new('RGBA', 'Image')
try: it.format.file_format = 'PNG'
except Exception as e: print('format fail', e)
fo.directory = OUTDIR
fo.file_name = 'I4-glare-v4'
tree.links.new(inp.outputs[0], glare.inputs[0])
tree.links.new(glare.outputs[0], fo.inputs['Image'])
sc.render.filepath = '/tmp/_glare_v4_tmp.png'
bpy.ops.render.render(write_still=True)
print('GLARE_V4_DONE')
