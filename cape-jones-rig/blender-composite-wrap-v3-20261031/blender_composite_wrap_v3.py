"""Blender compositor v3 — internal light + background upgrade + RIM LAYERING RULE.
Mars 17:01 CDT: upgrade background, make light affect COLOR ON HIM and put
SHADOWS on him around outlines, pec shadows / clothing folds / suit creases /
cape folds hit realistically. Open-source 2D relight approximation (see doc):
interior shading is done on the plate BEFORE compositing (fold-relief from
interior linework + directional cyan/gold gradient), because a flat 2D plate
has no normal/depth pass; a true per-fold normal pass needs a 3D rebuild
(Blender normal/depth render) — stated honestly in the doc, not faked.

RIM LAYERING RULE — CORRECTED 17:05 CDT (supersedes 17:02 reading):
Mars used "soft rim" and "soft halo" INTERCHANGEABLY — same thing, NOT two
layers. DEFAULT stack = HARD rim line (kept) + ONE soft layer (soft rim =
soft halo). Variants: hard+soft together (default), soft alone sometimes,
hard alone as control. EXPERIMENTAL ONLY: one test with soft rim on top of
a soft halo as two separate layers — shown to Mars, HE decides; NEVER the
default and NEVER presented as what he originally meant.
Stack order bottom->top: ground spill, HARD rim, SOFT rim, plate, inner wrap,
shaft haze. Hard = dilate 3, no blur, factor 0.85 (sharp, distinct).
Soft = dilate 6, blur 5, factor 0.60 (v2 soft rim) — plus, in the experimental
variant ONLY, an extra wider soft halo (dilate 12, blur 12, factor 0.30)
UNDER the soft rim.
Combined dual-light case only; gold-rim-alone is separate (still owed).
Blender 5.2.3 LTS output path (from v1/v2): CompositorNodeTree with interface
OUTPUT + NodeGroupOutput, render with use_compositing + write_still.
SetAlpha + AlphaOver only, never MixRGB Add with a small Factor image.
"""
import bpy

R = '/home/hatch/workspace/cape-jones-rig'
OUTDIR = R + '/blender-composite-wrap-v3-20261031'
BG = OUTDIR + '/scratch/bg-upgraded-v3b-20261031.png'
CYAN = R + '/blender-composite-fix-20261031/scratch/solid-cyan-640x360.png'
BRIGHT = OUTDIR + '/scratch/solid-brightcyan-640x360.png'
SCR = OUTDIR + '/scratch'


def img(nodes, path, name, x, y):
    n = nodes.new('CompositorNodeImage'); n.name = name; n.location = (x, y)
    n.image = bpy.data.images.load(path); return n


def mult(nodes, links, inp, factor, name, x, y):
    m = nodes.new('ShaderNodeMath'); m.name = name; m.location = (x, y)
    m.operation = 'MULTIPLY'; links.new(inp, m.inputs[0])
    m.inputs[1].default_value = factor; return m.outputs['Value']


def setalpha(nodes, links, image_out, alpha_out, name, x, y):
    s = nodes.new('CompositorNodeSetAlpha'); s.name = name; s.location = (x, y)
    links.new(image_out, s.inputs['Image']); links.new(alpha_out, s.inputs['Alpha'])
    return s.outputs['Image']


def alphaover(nodes, links, bg, fg, name, x, y):
    o = nodes.new('CompositorNodeAlphaOver'); o.name = name; o.location = (x, y)
    links.new(bg, o.inputs['Background']); links.new(fg, o.inputs['Foreground'])
    return o.outputs['Image']


def band(nodes, links, alpha, cyan_img, dil, blur, factor, tag, y, img_override=None):
    d = nodes.new('CompositorNodeDilateErode'); d.name = tag + '_Dilate'; d.location = (-150, y)
    d.inputs['Size'].default_value = dil; links.new(alpha, d.inputs['Mask'])
    cur = d.outputs['Mask']
    if blur:
        b = nodes.new('CompositorNodeBlur'); b.name = tag + '_Blur'; b.location = (100, y)
        b.inputs['Size'].default_value = (float(blur), float(blur)); links.new(cur, b.inputs['Image']); cur = b.outputs['Image']
    sub = nodes.new('ShaderNodeMath'); sub.name = tag + '_SubAlpha'; sub.location = (350, y)
    sub.operation = 'SUBTRACT'; links.new(cur, sub.inputs[0]); links.new(alpha, sub.inputs[1])
    fa = mult(nodes, links, sub.outputs['Value'], factor, tag + '_Factor', 600, y)
    src = img_override.outputs['Image'] if img_override is not None else cyan_img.outputs['Image']
    return setalpha(nodes, links, src, fa, tag + '_SetAlpha', 850, y), fa


