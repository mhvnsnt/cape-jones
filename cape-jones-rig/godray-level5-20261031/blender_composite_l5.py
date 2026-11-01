"""Blender 5.2.3 compositor ONLY — L5 shot.
Modes (argv): L5 | L5_APOSE
L5 = ALL of L4, PLUS all of (L5 spec):
 1. Crisp distinct shafts: crisp-shaft background (hard-edged diagonal bands,
    2px feather) instead of soft v2 wash.
 2. Estimated-normal interior shading: per-pixel dot(N, light) layers built
    from the plate's own luminance gradient (shape-from-shading proxy, per
    the L5 spec's 'normal/depth pass or estimated normals'). Gold light from
    the left, cyan light from the right. NOT a flat gradient wash (L4).
 3. Side-weighted wrap: spill + outer rim alpha weighted 1.0 (backlit left)
    -> 0.35 (front right).
 4. Full colour tracking: measured after render into color-tracking-l5.json.
 5. Shot-to-shot consistency: same script/stack for L5 (arms-up) and
    L5_APOSE (apose, own silhouette rings); re-render must be pixel-identical.
View transform: Standard (gold preserved, as in L4). Glare gentler: 0.85/0.15.
Verified 5.2 output path: scene.compositing_node_group, GroupOutput,
real render, CPU compositor.
Usage: blender -b --python blender_composite_l5.py -- L5|L5_APOSE
"""
import bpy, sys
mode = sys.argv[-1] if sys.argv[-1] in ("L5", "L5_APOSE") else "L5"
L3 = '/home/hatch/workspace/cape-jones-rig/godray-level3-20261031'
L4 = '/home/hatch/workspace/cape-jones-rig/godray-level4-20261031'
R = '/home/hatch/workspace/cape-jones-rig/godray-level5-20261031'
if mode == "L5":
    PLATE = '/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png'
    TAG, INNER, OUTER = 'armsup', L3 + '/mask-inner.png', L3 + '/mask-outer.png'
    SHADOWS = True
else:
    PLATE = '/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png'
    TAG, INNER, OUTER = 'apose', R + '/mask-inner-apose.png', R + '/mask-outer-apose.png'
    SHADOWS = False  # L3 ground/cast layers are arms-up geometry; apose uses pool only
OUT = f'{R}/l5-shot-{TAG.lower()}-20261031.png'
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
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
tree = bpy.data.node_groups.new(f"L5_{mode}", "CompositorNodeTree")
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

bg = img("CrispShaftBG", R + '/godray-bg-v3-crisp-1100x1500.png', -1200, 400)
cur = bg
if SHADOWS:
    cur = over("Over_Ground", cur, img("GroundShadow", L3 + '/layer-ground-shadow.png', -1200, 100), -900, 300)
    cur = over("Over_Cast", cur, img("CastShadow", L3 + '/layer-cast-shadow.png', -1200, -200), -600, 300)
plate = img("Plate_Untouched", PLATE, -1200, -500)
cur = over("Over_Plate", cur, plate, -300, 300)
# ground light pool (answers the shafts)
cur = over("Over_Pool", cur, img("GroundPool", R + '/ground-pool-l5.png', 0, -400), 0, 300)
# bleed (arms-up: L3 bleed mask; apose: own dilate-8 ring)
if SHADOWS:
    cur = over("Over_BleedCyan", cur, rim_layer("BleedCyan", L3 + '/solid-cyanbleed.png', L3 + '/mask-bleed.png', 300, -100), 300, 300)
else:
    cur = over("Over_BleedCyan", cur, rim_layer("BleedCyanApose", L3 + '/solid-cyanbleed.png', R + '/mask-bleed-apose.png', 300, -100), 300, 300)
cur = over("Over_SpillCyanSW", cur, img("SpillCyanSW", (R + '/spill-cyan-apose.png') if not SHADOWS else (R + '/spill-cyan-sideweighted.png'), 600, -400), 600, 300)
cur = over("Over_SpillGoldSW", cur, img("SpillGoldSW", (R + '/spill-gold-apose.png') if not SHADOWS else (R + '/spill-gold-sideweighted.png'), 900, -400), 900, 300)
# (2) estimated-normal interior shading, clipped to plate by construction
cur = over("Over_NormalGold", cur, img("NormalGold", R + f'/normal-shade-gold-{TAG}.png', 1200, -400), 1200, 300)
cur = over("Over_NormalCyan", cur, img("NormalCyan", R + f'/normal-shade-cyan-{TAG}.png', 1500, -400), 1500, 300)
# rim inner cyan / outer gold, outer ring SIDE-WEIGHTED for real:
# pre-built RGBA ring image (alpha already 1.0 left -> 0.35 right).
cur = over("Over_RimInnerCyan", cur, rim_layer("RimInnerCyan", L3 + '/solid-cyan.png', INNER, 1800, -100), 1800, 300)
cur = over("Over_RimOuterGoldSW", cur, img("RimOuterGoldSW", R + f'/rim-outer-gold-sideweighted-{TAG}.png', 2100, -100), 2100, 300)
# hard + soft double layer: blurred copy of outer ring as soft halo
soft = rim_layer("RimOuterGoldSoft", L3 + '/solid-gold.png', OUTER, 2400, -100)
blur = nodes.new("CompositorNodeBlur"); blur.name = "SoftHaloBlur"; blur.location = (2400, 300)
try:
    blur.inputs['Size'].default_value = 12.0
except Exception:
    blur.inputs['Size'].default_value = (12.0, 12.0)
links.new(soft.outputs['Image'], blur.inputs['Image'])
cur = over("Over_SoftHalo", cur, blur, 2700, 300)
# foreground dust
cur = over("Over_Dust", cur, img("DustFG", R + '/dust-foreground-l5.png', 3000, -400), 3000, 300)
# gentler Glare than L4 (0.85 / 0.15)
glare = nodes.new("CompositorNodeGlare"); glare.name = "BloomFogGlowL5"; glare.location = (3300, 300)
try:
    glare.inputs['Threshold'].default_value = 0.85
    glare.inputs['Size'].default_value = 6.0
    glare.inputs['Strength'].default_value = 0.15
except Exception as e:
    print("glare inputs note", e)
links.new(cur.outputs['Image'], glare.inputs['Image'])
out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (3600, 300)
links.new(glare.outputs['Image'], out.inputs['Image'])
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"rendering {mode} ...")
bpy.ops.render.render(write_still=True)
print(f"{mode}_DONE", OUT)
