#!/usr/bin/env python3
"""Group A method proxies — NOT the original tools.
RIFE/FILM/RAFT: classical Farneback dense flow + warp + blend (OpenCV, free).
ToonCrafter: same flow warp on a cartoon pair + flow-guide overlay panel (no diffusion, no new content invented).
EbSynth: a painted stroke on a SEPARATE overlay layer, warped by the same flow and composited
  over the flow-warped base — base art pixels are never recoloured in place; the overlay is also saved alone.
Originals not run: no GPU (nvidia-smi absent), no torch on this VM, ToonCrafter needs ~16-26 GB VRAM
and a ~5 GB checkpoint, RAFT/RIFE/FILM need PyTorch+CUDA weights, EbSynth has no Linux CLI
(Windows/macOS desktop / browser v2 with upload). See GROUP-A.md for the honest status per tool.
Inputs: Cape v7c pose/dance frames, downscaled 2x (1100x1500 -> 550x750) for CPU speed; outputs dated 20261031.
"""
import os, json, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.expanduser("~/workspace/cape-jones-rig/experimental-25-20261031/group-a-interpolation/proofs")
os.makedirs(OUT, exist_ok=True)
W, H = 550, 750

def load(p):
    im = Image.open(p).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    out = Image.alpha_composite(bg, im).convert("RGB").resize((W, H), Image.LANCZOS)
    return np.array(out)

def flow(a, b, winsize=15, levels=3, iters=3):
    ga = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY); gb = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY)
    return cv2.calcOpticalFlowFarneback(ga, gb, None, 0.5, levels, winsize, iters, 5, 1.2, 0)

def warp(img, fl):
    h, w = fl.shape[:2]
    xs, ys = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(img, (xs + fl[..., 0]).astype(np.float32), (ys + fl[..., 1]).astype(np.float32),
                     cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def interp(a, b, t, **kw):
    fab = flow(a, b, **kw); fba = flow(b, a, **kw)
    wa = warp(a, fab * t); wb = warp(b, fba * (1 - t))
    return ((1 - t) * wa.astype(np.float32) + t * wb.astype(np.float32)).astype(np.uint8), fab, fba

def contact(panels, labels, path, thumb_w=275):
    thumbs = []
    for p in panels:
        im = Image.fromarray(p).resize((thumb_w, int(thumb_w * H / W)), Image.LANCZOS)
        thumbs.append(im)
    th = thumbs[0].height + 28
    sheet = Image.new("RGB", (thumb_w * len(thumbs), th), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(thumbs, labels)):
        sheet.paste(im, (i * thumb_w, 28)); d.text((i * thumb_w + 6, 6), lab, fill=(255, 255, 0))
    sheet.save(path); return path

def gif(frames, path, dur=260):
    ims = [Image.fromarray(f) for f in frames]
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=dur, loop=0)
    return path

def stats(fl):
    mag = np.sqrt((fl ** 2).sum(axis=2))
    return {"mean_px": round(float(mag.mean()), 2), "median_px": round(float(np.median(mag)), 2),
            "p90_px": round(float(np.percentile(mag, 90)), 2), "max_px": round(float(mag.max()), 2),
            "pct_gt_20px": round(float((mag > 20).mean() * 100), 1)}

def flow_viz(fl):
    mag, ang = cv2.cartToPolar(fl[..., 0], fl[..., 1])
    hsv = np.zeros((H, W, 3), dtype=np.uint8)
    hsv[..., 0] = (ang * 180 / np.pi / 2).astype(np.uint8)
    hsv[..., 1] = 255
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

POSES = f"{BASE}/pose-dialects-20261031"
DANCE = f"{BASE}/clips-v7c/dance"
results = {}

