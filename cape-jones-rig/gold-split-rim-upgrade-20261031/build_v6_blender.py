"""Blender 5.2.3 compositor - V6 medium outer-only rim, seam 550.
Same stack as the PIL V6 build, but rendered through Blender to prove
the outer-only method in the compositor itself: bg -> shadows ->
outer-only rim (gold left / cyan right of seam, dilate-minus-alpha,
zero pixels inside the plate alpha) -> plate ON TOP -> output.
Standard view transform, look None. No Glare over the figure in this
variant (cyan bloom in the PIL build is outside-silhouette only);
this Blender render is the clean rim proof.
Usage: blender -b --python build_v6_blender.py
"""
import bpy
R = '/home/hatch/workspace/cape-jones-rig/gold-split-rim-upgrade-20261031'
L3 = '/home/hatch/workspace/cape-jones-rig/godray-level3-20261031'
PLATE = '/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png'
OUT = f'{R}/v6-medium-outer-only-blender-20261031.png'
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.use_nodes = True
scene.render.use_compositing = True
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 1100
scene.render.resolution_y = 1500
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = OUT
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
tree = bpy.data.node_groups.new("V6OuterOnly", "CompositorNodeTree")
scene.compositing_node_group = tree
nodes = tree.nodes; links = tree.links
tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")

def img(name, path, x, y):
    n = nodes.new("CompositorNodeImage"); n.name = name; n.location = (x, y)
    n.image = bpy.data.images.load(path); return n

def over(name, bg_node, fg_node, x, y):
    n = nodes.new("CompositorNodeAlphaOver"); n.name = name; n.location = (x, y)
    links.new(bg_node.outputs['Image'], n.inputs['Background'])
    links.new(fg_node.outputs['Image'], n.inputs['Foreground'])
    return n

def rim_layer(name, solid_path, mask_path, x, y):
    solid = img(name + "_solid", solid_path, x - 250, y)
    mask = img(name + "_mask", mask_path, x - 250, y - 200)
    sep = nodes.new("CompositorNodeSeparateColor"); sep.name = name + "_sep"; sep.location = (x, y - 200)
    links.new(mask.outputs['Image'], sep.inputs['Image'])
    seta = nodes.new("CompositorNodeSetAlpha"); seta.name = name; seta.location = (x, y)
    links.new(solid.outputs['Image'], seta.inputs['Image'])
    links.new(sep.outputs['Alpha'], seta.inputs['Alpha'])
    return seta

bg = img("GodRayV2_Light", L3 + '/godray-bg-v2-1100x1500.png', -1200, 400)
ground = img("GroundShadow", L3 + '/layer-ground-shadow.png', -1200, 100)
cast = img("CastShadow", L3 + '/layer-cast-shadow.png', -1200, -200)
cur = over("Over_BG_Ground", bg, ground, -900, 300)
cur = over("Over_Cast", cur, cast, -600, 300)
# outer-only rims UNDER the plate
cur = over("Over_RimGoldL", cur, rim_layer("RimGoldL", L3 + '/solid-gold.png', R + '/mask-outer-only-gold-left-12px.png', 0, -100), 0, 300)
cur = over("Over_RimCyanR", cur, rim_layer("RimCyanR", L3 + '/solid-cyan.png', R + '/mask-outer-only-cyan-right-12px.png', 300, -100), 300, 300)
# plate ON TOP - line preservation
cur = over("Over_Plate", cur, img("ArmsUpPlate_Untouched", PLATE, -1200, -500), 600, 300)
out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (900, 300)
links.new(cur.outputs['Image'], out.inputs['Image'])
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace('.png', '.blend'))
print("rendering V6 Blender outer-only ...")
bpy.ops.render.render(write_still=True)
print("V6_BLENDER_DONE", OUT)
