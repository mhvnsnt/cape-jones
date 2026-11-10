"""Blender compositor v2 — light WRAP around the character, realistic.
Mars 2026-10-31 16:29 CDT: upgrade the composite even more, more
industry-standard stuff. Mars 16:30 CDT CORRECTION: "more realistic"
means the LIGHTING, EFFECTS and GOD RAYS — NOT the background itself.
So: the background / volumetric base is left EXACTLY as it was in v1
(same Cycles base file, same gold grade on background only). Only the
light coming around him is new: wrap, rim, spill, bleed, shaft haze.

Combined dual-light case ONLY (Mars 15:48 CDT): cyan backlight +
gold LUT/overlay combined. Gold rim alone gets NO cyan backlight;
that shot is separate and is NOT this file.

Blender 5.2.3 LTS output path (verified in v1):
- CompositorNodeComposite is UNDEFINED in 5.2. Use a
  CompositorNodeTree assigned to scene.compositing_node_group with
  an interface OUTPUT socket "Image" + NodeGroupOutput.
- Render with scene.render.use_compositing=True and
  bpy.ops.render.render(write_still=True); building/saving alone
  produces NO image.
- All wrap layers go through SetAlpha + AlphaOver (NOT MixRGB Add
  with a small Factor image — that cropped the canvas in v1).
- Dilate/Erode: Size positive = dilate, Size negative = erode
  (probed in 5.2.3). Blur: Gaussian, Size is a VECTOR socket.
- Base art is never recoloured: plate goes in untouched; gold tint
  is on the background only; cyan is only in wrap/spill/haze layers.
"""
import bpy

BASE = '/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/scratch/volumetric-base-20261031.png'
CYAN = '/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/scratch/solid-cyan-640x360.png'
OUTDIR = '/home/hatch/workspace/cape-jones-rig/blender-composite-wrap-v2-20261031'

POSES = [
    ('apose', '/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png'),
    ('armsup', '/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png'),
]


def img(nodes, path, name, x, y):
    n = nodes.new('CompositorNodeImage'); n.name = name; n.location = (x, y)
    n.image = bpy.data.images.load(path)
    return n


def math_mult(nodes, links, inp, factor, name, x, y):
    m = nodes.new('ShaderNodeMath'); m.name = name; m.location = (x, y)
    m.operation = 'MULTIPLY'
    links.new(inp, m.inputs[0])
    m.inputs[1].default_value = factor
    return m.outputs['Value']


def setalpha(nodes, links, image_out, alpha_out, name, x, y):
    s = nodes.new('CompositorNodeSetAlpha'); s.name = name; s.location = (x, y)
    links.new(image_out, s.inputs['Image'])
    links.new(alpha_out, s.inputs['Alpha'])
    return s.outputs['Image']


def alphaover(nodes, links, bg, fg, name, x, y):
    o = nodes.new('CompositorNodeAlphaOver'); o.name = name; o.location = (x, y)
    links.new(bg, o.inputs['Background'])
    links.new(fg, o.inputs['Foreground'])
    return o.outputs['Image']


