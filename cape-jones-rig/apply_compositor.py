#!/usr/bin/env python3
"""
apply_compositor.py — wired compositor stack for Cape Jones.
Reads compositor-stack-spec.json in the same directory.
Source: COLOR-LIGHTING-COMPOSITING-RESEARCH-20261031.md (10 sections),
COMPOSITING-LIGHTING-SPEC.md, COLOR-KEY-VFX-STACK-10.md.

Layer order (names match the spec, and the Blender node tree):
 1_background, 2_color_key_tint_background_only, 3_fog_per_plane_background_only,
 4_wet_reflection_under_character, 5_hard_shadow_under_character,
 6_character_untouched, 7_internal_light_Screen, 8_internal_shadow_Multiply,
 9_rim_outer_only_Add, 10_bleed_edge_band_Screen,
 11_bloom_glow_Add_existing_bright_areas_only, 12_god_rays_Screen_gradient,
 13_contact_strip_darkest_at_feet, 14_foreground_none,
 15_LUT_trilinear, 16_delivery_JPG_sRGB

Standing rules, enforced in code:
 - Base art is never recoloured: the rig layer is copied, light/shadow/rim/bleed
   are separate layers composited over it.
 - Rim is outer-only, 2-4 px, dilated alpha minus original alpha, Add.
   No inner outline.
 - Bleed is an outer edge band only (rim_px to rim_px+8), Screen, low opacity.
   Never a whole-suit tint.
 - Shadow hue is cool blue-violet, not black. Contact strip darkest at feet.
 - God rays are gradient-falloff shafts, Screen ~20%, not flat cones.
 - Wet reflection is a flipped duplicate, gradient fade, blur, floor-gated.
   Where no wet floor is established, it is SKIPPED and logged, not faked.
 - LUT: the actual .cube file is applied by trilinear interpolation.
   LUTs in showcase/luts-30/ are templates, not final approved grades.
 - This is a pipeline test, not a final shot: the v6 apose source carries
   red rig-label circles (ARM/LEG labels). They are NOT painted over here.

Usage:
  python3 apply_compositor.py --condition daylight
  python3 apply_compositor.py --all
Output: showcase/composited-<condition>-20261031.jpg
"""
import argparse, json, math, os, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

HERE = Path(__file__).resolve().parent
SPEC = HERE / "compositor-stack-spec.json"
BG_CANDIDATES = [
    Path.home() / "workspace/cape-jones-flying/characters/sheets/backgrounds",
    HERE / "backgrounds",
]
OUT_DIR = HERE / "showcase"


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def find_bg(name):
    for d in BG_CANDIDATES:
        p = d / name
        if p.exists():
            return p
    raise FileNotFoundError(f"background {name} not found in {BG_CANDIDATES}")


