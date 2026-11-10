"""Blender 5.2.3 compositor ONLY — L3 V4/V5 rebuilds.
Correction 16:30 CDT: realism is for LIGHT/EFFECTS/GOD RAYS, NOT the background
painting. The volumetric file here is a LIGHT layer behind the plate; no painted
background is repainted or altered in this script.
Verified 5.2 output path (from the earlier compositor fix): do NOT use
CompositorNodeComposite (undefined in 5.2). Use a new CompositorNodeTree
assigned to scene.compositing_node_group with an interface OUTPUT socket
"Image", linked from NodeGroupOutput, and a real render with
use_compositing=True + write_still=True.
PIL in this folder made helper masks/solids only; the shot is composited here.
Layer order: bg (god-ray light) -> ground shadow -> cast shadow -> plate
(untouched) -> bleed -> spill on character -> rim inner -> rim outer -> Glare.
V4: inner cyan / outer gold, bleed cyan, spill cyan+gold.
V5: inner gold-left/cyan-right, outer gold-left/cyan-right, bleed gold+cyan,
spill cyan+gold.
Usage: blender -b --python blender_composite_l3.py -- V4|V5
"""
import bpy, sys
variant = sys.argv[-1] if sys.argv[-1] in ("V4", "V5") else "V4"
R = '/home/hatch/workspace/cape-jones-rig/godray-level3-20261031'
BG = R + '/godray-bg-v2-1100x1500.png'
PLATE = '/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png'
OUT = f'{R}/{variant.lower()}-level3-20261031.png'
BLEND = f'{R}/{variant.lower()}-level3-20261031.blend'
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.use_nodes = True
scene.render.use_compositing = True
# Headless fix: EEVEE aborts without libEGL on this VM (exit 134); Cycles CPU avoids it.
scene.render.engine = 'CYCLES'
scene.render.compositor_device = 'CPU'  # headless: GPU compositor aborts without libEGL (exit 134)
scene.cycles.device = 'CPU'
scene.cycles.samples = 1
scene.render.resolution_x = 1100
scene.render.resolution_y = 1500
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = OUT
tree = bpy.data.node_groups.new(f"L3_{variant}", "CompositorNodeTree")
scene.compositing_node_group = tree
tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
nodes = tree.nodes; links = tree.links
def img(name, path, x, y):
    n = nodes.new("CompositorNodeImage"); n.name = name; n.location = (x, y)
    n.image = bpy.data.images.load(path); return n
def over(name, bg_node, fg_node, x, y):
    n = nodes.new("CompositorNodeAlphaOver"); n.name = name; n.location = (x, y)
    links.new(bg_node.outputs['Image'], n.inputs['Background'])
    links.new(fg_node.outputs['Image'], n.inputs['Foreground'])
    return n
def rim_layer(name, solid_path, mask_path, x, y):
    """Solid colour + mask alpha -> a rim layer image, via SetAlpha."""
    solid = img(name + "_solid", solid_path, x - 250, y)
    mask = img(name + "_mask", mask_path, x - 250, y - 200)
    sep = nodes.new("CompositorNodeSeparateColor"); sep.name = name + "_sep"; sep.location = (x, y - 200)
    links.new(mask.outputs['Image'], sep.inputs['Image'])
    seta = nodes.new("CompositorNodeSetAlpha"); seta.name = name; seta.location = (x, y)
    links.new(solid.outputs['Image'], seta.inputs['Image'])
    links.new(sep.outputs['Alpha'], seta.inputs['Alpha'])
    return seta
bg = img("GodRayV2_Light", BG, -1200, 400)
ground = img("GroundShadow", R + '/layer-ground-shadow.png', -1200, 100)
cast = img("CastShadow", R + '/layer-cast-shadow.png', -1200, -200)
plate = img("ArmsUpPlate_Untouched", PLATE, -1200, -500)
cur = over("Over_BG_Ground", bg, ground, -900, 300)
cur = over("Over_Cast", cur, cast, -600, 300)
cur = over("Over_Plate", cur, plate, -300, 300)
# bleed (edge band, low alpha via mask itself — mask is a blurred band)
if variant == "V4":
    cur = over("Over_BleedCyan", cur, rim_layer("BleedCyan", R + '/solid-cyanbleed.png', R + '/mask-bleed.png', 0, -100), 0, 300)
else:
    cur = over("Over_BleedGold", cur, rim_layer("BleedGold", R + '/solid-goldbleed.png', R + '/mask-bleed.png', 0, -100), 0, 300)
    cur = over("Over_BleedCyan2", cur, rim_layer("BleedCyan", R + '/solid-cyanbleed.png', R + '/mask-bleed.png', 300, -100), 300, 300)
# spill on character (pre-clipped to plate alpha in the helper layer)
cur = over("Over_SpillCyan", cur, img("SpillCyan", R + '/layer-spill-cyan.png', 0, -400), 600, 300)
cur = over("Over_SpillGold", cur, img("SpillGold", R + '/layer-spill-gold.png', 300, -400), 900, 300)
# rims
if variant == "V4":
    cur = over("Over_RimInnerCyan", cur, rim_layer("RimInnerCyan", R + '/solid-cyan.png', R + '/mask-inner.png', 1200, -100), 1200, 300)
    cur = over("Over_RimOuterGold", cur, rim_layer("RimOuterGold", R + '/solid-gold.png', R + '/mask-outer.png', 1500, -100), 1500, 300)
else:
    cur = over("Over_RimInnerL", cur, rim_layer("RimInnerGoldL", R + '/solid-gold.png', R + '/mask-inner-left.png', 1200, -100), 1200, 300)
    cur = over("Over_RimInnerR", cur, rim_layer("RimInnerCyanR", R + '/solid-cyan.png', R + '/mask-inner-right.png', 1500, -100), 1500, 300)
    cur = over("Over_RimOuterL", cur, rim_layer("RimOuterGoldL", R + '/solid-gold.png', R + '/mask-outer-left.png', 1800, -100), 1800, 300)
    cur = over("Over_RimOuterR", cur, rim_layer("RimOuterCyanR", R + '/solid-cyan.png', R + '/mask-outer-right.png', 2100, -100), 2100, 300)
# bloom / fog glow — only bright shafts + rim bloom
glare = nodes.new("CompositorNodeGlare"); glare.name = "BloomFogGlow"; glare.location = (2400, 300)
# Glare in Blender 5.2 is socket-driven (no glare_type/threshold attributes):
# Type menu defaults to FOG_GLOW; set Threshold/Size/Strength via inputs.
try:
    glare.inputs['Threshold'].default_value = 0.75
    glare.inputs['Size'].default_value = 6.0
    glare.inputs['Strength'].default_value = 0.35
except Exception as e:
    print("glare inputs note", e)
links.new(cur.outputs['Image'], glare.inputs['Image'])
out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (2700, 300)
links.new(glare.outputs['Image'], out.inputs['Image'])
print("nodes:", [n.name for n in nodes])
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"rendering L3 {variant} ...")
bpy.ops.render.render(write_still=True)
print(f"L3_{variant}_DONE", OUT)
