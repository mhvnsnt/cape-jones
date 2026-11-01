"""Ghost measurement for serve-to-guard v3, SAME method as v2 measure_ghost.py:
silhouette = mean-abs distance from grey-128 > 40; edge = silhouette pixel
with a non-silhouette 4-neighbour; double-edge ratio = mid edge / mean(key
edges); wash = pixels in serve-xor-guard silhouette where the mid pixel sits
halfway between that key's pixel and grey (diff to grey 20..120 AND diff to
key >20) — exactly what a 50% crossfade produces in a non-overlap region.
Keys/mid are taken from the v3 xsheet (first serve KEY hold, first guard KEY
hold, serve->guard BREAKDOWN arc frame j=3) and from the v3 view frames,
which are the grey-128 view copies. v1/v2 numbers are QUOTED from the v2
report (not re-measured here) and labelled as such.
"""
import os, csv, json
import numpy as np
from PIL import Image

R = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(R, "workstream-b-sweep-20261031")
FR = os.path.join(OUT, "frames", "serve-to-guard-v3")
# view frames are not saved individually; rebuild view from transparent masters
# on grey-128, same as build_sequence did.
GREY = (128, 128, 128, 255)
masters = []
for i in range(1000):
    p = os.path.join(FR, f"f{i:03d}.png")
    if not os.path.exists(p):
        break
    masters.append(Image.open(p).convert("RGBA"))
print("masters:", len(masters))
uw = max(m.size[0] for m in masters) + 80; uh = max(m.size[1] for m in masters) + 80
uw += uw % 2; uh += uh % 2
ground = uh - 40
view = []
for m in masters:
    c = Image.new("RGBA", (uw, uh), (0, 0, 0, 0))
    c.alpha_composite(m, ((uw - m.size[0]) // 2, ground - m.size[1]))
    view.append(np.asarray(Image.alpha_composite(Image.new("RGBA", (uw, uh), GREY), c).convert("RGB")).astype(int))

rows = list(csv.DictReader(open(os.path.join(OUT, "move-serve-to-guard-v3-20261031-xsheet-20261031.csv"))))
serve_key = next(int(r["frame"]) for r in rows if r["kind"] == "KEY hold" and "serve" in r["from"])
guard_key = next(int(r["frame"]) for r in rows if r["kind"] == "KEY hold" and "guard" in r["from"])
mid = next(int(r["frame"]) for r in rows if "BREAKDOWN arc" in r["kind"] and r["from"].find("serve") >= 0)
print("serve key", serve_key, "guard key", guard_key, "mid", mid)

def sil(a):
    return (np.abs(a - 128).mean(axis=2) > 40)
def edge_of(s):
    e = np.zeros_like(s)
    e[1:-1, 1:-1] = s[1:-1, 1:-1] & (~s[:-2, 1:-1] | ~s[2:, 1:-1] | ~s[1:-1, :-2] | ~s[1:-1, 2:])
    return e
S, G, M = sil(view[serve_key]), sil(view[guard_key]), sil(view[mid])
es, eg, em = edge_of(S).sum(), edge_of(G).sum(), edge_of(M).sum()
xor = S ^ G
wash = 0
for key, arr in ((S, view[serve_key]), (G, view[guard_key])):
    d_grey = np.abs(view[mid] - 128).mean(axis=2)
    d_key = np.abs(view[mid] - arr).mean(axis=2)
    wash += int(((xor & key) & (d_grey >= 20) & (d_grey <= 120) & (d_key > 20)).sum())
# wash counted per key in v2 style: report as fraction of xor pixels (v2 used
# 25,525/26,532 = union-style single count; here take max per-key overlap to
# stay comparable, and also report raw)
res = {"serve_key_frame": serve_key, "guard_key_frame": guard_key, "mid_frame": mid,
       "mid_silhouette_px": int(M.sum()), "mid_edge_px": int(em),
       "key_edge_mean": float((es + eg) / 2), "double_edge_ratio": float(em / ((es + eg) / 2)),
       "xor_px": int(xor.sum()), "wash_px": int(wash),
       "wash_pct": float(100 * wash / max(1, int(xor.sum()))),
       "v1_quoted_from_v2_report": {"double_edge_ratio": 1.32, "wash_pct": 96.2},
       "v2_quoted_from_v2_report": {"double_edge_ratio": 1.01, "wash_pct": 17.2}}
print(json.dumps(res, indent=1))
with open(os.path.join(OUT, "serve-to-guard-v3-ghost-20261031.json"), "w") as fh:
    json.dump(res, fh, indent=1)
