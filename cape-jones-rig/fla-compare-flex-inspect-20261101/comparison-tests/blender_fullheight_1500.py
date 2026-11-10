"""T5 our-side completion, 2026-11-01: full-height Blender re-render.
Adapted from clean-100-20261031/stack-tests/blender_stack_test.py with ONLY
two changes: resolution_y 1100 -> 1500, and filepath -> this job's new folder.
Same source (rig-apose-v7c-clean-transparent.png, 1100x1500), same engine
(BLENDER_WORKBENCH), same compositor nodes. The original 1100x1100 file is
NOT overwritten. Run with Blender 5.2.3 --background --python this file.
"""
import bpy, os
RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = "/home/hatch/workspace/cape-jones-rig/fla-compare-flex-inspect-20261101/comparison-tests"
img_path = f"{RIG}/rig-apose-v7c-clean-transparent.png"
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1100
scene.render.resolution_y = 1500
scene.render.film_transparent = True
scene.render.filepath = f"{OUT}/blender-compositor-apose-fullheight-20261101.png"
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
tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
out_node = tree.nodes.new('NodeGroupOutput')
tree.links.new(img_node.outputs['Image'], out_node.inputs['Image'])
print("BLENDER_TEST image:", img.name, img.size[0], img.size[1], "nodes:", len(tree.nodes))
bpy.ops.render.render(write_still=True)
print("BLENDER_TEST rendered:", scene.render.filepath, os.path.getsize(scene.render.filepath))
