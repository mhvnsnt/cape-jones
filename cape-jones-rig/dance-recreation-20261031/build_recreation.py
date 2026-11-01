"""Dance recreation builder, 2026-10-31.
Method: IMAGE-INTERPOLATION between already-corrected rendered frames.
NOT a rig re-pose: keys are the approved-corrected renders, inbetweens are
alpha cross-blends (t=0.5) between consecutive timeline steps.
Timing preserved: same total duration as the originals, more drawings/sec.
A: arm-snap keys (63, f001..f109 on twos) -> fill to 109-step grid -> 217 frames @48fps (4.52s)
B: combine frames (108 consecutive f000..f107) -> 215 frames @48fps (4.48s)
Audio: SILENT. No song invented. See AUDIO-SLOT doc.
"""
import os, re
from PIL import Image
BASE = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(BASE, "dance-recreation-20261031")

def load(p):
    return Image.open(p).convert("RGBA")

def blend(a, b, t=0.5):
    return Image.blend(a, b, t)

def build_a():
    src = os.path.join(BASE, "dance-arm-snap-20261031/frames")
    files = sorted(os.listdir(src))
    keys = {}
    for f in files:
        n = int(re.search(r'f(\d+)', f).group(1))
        keys[n] = load(os.path.join(src, f))
    # fill 1..109 grid: key where present, else midpoint blend of neighbours
    grid = {}
    for n in range(1, 110):
        if n in keys:
            grid[n] = keys[n]
        else:
            # neighbours are n-1 and n+1 (both keys, since maxgap=2)
            grid[n] = blend(keys[n-1], keys[n+1], 0.5)
    # now double to 48fps: 1 inbetween between each consecutive grid step
    seq = []
    steps = list(range(1, 110))
    for i, n in enumerate(steps):
        seq.append(grid[n])
        if i < len(steps)-1:
            seq.append(blend(grid[n], grid[n+1], 0.5))
    outdir = os.path.join(OUT, "frames-a")
    for i, im in enumerate(seq):
        im.save(os.path.join(outdir, f"rec-a-f{i:03d}.png"))
    return seq, keys, grid

def build_b():
    src = os.path.join(BASE, "mochiichao-combine-build-20261031/frames")
    files = sorted(os.listdir(src))
    keys = [load(os.path.join(src, f)) for f in files]  # 108 consecutive
    seq = []
    for i, im in enumerate(keys):
        seq.append(im)
        if i < len(keys)-1:
            seq.append(blend(im, keys[i+1], 0.5))
    outdir = os.path.join(OUT, "frames-b")
    for i, im in enumerate(seq):
        im.save(os.path.join(outdir, f"rec-b-f{i:03d}.png"))
    return seq, keys

seqA, keysA, gridA = build_a()
seqB, keysB = build_b()
print(f"A: keys={len(keysA)} grid=109 seq={len(seqA)} @48fps={len(seqA)/48:.2f}s")
print(f"B: keys={len(keysB)} seq={len(seqB)} @48fps={len(seqB)/48:.2f}s")

# contact strips: key -> inbetween -> key
def strip(imgs, labels, path, w=440):
    # imgs are full-size; downscale to w, height proportional
    thumbs = []
    for im in imgs:
        h = int(im.size[1] * w / im.size[0])
        bg = Image.new("RGBA", (w, h), (128,128,128,255))
        t = im.resize((w, h))
        bg.alpha_composite(t)
        thumbs.append(bg.convert("RGB"))
    H = thumbs[0].size[1]
    sheet = Image.new("RGB", (w*len(thumbs), H+30), (255,255,255))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(thumbs):
        sheet.paste(t, (i*w, 30))
        d.text((i*w+8, 8), labels[i], fill=(0,0,0))
    sheet.save(path)
    print(path, sheet.size)

# A transitions: grid f015 (key) -> f016 (interp) -> f017 (key); and kick f042->f043->f044
# seqA index: grid step n is at seq index (n-1)*2
def seqA_at(n): return seqA[(n-1)*2]
strip([gridA[15], blend(gridA[15], gridA[17], 0.5) if False else seqA[(15-1)*2+1], gridA[17]],
      ["A f015 KEY", "A f015.5 INBETWEEN", "A f017 KEY"],
      os.path.join(OUT, "contact-a-transition-f015-20261031.png"))
strip([gridA[42], seqA[(42-1)*2+1], gridA[43] if 43 in gridA else gridA[44]],
      ["A f042 KEY kick", "A inbetween", "A next KEY"],
      os.path.join(OUT, "contact-a-transition-kick-20261031.png"))
# B transitions: first two pairs
strip([keysB[0], seqB[1], keysB[1]], ["B f000 KEY", "B inbetween", "B f001 KEY"],
      os.path.join(OUT, "contact-b-transition-20261031.png"))
strip([keysB[40], seqB[81], keysB[41]], ["B f040 KEY", "B inbetween", "B f041 KEY"],
      os.path.join(OUT, "contact-b-transition2-20261031.png"))
