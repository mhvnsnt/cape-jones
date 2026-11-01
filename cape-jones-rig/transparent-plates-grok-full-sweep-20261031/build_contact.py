#!/usr/bin/env python3
"""Contact: sample across groups, grey original top, transparent on checkerboard below."""
import json, pathlib
from PIL import Image, ImageDraw
BASE = pathlib.Path.home()/"workspace/cape-jones-rig/transparent-plates-grok-full-sweep-20261031"
SRC = pathlib.Path.home()/"workspace/cape-jones-flying/characters/sheets"
man = json.load(open(BASE/"conversion-manifest.json"))
conv = [m for m in man if m["status"]=="converted"]
# pick up to 3 per group, preferring cape sheets first, then first alphabetical
import collections
byg = collections.defaultdict(list)
for m in conv: byg[m["group"]].append(m)
samples=[]
cape_first = [m for m in conv if "cape" in m["source"].lower()]
for m in cape_first: samples.append(m)
for g in sorted(byg):
    for m in sorted(byg[g], key=lambda x: x["source"])[:3]:
        if m not in samples: samples.append(m)
# checkerboard
def checker(size, cell=20):
    img = Image.new("RGB", size, (255,255,255))
    d = ImageDraw.Draw(img)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x//cell + y//cell) % 2: d.rectangle([x,y,x+cell-1,y+cell-1], fill=(200,200,200))
    return img
TW=320
rows=[]
for m in samples:
    src = Image.open(SRC/m["source"]).convert("RGB")
    dst = Image.open(BASE/"plates"/m["output"]).convert("RGBA")
    for im in (src, dst):
        pass
    # thumb sizes
    def thumb(im, bg=None):
        w,h = im.size; s = TW/w; nh = max(1, int(h*s))
        t = im.resize((TW, nh))
        if bg is not None:
            bgim = bg((TW, nh)); bgim.paste(t, (0,0), t); return bgim
        return t.convert("RGB")
    top = thumb(src); bot = thumb(dst, bg=checker)
    rows.append((m, top, bot))
# stack: each sample = top+bottom side by side? Simpler: grid 4 columns, each cell top original / bottom checker, labelled
cols=4
cellh = max(max(r[1].height, r[2].height) for r in rows) + 40
# build per-sample vertical pair
pairs=[]
for m, top, bot in rows:
    h = top.height + bot.height + 30
    pair = Image.new("RGB", (TW, h), (30,30,30))
    pair.paste(top, (0,15)); pair.paste(bot, (0,15+top.height))
    d = ImageDraw.Draw(pair); d.text((4,1), m["source"][:44], fill=(255,255,0))
    pairs.append(pair)
rows_n = (len(pairs)+cols-1)//cols
H = rows_n * max(p.height for p in pairs)
sheet = Image.new("RGB", (cols*TW, H), (20,20,20))
for i, p in enumerate(pairs):
    sheet.paste(p, ((i%cols)*TW, (i//cols)*p.height))
sheet.save(BASE/"transparency-contact-grok-full-sweep-20261031.png")
print(f"samples {len(samples)} contact {sheet.size}")
for m in samples: print(m["group"], m["source"], f"{m['alpha_frac']:.3f}", m["quality"])