def build(plate_path, out_path, blend_path, mode):
    # mode: 'full' hard+soft, 'soft' soft-only, 'hard' hard-only, 'exp' hard+halo+soft
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.use_nodes = True; scene.render.use_compositing = True
    scene.render.resolution_x = 640; scene.render.resolution_y = 360
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'; scene.render.filepath = out_path
    tree = bpy.data.node_groups.new('CapeJonesWrapV3', 'CompositorNodeTree')
    scene.compositing_node_group = tree
    tree.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    nodes = tree.nodes; links = tree.links
    bg = img(nodes, BG, 'BG_Upgraded_V3', -900, 300)
    gold = nodes.new('ShaderNodeMixRGB'); gold.name = 'GoldGrade_BG_Only'; gold.location = (-650, 300)
    gold.blend_type = 'MULTIPLY'; gold.inputs['Factor'].default_value = 1.0
    gold.inputs['Color2'].default_value = (1.0, 0.86, 0.64, 1.0)
    links.new(bg.outputs['Image'], gold.inputs['Color1']); cur = gold.outputs['Color']
    fg = img(nodes, plate_path, 'CharacterPlate_Shaded_V3', -900, -300)
    scale = nodes.new('CompositorNodeScale'); scale.name = 'Plate_Scale'; scale.location = (-650, -300)
    scale.inputs['Type'].default_value = 'Relative'; scale.inputs['X'].default_value = 0.213; scale.inputs['Y'].default_value = 0.213
    links.new(fg.outputs['Image'], scale.inputs['Image'])
    trans = nodes.new('CompositorNodeTransform'); trans.name = 'Plate_Translate'; trans.location = (-400, -300)
    trans.inputs['X'].default_value = 0; trans.inputs['Y'].default_value = 10
    links.new(scale.outputs['Image'], trans.inputs['Image'])
    sep = nodes.new('CompositorNodeSeparateColor'); sep.name = 'Plate_Alpha'; sep.location = (-400, -550)
    links.new(trans.outputs['Image'], sep.inputs['Image']); alpha = sep.outputs['Alpha']
    cyan_img = img(nodes, CYAN, 'SolidCyan', -400, -800)
    bright_img = img(nodes, BRIGHT, 'SolidBrightCyan_HardRim', -400, -1050)
    # ground spill (same as v2)
    spill, _ = band(nodes, links, alpha, cyan_img, 8, 6, 0.20, 'Spill', -800)
    tr = nodes.new('CompositorNodeTransform'); tr.name = 'Spill_ShiftDown'; tr.location = (1100, -800)
    tr.inputs['Y'].default_value = -12; links.new(spill, tr.inputs['Image'])
    cur = alphaover(nodes, links, cur, tr.outputs['Image'], 'Over_Spill', 1350, -800)
    soft_alpha = None
    if mode in ('full', 'hard', 'exp'):
        hard, _ = band(nodes, links, alpha, cyan_img, 3, 0, 0.90, 'HardRim', -550, img_override=bright_img)
        cur = alphaover(nodes, links, cur, hard, 'Over_HardRim', 1350, -550)
    if mode == 'exp':
        halo, _ = band(nodes, links, alpha, cyan_img, 12, 12, 0.30, 'SoftHalo_EXP', -1050)
        cur = alphaover(nodes, links, cur, halo, 'Over_SoftHalo_EXP', 1350, -1050)
    if mode in ('full', 'soft', 'exp'):
        soft, soft_alpha = band(nodes, links, alpha, cyan_img, 6, 5, 0.60, 'SoftRim', -1300)
        cur = alphaover(nodes, links, cur, soft, 'Over_SoftRim', 1350, -1300)
    cur = alphaover(nodes, links, cur, trans.outputs['Image'], 'Over_Plate', 1600, -300)
    # inner wrap (v2)
    ero = nodes.new('CompositorNodeDilateErode'); ero.name = 'Inner_Erode'; ero.location = (-150, -1550)
    ero.inputs['Size'].default_value = -8; links.new(alpha, ero.inputs['Mask'])
    bl = nodes.new('CompositorNodeBlur'); bl.name = 'Inner_Blur'; bl.location = (100, -1550)
    bl.inputs['Size'].default_value = (3.0, 3.0); links.new(ero.outputs['Mask'], bl.inputs['Image'])
    sub2 = nodes.new('ShaderNodeMath'); sub2.name = 'Inner_Sub'; sub2.location = (350, -1550)
    sub2.operation = 'SUBTRACT'; links.new(alpha, sub2.inputs[0]); links.new(bl.outputs['Image'], sub2.inputs[1])
    ia = mult(nodes, links, sub2.outputs['Value'], 0.35, 'Inner_Factor', 600, -1550)
    inner = setalpha(nodes, links, cyan_img.outputs['Image'], ia, 'Inner_SetAlpha', 850, -1550)
    cur = alphaover(nodes, links, cur, inner, 'Over_InnerWrap', 1600, -1550)
    # shaft haze masked to soft band (fall back to hard band if soft absent)
    haze_src = soft_alpha if soft_alpha is not None else ia
    blurb = nodes.new('CompositorNodeBlur'); blurb.name = 'Haze_Blur'; blurb.location = (100, -1800)
    blurb.inputs['Size'].default_value = (20.0, 20.0); links.new(gold.outputs['Color'], blurb.inputs['Image'])
    ha = mult(nodes, links, haze_src, 0.18, 'Haze_Factor', 350, -1800)
    haze = setalpha(nodes, links, blurb.outputs['Image'], ha, 'Haze_SetAlpha', 600, -1800)
    cur = alphaover(nodes, links, cur, haze, 'Over_Haze', 1600, -1800)
    out = nodes.new('NodeGroupOutput'); out.name = 'Output'; out.location = (1900, 0)
    links.new(cur, out.inputs['Image'])
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    bpy.ops.render.render(write_still=True); print('RENDERED', out_path)


JOBS = [
    ('apose', SCR + '/plate-apose-shaded-v3.png', 'full'),
    ('armsup', SCR + '/plate-armsup-shaded-v3.png', 'full'),
    ('fighting', SCR + '/plate-fighting-shaded-v3.png', 'full'),
    ('apose-soft-only', SCR + '/plate-apose-shaded-v3.png', 'soft'),
    ('apose-hard-only', SCR + '/plate-apose-shaded-v3.png', 'hard'),
    ('apose-exp-soft-on-halo', SCR + '/plate-apose-shaded-v3.png', 'exp'),
]
for name, plate, mode in JOBS:
    build(plate, f'{OUTDIR}/wrap-v3-{name}-20261031.png', f'{OUTDIR}/wrap-v3-{name}-20261031.blend', mode)
print('WRAP V3 DONE')
