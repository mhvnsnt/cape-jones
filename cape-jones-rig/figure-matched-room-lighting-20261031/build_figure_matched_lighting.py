"""Figure-matched room lighting for Cape Jones.
Base art is NEVER recoloured in place: lighting lives on separate layers
(tint, shadow, line-light, interior sheen, outer rim, bounce, glow) composited
over a copy of the clean base plate. Base file itself is untouched.
Comic-book / high-quality 2D TV method, implemented in PIL/numpy:
 - three-point lighting, rim follows key colour (RIM-COLOR-RULE, hue +-20deg)
 - cel shading bands by light factor, not a flat tint wash
 - ink-line lighting: thin ink band (ink within 3px of non-ink) is recoloured
   toward rim on the light side and toward shadow on the away side, so pec,
   rib, muscle, clothing-wrinkle and cowl lines carry the light
 - form sheen: inside-edge band on the light side, following contours
 - ground bounce for pool rooms, bloom proxy for glare room
No vendor render is claimed: Blender Cycles / Harmony / AE methods are
documented as mappings where not run; the PIL code below is the RUN part.
"""
import json, os, shutil
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.expanduser('~/workspace/cape-jones-rig/figure-matched-room-lighting-20261031/')
SHAFT = os.path.expanduser('~/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/')
OLD = os.path.expanduser('~/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/')
PAD = 80

def load_rgba(p):
    return np.array(Image.open(p).convert('RGBA')).astype(np.float32)

def save(arr, p):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA').save(p)

def pad(arr, pad=PAD):
    return np.pad(arr, ((pad, pad), (pad, pad), (0, 0)), mode='constant')

def dilate(mask, n):
    return ndimage.binary_dilation(mask, iterations=n)

def room_background(kind, colour, size=(1100, 1500)):
    """Simple measured room: vertical gradient + soft light column in colour.
    Only used for colour scenarios; shafts rooms use their real renders."""
    h, w = size[1], size[0]
    yy = np.linspace(0, 1, h)[:, None]
    base = np.zeros((h, w, 3), np.float32)
    c = np.array(colour, np.float32)
    for ch in range(3):
        base[:, :, ch] = (18 + 30 * yy) * (c[ch] / 128.0 + 0.4)
    xx = np.linspace(0, 1, w)[None, :]
    col = np.exp(-((xx - 0.5) ** 2) / 0.08) * (1.0 - 0.4 * yy)
    for ch in range(3):
        base[:, :, ch] += col * c[ch] * 0.55
    return np.clip(base, 0, 255)

