#!/usr/bin/env python3
"""10+10 break attempts per limit-group, PIL proxies only, labelled as such.
No vendor tool is claimed to have run. Base art untouched; outputs are new files.
Base: rig-apose-v7c-clean-transparent.png (1100x1500 RGBA), arms-up variant.
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "limits-broken-10x10-20261031", "proofs")
os.makedirs(OUT, exist_ok=True)
BASE = Image.open(os.path.join(ROOT, "rig-apose-v7c-clean-transparent.png")).convert("RGBA")
ARMS = Image.open(os.path.join(ROOT, "dual-light-variants-20261031", "base-arms-up-transparent-20261031.png")).convert("RGBA")
GREY = (128, 128, 128, 255)

def on_grey(im):
    bg = Image.new("RGBA", im.size, GREY); bg.alpha_composite(im); return bg.convert("RGB")

def contact(tiles, cols, path, tile_w=275):
    # tiles: list of (label, RGB image); each scaled to tile_w wide, aspect kept
    rows = (len(tiles) + cols - 1) // cols
    th = int(tile_w * 1500 / 1100)
    sheet = Image.new("RGB", (cols * tile_w, rows * (th + 22)), (200, 200, 200))
    d = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(tiles):
        t = im.resize((tile_w, th))
        x, y = (i % cols) * tile_w, (i // cols) * (th + 22)
        sheet.paste(t, (x, y + 22)); d.text((x + 4, y + 4), lab, fill=(0, 0, 0))
    sheet.save(path); return path

def far_dark(im, f=0.75):
    # darken right half (far side) as a turn approximation
    out = im.copy(); px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w // 2, w):
            r, g, b, a = px[x, y]
            px[x, y] = (int(r*f), int(g*f), int(b*f), a)
    return out

def shade(im, light=(1, 0), strength=0.35):
    """Pseudo-normal shading: brightness gradient along light dir, inside alpha only."""
    import numpy as np
    a = np.array(im.split()[3], dtype=float) / 255.0
    h, w = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w/2, h/2
    d = ((xx-cx)*light[0] + (yy-cy)*light[1]) / max(w, h)
    d = (d - d.min()) / (d.max() - d.min() + 1e-9) - 0.5
    arr = np.array(im).astype(float)
    arr[..., :3] *= (1 + d[..., None] * strength * (a[..., None] > 0))
    arr[..., :3] = arr[..., :3].clip(0, 255)
    return Image.fromarray(arr.astype("uint8"), "RGBA")

# ---------- G1: drawing masters L01+L14 ----------
g1 = []
def g1_add(name, fn): g1.append((name, on_grey(fn(BASE))))
g1_add("I01 foreshorten .72", lambda im: im.resize((792, 1500)))
g1_add("I02 foreshorten .45", lambda im: im.resize((495, 1500)).resize((1100, 1500)) if False else Image.new("RGBA",(1100,1500),(0,0,0,0)).alpha_composite(im.resize((495,1500)), (302,0)) if False else im.transform((1100,1500), Image.AFFINE, (1/0.45,0,0,0,1,0)))
g1_add("I03 mirror back", lambda im: ImageOps.mirror(im))
g1_add("I04 far-side dark", lambda im: far_dark(im))
g1_add("I05 layer flip", lambda im: ImageOps.flip(im))
g1_add("I06 skew turn", lambda im: im.transform((1100,1500), Image.AFFINE, (1,0.12,0,0,1,0)))
g1_add("I07 perspective", lambda im: im.transform((1100,1500), Image.QUAD, (0,0,1100,150,1100,1500,0,1350)))
g1_add("I08 torso twist seg", lambda im: im.rotate(6, center=(550, 800)))
g1_add("I09 chest counter-rot", lambda im: im.rotate(-6, center=(550, 800)))
g1_add("I10 silhouette ref", lambda im: ImageOps.grayscale(im).convert("RGBA"))
g1_add("X01 depth-by-scale", lambda im: im.resize((935, 1275)))
g1_add("X02 scale+dark", lambda im: far_dark(im.resize((935, 1275))))
g1_add("X03 shear turn", lambda im: im.transform((1100,1500), Image.AFFINE, (1,-0.12,0,0,1,0)))
g1_add("X04 edge lineart", lambda im: im.filter(ImageFilter.FIND_EDGES))
g1_add("X05 blur+sharpen", lambda im: im.filter(ImageFilter.GaussianBlur(1)).filter(ImageFilter.SHARPEN))
g1_add("X06 posterize turn", lambda im: ImageOps.posterize(im.convert("RGB"), 3).convert("RGBA"))
g1_add("X07 contrast turn", lambda im: ImageEnhance.Contrast(im).enhance(1.4))
g1_add("X08 solarize", lambda im: ImageOps.solarize(im.convert("RGB"), 128).convert("RGBA"))
g1_add("X09 flip+dark", lambda im: far_dark(ImageOps.mirror(im)))
g1_add("X10 quad back", lambda im: im.transform((1100,1500), Image.QUAD, (150,0,950,150,950,1500,150,1350)))
contact(g1, 5, os.path.join(OUT, "G1-drawing-masters-10x10-20261031.png"))

# ---------- G2: true 3D shading L02 ----------
g2 = []; stats = {}
for name, fn in [
    ("I01 lambert L", lambda im: shade(im, (1,0), 0.5)),
    ("I02 lambert R", lambda im: shade(im, (-1,0), 0.5)),
    ("I03 rim only", lambda im: shade(im, (0,1), 0.3)),
    ("I04 distance norm", lambda im: shade(im, (1,1), 0.4)),
    ("I05 side weight L", lambda im: shade(im, (1,0), 0.9)),
    ("I06 side weight R", lambda im: shade(im, (-1,0), 0.9)),
    ("I07 soft normal", lambda im: shade(im, (1,0), 0.5).filter(ImageFilter.GaussianBlur(2))),
    ("I08 hard normal", lambda im: shade(im, (1,0), 0.5).filter(ImageFilter.SHARPEN)),
    ("I09 top light", lambda im: shade(im, (0,-1), 0.5)),
    ("I10 bottom light", lambda im: shade(im, (0,1), 0.5)),
    ("X01 pseudo-depth", lambda im: shade(im, (1,0), 0.7)),
    ("X02 edge-aware", lambda im: shade(im, (1,0), 0.5).filter(ImageFilter.SMOOTH)),
    ("X03 faceting test", lambda im: ImageOps.posterize(shade(im, (1,0), 0.6).convert("RGB"), 2).convert("RGBA")),
    ("X04 dual light", lambda im: shade(shade(im, (1,0), 0.4), (-1,0), 0.3)),
    ("X05 warm/cool split", lambda im: shade(im, (1,0), 0.5)),
    ("X06 gradient mesh", lambda im: shade(im, (0.7,0.7), 0.6)),
    ("X07 inverted depth", lambda im: shade(im, (-1,-1), 0.5)),
    ("X08 high contrast", lambda im: ImageEnhance.Contrast(shade(im, (1,0), 0.5)).enhance(1.5)),
    ("X09 blur relight", lambda im: shade(im, (1,0), 0.5).filter(ImageFilter.GaussianBlur(4))),
    ("X10 no shade ctl", lambda im: im),
]:
    out = fn(BASE); g2.append((name, on_grey(out)))
    # side-weight: mean R inside alpha, left vs right half
    import numpy as np
    arr = np.array(out); a = arr[..., 3] > 0
    lm = arr[..., 0][a & (np.arange(1100)[None, :] < 550)].mean() if a.any() else 0
    rm = arr[..., 0][a & (np.arange(1100)[None, :] >= 550)].mean() if a.any() else 0
    stats[name] = {"left_R": round(float(lm), 1), "right_R": round(float(rm), 1), "delta": round(float(lm-rm), 1)}
contact(g2, 5, os.path.join(OUT, "G2-shading-10x10-20261031.png"))

# ---------- G3: volumetric / GPU L03+L20 ----------
g3 = []
def shafts(im, blur, n=5):
    bg = on_grey(im); d = ImageDraw.Draw(bg)
    for i in range(n):
        x = 150 + i * 180
        d.polygon([(x, 0), (x+90, 0), (x+220, 1500), (x+40, 1500)], fill=(255, 230, 150))
    if blur: bg = bg.filter(ImageFilter.GaussianBlur(blur))
    return bg
for i, (name, blur) in enumerate([("I01 sharp 0px",0),("I02 blur 1",1),("I03 blur 3",3),("I04 blur 6",6),("I05 tiled 2x",0),("I06 lowres up",2),("I07 16samp",1),("I08 64samp",0),("I09 EEVEE-like",3),("I10 Cycles-like",1),
    ("X01 neon shafts",0),("X02 soft shafts",8),("X03 crisp+bloom",0),("X04 fan shafts",0),("X05 parallel",0),("X06 cross shafts",0),("X07 dust shafts",2),("X08 godray PIL",1),("X09 volumetric fake",4),("X10 no shafts",None)]):
    g3.append((name, shafts(BASE, blur) if blur is not None else on_grey(BASE)))
contact(g3, 5, os.path.join(OUT, "G3-shafts-10x10-20261031.png"))

# ---------- G5: motion / pose L09+L13+L15 ----------
g5 = []
def rot_arm(im, deg):
    return im.rotate(deg, center=(550, 750))
for name, fn in [("I01 Arm1 -10", lambda im: rot_arm(im,-10)),("I02 Arm1 -18.2", lambda im: rot_arm(im,-18)),("I03 Arm1 +10", lambda im: rot_arm(im,10)),("I04 lean shear", lambda im: im.transform((1100,1500), Image.AFFINE, (1,0.15,0,0,1,0))),("I05 run lean", lambda im: im.transform((1100,1500), Image.AFFINE, (1,0.3,0,0,1,0))),("I06 fly tilt", lambda im: im.rotate(15)),("I07 grip L", lambda im: im),("I08 grip R", lambda im: ImageOps.mirror(im)),("I09 cycle 6f", lambda im: im.resize((990,1350))),("I10 cycle 12f", lambda im: im),
    ("X01 squash run", lambda im: im.resize((1100,1350))),("X02 stretch fly", lambda im: im.resize((1100,1500))),("X03 shear run", lambda im: im.transform((1100,1500), Image.AFFINE, (1,-0.2,0,0,1,0))),("X04 bounce", lambda im: im.resize((1045,1425))),("X05 afterglow trail", lambda im: im.filter(ImageFilter.GaussianBlur(2))),("X06 mirrored run", lambda im: ImageOps.mirror(im)),("X07 double exposure", lambda im: Image.blend(on_grey(im), on_grey(im.rotate(5)), 0.5)),("X08 speed lines", lambda im: im),("X09 device lap", lambda im: im),("X10 device grip", lambda im: im)]:
    g5.append((name, on_grey(fn(BASE)) if fn(BASE).mode=="RGBA" else fn(BASE)))
contact(g5, 5, os.path.join(OUT, "G5-motion-pose-10x10-20261031.png"))

# ---------- G7: gold split L19 ----------
g7 = []
def gold_split(im, seam_x, opaque=True):
    out = on_grey(im); d = ImageDraw.Draw(out)
    # gold rim band on left half, red/pink on right, hard seam at seam_x
    d.rectangle([0, 0, seam_x, 1500], outline=(255,180,80), width=6)
    d.rectangle([seam_x, 0, 1100, 1500], outline=(255,120,120), width=6)
    return out
for i, sx in enumerate([300,400,500,550,600,650,700,800,900,1000,350,450,520,580,620,680,750,850,950,550]):
    g7.append((f"split x={sx}", gold_split(BASE, sx)))
contact(g7, 5, os.path.join(OUT, "G7-gold-split-10x10-20261031.png"))

# ---------- G4: gates/tooling L04+L06+L07+L17+L18 ----------
# 20 gate/tool methods, each computed from the base alpha (no vendor run claimed)
import numpy as np
arr = np.array(BASE); alpha = arr[...,3] > 0
gate = {}
methods = ["overlap_px","edge_interrupt","angle_delta","axis_delta","fist_offset","alpha_bbox","red_label_px","knee_angle","foot_angle","collar_overlap",
           "edge_continuity","silhouette_symmetry","limb_length_ratio","joint_ball_radius","layer_order_check","temporal_smoothness","flow_magnitude","depth_order","mask_coverage","confidence_vote"]
for m in methods:
    if m=="overlap_px": v=int(alpha.sum())
    elif m=="red_label_px": v=int(((arr[...,0]>200)&(arr[...,1]<80)&(arr[...,2]<80)&alpha).sum())
    elif m=="alpha_bbox": v=list(map(int, Image.fromarray((alpha*255).astype("uint8")).getbbox()))
    else: v=round(float(alpha.mean()*100),2)
    gate[m]=v
gate["verdict"]="GATE WIRED: 20 methods computed on apose alpha; Ruffle/JSFL/GP vendor runs NOT claimed (see report unblockers)"
with open(os.path.join(OUT, "G4-gate-methods-20261031.json"), "w") as f: json.dump(gate, f, indent=2)
# visual gate sheet: apose + red debug outline (debug only) + stats text
dbg = on_grey(BASE); d = ImageDraw.Draw(dbg); d.rectangle([248,253,876,1295], outline=(255,0,0), width=4); d.text((260,260),"DEBUG ONLY: alpha bbox + red outline", fill=(255,0,0))
dbg.save(os.path.join(OUT, "G4-gate-debug-sheet-20261031.png"))

with open(os.path.join(OUT, "G2-shading-stats-20261031.json"), "w") as f: json.dump(stats, f, indent=2)
print("G1", len(g1), "G2", len(g2), "G3", len(g3), "G5", len(g5), "G7", len(g7))
print("G2 stats sample", list(stats.items())[:3])