def chroma_key_grey(rig_path):
    """Transparent v6 rig: grey 128 background -> alpha 0. Nothing else changed."""
    im = Image.open(rig_path).convert("RGB")
    arr = np.array(im).astype(int)
    grey = np.all(np.abs(arr - 128) < 12, axis=2)
    alpha = np.where(grey, 0, 255).astype(np.uint8)
    rgba = np.dstack([arr, alpha]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def screen(a, b):
    # a, b: float arrays 0..1, same shape
    return 1.0 - (1.0 - a) * (1.0 - b)


def multiply(a, b):
    return a * b


def dilate_alpha(alpha, px):
    if px <= 0:
        return alpha.copy()
    return ndimage.binary_dilation(alpha > 0, iterations=px)


def parse_cube(path):
    size = None
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("LUT_3D_SIZE"):
                size = int(line.split()[1])
                continue
            if line.startswith(("DOMAIN_", "TITLE", "LUT_1D", "LUT_3D")):
                continue
            parts = line.split()
            if len(parts) == 3:
                rows.append([float(x) for x in parts])
    if size is None or len(rows) != size ** 3:
        raise ValueError(f"bad .cube {path}: size={size} rows={len(rows)}")
    # .cube order: R fastest, then G, then B -> reshape (B, G, R, 3)
    lut = np.array(rows, dtype=np.float32).reshape(size, size, size, 3)
    return lut, size


def apply_lut_chunked(img_rgb, lut, size):
    """Trilinear .cube application, row-chunked to bound memory."""
    arr = img_rgb.astype(np.float32) / 255.0
    out = np.empty_like(arr)
    scale = size - 1
    for y0 in range(0, arr.shape[0], 128):
        chunk = arr[y0:y0 + 128]
        x = chunk * scale
        x0 = np.floor(x).astype(np.int32)
        x1 = np.minimum(x0 + 1, scale)
        f = x - x0
        # x channels are (R, G, B) -> lut axes are (B, G, R)
        r0, g0, b0 = x0[..., 0], x0[..., 1], x0[..., 2]
        r1, g1, b1 = x1[..., 0], x1[..., 1], x1[..., 2]
        fr, fg, fb = f[..., 0], f[..., 1], f[..., 2]
        acc = np.zeros_like(chunk)
        for db, wb in ((b0, 1 - fb), (b1, fb)):
            for dg, wg in ((g0, 1 - fg), (g1, fg)):
                for dr, wr in ((r0, 1 - fr), (r1, fr)):
                    w = (wb * wg * wr)[..., None]
                    acc += w * lut[db, dg, dr]
        out[y0:y0 + 128] = acc
    return np.clip(out * 255.0, 0, 255).astype(np.uint8)


def _ground_shadow_alpha(rig_alpha, bbox_canvas, floor_y, W, H):
    """Flatten character alpha to a ground shadow at floor_y."""
    x0, y0, x1, y1 = bbox_canvas
    out = np.zeros_like(rig_alpha)
    region = rig_alpha[y0:y1, x0:x1]
    if region.size == 0:
        return out
    img = Image.fromarray((region * 255).astype(np.uint8))
    squashed = img.resize((img.size[0], max(2, int(img.size[1] * 0.25))), Image.BILINEAR)
    # Paste squashed shadow with its top at floor_y - 6, offset +24 px in x.
    sy0 = max(0, floor_y - 6)
    sy1 = min(H, sy0 + squashed.size[1])
    sx0 = min(W - 1, x0 + 24)
    sx1 = min(W, sx0 + squashed.size[0])
    crop = np.array(squashed)[:sy1 - sy0, :sx1 - sx0] / 255.0
    out[sy0:sy1, sx0:sx1] = np.maximum(out[sy0:sy1, sx0:sx1], crop)
    return out


def composite_condition(name, cond, verbose=True):
    log = []
    bg = Image.open(find_bg(cond["background"])).convert("RGB").resize((1168, 784))
    W, H = bg.size
    bg_arr = np.array(bg).astype(np.float32) / 255.0

    # 2_color_key_tint_background_only: LUT multiplier on background only.
    mult = np.array(cond["lut_multiplier"], dtype=np.float32)
    bg_arr = np.clip(bg_arr * mult, 0, 1)
    log.append(f"color_key_tint background multiplier {cond['lut_multiplier']}")

    # 3_fog_per_plane_background_only: far band strongest, near band weakest.
    fog_rgb = np.array(hex_rgb(cond["fog_color"]), dtype=np.float32) / 255.0
    fog_op = cond["fog_opacity"]
    for (y_frac0, y_frac1, strength) in [(0.0, 0.45, 1.0), (0.45, 0.75, 0.55), (0.75, 1.0, 0.15)]:
        y0, y1 = int(H * y_frac0), int(H * y_frac1)
        a = fog_op * strength
        bg_arr[y0:y1] = bg_arr[y0:y1] * (1 - a) + fog_rgb * a
    log.append(f"fog per-plane opacity {fog_op}, colour {cond['fog_color']}")

    # Rig placement: scale to 520 px tall, feet (alpha bbox bottom) at floor_y.
    rig = chroma_key_grey(HERE / "reposes/joint-apose-v6-20261031.png")
    scale = 520 / rig.size[1]
    rig = rig.resize((int(rig.size[0] * scale), 520), Image.LANCZOS)
    alpha = np.array(rig)[:, :, 3] > 10
    ys, xs = np.where(alpha)
    bbox = (xs.min(), ys.min(), xs.max(), ys.max())  # in rig-local coords
    floor_y = int(H * cond["floor_y_fraction"])
    paste_x = int(W / 2 - rig.size[0] / 2)
    paste_y = floor_y - bbox[3]
    _bbox_canvas = (bbox[0] + paste_x, bbox[1] + paste_y, bbox[2] + paste_x, bbox[3] + paste_y)
    log.append(f"rig placed: paste=({paste_x},{paste_y}) bbox_bottom->floor_y={floor_y}")

    # Full-canvas rig layer (character, untouched) and its alpha.
    canvas_rig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas_rig.paste(rig, (paste_x, paste_y), rig)
    rig_arr = np.array(canvas_rig).astype(np.float32)
    rig_alpha = rig_arr[:, :, 3] / 255.0
    rig_rgb = rig_arr[:, :, :3] / 255.0

    comp = bg_arr.copy()  # start from background

    # 4_wet_reflection_under_character (floor-gated, ~30% wet, gradient + blur)
    if cond["wet_opacity"] > 0:
        # Build a flipped rig image whose top aligns with floor_y, then fade it.
        flip_img = rig.transpose(Image.FLIP_TOP_BOTTOM)
        # rig bbox top in flipped image corresponds to original bbox bottom.
        flip_top = floor_y
        flip_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        flip_canvas.paste(flip_img, (paste_x, flip_top - (flip_img.size[1] - bbox[3])), flip_img)
        flip_canvas = flip_canvas.filter(ImageFilter.GaussianBlur(4))  # progressive blur, draft approx.
        fa = np.array(flip_canvas).astype(np.float32)
        fa_alpha = fa[:, :, 3] / 255.0
        # Gradient fade: 1.0 at floor_y -> 0 at bottom of frame.
        grad = np.clip(1.0 - (np.arange(H)[:, None] - floor_y) / max(1, H - floor_y), 0, 1)
        grad = np.where(np.arange(H)[:, None] < floor_y, 0, grad)
        a = fa_alpha * grad * cond["wet_opacity"]
        comp = comp * (1 - a[..., None]) + (fa[:, :, :3] / 255.0) * a[..., None]
        log.append(f"wet_reflection applied opacity {cond['wet_opacity']} floor_y {floor_y}")
    else:
        log.append("wet_reflection SKIPPED: no wet floor established for this condition")

    # 5_hard_shadow_under_character: GROUND shadow, not a duplicate ghost.
    # Flatten the silhouette vertically (0.25x) and lay it at the feet, offset
    # slightly in the light direction. A full offset duplicate read as a ghost
    # on bright backgrounds in the first run, so it was replaced.
    shadow_hue = np.array(hex_rgb(cond["shadow_hue"]), dtype=np.float32) / 255.0
    shadow_alpha = np.zeros_like(rig_alpha)
    # Use rig-local bbox (defined after rig placement, before this block in
    # the original order this code runs after placement, so bbox exists).
    char_alpha_img = Image.fromarray((rig_alpha * 255).astype(np.uint8))
    # bbox in canvas coords is computed below; to avoid ordering issues, the
    shadow_alpha = _ground_shadow_alpha(rig_alpha, _bbox_canvas, floor_y, W, H)
    shadow_alpha = ndimage.gaussian_filter(shadow_alpha, 3)
    a = shadow_alpha * cond["shadow_opacity"]
    comp = comp * (1 - a[..., None]) + shadow_hue * a[..., None]
    log.append(f"hard_shadow ground-flattened hue {cond['shadow_hue']} opacity {cond['shadow_opacity']} at floor_y {floor_y}")

    # 6_character_untouched
    comp = comp * (1 - rig_alpha[..., None]) + rig_rgb * rig_alpha[..., None]
    log.append("character composited untouched (copy, not modified in place)")

    # 7_internal_light_Screen + 8_internal_shadow_Multiply, masked to lit side.
    # Lit-side mask: horizontal ramp across the character bbox.
    x0, y0, x1, y1 = bbox[0] + paste_x, bbox[1] + paste_y, bbox[2] + paste_x, bbox[3] + paste_y
    width = max(1, x1 - x0)
    ramp = np.zeros((H, W), dtype=np.float32)
    xs_grid = np.arange(W, dtype=np.float32)
    if cond["light_side"] == "left":
        ramp_vals = np.clip(1.0 - (xs_grid - x0) / width, 0, 1)
    else:
        ramp_vals = np.clip((xs_grid - x0) / width, 0, 1)
    ramp[:] = ramp_vals[None, :]
    light_rgb = np.array(hex_rgb(cond["light_color"]), dtype=np.float32) / 255.0
    light_a = rig_alpha * ramp * cond["light_opacity"]
    # Screen blend of the light layer over the composite, masked:
    # screen(comp, light) weighted by light_a:
    comp = comp * (1 - light_a[..., None]) + screen(comp, np.tile(light_rgb, (H, W, 1))) * light_a[..., None]
    shadow_a = rig_alpha * (1 - ramp) * cond["shadow_opacity"] * 0.6
    shadow_col = np.array(hex_rgb(cond["shadow_hue"]), dtype=np.float32) / 255.0
    comp = comp * (1 - shadow_a[..., None]) + multiply(comp, np.tile(shadow_col, (H, W, 1))) * shadow_a[..., None]
    log.append(f"internal_light Screen {cond['light_color']} {cond['light_opacity']} side {cond['light_side']}; internal_shadow Multiply {cond['shadow_hue']}")

    # 9_rim_outer_only_Add: dilated alpha minus original, 2-4 px.
    rim_px = int(cond["rim_px"])
    dilated = dilate_alpha(rig_alpha, rim_px)
    rim_mask = dilated & (rig_alpha <= 0.5)
    rim_rgb = np.array(hex_rgb(cond["rim_color"]), dtype=np.float32) / 255.0
    rim_a = rim_mask.astype(np.float32)
    comp = np.clip(comp + rim_rgb * rim_a[..., None], 0, 1)
    log.append(f"rim outer-only {rim_px}px {cond['rim_color']} Add")

    # 10_bleed_edge_band_Screen: rim_px to rim_px+8 outer band only.
    dilated_b = dilate_alpha(rig_alpha, rim_px + 5)
    bleed_mask = dilated_b & (~dilated)
    bleed_rgb = np.array(hex_rgb(cond["bleed_color"]), dtype=np.float32) / 255.0
    bleed_a = bleed_mask.astype(np.float32) * cond["bleed_opacity"]
    comp = comp * (1 - bleed_a[..., None]) + screen(comp, np.tile(bleed_rgb, (H, W, 1))) * bleed_a[..., None]
    log.append(f"bleed edge-band Screen {cond['bleed_color']} {cond['bleed_opacity']}")

    # 11_bloom_glow_Add_existing_bright_areas_only: blur of bright pixels, Add, low.
    bright = np.clip((comp - 0.75) / 0.25, 0, 1)
    bloom = ndimage.gaussian_filter(bright, 6)
    comp = np.clip(comp + bloom * cond["bloom_opacity"], 0, 1)
    log.append(f"bloom/glow Add existing bright areas only {cond['bloom_opacity']} (no fake blast art)")

    # 12_god_rays_Screen_gradient_falloff (gated)
    if cond["god_ray_opacity"] > 0:
        ray_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ray_layer)
        ray_rgb = hex_rgb(cond["god_ray_color"])
        for (top_x, bottom_x) in [(int(W * 0.30), int(W * 0.42)), (int(W * 0.55), int(W * 0.68))]:
            d.polygon([(top_x, 0), (top_x + 60, 0), (bottom_x + 140, H), (bottom_x - 60, H)],
                      fill=ray_rgb + (255,))
        ray_layer = ray_layer.filter(ImageFilter.GaussianBlur(10))
        ra = np.array(ray_layer).astype(np.float32)
        # Gradient falloff along length: strong at top, fading to 0 at bottom.
        grad = np.clip(1.0 - np.arange(H)[:, None] / H, 0, 1) ** 1.5
        ra_a = (ra[:, :, 3] / 255.0) * grad * cond["god_ray_opacity"]
        comp = comp * (1 - ra_a[..., None]) + screen(comp, np.tile(np.array(ray_rgb, dtype=np.float32) / 255.0, (H, W, 1))) * ra_a[..., None]
        log.append(f"god_rays gradient Screen {cond['god_ray_color']} {cond['god_ray_opacity']}")
    else:
        log.append("god_rays SKIPPED: no volumetric source established for this condition")

    # 13_contact_strip_darkest_at_feet: two pads under the feet only.
    # A full-width bar read as a black plank in the first run, so it was replaced.
    strip = np.zeros((H, W), dtype=np.float32)
    bw = max(1, x1 - x0)
    for centre_frac in (0.38, 0.62):
        cx = int(x0 + bw * centre_frac)
        hw = int(bw * 0.11)
        strip[max(0, floor_y - 3):floor_y + 5, max(0, cx - hw):cx + hw] = 0.4
    strip = ndimage.gaussian_filter(strip, 1.5)
    comp = comp * (1 - strip[..., None]) + multiply(comp, np.tile(shadow_hue, (H, W, 1))) * strip[..., None]
    log.append("contact_strip two foot pads darkest at feet (Multiply, 0.4, blurred)")

    # 15_LUT_trilinear (actual .cube)
    lut_path = HERE / cond["lut"]
    lut, size = parse_cube(lut_path)
    out_rgb = apply_lut_chunked((np.clip(comp, 0, 1) * 255).astype(np.uint8), lut, size)
    log.append(f"LUT applied {cond['lut']} size {size} trilinear (template, not final approved)")

    out = Image.fromarray(out_rgb, "RGB")
    out_path = OUT_DIR / f"composited-{name}-20261031.jpg"
    out.save(out_path, quality=92)
    if verbose:
        print(f"{name}: {out_path} ({out.size})")
        for line in log:
            print(f"  - {line}")
    return out_path, log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    spec = json.loads(SPEC.read_text())
    conds = spec["conditions"]
    if args.all:
        names = sorted(conds)
    elif args.condition:
        names = [args.condition]
    else:
        names = ["daylight"]
    for name in names:
        if name not in conds:
            print(f"unknown condition {name}; known: {sorted(conds)}", file=sys.stderr)
            sys.exit(2)
        composite_condition(name, conds[name])


if __name__ == "__main__":
    main()
