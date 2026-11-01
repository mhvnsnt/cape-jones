"""Extended full-res numeric QC, 2026-11-01 (read-only on sources).
Extends build-still-20261101/inspection/qc_all.py with:
 - SHA256 duplicate groups (exact-byte duplicates) across all 3,818
 - aspect outliers (bbox aspect > 8 or < 0.125)
 - single-colour pieces (all opaque px one RGB)
 - size outliers (opaque px > 500,000 or bbox area > 1,000,000)
 - per-top-folder counts for the old set
Outputs JSON text only in this folder. No PNG output, no original touched.
"""
import os, json, hashlib
from PIL import Image
import numpy as np
ROOT = '/home/hatch/workspace/cape-jones-rig'
OUT = '/home/hatch/workspace/cape-jones-rig/fla-compare-flex-inspect-20261101/inspection'
sets = {'old_sliced_clean': ROOT + '/sliced-clean-20261031',
        'new_sliced_68_sheets': ROOT + '/sliced-68-unsliced-20261031/sheets'}
all_rows = []
summary = {}
for name, base in sets.items():
    files = []
    for dp, dn, fn in os.walk(base):
        for f in fn:
            if f.lower().endswith('.png'):
                files.append(os.path.join(dp, f))
    files.sort()
    blank = tiny = corrupt = 0; tot = 0
    aspect_out = []; single_colour = []; huge = []
    per_folder = {}
    for p in files:
        rel = os.path.relpath(p, ROOT)
        top = rel.split('/')[1] if '/' in rel else rel
        per_folder[top] = per_folder.get(top, 0) + 1
        try:
            with open(p, 'rb') as fh:
                h = hashlib.sha256(fh.read()).hexdigest()
            im = Image.open(p); im.load()
            a = np.array(im.convert('RGBA'))
            alpha = a[:, :, 3] > 10
            op = int(alpha.sum())
            tot += op
            ys, xs = np.where(alpha)
            if op == 0:
                blank += 1
                bw = bh = 0; aspect = 0
            else:
                bw = int(xs.max() - xs.min() + 1); bh = int(ys.max() - ys.min() + 1)
                aspect = round(bw / bh, 3) if bh else 0
                if aspect > 8 or aspect < 0.125:
                    aspect_out.append({"file": rel, "bbox": [bw, bh], "aspect": aspect, "opaque": op})
                if bw * bh > 1000000 or op > 500000:
                    huge.append({"file": rel, "bbox": [bw, bh], "opaque": op})
                cols = set(map(tuple, np.unique(a[alpha][:, :3], axis=0).tolist()))
                if len(cols) == 1:
                    single_colour.append({"file": rel, "colour": list(cols)[0], "opaque": op})
            if 0 < op < 800:
                tiny += 1
            all_rows.append({"file": rel, "sha256": h, "w": im.size[0], "h": im.size[1],
                             "opaque": op, "set": name})
        except Exception as e:
            corrupt += 1
            all_rows.append({"file": rel, "sha256": None, "error": str(e), "set": name})
    summary[name] = {"files": len(files), "blank": blank, "tiny_lt800": tiny,
                     "corrupt": corrupt, "total_opaque_px": tot,
                     "aspect_outliers": len(aspect_out), "single_colour": len(single_colour),
                     "huge": len(huge), "per_top_folder": per_folder,
                     "aspect_outlier_files": aspect_out[:30],
                     "single_colour_files": single_colour[:30],
                     "huge_files": huge[:30]}
    print(name, {k: v for k, v in summary[name].items() if not isinstance(v, (list, dict))})
# duplicates
by_hash = {}
for r in all_rows:
    if r.get("sha256"):
        by_hash.setdefault(r["sha256"], []).append(r["file"])
dup_groups = {h: fs for h, fs in by_hash.items() if len(fs) > 1}
dup_extra = sum(len(fs) - 1 for fs in dup_groups.values())
print("duplicate groups:", len(dup_groups), "extra copies:", dup_extra)
for h, fs in list(dup_groups.items())[:20]:
    print("  DUP", h[:12], fs)
# manifest re-check
m = json.load(open(ROOT + '/sliced-68-unsliced-20261031/SLICING-MANIFEST-20261031.json'))
summary["new_manifest"] = {"sheets": m["sheets_sliced"], "pieces": m["total_new_pieces"],
                           "named": m["named"], "mixed": m["mixed"],
                           "named_check_sum": sum(s["named"] for s in m["sheets"]),
                           "mixed_check_sum": sum(s["mixed"] for s in m["sheets"])}
summary["duplicates"] = {"groups": len(dup_groups), "extra_copies": dup_extra,
                         "groups_detail": {h: fs for h, fs in list(dup_groups.items())[:50]}}
summary["total_files"] = sum(summary[s]["files"] for s in sets)
json.dump(summary, open(os.path.join(OUT, "qc-fullres-3818-20261101.json"), "w"), indent=1)
print("TOTAL", summary["total_files"])
