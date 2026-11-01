"""Blender 5.2.3 compositor ONLY - gold-split wire-100 V5 opaque split.
Plate: dual-light-variants base-arms-up-transparent (APPROVED arms-up plate,
untouched). Stack: god-ray bg -> ground shadow -> cast shadow -> plate ->
seam-split bleed (gold left / cyan right) -> spill -> OPAQUE split rims
(gold left of seam 550, cyan right of seam 550, alpha 1.0, zero overlap) ->
cyan-side-only Glare (Glare branch masked to x>=550 AFTER the gold rim,
so cyan bloom cannot cross the seam into gold) -> output.
View transform is an argv mode: STANDARD (main), AGX (control), ACES13 (control).
Controls use the same node tree minus the Glare branch, to isolate view transform.
Usage: blender -b --python build_gold_split.py -- STANDARD|AGX|ACES13
"""
import bpy, sys
mode = sys.argv[-1] if sys.argv[-1] in ("STANDARD", "AGX", "ACES13") else "STANDARD"
R = '/home/hatch/workspace/cape-jones-rig/gold-split-wire100-20261031'
L3 = '/home/hatch/workspace/cape-jones-rig/godray-level3-20261031'
PLATE = '/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png'
OUT = {'STANDARD': f'{R}/v5-opaque-split-standard-20261031.png',
       'AGX': f'{R}/v5-opaque-split-agx-control-20261031.png',
       'ACES13': f'{R}/v5-opaque-split-aces-control-20261031.png'}[mode]
BLEND = OUT.replace('.png', '.blend')
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.use_nodes = True
scene.render.use_compositing = True
scene.render.engine = 'CYCLES'
scene.render.compositor_device = 'CPU'
scene.cycles.device = 'CPU'
scene.cycles.samples = 1
scene.render.resolution_x = 1100
scene.render.resolution_y = 1500
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = OUT
scene.view_settings.view_transform = {'STANDARD': 'Standard', 'AGX': 'AgX', 'ACES13': 'ACES 1.3'}[mode]
scene.view_settings.look = 'None'
print("VIEW_TRANSFORM", scene.view_settings.view_transform)
tree = bpy.data.node_groups.new(f"GoldSplit_{mode}", "CompositorNodeTree")
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
plate = img("ArmsUpPlate_Untouched", PLATE, -1200, -500)
cur = over("Over_BG_Ground", bg, ground, -900, 300)
cur = over("Over_Cast", cur, cast, -600, 300)
cur = over("Over_Plate", cur, plate, -300, 300)
# seam-split bleed, gold left / cyan right, under the rims
cur = over("Over_BleedGoldLeft", cur, rim_layer("BleedGoldL", L3 + '/solid-goldbleed.png', R + '/bleed-gold-left.png', 0, -100), 0, 300)
cur = over("Over_BleedCyanRight", cur, rim_layer("BleedCyanR", L3 + '/solid-cyanbleed.png', R + '/bleed-cyan-right.png', 300, -100), 300, 300)
# spill on character, as in L3 (pre-clipped layers, under the rims)
cur = over("Over_SpillCyan", cur, img("SpillCyan", L3 + '/layer-spill-cyan.png', 0, -400), 600, 300)
cur = over("Over_SpillGold", cur, img("SpillGold", L3 + '/layer-spill-gold.png', 300, -400), 900, 300)
# OPAQUE split rims, alpha 1.0, zero left/right overlap, seam x=550
cur = over("Over_RimInnerGoldL", cur, rim_layer("RimInnerGoldL", L3 + '/solid-gold.png', R + '/opaque-inner-left.png', 1200, -100), 1200, 300)
cur = over("Over_RimInnerCyanR", cur, rim_layer("RimInnerCyanR", L3 + '/solid-cyan.png', R + '/opaque-inner-right.png', 1500, -100), 1500, 300)
cur = over("Over_RimOuterGoldL", cur, rim_layer("RimOuterGoldL", L3 + '/solid-gold.png', R + '/opaque-outer-left.png', 1800, -100), 1800, 300)
cur = over("Over_RimOuterCyanR", cur, rim_layer("RimOuterCyanR", L3 + '/solid-cyan.png', R + '/opaque-outer-right.png', 2100, -100), 2100, 300)

if mode == "STANDARD":
    # Cyan-side-only bloom: Glare branch, then SetAlpha to seam-right mask,
    # then over onto the finished composite. Gold side never sees cyan bloom.
    glare = nodes.new("CompositorNodeGlare"); glare.name = "BloomCyanSideOnly"; glare.location = (2400, 300)
    try:
        glare.inputs['Threshold'].default_value = 0.80
        glare.inputs['Size'].default_value = 6.0
        glare.inputs['Strength'].default_value = 0.20
    except Exception as e:
        print("glare inputs note", e)
    links.new(cur.outputs['Image'], glare.inputs['Image'])
    seam = img("SeamRightMask", R + '/seam-right-mask.png', 2400, -400)
    sep = nodes.new("CompositorNodeSeparateColor"); sep.name = "SeamRight_sep"; sep.location = (2400, -200)
    links.new(seam.outputs['Image'], sep.inputs['Image'])
    seta = nodes.new("CompositorNodeSetAlpha"); seta.name = "BloomCyanSideOnly_masked"; seta.location = (2700, 300)
    links.new(glare.outputs['Image'], seta.inputs['Image'])
    links.new(sep.outputs['Alpha'], seta.inputs['Alpha'])
    final = over("Over_BloomCyanSideOnly", cur, seta, 3000, 300)
else:
    final = cur  # controls: no Glare, isolates view transform

out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (3300, 300)
links.new(final.outputs['Image'], out.inputs['Image'])
print("nodes:", [n.name for n in nodes])
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"rendering GoldSplit {mode} ...")
bpy.ops.render.render(write_still=True)
print(f"GoldSplit_{mode}_DONE", OUT)
