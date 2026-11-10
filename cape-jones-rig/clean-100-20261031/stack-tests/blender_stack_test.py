import bpy, os
RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = "/home/hatch/workspace/cape-jones-rig/clean-100-20261031/stack-tests"
img_path = f"{RIG}/rig-apose-v7c-clean-transparent.png"
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1100
scene.render.resolution_y = 1100
scene.render.film_transparent = True
scene.render.filepath = f"{OUT}/blender-compositor-apose-20261031.png"
scene.use_nodes = True
tree = scene.compositing_node_group
if tree is None:
    tree = bpy.data.node_groups.new("StackTestCompositor", "CompositorNodeTree")
    scene.compositing_node_group = tree
print("BLENDER_TEST tree:", tree)
tree.nodes.clear()
img_node = tree.nodes.new('CompositorNodeImage')
img = bpy.data.images.load(img_path)
img_node.image = img
# Blender 5.2 pattern (per blender-compositor-stack.py): group output socket, not CompositorNodeComposite (undefined in 5.2)
tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
out_node = tree.nodes.new('NodeGroupOutput')
tree.links.new(img_node.outputs['Image'], out_node.inputs['Image'])
print("BLENDER_TEST image:", img.name, img.size[0], img.size[1], "nodes:", len(tree.nodes))
bpy.ops.render.render(write_still=True)
print("BLENDER_TEST rendered:", scene.render.filepath, os.path.getsize(scene.render.filepath))