def build(plate_path, out_path, blend_path, wrap):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.use_nodes = True
    scene.render.use_compositing = True
    scene.render.resolution_x = 640
    scene.render.resolution_y = 360
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = out_path

    tree = bpy.data.node_groups.new('CapeJonesWrapV2', 'CompositorNodeTree')
    scene.compositing_node_group = tree
    tree.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    nodes = tree.nodes; links = tree.links

    # --- Background, UNCHANGED from v1 (correction 16:30: do not repaint it)
    bg = img(nodes, BASE, 'VolumetricBase_V1_Unchanged', -900, 300)
    gold = nodes.new('ShaderNodeMixRGB'); gold.name = 'GoldGrade_BG_Only'; gold.location = (-650, 300)
    gold.blend_type = 'MULTIPLY'; gold.inputs['Factor'].default_value = 1.0
    gold.inputs['Color2'].default_value = (1.0, 0.86, 0.64, 1.0)
    links.new(bg.outputs['Image'], gold.inputs['Color1'])
    cur = gold.outputs['Color']

    # --- Plate, untouched, same scale/translate as v1 for comparability
    fg = img(nodes, PLATE_PATH, 'CharacterPlate_Untouched', -900, -300)
    scale = nodes.new('CompositorNodeScale'); scale.name = 'Plate_Scale'; scale.location = (-650, -300)
    scale.inputs['Type'].default_value = 'Relative'
    scale.inputs['X'].default_value = 0.213; scale.inputs['Y'].default_value = 0.213
    links.new(fg.outputs['Image'], scale.inputs['Image'])
    trans = nodes.new('CompositorNodeTransform'); trans.name = 'Plate_Translate'; trans.location = (-400, -300)
    trans.inputs['X'].default_value = 0; trans.inputs['Y'].default_value = 10
    links.new(scale.outputs['Image'], trans.inputs['Image'])

    sep = nodes.new('CompositorNodeSeparateColor'); sep.name = 'Plate_Alpha'; sep.location = (-400, -550)
    links.new(trans.outputs['Image'], sep.inputs['Image'])
    alpha = sep.outputs['Alpha']
    cyan_img = img(nodes, CYAN, 'SolidCyan_FullCanvas', -400, -800)

    if wrap:
        # --- 1. OUTER WRAP: dilate 14, blur 10 -> minus alpha = soft edge band.
        # Blur falloff = no hard halo; this is light bending around the
        # silhouette, not a flat rim line.
        dil = nodes.new('CompositorNodeDilateErode'); dil.name = 'Wrap_Dilate14'; dil.location = (-150, -550)
        dil.inputs['Size'].default_value = 6
        links.new(alpha, dil.inputs['Mask'])
        blur = nodes.new('CompositorNodeBlur'); blur.name = 'Wrap_Blur10'; blur.location = (100, -550)
        blur.inputs['Size'].default_value = (5.0, 5.0)
        links.new(dil.outputs['Mask'], blur.inputs['Image'])
        sub = nodes.new('ShaderNodeMath'); sub.name = 'Wrap_SubtractAlpha'; sub.location = (350, -550)
        sub.operation = 'SUBTRACT'
        links.new(blur.outputs['Image'], sub.inputs[0])
        links.new(alpha, sub.inputs[1])
        wrap_alpha = math_mult(nodes, links, sub.outputs['Value'], 0.60, 'Wrap_Falloff_0.60', 600, -550)
        wrap_img = setalpha(nodes, links, cyan_img.outputs['Image'], wrap_alpha, 'Wrap_SetAlpha', 850, -550)

        # --- 2. GROUND SPILL: dilated blurred alpha, shifted down, low alpha.
        # Cyan backlight pooling on the ground around his feet.
        dil2 = nodes.new('CompositorNodeDilateErode'); dil2.name = 'Spill_Dilate18'; dil2.location = (-150, -800)
        dil2.inputs['Size'].default_value = 8
        links.new(alpha, dil2.inputs['Mask'])
        blur2 = nodes.new('CompositorNodeBlur'); blur2.name = 'Spill_Blur12'; blur2.location = (100, -800)
        blur2.inputs['Size'].default_value = (6.0, 6.0)
        links.new(dil2.outputs['Mask'], blur2.inputs['Image'])
        spill_alpha = math_mult(nodes, links, blur2.outputs['Image'], 0.20, 'Spill_Falloff_0.20', 350, -800)
        spill_img = setalpha(nodes, links, cyan_img.outputs['Image'], spill_alpha, 'Spill_SetAlpha', 600, -800)
        tr = nodes.new('CompositorNodeTransform'); tr.name = 'Spill_ShiftDown'; tr.location = (850, -800)
        tr.inputs['X'].default_value = 0; tr.inputs['Y'].default_value = -12
        links.new(spill_img, tr.inputs['Image'])
        cur = alphaover(nodes, links, cur, tr.outputs['Image'], 'Over_GroundSpill', 1100, -800)
        cur = alphaover(nodes, links, cur, wrap_img, 'Over_OuterWrap', 1100, -550)

        # --- 3. PLATE over bg + spill + outer wrap (shafts occluded by body)
        cur = alphaover(nodes, links, cur, trans.outputs['Image'], 'Over_Plate', 1350, -300)

        # --- 4. INNER WRAP: light coming around ONTO front edge surfaces.
        # Erode 10, blur 4, alpha minus that = band just inside the edge.
        ero = nodes.new('CompositorNodeDilateErode'); ero.name = 'Inner_Erode10'; ero.location = (-150, -1050)
        ero.inputs['Size'].default_value = -8
        links.new(alpha, ero.inputs['Mask'])
        blur3 = nodes.new('CompositorNodeBlur'); blur3.name = 'Inner_Blur4'; blur3.location = (100, -1050)
        blur3.inputs['Size'].default_value = (3.0, 3.0)
        links.new(ero.outputs['Mask'], blur3.inputs['Image'])
        sub2 = nodes.new('ShaderNodeMath'); sub2.name = 'Inner_Subtract'; sub2.location = (350, -1050)
        sub2.operation = 'SUBTRACT'
        links.new(alpha, sub2.inputs[0])
        links.new(blur3.outputs['Image'], sub2.inputs[1])
        inner_alpha = math_mult(nodes, links, sub2.outputs['Value'], 0.35, 'Inner_Falloff_0.35', 600, -1050)
        inner_img = setalpha(nodes, links, cyan_img.outputs['Image'], inner_alpha, 'Inner_SetAlpha', 850, -1050)
        cur = alphaover(nodes, links, cur, inner_img, 'Over_InnerWrap', 1100, -1050)

        # --- 5. SHAFT HAZE: blurred background, masked to the outer wrap
        # band at low factor — atmospheric perspective, shafts appearing
        # to bend around the body rather than stop dead behind it.
        blurb = nodes.new('CompositorNodeBlur'); blurb.name = 'Haze_Blur20'; blurb.location = (100, -1300)
        blurb.inputs['Size'].default_value = (20.0, 20.0)
        links.new(gold.outputs['Color'], blurb.inputs['Image'])
        haze_alpha = math_mult(nodes, links, wrap_alpha, 0.18, 'Haze_Falloff_0.18', 350, -1300)
        haze_img = setalpha(nodes, links, blurb.outputs['Image'], haze_alpha, 'Haze_SetAlpha', 600, -1300)
        cur = alphaover(nodes, links, cur, haze_img, 'Over_ShaftHaze', 1100, -1300)
    else:
        # Control: plate over background only, no wrap/spill/haze.
        cur = alphaover(nodes, links, cur, trans.outputs['Image'], 'Over_Plate_Control', 1100, -300)

    out = nodes.new('NodeGroupOutput'); out.name = 'Output'; out.location = (1600, 0)
    links.new(cur, out.inputs['Image'])
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    bpy.ops.render.render(write_still=True)
    print('RENDERED', out_path)


for name, PLATE_PATH in POSES:
    build(PLATE_PATH, f'{OUTDIR}/wrap-v2-{name}-20261031.png',
          f'{OUTDIR}/wrap-v2-{name}-20261031.blend', wrap=True)
    build(PLATE_PATH, f'{OUTDIR}/control-no-wrap-{name}-20261031.png',
          f'{OUTDIR}/control-no-wrap-{name}-20261031.blend', wrap=False)
print('WRAP V2 DONE')
