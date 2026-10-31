"""
blender-proof-render-20261031.py — Blender 5.2.3 LTS ONLY (NOT 4.5.3).
Cape Jones Workstream E: Blender production render + ACES + compositing,
end-to-end proof shot. CPU render, modest resolution.

Run:
  blender --background --python blender-proof-render-20261031.py -- \
    <pose.png> <mode> <view_transform> <display_device> <out.png> <out.blend>
  mode: proof | mask | shadow
    proof: Level 2 v2 (Blender translation) — grade + bottom-band contact
           shadow + outer-only rim ADD + edge-band bleed SCREEN. NO god
           rays (Level 2 never has them), NO Glare/bloom (Level 3), NO .cube
           LUT node (Blender 5.2 compositor has none; the LUT file is
           recorded in a text block, NOT claimed as applied).
    mask:  grey-key mask diagnostic only (white silhouette on black).
    shadow: shadow-chain diagnostic only — background plate + shadow
           layer, NO graded character on top, so the shadow shape and
           position are fully visible (used to debug placement).

STANDING RULES ENFORCED HERE:
 - Label refusal: plate with >100 pure-red pixels (R>0.99, G<0.01, B<0.01
   in Blender's image.pixels buffer, which reads the PNG sRGB values
   directly — pure red is (1,0,0) in both sRGB and linear, so the gate
   is space-proof; pure-red count on the approved fighting pose = 0)
   REFUSES with SystemExit, no render. NOTE: the grey-key centre is NOT
   the pixel-buffer value (0.502) — compositor nodes run scene-linear,
   so the key centre is 0.216 (see GREY_CENTRE correction above).
 - Never recolour base art: the Character_untouched image node is never
   modified in place. Grade/rim/bleed/shadow are separate nodes layered
   OVER it. The background layer is the untouched plate itself, so the
   grey-128 background stays ungraded as a control (DIFFERS from PIL v2,
   which graded the whole plate including background — see report).
 - Level 2 v2 colours (RIM-COLOR-RULE, 2026-10-31): gain (1.10,0.95,0.70),
   rim warm amber sRGB (255,180,80), bleed orange sRGB (255,120,0),
   shadow cool blue-violet sRGB (40,40,90). Socket colours are stored
   LINEAR (sRGB->linear converted) because the compositor works in
   scene-linear and the view transform encodes back to display sRGB.
   Gain is a multiplier and is NOT converted.
 - Blender 5.2 API notes (verified by probe, 2026-10-31):
   * compositor tree = scene.compositing_node_group (CompositorNodeTree
     group); scene.node_tree does NOT exist; CompositorNodeComposite
     does NOT exist — Group Output is the output.
   * CompositorNodeMath / CompositorNodeMixRGB / CompositorNodeSepRGBA /
     CompositorNodeRGBCurve / CompositorNodeMix / CompositorNodeColorRamp
     are UNDEFINED in 5.2. Use ShaderNodeMath / ShaderNodeMixRGB /
     CompositorNodeSeparateColor instead.
   * Glare Type string is 'Fog Glow' (not 'FOG_GLOW'); not used here
     (Level 2 has no bloom), listed for the record.
   * Engine id is BLENDER_EEVEE (not BLENDER_EEVEE_NEXT) in 5.2.
   * View transforms available (sRGB display): Standard, ACES 1.3,
     ACES 2.0, AgX, False Color, Raw. Display devices include sRGB and
     Rec.1886 (BT.1886 ~2.4 gamma EOTF).
 - Blender differences from PIL v2, stated plainly (not hidden):
   * Grade/rim/bleed math runs in scene-linear, not PIL sRGB space, so
     measured output RGB differs from PIL v2 numbers; hue family is the
     same (R>G>B warm). Measured values are in the report, not claimed
     as a pixel match.
   * Rim/bleed are uniform (no lit-side left 1.0 -> right 0.3 fade):
     PIL v2's directional fade is OWED in the Blender stack.
   * Internal line light (PIL v2 dark-line tint) is NOT in this build:
     OWED. Shadow is a bottom-band blurred contact shape, NOT PIL v2's
     ellipse + two foot pads: geometry differs, colour/opacity family
     matches. Both are listed as owed refinements in the report.
"""
import sys, os, time

try:
    import bpy
except ImportError:
    raise SystemExit("This script must run inside Blender 5.2.3: blender --background --python blender-proof-render-20261031.py -- <args>")

