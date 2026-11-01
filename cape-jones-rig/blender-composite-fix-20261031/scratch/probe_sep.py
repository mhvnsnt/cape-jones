import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.use_nodes=True
tree=bpy.data.node_groups.new("P","CompositorNodeTree")
scene.compositing_node_group=tree
for t in ["CompositorNodeSeparateColor","CompositorNodeSepRGBA","CompositorNodeSetAlpha","CompositorNodeAlphaConvert"]:
    try:
        n=tree.nodes.new(t)
        print(t, "OK", [(i.name) for i in n.inputs], [(o.name) for o in n.outputs])
    except Exception as e:
        print(t, "FAIL", e)
