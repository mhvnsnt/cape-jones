"""Group D proofs — METHOD-WIRED ONLY (PIL/numpy/scipy).
No ControlNet, Style2Paints, Anime2Sketch, Natron, MiDaS or Depth Anything
model was run here: local VM has no GPU and torch is not installed.
Every output is labelled METHOD-WIRED / PROXY / REFERENCE ONLY.
Source pose is never overwritten; proofs are new dated files in proofs/.
Source: pose-dialects-20261031/jojo-01-contrapposto-s-curve-20261031.png
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
from scipy import ndimage

SRC = os.path.expanduser("~/workspace/cape-jones-rig/pose-dialects-20261031/jojo-01-contrapposto-s-curve-20261031.png")
OUT = os.path.expanduser("~/workspace/cape-jones-rig/experimental-25-20261031/group-d-effects-depth-style/proofs")
os.makedirs(OUT, exist_ok=True)
orig = Image.open(SRC).convert("RGBA")
W, H = orig.size  # 1100x1500
alpha = np.array(orig.split()[3])
mask = alpha > 10
print("source", orig.size, "opaque px", int(mask.sum()))

def label(img, text, size=28):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, size + 14], fill=(0, 0, 0))
    d.text((10, 7), text, fill=(255, 255, 0))
    return img

def sheet(panels, titles, path, cols=3):
    tw = 366
    th = int(tw * H / W)
    cells = []
    for p, t in zip(panels, titles):
        c = p.convert("RGB").resize((tw, th))
        d = ImageDraw.Draw(c); d.rectangle([0, 0, tw, 30], fill=(0, 0, 0)); d.text((8, 8), t, fill=(255, 255, 0))
        cells.append(c)
    rows = (len(cells) + cols - 1) // cols
    s = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
    for i, c in enumerate(cells):
        s.paste(c, ((i % cols) * tw, (i // cols) * th))
    s.save(path); print(path, s.size)

# --- shared derivatives ---
grey = ImageOps.grayscale(orig.convert("RGB"))
# edge / lineart proxy: FIND_EDGES on grey, inverted, masked to silhouette
edges = grey.filter(ImageFilter.FIND_EDGES)
ea = np.array(edges).astype(float)
line = np.clip(255 - ea * 2.2, 0, 255).astype(np.uint8)
line_img = Image.fromarray(line).convert("RGB")
line_img.putalpha(Image.fromarray(np.where(mask, 255, 0).astype(np.uint8)))
# XDoG-ish: blurred grey minus grey
blur = grey.filter(ImageFilter.GaussianBlur(2))
xdog = Image.fromarray(np.clip(255 - (np.array(blur).astype(int) - np.array(grey).astype(int)) * 3, 0, 255).astype(np.uint8))

# pseudo-depth: distance transform inside silhouette (centre=near/bright)
dist = ndimage.distance_transform_edt(mask)
depth = np.zeros_like(dist, dtype=float)
if dist.max() > 0: depth = dist / dist.max()
# vertical cue: upper body slightly nearer is NOT assumed; keep pure silhouette distance, labelled
depth_img = Image.fromarray((depth * 255).astype(np.uint8)).convert("RGB")
depth_img.putalpha(Image.fromarray(np.where(mask, 255, 0).astype(np.uint8)))
# depth colour ramp (near=warm white, far=dark blue) as separate layer
ramp = np.zeros((H, W, 3), dtype=np.uint8)
ramp[..., 0] = (depth * 255).astype(np.uint8); ramp[..., 1] = (depth * 180).astype(np.uint8); ramp[..., 2] = (255 - depth * 180).astype(np.uint8)
ramp_img = Image.fromarray(ramp); ramp_img.putalpha(Image.fromarray(np.where(mask, 255, 0).astype(np.uint8)))

# 1 ControlNet conditioning pack
sheet([orig, depth_img, line_img],
      ["1 ORIGINAL (unmodified source)", "2 DEPTH CONDITION (method-wired)", "3 LINEART CONDITION (method-wired)"],
      f"{OUT}/01-controlnet-conditioning-pack-20261031.png")
json.dump({"project": "ControlNet", "status": "METHOD-WIRED, model NOT run",
  "conditioning": ["depth (silhouette-distance proxy)", "lineart (edge proxy)"],
  "real_checkpoints_for_next_step": ["lllyasviel/control_v11f1p_sd15_depth", "lllyasviel/control_v11p_sd15_lineart"],
  "cape_use": "Feed depth+lineart as ControlNet conditions so a re-render keeps pose/silhouette while style/lighting change; never as character generator",
  "source": "pose-dialects-20261031/jojo-01-contrapposto-s-curve-20261031.png", "base_art_recoloured": False},
  open(f"{OUT}/01-controlnet-conditioning-spec-20261031.json", "w"), indent=2)

# 2 Style2Paints method: lineart + colour hints + flat reference (separate layer, reference only)
hints = line_img.copy(); d = ImageDraw.Draw(hints)
# sample colours from original at a few silhouette points (approx body regions)
for (x, y, r) in [(550, 300, 26), (550, 650, 26), (430, 950, 26), (680, 950, 26), (550, 1250, 26)]:
    px = orig.getpixel((x, y))
    d.ellipse([x - r, y - r, x + r, y + r], fill=px[:3], outline=(255, 0, 0), width=4)
# flat reference: median/quantized original masked to silhouette, labelled reference
flat = orig.convert("RGB").quantize(colors=8).convert("RGB")
flat.putalpha(Image.fromarray(np.where(mask, 255, 0).astype(np.uint8)))
sheet([line_img, hints, flat],
      ["LINEART (proxy)", "COLOUR HINTS (Style2Paints workflow)", "FLAT REFERENCE ONLY - NOT BASE ART"],
      f"{OUT}/02-style2paints-method-reference-20261031.png")
json.dump({"project": "Style2Paints", "status": "METHOD-WIRED, model NOT run",
  "workflow_mirrored": "lineart -> sparse colour hints -> flat fill -> (real V4 would return layered PSD)",
  "cape_use": "Colourisation REFERENCE for a new flat pass; approved flats are repainted by hand, base art is never recoloured in place",
  "base_art_recoloured": False}, open(f"{OUT}/02-style2paints-method-spec-20261031.json", "w"), indent=2)

# 3 Anime2Sketch proxy
sheet([orig, line_img, xdog],
      ["ORIGINAL COLOUR", "SKETCH PROXY (edge, inverted)", "XDoG-STYLE PROXY (blur-difference)"],
      f"{OUT}/03-anime2sketch-line-extraction-proxy-20261031.png")
json.dump({"project": "Anime2Sketch", "status": "METHOD-WIRED, model NOT run",
  "proxy": "PIL FIND_EDGES + blur-difference; real Anime2Sketch is a learned GAN extractor (MIT) needing PyTorch + weights",
  "cape_use": "Recover clean lineart from a coloured frame so it can be re-flatted / re-lit without redrawing; check line breaks by eye before use",
  "base_art_recoloured": False}, open(f"{OUT}/03-anime2sketch-method-spec-20261031.json", "w"), indent=2)

# 4 Natron-style node composite: Read -> Grade(warm) -> Rim(edge glow) -> Merge over bg
bg = Image.new("RGBA", (W, H), (18, 24, 48, 255))
for y in range(H):
    c = int(18 + 30 * y / H); bg.paste((c, c + 10, 60, 255), [0, y, W, y + 1])
graded = ImageEnhance.Color(orig).enhance(1.15)
graded = ImageEnhance.Brightness(graded).enhance(1.05)
# rim: edge mask dilated, warm amber per rim-colour rule (255,180,80)
edge_mask = np.array(line_img.convert("L")) < 200
rim = np.zeros((H, W, 4), dtype=np.uint8)
rim[..., 0] = 255; rim[..., 1] = 180; rim[..., 2] = 80
rim[..., 3] = np.where(edge_mask & mask, 160, 0).astype(np.uint8)
rim_img = Image.fromarray(rim).filter(ImageFilter.GaussianBlur(2))
comp = bg.copy(); comp.alpha_composite(rim_img); comp.alpha_composite(graded)
# node graph diagram
g = Image.new("RGB", (1100, 420), (30, 30, 30)); d = ImageDraw.Draw(g)
nodes = ["Read\n(pose PNG)", "Grade\nwarm L2", "Rim\namber edge", "Merge\n over bg", "Write\nPNG (proof)"]
for i, n in enumerate(nodes):
    x = 40 + i * 210; d.rectangle([x, 150, x + 170, 250], outline=(255, 255, 0), width=3); d.text((x + 15, 175), n, fill=(255, 255, 255))
    if i < 4: d.line([x + 170, 200, x + 210, 200], fill=(255, 255, 0), width=4)
d.text((40, 40), "NATRON-STYLE NODE GRAPH (method-wired in PIL - Natron binary NOT run)", fill=(255, 255, 0))
d.text((40, 300), "Read -> Grade -> Rim -> Merge -> Write  |  base art on its own layer, grade/rim are separate layers", fill=(255, 255, 255))
g.save(f"{OUT}/04-natron-node-graph-20261031.png")
sheet([orig, comp, ramp_img],
      ["ORIGINAL", "NODE COMPOSITE (grade+rim+bg)", "DEPTH RAMP (for Merge order)"],
      f"{OUT}/04-natron-composite-proof-20261031.png")
json.dump({"project": "Natron", "status": "METHOD-WIRED, Natron binary NOT run",
  "reason": "No Natron binary installed on this VM; upstream is community-maintained (GPL-2.0, Qt5-era; FreeBSD port expired 2026-09-30 for Qt5 WebEngine; 2026 community fork adds Qt6/Cycles, Windows-only, self-described vibe-coded - NOT adopted sight-unseen)",
  "nodes": ["Read", "Grade(warm L2)", "Rim(amber 255,180,80, edge glow)", "Merge over background", "Write"],
  "cape_use": "Free node compositor alternative to Blender compositor for rim/wrap/glow passes; adopt only after a real Natron/Blender A-B test",
  "base_art_recoloured": False}, open(f"{OUT}/04-natron-node-spec-20261031.json", "w"), indent=2)

# 5 MiDaS / Depth Anything method: depth map + 2.5D parallax proof (2 shifted layers)
# parallax: near (depth>0.5) shifted +12px, far shifted -6px, composited = depth-order demo, NOT a render
near = np.where(depth > 0.5, 1, 0); far = np.where((depth <= 0.5) & mask, 1, 0)
def masked_shift(frac, dx):
    a = np.array(orig); a[..., 3] = np.where(frac, a[..., 3], 0).astype(np.uint8)
    im = Image.fromarray(a); return im.transform(im.size, Image.AFFINE, (1, 0, -dx, 0, 1, 0))
par = Image.new("RGBA", (W, H), (10, 10, 20, 255)); par.alpha_composite(masked_shift(far, -6)); par.alpha_composite(masked_shift(near, 12))
sheet([orig, depth_img, par],
      ["ORIGINAL", "PSEUDO-DEPTH (silhouette distance)", "2.5D PARALLAX DEMO (near +12 / far -6)"],
      f"{OUT}/05-midas-depthanything-pseudo-depth-20261031.png")
json.dump({"project": "MiDaS / Depth Anything", "status": "METHOD-WIRED, models NOT run",
  "proxy": "scipy distance_transform_edt inside silhouette, normalised 0-1, relative only (no metres)",
  "real_next_step": "Depth Anything V2/V3 small or MiDaS small on Kaggle/Colab free GPU (torch required, not installed here); then compare proxy vs model depth on same frame",
  "cape_use": "Depth maps drive 2.5D parallax, rim/wrap falloff and layer ordering; relative depth is enough for cutout parallax, metric depth is not needed",
  "base_art_recoloured": False}, open(f"{OUT}/05-midas-depthanything-method-spec-20261031.json", "w"), indent=2)

print("done")
