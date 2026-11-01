"""10-flex figure-extraction attempt #2 (2026-11-01) — NEW methods, not a re-run.
Source: transparent-plates-grok-full-sweep-20261031/plates/exposure-sheets/exposure-sheet-10-flex.png
Methods (all read-only on the source; outputs are JSON text only, no PNGs):
 A. Re-confirm alpha components in the figure column (x300-860).
 B. White-suit components: opaque AND NOT near-black (RGB sum >= 150).
    If white suit separated per figure, this yields ~10 large components.
 C. Purple-head scan: per-row purple-px counts in the figure column; find
    head bands (purple clusters) for all 10 frames, including the 4 whose
    cowls did not isolate as single blobs in attempt #1.
 D. Row-width profile: opaque width per row (figure column) — overlap zones
    show as sustained wide runs, not gaps.
 E. Cut-line proposal (TEXT ONLY): midpoint between successive head centres
    as a PROPOSED manual rotoscope cut for Mars approval. These are NOT
    extracted strips and are NOT counted as split.
Purple rule (from FLA measurement, dark violet ~80,20,110):
    B > R+10 and B >= 85 and G <= 90 and R <= 170.
Near-black: R+G+B < 150.
"""
import json
from PIL import Image
from collections import deque

SRC = "/home/hatch/workspace/cape-jones-rig/transparent-plates-grok-full-sweep-20261031/plates/exposure-sheets/exposure-sheet-10-flex.png"
OUT = "/home/hatch/workspace/cape-jones-rig/fla-compare-flex-inspect-20261101/flex-10"
im = Image.open(SRC).convert("RGBA")
W, H = im.size
px = list(im.getdata())

def idx(x, y):
    return y * W + x

def is_opaque(p):
    return p[3] > 10

def is_black(p):
    return p[3] > 10 and (p[0] + p[1] + p[2]) < 150

def is_purple(p):
    r, g, b, a = p
    return a > 10 and b > r + 10 and b >= 85 and g <= 90 and r <= 170

# --- A. alpha components in figure column (BFS, 4-connectivity on the mask) ---
X0, X1 = 300, 860
mask = {}
for y in range(H):
    for x in range(X0, X1):
        if is_opaque(px[idx(x, y)]):
            mask[(x, y)] = True
seen = set()
comps = []
for start in list(mask):
    if start in seen:
        continue
    q = deque([start]); seen.add(start)
    pts = []
    while q:
        x, y = q.popleft(); pts.append((x, y))
        for nb in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if nb in mask and nb not in seen:
                seen.add(nb); q.append(nb)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    comps.append({"area": len(pts), "x0": min(xs), "y0": min(ys), "x1": max(xs), "y1": max(ys)})
comps.sort(key=lambda c: -c["area"])
print("A alpha components >=800px:", [c for c in comps if c["area"] >= 800][:6])

# --- B. white-suit components (opaque, not near-black) in figure column ---
mask2 = {}
for y in range(H):
    for x in range(X0, X1):
        p = px[idx(x, y)]
        if is_opaque(p) and not is_black(p):
            mask2[(x, y)] = True
seen = set(); comps2 = []
for start in list(mask2):
    if start in seen:
        continue
    q = deque([start]); seen.add(start); pts = []
    while q:
        x, y = q.popleft(); pts.append((x, y))
        for nb in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if nb in mask2 and nb not in seen:
                seen.add(nb); q.append(nb)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    comps2.append({"area": len(pts), "x0": min(xs), "y0": min(ys), "x1": max(xs), "y1": max(ys)})
comps2.sort(key=lambda c: -c["area"])
print("B white-suit components >=800px:", len([c for c in comps2 if c["area"] >= 800]))
for c in comps2[:12]:
    print("   ", c)

# --- C. purple per-row counts -> head bands ---
row_purple = []
for y in range(H):
    n = 0
    for x in range(X0, X1):
        if is_purple(px[idx(x, y)]):
            n += 1
    row_purple.append(n)
# bands: runs of rows with >=20 purple px, merged across gaps <=6 rows
bands = []
in_band = False; s = 0
for y, n in enumerate(row_purple):
    if n >= 20 and not in_band:
        in_band = True; s = y
    elif n < 20 and in_band:
        # look ahead: gap <=6 rows of <20 before next >=20 keeps band alive
        ahead = any(row_purple[y + k] >= 20 for k in range(1, 7) if y + k < H)
        if not ahead:
            bands.append((s, y - 1)); in_band = False
if in_band:
    bands.append((s, H - 1))
band_info = []
for (a, b) in bands:
    tot = sum(row_purple[a:b+1])
    if tot >= 300:
        band_info.append({"y0": a, "y1": b, "centre": round((a + b) / 2, 1), "purple_px": tot,
                          "peak_row": max(range(a, b+1), key=lambda y: row_purple[y])})
print("C purple bands >=300px:", band_info)

# --- D. row-width profile (opaque run width in figure column) ---
widths = []
for y in range(H):
    xs = [x for x in range(X0, X1) if is_opaque(px[idx(x, y)])]
    widths.append((max(xs) - min(xs) + 1) if xs else 0)
# gap rows: width 0 inside y105-1697?
gap_rows = [y for y in range(105, 1698) if widths[y] == 0]
print("D gap rows (width 0) inside figure span y105-1697:", len(gap_rows), gap_rows[:20])
print("D width stats in span: min", min(widths[105:1698]), "max", max(widths[105:1698]),
      "rows<100 wide:", sum(1 for w in widths[105:1698] if 0 < w < 100))

result = {
    "source": SRC, "size": [W, H],
    "A_alpha_components_ge800": [c for c in comps if c["area"] >= 800],
    "B_white_suit_components_ge800_count": len([c for c in comps2 if c["area"] >= 800]),
    "B_white_suit_components_ge800": [c for c in comps2 if c["area"] >= 800][:20],
    "C_purple_bands_ge300": band_info,
    "D_gap_rows_in_span": gap_rows,
    "D_width_min_max": [min(widths[105:1698]), max(widths[105:1698])],
    "ticks": [190, 344, 497, 650, 800, 954, 1108, 1262, 1425, 1571],
}
with open(f"{OUT}/flex10-attempt2-20261101.json", "w") as f:
    json.dump(result, f, indent=1)
print("wrote flex10-attempt2-20261101.json")
