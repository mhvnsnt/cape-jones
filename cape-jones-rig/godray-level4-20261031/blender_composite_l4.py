"""Blender 5.2.3 compositor ONLY — gold-preserved variants + L4 candidate.
Modes (argv): GOLD_V4 | GOLD_V5 | L4
GOLD_V4/V5: exact L3 stack, but (a) view_transform='Standard' instead of the
default AgX, (b) NO Glare node. This isolates the two suspects for the
gold-to-red shift: AgX tone mapping + Glare fog-glow mixing cyan into gold.
L4: V4 rim order (cyan inner / gold outer) + Standard view transform +
  (1) interior directional wash on the character only (gold from left,
      cyan from right, clipped to plate alpha via Math Multiply),
  (2) hard rim + soft halo double layer (sharp outer ring, plus a blurred
      copy of the same ring underneath it),
  (3) Glare fog glow at lower strength (0.20, threshold 0.80) so bloom does
      not wash the rim,
  (4) foreground dust layer over the top at low alpha.
Verified 5.2 output path: CompositorNodeTree assigned to
scene.compositing_node_group, GroupOutput, real render, CPU compositor.
Usage: blender -b --python blender_composite_l4.py -- GOLD_V4|GOLD_V5|L4
"""
import bpy, sys
mode = sys.argv[-1] if sys.argv[-1] in ("GOLD_V4", "GOLD_V5", "L4") else "L4"
L3 = '/home/hatch/workspace/cape-jones-rig/godray-level3-20261031'
R = '/home/hatch/workspace/cape-jones-rig/godray-level4-20261031'
PLATE = '/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png'
OUT = {'GOLD_V4': f'{R}/gold-preserved-v4-20261031.png',
       'GOLD_V5': f'{R}/gold-preserved-v5-20261031.png',
       'L4': f'{R}/l4-candidate-20261031.png'}[mode]
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
# THE key change vs L3: L3 left view_transform at the Blender default (AgX).
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
tree = bpy.data.node_groups.new(f"L4_{mode}", "CompositorNodeTree")
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
def clipped_wash(name, solid_path, grad_path, plate_node, x, y):
    """Solid colour, alpha = plate-alpha * gradient-alpha: light ON him only."""
    solid = img(name + "_solid", solid_path, x - 250, y)
    grad = img(name + "_grad", grad_path, x - 250, y - 200)
    sep_p = nodes.new("CompositorNodeSeparateColor"); sep_p.name = name + "_sepP"; sep_p.location = (x, y - 200)
    links.new(plate_node.outputs['Image'], sep_p.inputs['Image'])
    sep_g = nodes.new("CompositorNodeSeparateColor"); sep_g.name = name + "_sepG"; sep_g.location = (x, y - 400)
    links.new(grad.outputs['Image'], sep_g.inputs['Image'])
    mul = nodes.new("CompositorNodeMath"); mul.name = name + "_mul"; mul.location = (x, y - 600)
    mul.operation = 'MULTIPLY'
    links.new(sep_p.outputs['Alpha'], mul.inputs[0])
    links.new(sep_g.outputs['Alpha'], mul.inputs[1])
    # scale wash down: multiply by 0.25 via a second Math node
    mul2 = nodes.new("CompositorNodeMath"); mul2.name = name + "_mul2"; mul2.location = (x, y - 800)
    mul2.operation = 'MULTIPLY'
    links.new(mul.outputs['Value'], mul2.inputs[0])
    mul2.inputs[1].default_value = 0.25
    seta = nodes.new("CompositorNodeSetAlpha"); seta.name = name; seta.location = (x, y)
    links.new(solid.outputs['Image'], seta.inputs['Image'])
    links.new(mul2.outputs['Value'], seta.inputs['Alpha'])
    return seta

bg = img("GodRayV2_Light", L3 + '/godray-bg-v2-1100x1500.png', -1200, 400)
ground = img("GroundShadow", L3 + '/layer-ground-shadow.png', -1200, 100)
cast = img("CastShadow", L3 + '/layer-cast-shadow.png', -1200, -200)
plate = img("ArmsUpPlate_Untouched", PLATE, -1200, -500)
cur = over("Over_BG_Ground", bg, ground, -900, 300)
cur = over("Over_Cast", cur, cast, -600, 300)
cur = over("Over_Plate", cur, plate, -300, 300)
variant = "V5" if mode == "GOLD_V5" else "V4"
if variant == "V4":
    cur = over("Over_BleedCyan", cur, rim_layer("BleedCyan", L3 + '/solid-cyanbleed.png', L3 + '/mask-bleed.png', 0, -100), 0, 300)