# 1. RIFE proxy — moderate pair jojo-01 -> jojo-02, t=0.5 + 5-frame sequence
a = load(f"{POSES}/jojo-01-contrapposto-s-curve-20261031.png")
b = load(f"{POSES}/jojo-02-fashion-twist-point-20261031.png")
mid, fab, fba = interp(a, b, 0.5)
seq = [interp(a, b, t)[0] for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
contact([a, mid, b], ["A jojo-01", "RIFE-PROXY mid t=0.5 (flow warp, NOT RIFE)", "B jojo-02"],
        f"{OUT}/rife-proxy-jojo01-to-jojo02-20261031.png")
gif(seq, f"{OUT}/rife-proxy-jojo01-to-jojo02-20261031.gif")
results["rife_proxy"] = stats(fab)

# 2. FILM proxy — LARGE-motion pair ginyu-01 -> ginyu-03, bigger window/levels (scale-agnostic idea, classical)
a2 = load(f"{POSES}/ginyu-01-rollcall-chest-out-20261031.png")
b2 = load(f"{POSES}/ginyu-03-dance-shimmy-hips-out-20261031.png")
mid2, fab2, fba2 = interp(a2, b2, 0.5, winsize=25, levels=5, iters=5)
seq2 = [interp(a2, b2, t, winsize=25, levels=5, iters=5)[0] for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
contact([a2, mid2, b2], ["A ginyu-01", "FILM-PROXY mid t=0.5 large-motion (NOT FILM)", "B ginyu-03"],
        f"{OUT}/film-proxy-ginyu01-to-ginyu03-20261031.png")
gif(seq2, f"{OUT}/film-proxy-ginyu01-to-ginyu03-20261031.gif")
results["film_proxy"] = stats(fab2)

# 3. RAFT proxy — flow itself is the proof: HSV flow map + warped mid, pair ginyu-01 -> ginyu-02
a3 = load(f"{POSES}/ginyu-01-rollcall-chest-out-20261031.png")
b3 = load(f"{POSES}/ginyu-02-squat-elbows-out-goofy-20261031.png")
mid3, fab3, fba3 = interp(a3, b3, 0.5)
viz = flow_viz(fab3)
contact([a3, viz, b3], ["A ginyu-01", "RAFT-PROXY flow map HSV (NOT RAFT)", "B ginyu-02"],
        f"{OUT}/raft-proxy-flow-ginyu01-to-ginyu02-20261031.png")
contact([a3, mid3, b3], ["A ginyu-01", "RAFT-PROXY warped mid t=0.5", "B ginyu-02"],
        f"{OUT}/raft-proxy-warped-mid-20261031.png")
results["raft_proxy"] = stats(fab3)

# 4. ToonCrafter proxy — cartoon pair jojo-02 -> jojo-03, flow sequence + flow-guide arrows panel (no diffusion)
a4 = load(f"{POSES}/jojo-02-fashion-twist-point-20261031.png")
b4 = load(f"{POSES}/jojo-03-menacing-lean-hand-face-20261031.png")
mid4, fab4, fba4 = interp(a4, b4, 0.5)
seq4 = [interp(a4, b4, t)[0] for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
guide = mid4.copy()
for y in range(40, H, 60):
    for x in range(40, W, 60):
        fx, fy = fab4[y, x]
        if abs(fx) + abs(fy) > 4:
            cv2.arrowedLine(guide, (x, y), (int(x + fx * 2), int(y + fy * 2)), (255, 0, 0), 2, tipLength=0.4)
contact([a4, mid4, b4], ["A jojo-02", "TOONCRAFTER-PROXY mid (flow, NOT diffusion)", "B jojo-03"],
        f"{OUT}/tooncrafter-proxy-jojo02-to-jojo03-20261031.png")
contact([mid4, guide], ["mid (no guide)", "mid + flow-guide arrows (guide-layer concept only)"],
        f"{OUT}/tooncrafter-proxy-guide-20261031.png")
gif(seq4, f"{OUT}/tooncrafter-proxy-jojo02-to-jojo03-20261031.gif")
results["tooncrafter_proxy"] = stats(fab4)

# 5. EbSynth proxy — painted stroke on a SEPARATE layer, warped by flow, composited over warped base
a5 = load(f"{DANCE}/dance-01-a-v7c.png"); b5 = load(f"{DANCE}/dance-13-b-v7c.png")
mid5, fab5, fba5 = interp(a5, b5, 0.5)
# separate overlay layer: amber painted sash stroke on transparent layer, saved alone
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
d.polygon([(60, 330), (490, 260), (490, 330), (60, 400)], fill=(255, 170, 0, 130))
d.ellipse([230, 300, 320, 390], outline=(255, 170, 0, 180), width=8)
layer.save(f"{OUT}/ebsynth-proxy-painted-stroke-layer-only-20261031.png")
la = np.array(layer)
warped_layer = warp(la, fab5 * 0.5)  # RGBA warped by same flow
base_pil = Image.fromarray(mid5).convert("RGBA")
comp = Image.alpha_composite(base_pil, Image.fromarray(warped_layer)).convert("RGB")
comp_a = Image.alpha_composite(Image.fromarray(a5).convert("RGBA"), layer).convert("RGB")
contact([np.array(comp_a), np.array(comp), b5],
        ["A + painted stroke layer", "EB-PROXY mid: stroke warped by flow (NOT EbSynth)", "B dance-13-b"],
        f"{OUT}/ebsynth-proxy-dance01-to-dance13-20261031.png")
results["ebsynth_proxy"] = stats(fab5)
results["inputs"] = {"rife": "jojo-01->jojo-02", "film": "ginyu-01->ginyu-03 (large motion)",
                     "raft": "ginyu-01->ginyu-02", "tooncrafter": "jojo-02->jojo-03",
                     "ebsynth": "dance-01-a->dance-13-b", "size": "550x750 (2x downscale of 1100x1500)",
                     "method": "OpenCV Farneback dense flow + bidirectional warp + blend; EbSynth overlay separate layer"}
with open(os.path.expanduser("~/workspace/cape-jones-rig/experimental-25-20261031/group-a-interpolation/method-proxy-stats-20261031.json"), "w") as f:
    json.dump(results, f, indent=2)
print(json.dumps(results, indent=2))
print("DONE", sorted(os.listdir(OUT)))