GREY_CENTRE = 0.216   # Scene-LINEAR value of sRGB grey 128/255.
# CORRECTION (first mask run, 2026-10-31): Blender's image.pixels API
# reads the PNG sRGB buffer (grey 128 = 0.502), but compositor nodes
# operate scene-linear, where grey 128 = ((128/255+0.055)/1.055)**2.4
# = 0.216. Using 0.502 in the nodes keyed the BACKGROUND as foreground
# (background came out white, character speckled). 0.216 is the correct
# compositor-space centre; verified by the corrected mask run.
GREY_TOL = 0.044      # Linear equivalent of sRGB +/-12 around grey 128
                      # (linear 0.175..0.262, approx symmetric 0.044)
RED_LIMIT = 100

def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lin_rgb(r, g, b):
    return (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b), 1.0)

# Level 2 v2 coloured spec (linear socket values)
GAIN = (1.10, 0.95, 0.70, 1.0)
RIM_LIN = lin_rgb(255, 180, 80)
BLEED_LIN = lin_rgb(255, 120, 0)
SHADOW_LIN = lin_rgb(40, 40, 90)

def count_pure_red(img):
    px = img.pixels[:]
    red = 0
    for i in range(0, len(px), 4):
        if px[i] > 0.99 and px[i + 1] < 0.01 and px[i + 2] < 0.01:
            red += 1
    return red