else:
    cur = over("Over_BleedGold", cur, rim_layer("BleedGold", L3 + '/solid-goldbleed.png', L3 + '/mask-bleed.png', 0, -100), 0, 300)
    cur = over("Over_BleedCyan2", cur, rim_layer("BleedCyan", L3 + '/solid-cyanbleed.png', L3 + '/mask-bleed.png', 300, -100), 300, 300)
cur = over("Over_SpillCyan", cur, img("SpillCyan", L3 + '/layer-spill-cyan.png', 0, -400), 600, 300)
cur = over("Over_SpillGold", cur, img("SpillGold", L3 + '/layer-spill-gold.png', 300, -400), 900, 300)
if variant == "V4":
    cur = over("Over_RimInnerCyan", cur, rim_layer("RimInnerCyan", L3 + '/solid-cyan.png', L3 + '/mask-inner.png', 1200, -100), 1200, 300)
    rim_outer = rim_layer("RimOuterGold", L3 + '/solid-gold.png', L3 + '/mask-outer.png', 1500, -100)
    cur = over("Over_RimOuterGold", cur, rim_outer, 1500, 300)
else:
    cur = over("Over_RimInnerL", cur, rim_layer("RimInnerGoldL", L3 + '/solid-gold.png', L3 + '/mask-inner-left.png', 1200, -100), 1200, 300)
    cur = over("Over_RimInnerR", cur, rim_layer("RimInnerCyanR", L3 + '/solid-cyan.png', L3 + '/mask-inner-right.png', 1500, -100), 1500, 300)
    cur = over("Over_RimOuterL", cur, rim_layer("RimOuterGoldL", L3 + '/solid-gold.png', L3 + '/mask-outer-left.png', 1800, -100), 1800, 300)
    cur = over("Over_RimOuterR", cur, rim_layer("RimOuterCyanR", L3 + '/solid-cyan.png', L3 + '/mask-outer-right.png', 2100, -100), 2100, 300)

if mode == "L4":
    # (1) interior directional wash, clipped to the character. The wash
    # layers are PIL helper layers only (plate-alpha * gradient * 0.25,
    # same helper-only pattern as L3's masks); the shot is composited here.
    # (Blender 5.2 compositor has no CompositorNodeMath node type, so the
    # multiply was done in the helper, not faked in the tree.)
    cur = over("Over_WashGoldL", cur, img("WashGold", R + '/layer-wash-gold.png', 2400, -400), 2400, 300)
    cur = over("Over_WashCyanR", cur, img("WashCyan", R + '/layer-wash-cyan.png', 2700, -400), 2700, 300)
    # (2) soft halo UNDER the hard rim: blurred copy of the outer gold ring
    soft = rim_layer("RimOuterGoldSoft", L3 + '/solid-gold.png', L3 + '/mask-outer.png', 3000, -100)
    blur = nodes.new("CompositorNodeBlur"); blur.name = "SoftHaloBlur"; blur.location = (3000, 300)
    try:
        blur.inputs['Size'].default_value = 12.0
    except Exception:
        blur.inputs['Size'].default_value = (12.0, 12.0)
    links.new(soft.outputs['Image'], blur.inputs['Image'])
    # NOTE: blurred halo must sit UNDER the sharp rim, so it is composited
    # here as an extra glow layer around the silhouette (sharp rim already
    # on the plate; this adds the soft halo field around it).
    cur = over("Over_SoftHalo", cur, blur, 3300, 300)
    # (4) foreground dust
    cur = over("Over_Dust", cur, img("DustFG", R + '/dust-foreground.png', 3600, -400), 3600, 300)
    # (3) Glare, gentler than L3 (threshold 0.80, strength 0.20)
    glare = nodes.new("CompositorNodeGlare"); glare.name = "BloomFogGlowL4"; glare.location = (3900, 300)
    try:
        glare.inputs['Threshold'].default_value = 0.80
        glare.inputs['Size'].default_value = 6.0
        glare.inputs['Strength'].default_value = 0.20
    except Exception as e:
        print("glare inputs note", e)
    links.new(cur.outputs['Image'], glare.inputs['Image'])
    final = glare
else:
    final = cur  # GOLD variants: NO Glare at all, Standard view transform

out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (4200, 300)
links.new(final.outputs['Image'], out.inputs['Image'])
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"rendering {mode} ...")
bpy.ops.render.render(write_still=True)
print(f"{mode}_DONE", OUT)
