"""Wrap v4 stage 3 — Blender 5.2.3 compositor final, full height 1100x1500.
Known-good 5.2 path (from v1/v2/v3): CompositorNodeTree via
scene.compositing_node_group, NodeGroupOutput, render with use_compositing +
write_still. SetAlpha + AlphaOver only, never MixRGB Add with a small
Factor image. Shaft layer is screen-blended (MixRGB SCREEN) over the bg —
dark shaft background drops out, bright Cycles shafts + dust stay.
Rim (corrected rule): HARD rim (dilate 3, no blur, 0.90, bright near-white
cyan) + ONE soft layer (soft rim = soft halo, dilate 6, blur 5, 0.60).
Soft rim AND inner wrap are SIDE-WEIGHTED: their ring alpha is multiplied
by the sideweight map (normal-from-depth diffuse_back), so the backlit
side is genuinely stronger. Hard rim stays unweighted (sharp core).
Stack bottom->top: upgraded bg -> screen shafts -> ground spill ->
hard rim -> side-weighted soft rim -> relit plate -> side-weighted inner
wrap -> shaft haze masked to soft band.
Modes: 'full' = final; 'norim' = same bg+shafts+relit plate, NO rim/wrap
(for the rim-only proof); 'plateonly' is not needed — interior proof is
computed in numpy (relit vs original plate, inside alpha only).
"""
import bpy

R = '/home/hatch/workspace/cape-jones-rig'
OUTDIR = R + '/blender-composite-wrap-v4-20261031'
SCR = OUTDIR + '/scratch'
BG = SCR + '/bg-upgraded-v4-1100x1500.png'
SHAFTS = SCR + '/shafts-cycles-v4-1100x1500.png'
CYAN = SCR + '/solid-cyan-1100x1500.png'
BRIGHT = SCR + '/solid-brightcyan-1100x1500.png'

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

def band(nodes, links, alpha, cyan_img, dil, blur, factor, tag, y, weight=None):
    d = nodes.new('CompositorNodeDilateErode'); d.name = tag + '_Dilate'; d.location = (-150, y)
    d.inputs['Size'].default_value = dil; links.new(alpha, d.inputs['Mask'])
    cur = d.outputs['Mask']
    if blur:
        b = nodes.new('CompositorNodeBlur'); b.name = tag + '_Blur'; b.location = (100, y)
        b.inputs['Size'].default_value = (float(blur), float(blur)); links.new(cur, b.inputs['Image']); cur = b.outputs['Image']
    sub = nodes.new('ShaderNodeMath'); sub.name = tag + '_SubAlpha'; sub.location = (350, y)
    sub.operation = 'SUBTRACT'; links.new(cur, sub.inputs[0]); links.new(alpha, sub.inputs[1])
    fa = mult(nodes, links, sub.outputs['Value'], factor, tag + '_Factor', 600, y)
    if weight is not None:
        # side-weight: ring alpha * (0.30 + 0.70*sideweight) so backlit side wins
        sc = nodes.new('ShaderNodeMath'); sc.name = tag + '_WeightScale'; sc.location = (600, y - 120)
        sc.operation = 'MULTIPLY'; links.new(weight, sc.inputs[0]); sc.inputs[1].default_value = 0.70
        ad = nodes.new('ShaderNodeMath'); ad.name = tag + '_WeightAdd'; ad.location = (850, y - 120)
        ad.operation = 'ADD'; links.new(sc.outputs['Value'], ad.inputs[0]); ad.inputs[1].default_value = 0.30
        mw = nodes.new('ShaderNodeMath'); mw.name = tag + '_WeightMult'; mw.location = (1100, y - 120)
        mw.operation = 'MULTIPLY'; links.new(fa, mw.inputs[0]); links.new(ad.outputs['Value'], mw.inputs[1])
        fa = mw.outputs['Value']
    return setalpha(nodes, links, cyan_img.outputs['Image'], fa, tag + '_SetAlpha', 850, y), fa

