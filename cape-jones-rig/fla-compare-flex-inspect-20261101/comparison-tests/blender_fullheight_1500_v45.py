"""T5 full-height Blender re-render, Blender 4.5.3 API variant.
Same source/engine/resolution as the 5.2 script (1100x1500, WORKBENCH,
transparent film), adapted only for the 4.5 compositor API
(scene.node_tree + CompositorNodeComposite), because the 5.2.3 binary on
this VM fails headless on missing system libEGL.so.1. Output is in this
job's new folder; the original 1100x1100 file is NOT overwritten.
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
tree = scene.node_tree
tree.nodes.clear()
img_node = tree.nodes.new('CompositorNodeImage')
img = bpy.data.images.load(img_path)
img_node.image = img
out_node = tree.nodes.new('CompositorNodeComposite')
tree.links.new(img_node.outputs['Image'], out_node.inputs['Image'])
print("BLENDER_TEST image:", img.name, img.size[0], img.size[1], "nodes:", len(tree.nodes))
bpy.ops.render.render(write_still=True)
print("BLENDER_TEST rendered:", scene.render.filepath, os.path.getsize(scene.render.filepath))
