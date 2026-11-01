import bpy, sys, os
print("MINIMAL START")
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.use_nodes = True
scene.render.use_compositing = True
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = '/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/scratch/minimal-out.png'
tree = bpy.data.node_groups.new("MinimalComp", "CompositorNodeTree")
scene.compositing_node_group = tree
tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
nodes = tree.nodes
links = tree.links
bg = nodes.new("CompositorNodeImage"); bg.name = "BG"; bg.location = (-600, 300)
bg.image = bpy.data.images.load('/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/scratch/bg-test.png')
fg = nodes.new("CompositorNodeImage"); fg.name = "FG"; fg.location = (-600, -300)
fg.image = bpy.data.images.load('/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png')
print("FG image size", fg.image.size)
scale = nodes.new("CompositorNodeScale"); scale.name = "FG_Scale"; scale.location = (-300, -300)
scale.inputs['Type'].default_value = 'Relative'
scale.inputs['X'].default_value = 0.213
scale.inputs['Y'].default_value = 0.213
links.new(fg.outputs['Image'], scale.inputs['Image'])
trans = nodes.new("CompositorNodeTransform"); trans.name = "FG_Translate"; trans.location = (0, -300)
trans.inputs['X'].default_value = 203
trans.inputs['Y'].default_value = 20
links.new(scale.outputs['Image'], trans.inputs['Image'])
over = nodes.new("CompositorNodeAlphaOver"); over.name = "AlphaOver"; over.location = (300, 0)
print("AlphaOver inputs:", [(i.name) for i in over.inputs])
links.new(bg.outputs['Image'], over.inputs['Background'])
links.new(trans.outputs['Image'], over.inputs['Foreground'])
out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (600, 0)
links.new(over.outputs['Image'], out.inputs['Image'])
print("nodes:", [n.name for n in nodes])
print("links:", [(l.from_node.name, l.from_socket.name, l.to_node.name, l.to_socket.name) for l in links])
bpy.ops.wm.save_as_mainfile(filepath='/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/scratch/minimal-comp.blend')
print("saved blend, rendering...")
bpy.ops.render.render(write_still=True)
print("render done")
