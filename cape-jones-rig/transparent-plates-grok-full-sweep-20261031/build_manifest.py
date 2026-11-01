import json, pathlib, collections
import numpy as np
from PIL import Image

BASE = pathlib.Path.home()/"workspace/cape-jones-rig/transparent-plates-grok-full-sweep-20261031"
SRC = pathlib.Path.home()/"workspace/cape-jones-flying/characters/sheets"
OUT = BASE/"plates"
man = []
for src in sorted(SRC.rglob("*")):
    if not src.is_file() or src.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        continue
    rel = str(src.relative_to(SRC))
    group = rel.split("/")[0] if "/" in rel else "root"
    if group == "backgrounds":
        man.append({"source": rel, "group": group, "status": "excluded-background",
                    "reason": "Image IS a background/room, not a figure sheet; cutting its background would destroy it."})
        continue
    dst = OUT/(group if "/" in rel else "root")/(src.stem + ".png")
    try:
        im = Image.open(dst); a = np.array(im)[:, :, 3]
    except Exception as e:
        man.append({"source": rel, "group": group, "status": "FAILED", "error": str(e)})
        continue
    ys, xs = np.where(a > 10)
    frac = float((a > 10).mean())
    man.append({"source": rel, "group": group, "status": "converted",
                "output": str(dst.relative_to(OUT)),
                "size": [int(im.width), int(im.height)],
                "alpha_px_gt10": int((a > 10).sum()), "alpha_frac": frac,
                "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None,
                "quality": "PASS" if 0.05 <= frac <= 0.98 else ("CHECK-low" if frac < 0.05 else "CHECK-high")})
json.dump(man, open(BASE/"conversion-manifest.json", "w"), indent=1)
print("total", len(man), collections.Counter(m["status"] for m in man))
print(collections.Counter(m.get("quality") for m in man if m["status"] == "converted"))
for m in man:
    if m.get("quality", "").startswith("CHECK") or m["status"] == "FAILED":
        print(m["source"], m.get("alpha_frac"), m.get("quality"), m.get("error", ""))
print("by group:")
for g, n in sorted(collections.Counter(m["group"] for m in man).items()):
    c = sum(1 for m in man if m["group"] == g and m["status"] == "converted")
    print(g, "sources", n, "converted", c)