def build(plate_path, sideweight_path, out_path, blend_path, mode):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.use_nodes = True; scene.render.use_compositing = True
    scene.render.resolution_x = 1100; scene.render.resolution_y = 1500
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'; scene.render.filepath = out_path
    tree = bpy.data.node_groups.new('CapeJonesWrapV4', 'CompositorNodeTree')
    scene.compositing_node_group = tree
    tree.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    nodes = tree.nodes; links = tree.links
    bg = img(nodes, BG, 'BG_Upgraded_V4', -900, 300)
    sh = img(nodes, SHAFTS, 'Shafts_Cycles_V4', -900, 100)
    scrn = nodes.new('ShaderNodeMixRGB'); scrn.name = 'Screen_Shafts'; scrn.location = (-650, 200)
    scrn.blend_type = 'SCREEN'; scrn.inputs['Factor'].default_value = 1.0
    links.new(bg.outputs['Image'], scrn.inputs['Color1']); links.new(sh.outputs['Image'], scrn.inputs['Color2'])
    cur = scrn.outputs['Color']
    fg = img(nodes, plate_path, 'CharacterPlate_Relit_V4', -900, -300)
    sep = nodes.new('CompositorNodeSeparateColor'); sep.name = 'Plate_Alpha'; sep.location = (-650, -550)
    links.new(fg.outputs['Image'], sep.inputs['Image']); alpha = sep.outputs['Alpha']
    cyan_img = img(nodes, CYAN, 'SolidCyan', -400, -800)
    bright_img = img(nodes, BRIGHT, 'SolidBrightCyan_HardRim', -400, -1050)
    sw = None
    if mode == 'full':
        swimg = img(nodes, sideweight_path, 'SideWeight_Map', -400, -1300)
        swsep = nodes.new('CompositorNodeSeparateColor'); swsep.name = 'SideWeight_Sep'; swsep.location = (-150, -1300)
        links.new(swimg.outputs['Image'], swsep.inputs['Image']); sw = swsep.outputs['Red']
    if mode == 'full':
        spill, _ = band(nodes, links, alpha, cyan_img, 8, 6, 0.20, 'Spill', -800, weight=sw)
        tr = nodes.new('CompositorNodeTransform'); tr.name = 'Spill_ShiftDown'; tr.location = (1100, -800)
        tr.inputs['Y'].default_value = -12; links.new(spill, tr.inputs['Image'])
        cur = alphaover(nodes, links, cur, tr.outputs['Image'], 'Over_Spill', 1350, -800)
        hard, _ = band(nodes, links, alpha, cyan_img, 3, 0, 0.90, 'HardRim', -550, img_override=None) if False else (None, None)
        # hard rim with bright image: rebuild band manually to pass img_override
        d = nodes.new('CompositorNodeDilateErode'); d.name = 'HardRim_Dilate'; d.location = (-150, -550)
        d.inputs['Size'].default_value = 3; links.new(alpha, d.inputs['Mask'])
        sub = nodes.new('ShaderNodeMath'); sub.name = 'HardRim_SubAlpha'; sub.location = (350, -550)
        sub.operation = 'SUBTRACT'; links.new(d.outputs['Mask'], sub.inputs[0]); links.new(alpha, sub.inputs[1])
        fa = mult(nodes, links, sub.outputs['Value'], 0.90, 'HardRim_Factor', 600, -550)
        hard = setalpha(nodes, links, bright_img.outputs['Image'], fa, 'HardRim_SetAlpha', 850, -550)
        cur = alphaover(nodes, links, cur, hard, 'Over_HardRim', 1350, -550)
        soft, soft_alpha = band(nodes, links, alpha, cyan_img, 6, 5, 0.60, 'SoftRim', -1300, weight=sw)
        cur = alphaover(nodes, links, cur, soft, 'Over_SoftRim', 1350, -1300)
    cur = alphaover(nodes, links, cur, fg.outputs['Image'], 'Over_Plate', 1600, -300)
    if mode == 'full':
        ero = nodes.new('CompositorNodeDilateErode'); ero.name = 'Inner_Erode'; ero.location = (-150, -1550)
        ero.inputs['Size'].default_value = -8; links.new(alpha, ero.inputs['Mask'])
        bl = nodes.new('CompositorNodeBlur'); bl.name = 'Inner_Blur'; bl.location = (100, -1550)
        bl.inputs['Size'].default_value = (3.0, 3.0); links.new(ero.outputs['Mask'], bl.inputs['Image'])
        sub2 = nodes.new('ShaderNodeMath'); sub2.name = 'Inner_Sub'; sub2.location = (350, -1550)
        sub2.operation = 'SUBTRACT'; links.new(alpha, sub2.inputs[0]); links.new(bl.outputs['Image'], sub2.inputs[1])
        ia = mult(nodes, links, sub2.outputs['Value'], 0.35, 'Inner_Factor', 600, -1550)
        # side-weight inner wrap too
        sc = nodes.new('ShaderNodeMath'); sc.name = 'Inner_WeightScale'; sc.location = (600, -1670)
        sc.operation = 'MULTIPLY'; links.new(sw, sc.inputs[0]); sc.inputs[1].default_value = 0.70
        ad = nodes.new('ShaderNodeMath'); ad.name = 'Inner_WeightAdd'; ad.location = (850, -1670)
        ad.operation = 'ADD'; links.new(sc.outputs['Value'], ad.inputs[0]); ad.inputs[1].default_value = 0.30
        mw = nodes.new('ShaderNodeMath'); mw.name = 'Inner_WeightMult'; mw.location = (1100, -1670)
        mw.operation = 'MULTIPLY'; links.new(ia, mw.inputs[0]); links.new(ad.outputs['Value'], mw.inputs[1])
        inner = setalpha(nodes, links, cyan_img.outputs['Image'], mw.outputs['Value'], 'Inner_SetAlpha', 850, -1550)
        cur = alphaover(nodes, links, cur, inner, 'Over_InnerWrap', 1600, -1550)
        blurb = nodes.new('CompositorNodeBlur'); blurb.name = 'Haze_Blur'; blurb.location = (100, -1800)
        blurb.inputs['Size'].default_value = (20.0, 20.0); links.new(scrn.outputs['Color'], blurb.inputs['Image'])
        ha = mult(nodes, links, soft_alpha, 0.18, 'Haze_Factor', 350, -1800)
        haze = setalpha(nodes, links, blurb.outputs['Image'], ha, 'Haze_SetAlpha', 600, -1800)
        cur = alphaover(nodes, links, cur, haze, 'Over_Haze', 1600, -1800)
    out = nodes.new('NodeGroupOutput'); out.name = 'Output'; out.location = (1900, 0)
    links.new(cur, out.inputs['Image'])
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    bpy.ops.render.render(write_still=True); print('RENDERED', out_path)

JOBS = [
    ('apose', SCR + '/plate-apose-relit-v4.png', SCR + '/sideweight-apose-v4.png', 'full'),
    ('armsup', SCR + '/plate-armsup-relit-v4.png', SCR + '/sideweight-armsup-v4.png', 'full'),
    ('fighting', SCR + '/plate-fighting-relit-v4.png', SCR + '/sideweight-fighting-v4.png', 'full'),
    ('apose-norim', SCR + '/plate-apose-relit-v4.png', None, 'norim'),
]
for name, plate, swp, mode in JOBS:
    build(plate, swp, f'{OUTDIR}/wrap-v4-{name}-20261031.png', f'{OUTDIR}/wrap-v4-{name}-20261031.blend', mode)
print('WRAP V4 DONE')