def main():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    if len(argv) < 6:
        print("Usage: blender --background --python blender-proof-render-20261031.py -- <pose.png> <proof|mask> <view_transform> <display_device> <out.png> <out.blend>")
        raise SystemExit(2)
    pose_path, mode, view_transform, display_device, out_png, out_blend = argv[:6]
    # Blender background render CANNOT save to a './file.png' relative
    # path (Render error: No such file or directory — caught on the
    # first finals run, 2026-10-31). Force absolute paths here so any
    # caller, relative or absolute, renders correctly.
    pose_path = os.path.abspath(pose_path)
    out_png = os.path.abspath(out_png)
    out_blend = os.path.abspath(out_blend)
    if mode not in ("proof", "mask", "shadow"):
        raise SystemExit(f"unknown mode {mode}")
    if not os.path.exists(pose_path):
        raise SystemExit(f"pose not found: {pose_path}")

    t0 = time.time()
    # Factory reset FIRST: it clears all data, so any image loaded before
    # it would be removed (this bug was caught on the first mask run).
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # --- Label refusal gate (inside Blender, before any render) ---
    probe_img = bpy.data.images.load(pose_path)
    red = count_pure_red(probe_img)
    print(f"LABEL GATE: pure-red pixels in plate = {red} (limit {RED_LIMIT})")
    if red > RED_LIMIT:
        raise SystemExit(f"REFUSED: plate carries {red} red debug-label pixels (> {RED_LIMIT}). Use a clean plate.")
    W, H = probe_img.size
    print(f"PLATE: {pose_path} {W}x{H} colorspace={probe_img.colorspace_settings.name}")

    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 16
    scene.cycles.use_denoising = False
    # Modest CPU resolution: 60% of the 1100x1500 plate.
    scene.render.resolution_x = 660
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.filepath = out_png
    scene.view_settings.view_transform = view_transform
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    scene.display_settings.display_device = display_device
    scene.use_nodes = True
    tree = bpy.data.node_groups.new("CapeJonesBlenderProof", "CompositorNodeTree")
    scene.compositing_node_group = tree
    nodes, links = tree.nodes, tree.links
    nodes.clear()

    def node(ntype, name, x, y):
        n = nodes.new(ntype)
        n.name = name
        n.label = name
        n.location = (x, y)
        return n

    def math(op, name, x, y, v0=None, v1=None, l0=None, l1=None):
        n = node("ShaderNodeMath", name, x, y)
        n.operation = op
        if v0 is not None:
            n.inputs[0].default_value = v0
        if v1 is not None:
            n.inputs[1].default_value = v1
        if l0 is not None:
            links.new(l0, n.inputs[0])
        if l1 is not None:
            links.new(l1, n.inputs[1])
        return n

    def mix(blend, name, x, y, fac, c1_link=None, c2_rgb=None):
        n = node("ShaderNodeMixRGB", name, x, y)
        n.blend_type = blend
        n.inputs["Factor"].default_value = fac
        if c1_link is not None:
            links.new(c1_link, n.inputs["Color1"])
        if c2_rgb is not None:
            n.inputs["Color2"].default_value = c2_rgb
        return n

    char = node("CompositorNodeImage", "Character_untouched", -1200, 0)
    char.image = probe_img

    # --- Grey-key mask: max(|R-0.502|,|G-0.502|,|B-0.502|) > 0.047 ---
    sep = node("CompositorNodeSeparateColor", "Separate_R_G_B", -950, 0)
    links.new(char.outputs["Image"], sep.inputs["Image"])
    diffs = []
    for ch, cx in (("Red", -700), ("Green", -700), ("Blue", -700)):
        sub = math("SUBTRACT", f"KeyDiff_{ch}_sub", cx, 200, l0=sep.outputs[ch], v1=GREY_CENTRE)
        ab = math("ABSOLUTE", f"KeyDiff_{ch}_abs", cx + 150, 200, l0=sub.outputs["Value"])
        diffs.append(ab)
    max_rg = math("MAXIMUM", "KeyMax_RG", -400, 200, l0=diffs[0].outputs["Value"], l1=diffs[1].outputs["Value"])
    max_rgb = math("MAXIMUM", "KeyMax_RGB", -250, 200, l0=max_rg.outputs["Value"], l1=diffs[2].outputs["Value"])
    key_mask = math("GREATER_THAN", "KeyMask_grey128", -100, 200, l0=max_rgb.outputs["Value"], v1=GREY_TOL)

    # Feather mask 1-2px: VALUE -> Blur (RGBA) -> Separate -> Red channel.
    blur = node("CompositorNodeBlur", "KeyMask_Blur", 50, 200)
    blur.inputs[1].default_value = (1.5, 1.5)
    links.new(key_mask.outputs["Value"], blur.inputs["Image"])
    sep_blur = node("CompositorNodeSeparateColor", "KeyMask_Blurred_R", 200, 200)
    links.new(blur.outputs["Image"], sep_blur.inputs["Image"])
    feathered = sep_blur.outputs["Red"]

    char_keyed = node("CompositorNodeSetAlpha", "Character_keyed", 350, 200)
    links.new(char.outputs["Image"], char_keyed.inputs["Image"])
    links.new(feathered, char_keyed.inputs["Alpha"])

    if mode == "mask":
        # White silhouette on black: solid white, keyed alpha, over black bg.
        white = mix("MIX", "Mask_WhiteSolid", 500, 200, 1.0, c2_rgb=(1.0, 1.0, 1.0, 1.0))
        white.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
        masked = node("CompositorNodeSetAlpha", "Mask_Silhouette", 650, 200)
        links.new(white.outputs["Color"], masked.inputs["Image"])
        links.new(feathered, masked.inputs["Alpha"])
        black = mix("MIX", "Mask_BlackBg", 500, -100, 1.0, c2_rgb=(0.0, 0.0, 0.0, 1.0))
        black.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
        over = node("CompositorNodeAlphaOver", "Mask_OverBlack", 800, 200)
        links.new(black.outputs["Color"], over.inputs["Background"])
        links.new(masked.outputs["Image"], over.inputs["Foreground"])
        last, last_out = over, "Image"
    else:
        # --- Proof stack ---
        # 1. Background = untouched plate (grey stays ungraded, control).
        # 2. Shadow: FULL-SIZE squashed + blurred ground shadow, solid
        #    blue-violet, 0.35 opacity, under the character.
        #    HISTORY (2026-10-31, measured, not guessed): the Crop
        #    bottom-band feet-pads approach FAILED in Blender 5.2's
        #    compositor size handling — try1: AlphaOver centred the
        #    1100x320 strip at waist height (two pads floating at
        #    mid-torso, verified by try1-vs-try2 pixel diff: 2,687
        #    pixels in waist band y 358-418); try2: translating the
        #    small strip clipped it out entirely (try2-vs-try3 pixel
        #    diff = 0.0, shadow contributed zero pixels); try3:
        #    canvas+translate also contributed zero pixels. Root cause
        #    is small-image placement in this compositor version, so
        #    this build uses FULL-SIZE nodes only, whose behaviour was
        #    PROVEN by diagnostic: Scale anchors at canvas CENTRE
        #    (Y 0.25 shape landed y 374-533 output, centre 453) and
        #    Translate Y negative moves DOWN (Y -50 full-res moved the
        #    silhouette down 30 output px, measured against the true
        #    plate bbox x 182-499 / y 152-776). Chain: solid hue with
        #    keyed alpha -> Scale Y 0.22 (centred squash) -> Blur 20
        #    -> opacity 0.35 -> Translate Y -475 full-res (squashed
        #    centre 453 output -> feet centre ~738 output; -475 =
        #    -285 output px down) -> under character. HONEST LIMIT:
        #    this is a squashed+blurred ground blob, NOT PIL v2's
        #    ellipse + two foot pads — pads geometry is still OWED.
        solid = mix("MIX", "Shadow_SolidHue", 500, -500, 1.0, c2_rgb=SHADOW_LIN)
        solid.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
        shadow = node("CompositorNodeSetAlpha", "Shadow_Solid", 650, -300)
        links.new(solid.outputs["Color"], shadow.inputs["Image"])
        links.new(key_mask.outputs["Value"], shadow.inputs["Alpha"])
        squash = node("CompositorNodeScale", "Shadow_SquashY022", 800, -300)
        squash.inputs["Type"].default_value = 'Relative'
        squash.inputs["X"].default_value = 1.0
        squash.inputs["Y"].default_value = 0.22
        links.new(shadow.outputs["Image"], squash.inputs["Image"])
        sblur = node("CompositorNodeBlur", "Shadow_Blur20", 950, -300)
        sblur.inputs[1].default_value = (20.0, 20.0)
        links.new(squash.outputs["Image"], sblur.inputs["Image"])
        ssep = node("CompositorNodeSeparateColor", "Shadow_Alpha", 1100, -300)
        links.new(sblur.outputs["Image"], ssep.inputs["Image"])
        sop = math("MULTIPLY", "Shadow_Opacity035", 1250, -300, l0=ssep.outputs["Alpha"], v1=0.35)
        shadow2 = node("CompositorNodeSetAlpha", "Shadow_Solid_Blurred", 1400, -300)
        links.new(sblur.outputs["Image"], shadow2.inputs["Image"])
        links.new(sop.outputs["Value"], shadow2.inputs["Alpha"])
        shadow_move = node("CompositorNodeTranslate", "Shadow_TranslateToFeet", 1550, -300)
        shadow_move.inputs["X"].default_value = 0.0
        shadow_move.inputs["Y"].default_value = -475.0
        links.new(shadow2.outputs["Image"], shadow_move.inputs["Image"])
        over_shadow = node("CompositorNodeAlphaOver", "AlphaOver_shadow_under", 1700, 0)
        links.new(char.outputs["Image"], over_shadow.inputs["Background"])
        links.new(shadow_move.outputs["Image"], over_shadow.inputs["Foreground"])
        # 3. Graded character over shadow.
        graded = mix("MULTIPLY", "Grade_Gain_110_095_070", 1780, 200, 1.0,
                     c1_link=char_keyed.outputs["Image"], c2_rgb=GAIN)
        over_char = node("CompositorNodeAlphaOver", "AlphaOver_graded_character", 1930, 0)
        links.new(over_shadow.outputs["Image"], over_char.inputs["Background"])
        links.new(graded.outputs["Color"], over_char.inputs["Foreground"])
        last, last_out = over_char, "Image"
        # 4. Rim outer-only ADD, warm amber, 3px at full res.
        dil3 = node("CompositorNodeDilateErode", "Rim_Dilate3", 2080, 400)
        dil3.inputs["Size"].default_value = 3
        links.new(key_mask.outputs["Value"], dil3.inputs["Mask"])
        rim_sub = math("SUBTRACT", "Rim_SubtractOriginal", 2230, 400,
                       l0=dil3.outputs["Mask"], l1=key_mask.outputs["Value"])
        rim = node("ShaderNodeMixRGB", "Rim_Add_warm_amber", 2380, 400)
        rim.blend_type = "ADD"
        links.new(rim_sub.outputs["Value"], rim.inputs["Factor"])
        links.new(last.outputs[last_out], rim.inputs["Color1"])
        rim.inputs["Color2"].default_value = RIM_LIN
        last, last_out = rim, "Color"
        # 5. Bleed edge-band SCREEN, orange, band 3..8px, 0.20.
        dil8 = node("CompositorNodeDilateErode", "Bleed_Dilate8", 2080, 650)
        dil8.inputs["Size"].default_value = 8
        links.new(key_mask.outputs["Value"], dil8.inputs["Mask"])
        bleed_sub = math("SUBTRACT", "Bleed_SubtractRim", 2230, 650,
                         l0=dil8.outputs["Mask"], l1=dil3.outputs["Mask"])
        bleed_op = math("MULTIPLY", "Bleed_Opacity020", 2380, 650,
                        l0=bleed_sub.outputs["Value"], v1=0.20)
        bleed = node("ShaderNodeMixRGB", "Bleed_Screen_orange", 2530, 650)
        bleed.blend_type = "SCREEN"
        links.new(bleed_op.outputs["Value"], bleed.inputs["Factor"])
        links.new(last.outputs[last_out], bleed.inputs["Color1"])
        bleed.inputs["Color2"].default_value = BLEED_LIN
        last, last_out = bleed, "Color"
        if mode == "shadow":
            # Diagnostic override: graded/rim/bleed nodes above are built
            # but unused in this mode. Output is a PLAIN GREY background
            # + shadow layer only (NOT the character plate, which would
            # hide the shadow again) — so shape/position are fully visible.
            grey = mix("MIX", "ShadowDiag_GreyBg", 2600, -300, 1.0,
                       c2_rgb=(0.216, 0.216, 0.216, 1.0))
            grey.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
            diag = node("CompositorNodeAlphaOver", "ShadowDiag_OverGrey", 2750, -300)
            links.new(grey.outputs["Color"], diag.inputs["Background"])
            links.new(shadow_move.outputs["Image"], diag.inputs["Foreground"])
            last, last_out = diag, "Image"

    # Final scale to render resolution (60% of plate).
    scale = node("CompositorNodeScale", "Output_Scale_060", 2730, 200)
    scale.inputs["Type"].default_value = 'Relative'
    scale.inputs["X"].default_value = 0.6
    scale.inputs["Y"].default_value = 0.6
    links.new(last.outputs[last_out], scale.inputs["Image"])

    tree.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    out = nodes.new("NodeGroupOutput")
    out.name = "Output"
    out.location = (2930, 200)
    links.new(scale.outputs["Image"], out.inputs["Image"])

    txt_name = "SHOT_SPEC"
    txt = bpy.data.texts.new(txt_name) if txt_name not in bpy.data.texts else bpy.data.texts[txt_name]
    txt.clear()
    txt.write(
        f"Mode: {mode}\nPose (clean, label-gate passed, pure-red={red}): {pose_path}\n"
        f"View: {view_transform} / Display: {display_device} / Exposure 0 / Gamma 1\n"
        f"Grade: gain (1.10,0.95,0.70) linear, character layer only; grey background ungraded (control).\n"
        f"Rim: outer-only 3px ADD warm amber sRGB (255,180,80) [linear socket]; uniform, no lit-side fade (owed).\n"
        f"Bleed: band 3..8px SCREEN orange sRGB (255,120,0) [linear socket] x 0.20, edge band only.\n"
        f"Shadow: FULL-SIZE squashed (Y 0.22, centred) + blurred (20px) ground shadow,\n"
        f"blue-violet (40,40,90) x 0.35, translated to feet (Y -475 full-res).\n"
        f"NOT PIL v2 ellipse+two-pads geometry — pads geometry is OWED.\n"
        f"NOT in this build: god rays (Level 2 never has them), Glare/bloom (Level 3),\n"
        f".cube LUT node (none exists in Blender 5.2 compositor), internal line light (owed),\n"
        f"lit-side rim/bleed fade (owed), PIL ellipse+two-pad shadow geometry (geometry differs).\n"
        f"Base art: Character_untouched node never modified in place. No labels in finals.\n"
        f"PROOF SHOT ONLY — not Mars-approved. Engine: BLENDER_EEVEE CPU, 660x900.\n"
    )
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    print(f"NODES: {len(nodes)} LINKS: {len(links)}")
    print(f"NODE NAMES: {[n.name for n in nodes]}")
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t0
    print(f"RENDERED: {out_png} in {dt:.1f}s exists={os.path.exists(out_png)} size={os.path.getsize(out_png) if os.path.exists(out_png) else 0}")
    print(f"BLEND: {out_blend}")

if __name__ == "__main__":
    main()