def light_figure(base, spec):
    """Returns (lit_figure_rgba_padded, layer_stats, layer_images_dict)."""
    fig = pad(base)  # H,W,4 float
    alpha = fig[:, :, 3] / 255.0
    mask = alpha > 0.05
    rgb = fig[:, :, :3].copy()
    H, W = mask.shape
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    yn = (np.arange(H)[:, None] - y0) / max(1, (y1 - y0))  # 0 top .. 1 bottom
    xn = (np.arange(W)[None, :] - x0) / max(1, (x1 - x0))
    # ---- light factor per direction ----
    d = spec['direction']
    if d == 'overhead':
        lf = 1.0 - 0.85 * yn
    elif d == 'overhead_centre':
        lf = (1.0 - 0.85 * yn) * (0.75 + 0.45 * np.exp(-((xn - 0.5) ** 2) / 0.12))
    elif d == 'front':
        lf = 0.85 + 0.15 * (1 - yn)
    elif d == 'back':
        # backlight: light at silhouette, away from centre
        dist_bg = ndimage.distance_transform_edt(mask)
        edge = np.clip(1.0 - dist_bg / 40.0, 0, 1)
        lf = 0.35 + 0.65 * edge
    elif d == 'cool_front':
        lf = 0.80 + 0.20 * (1 - yn)
    else:
        lf = 1.0 - 0.5 * yn
    lf = np.clip(lf, 0, 1)
    lf = np.broadcast_to(lf, (H, W)).copy()
    # ---- ink band: dark pixels within 3px of a non-dark pixel ----
    ink = mask & (rgb.sum(axis=2) < 240)
    nonink = ~ink
    dist_nonink = ndimage.distance_transform_edt(ink)  # 0 outside ink? edt of ink gives dist to 0 (non-ink) for ink px
    # distance_transform_edt(ink) returns distance to nearest 0 for non-zero px
    line_band = ink & (dist_nonink <= 3.0)
    # ---- tint + cel shading on non-ink interior ----
    gain = np.array(spec['gain'], np.float32)
    tint = rgb * gain[None, None, :]
    # cel bands: quantise light factor into 3 steps for comic cel read
    cel = np.where(lf > 0.66, 1.12, np.where(lf > 0.33, 0.92, 0.72))
    shaded = tint * cel[:, :, None]
    # shadow colour on away side
    sh = np.array(spec['shadow'], np.float32)
    shadow_w = np.clip((0.45 - lf) / 0.45, 0, 1) * 0.45
    shaded = shaded * (1 - shadow_w[:, :, None]) + sh[None, None, :] * shadow_w[:, :, None] * 0.6
    out = rgb.copy()
    out[mask & ~line_band] = shaded[mask & ~line_band]
    # ---- line-light: ink band recoloured toward rim / shadow by light ----
    rim = np.array(spec['rim'], np.float32)
    line_strength = np.clip(lf * 1.15, 0, 1)
    lit_line = rgb * 0.25 + rim[None, None, :] * 0.75
    dark_line = rgb * 0.6 + sh[None, None, :] * 0.4
    line_out = lit_line * line_strength[:, :, None] + dark_line * (1 - line_strength[:, :, None])
    # blend line band strongly toward lit/dark line (0.8) so lines visibly carry light
    out[line_band] = out[line_band] * 0.2 + line_out[line_band] * 0.8
    # ---- interior sheen: inside-edge band on light side ----
    dist_bg = ndimage.distance_transform_edt(mask)
    sheen_band = mask & (dist_bg <= 14)
    sheen_w = np.clip(lf, 0, 1) * 0.38
    out[sheen_band] = out[sheen_band] * (1 - sheen_w[sheen_band][:, None]) + rim[None, None, :] * sheen_w[sheen_band][:, None]
    # ---- ground bounce (pools room only) ----
    if spec.get('bounce'):
        bcol = np.array(spec['bounce'], np.float32)
        bw = np.clip((yn - 0.72) / 0.28, 0, 1) * 0.45
        bw = np.broadcast_to(bw, (H, W)).copy()
        out[mask] = out[mask] * (1 - bw[mask][:, None]) + bcol[None, None, :] * bw[mask][:, None]
    # ---- outer rim ----
    rim_mask = dilate(mask, 6) & ~mask
    rim_alpha = np.zeros((H, W), np.float32)
    if d in ('overhead', 'overhead_centre'):
        rw = np.clip(1.1 - yn, 0, 1)
    elif d == 'back':
        rw = np.ones_like(yn)
    else:
        rw = 0.85 + 0.15 * (1 - yn)
    rw = np.broadcast_to(rw, (H, W)).copy()
    rim_alpha[rim_mask] = 235 * rw[rim_mask]
    # glow (glare room): blurred rim+sheen
    glow = None
    if spec.get('glow'):
        g = np.zeros((H, W, 4), np.float32)
        g[:, :, :3] = rim
        g[:, :, 3] = rim_alpha * 0.6
        glow = np.array(Image.fromarray(np.clip(g, 0, 255).astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
    # composite: base lit figure, then glow behind rim? glow over figure edge only
    res = np.zeros((H, W, 4), np.float32)
    res[:, :, :3] = out
    res[:, :, 3] = fig[:, :, 3]
    if glow is not None:
        ga = (glow[:, :, 3] / 255.0) * 0.55
        res[:, :, :3] = res[:, :, :3] * (1 - ga[:, :, None]) + glow[:, :, :3] * ga[:, :, None]
        res[:, :, 3] = np.maximum(res[:, :, 3], glow[:, :, 3] * 0.55)
    # outer rim on top
    ra = rim_alpha / 255.0
    res[:, :, :3] = res[:, :, :3] * (1 - ra[:, :, None]) + rim[None, None, :] * ra[:, :, None]
    res[:, :, 3] = np.maximum(res[:, :, 3], rim_alpha)
    stats = {
        'figure_alpha_px': int(mask.sum()),
        'line_band_px': int(line_band.sum()),
        'ink_px': int(ink.sum()),
        'rim_px': int(rim_mask.sum()),
        'rim_mean_light_factor': float(lf[rim_mask].mean()) if rim_mask.any() else 0,
        'line_band_mean_light_factor': float(lf[line_band].mean()) if line_band.any() else 0,
    }
    layers = {'line_band': line_band, 'rim_mask': rim_mask, 'light_factor': lf}
    return res, stats, layers

SCEN = [
    dict(id='S1-v2-warm-overhead', room='shafts-v2', direction='overhead',
         gain=[1.10, 0.95, 0.70], rim=[255, 180, 80], shadow=[40, 50, 90],
         room_file='shafts-only-cycles-v2-20261031.png', room_src='shafts upgrade'),
    dict(id='S2-v3-warm-overhead-strong', room='shafts-v3', direction='overhead_centre',
         gain=[1.15, 0.98, 0.72], rim=[255, 190, 90], shadow=[40, 50, 90],
         room_file='shafts-only-cycles-v3-20261031.png', room_src='shafts upgrade'),
    dict(id='S3-v3pools-warm-overhead-bounce', room='shafts-v3pools', direction='overhead_centre',
         gain=[1.12, 0.96, 0.71], rim=[255, 185, 85], shadow=[42, 52, 92], bounce=[255, 180, 80],
         room_file='composite-environmental-depth-lighting-v3-pools-20261031.png', room_src='shafts upgrade (figure in room file is unlit; room layer re-used, figure replaced by lit figure)'),
    dict(id='S4-glare-warm-overhead-glow', room='shafts-glare', direction='overhead',
         gain=[1.10, 0.95, 0.70], rim=[255, 180, 80], shadow=[40, 50, 90], glow=True,
         room_file='shafts-glare-blender-20261031.png', room_src='shafts upgrade'),
    dict(id='S5-colour-magenta-rose', room='colour-magenta', direction='front',
         gain=[1.25, 0.70, 0.90], rim=[255, 178, 229], shadow=[60, 30, 70], colour=[255, 120, 200]),
    dict(id='S6-colour-cyan-dual-backlight', room='colour-cyan-dual', direction='back',
         gain=[0.90, 1.05, 1.15], rim=[0, 200, 255], shadow=[20, 40, 70], colour=[0, 180, 230]),
    dict(id='S7-colour-golden-hour-front', room='colour-gold', direction='front',
         gain=[1.10, 0.95, 0.70], rim=[255, 180, 80], shadow=[40, 50, 90], colour=[255, 180, 80]),
    dict(id='S8-colour-cool-blue-night', room='colour-blue-night', direction='cool_front',
         gain=[0.85, 0.95, 1.20], rim=[160, 200, 255], shadow=[15, 25, 55], colour=[90, 140, 230]),
]

def main():
    base = load_rgba(SHAFT + 'figure-only-plate-20261031.png')
    base_img = Image.open(SHAFT + 'figure-only-plate-20261031.png').convert('RGBA')
    report = {'scenarios': [], 'presets': []}
    # ---- four separate presets ----
    presets = [
        ('01-v2-base', 'SHAFTS V2 BASE', SHAFT + 'shafts-only-cycles-v2-20261031.png',
         OLD + 'composite-shafts-behind-v2-20261031.png',
         {'lights': 'Sun down energy 4.0 colour (1.0,0.88,0.60) + 5 spots energy 6000 colour (1.0,0.88,0.62) spot 28deg blend 0.5',
          'slats': 6, 'volume': 'Principled Volume density 0.28 anisotropy 0.7 colour (1.0,0.85,0.55), CPU 32 samples',
          'mid_columns': [[282, 379], [494, 604], [721, 816]], 'mid_peak_mean': 54.8, 'mid_valley_mean': 22.9,
          'shaft_centre_mean_RGB': [72.4, 62.8, 47.1], 'dark_corner_mean_RGB': [22.9, 20.4, 18.8],
          'defects': ['Only 3 of 5 built gaps read clearly; outer 2 too dim', 'No ground light pools in v2 (floor removed)', 'Ceiling slats dominate top']}),
        ('02-v3-cycles', 'SHAFTS V3 CYCLES', SHAFT + 'shafts-only-cycles-v3-20261031.png',
         SHAFT + 'methods/I1-cycles-v3-composite-20261031.png',
         {'lights': 'Narrower slats 0.35 (was 0.55), thinner 0.15, wider volume x 6.0, outer spots 12000, centre 8000, spot 32deg, Sun 5.0, samples 24, Cycles denoising ON',
          'mid_columns': [[172, 232], [298, 800], [866, 927]], 'mean_RGB': [56.0, 49.0, 40.3],
          'defects': ['Centre 3 merged into one wide run — NOT 5-column separation', 'Ceiling slats still dominate top']}),
        ('03-v3-pools', 'SHAFTS V3+POOLS IMPROVED FINAL', SHAFT + 'composite-environmental-depth-lighting-v3-pools-20261031.png',
         SHAFT + 'composite-environmental-depth-lighting-v3-pools-20261031.png',
         {'lights': 'V3 Cycles + ground pools: warm ellipses at feet_y 1282, centres 165/330/550/770/935, radii 150/110/70, alpha 90/120/140, blur 18, behind figure',
          'mean_RGB_composite': [71.7, 65.9, 60.7],
          'defects': ['Pools are a composite pass, not true in-scene floor pools', 'Centre columns merged (from V3)', 'Ceiling slats still dominate top']}),
        ('04-glare-composite', 'SHAFTS GLARE COMPOSITE', SHAFT + 'shafts-glare-blender-20261031.png',
         SHAFT + 'methods/I4-glare-composite-20261031.png',
         {'lights': 'Blender Glare Fog Glow, Quality High, Threshold 0.6, Strength 0.5, Size 6, xvfb-run (headless background aborts exit 134, libEGL)',
          'mean_RGB': [23.1, 20.4, 19.1], 'max_RGB': 186,
          'defects': ['Effect subtle — bright centre column glows; dramatic halo NOT claimed', 'Eevee render still 0 files', 'Per-shot shafts 0/30']}),
    ]
    for pid, pname, room_src, comp_src, meas in presets:
        d = os.path.join(ROOT, 'presets', pid)
        os.makedirs(d, exist_ok=True)
        room = Image.open(room_src).convert('RGBA'); room.save(os.path.join(d, 'room-' + pid + '-20261031.png'))
        comp = Image.open(comp_src).convert('RGBA'); comp.save(os.path.join(d, 'composite-' + pid + '-20261031.png'))
        spec = {'preset_name': pname, 'preset_id': pid, 'saved': '2026-10-31',
                'approval': '0/1 separately', 'merged': False,
                'source_room_file': os.path.basename(room_src), 'source_composite_file': os.path.basename(comp_src),
                'room_size': list(room.size), 'room_mean_RGB': [round(float(x), 1) for x in np.array(room.convert('RGB')).reshape(-1, 3).mean(axis=0)],
                'measurements': meas,
                'rule': 'Shafts always behind figure; base art never recoloured; no-crop; do NOT claim 5 columns / Glare / Eevee unless measured file exists. This preset is SEPARATE — it does not merge into or overwrite the Environmental Depth and Lighting preset.'}
        with open(os.path.join(d, 'PRESET-' + pid.upper() + '-20261031.json'), 'w') as f:
            json.dump(spec, f, indent=2)
        report['presets'].append({'id': pid, 'name': pname, 'room_mean_RGB': spec['room_mean_RGB'], 'approval': '0/1'})
    # ---- figure-matched versions ----
    for s in SCEN:
        lit, stats, layers = light_figure(base, s)
        save(lit, os.path.join(ROOT, 'figures', s['id'] + '-lit-transparent-20261031.png'))
        # room background
        if 'room_file' in s:
            room = np.array(Image.open(SHAFT + s['room_file']).convert('RGBA')).astype(np.float32)
            # for S3 the room file already contains an unlit figure; use shafts-only v3 as room instead
            if s['id'].startswith('S3'):
                room = np.array(Image.open(SHAFT + 'shafts-only-cycles-v3-20261031.png').convert('RGBA')).astype(np.float32)
                # add pools behind figure area: warm ellipses at feet (in padded coords? room is 1100x1500, figure pad shifts) - pools drawn on room before figure paste, at feet_y 1282
                from PIL import ImageDraw
                rim_room = Image.fromarray(np.clip(room, 0, 255).astype(np.uint8), 'RGBA')
                ov = Image.new('RGBA', rim_room.size, (0, 0, 0, 0))
                dr = ImageDraw.Draw(ov)
                for cx, r, al in [(165, 150, 90), (330, 110, 120), (550, 70, 140), (770, 110, 120), (935, 150, 90)]:
                    dr.ellipse([cx - r, 1282 - 35, cx + r, 1282 + 35], fill=(255, 180, 80, al))
                ov = ov.filter(ImageFilter.GaussianBlur(18))
                room = np.array(Image.alpha_composite(rim_room, ov)).astype(np.float32)
        else:
            room_rgb = room_background(s['room'], s['colour'])
            room = np.zeros((1500, 1100, 4), np.float32); room[:, :, :3] = room_rgb; room[:, :, 3] = 255
        # paste lit figure (padded 1260x1660) onto room canvas padded to same: centre lit on 1260x1660 room canvas
        room_big = np.zeros((1500 + 2 * PAD, 1100 + 2 * PAD, 4), np.float32)
        room_big[PAD:PAD + 1500, PAD:PAD + 1100, :3] = room[:, :, :3]
        room_big[PAD:PAD + 1500, PAD:PAD + 1100, 3] = 255
        # shafts behind figure: figure alpha masks room (already true by pasting lit over room)
        fa = lit[:, :, 3:4] / 255.0
        comp = room_big * (1 - fa) + lit * fa
        comp[:, :, 3] = np.maximum(room_big[:, :, 3], lit[:, :, 3])
        save(comp, os.path.join(ROOT, 'figures', s['id'] + '-on-room-20261031.png'))
        # grey display version (lit on grey, for line read)
        grey = np.zeros_like(lit); grey[:, :, :3] = 128; grey[:, :, 3] = 255
        disp = grey * (1 - fa) + lit * fa; disp[:, :, 3] = np.maximum(grey[:, :, 3], lit[:, :, 3])
        save(disp, os.path.join(ROOT, 'figures', s['id'] + '-on-grey-20261031.png'))
        # no-crop check
        edge = np.concatenate([comp[0, :, 3], comp[-1, :, 3], comp[:, 0, 3], comp[:, -1, 3]])
        # figure-only edge: lit figure edge alpha (rim/glow must not touch padded canvas edge)
        fedge = np.concatenate([lit[0, :, 3], lit[-1, :, 3], lit[:, 0, 3], lit[:, -1, 3]])
        # measured lit means inside figure
        m = lit[:, :, 3] > 10
        lit_mean = [round(float(x), 1) for x in lit[:, :, :3][m].mean(axis=0)]
        base_m = base[:, :, 3] > 10
        base_mean = [round(float(x), 1) for x in base[:, :, :3][base_m].mean(axis=0)]
        # line-band lit vs base: sample line band in padded coords (offset PAD)
        report['scenarios'].append({**{k: s[k] for k in ('id', 'room', 'direction', 'gain', 'rim', 'shadow')},
            'lit_mean_RGB': lit_mean, 'base_mean_RGB': base_mean,
            'figure_alpha_px': stats['figure_alpha_px'], 'line_band_px': stats['line_band_px'],
            'rim_px': stats['rim_px'], 'line_band_mean_light_factor': round(stats['line_band_mean_light_factor'], 3),
            'no_crop_padded_edge_alpha_max': float(fedge.max()), 'canvas': list(lit.shape[:2][::-1])})
        print(s['id'], stats, 'lit_mean', lit_mean, 'edge_max', float(fedge.max()))
    with open(os.path.join(ROOT, 'FIGURE-MATCHED-LIGHTING-REPORT-20261031.json'), 'w') as f:
        json.dump(report, f, indent=2)
    print('DONE', len(report['scenarios']), 'scenarios,', len(report['presets']), 'presets')

if __name__ == '__main__':
    main()
