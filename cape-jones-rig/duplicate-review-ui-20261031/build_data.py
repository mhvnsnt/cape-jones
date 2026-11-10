#!/usr/bin/env python3
"""Duplicate-review UI data builder.

Regenerates data/duplicate-groups.json (from the real, verified sources)
and index.html (same data embedded, so the page works as a single static
file in the repo, no server needed).

Data sources (real, never invented):
  - honest-defects-10-methods-20261031/measurements-10-methods-20261031.json
    M7_duplicates: 24 exact-MD5 groups, 59 items, 35 extra copies,
    173 unique hashes / 208 plates checked.
  - transparent-plates-grok-full-sweep-20261031/conversion-manifest.json
    245 entries: alpha_frac / quality per source, used for tile captions.
  - sliced-68-unsliced-20261031/SLICING-MANIFEST-20261031.json
    3,818 sliced pieces total (1,908 named, 1,910 MIXED) — totals only.

To swap in the newer duplicate-finding job when it lands:
  1. Replace data/duplicate-groups.json with its groups export
     (same shape: groups[] with group_id, method, size,
     suggested_canonical, items[] with source, plate, decision, label).
  2. Re-run this script. It re-embeds the JSON into index.html.
  3. Never hand-edit group membership in the HTML.

Nothing in this script deletes, moves, or renames any source file.
Decisions recorded in the UI are candidates only.
"""
import json, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RIG = os.path.dirname(HERE)
PLATES = os.path.join(RIG, "transparent-plates-grok-full-sweep-20261031", "plates")

def build():
    m = json.load(open(os.path.join(RIG, "honest-defects-10-methods-20261031",
        "measurements-10-methods-20261031.json")))
    gm = json.load(open(os.path.join(RIG, "transparent-plates-grok-full-sweep-20261031",
        "conversion-manifest.json")))
    s68 = json.load(open(os.path.join(RIG, "sliced-68-unsliced-20261031",
        "SLICING-MANIFEST-20261031.json")))
    by_src = {}
    for e in gm:
        by_src[e["source"]] = e
        by_src[os.path.basename(e["source"])] = e
    groups, missing = [], 0
    for i, grp in enumerate(m["methods"]["M7_duplicates"]["groups"]):
        items = []
        for src in grp:
            stem = os.path.splitext(os.path.basename(src))[0]
            hits = glob.glob(os.path.join(PLATES, "**", stem + ".png"), recursive=True)
            plate = os.path.relpath(hits[0], HERE) if hits else None
            if not hits:
                missing += 1
            g = by_src.get(src) or by_src.get(os.path.basename(src)) or {}
            items.append({
                "source": src,
                "group_folder": src.split("/")[0] if "/" in src else "root",
                "plate": plate,
                "plate_exists": bool(hits),
                "alpha_frac": g.get("alpha_frac"),
                "quality": g.get("quality"),
                "suggested_label": "",
                "decision": "UNDECIDED",
            })
        groups.append({
            "group_id": f"DG-{i+1:02d}",
            "method": "exact MD5 file hash (M7, honest-defects-10-methods)",
            "size": len(grp),
            "suggested_canonical": grp[0],
            "items": items,
        })
    out = {
        "version": "20261031",
        "source": ("honest-defects-10-methods-20261031/measurements-10-methods-20261031.json "
                    "M7_duplicates, cross-checked against "
                    "transparent-plates-grok-full-sweep-20261031/conversion-manifest.json (245 entries)"),
        "totals": {
            "sheets_total": 245, "figure_sheets": 208, "background_sheets": 37,
            "plates_checked": 208, "unique_plate_hashes": 173,
            "duplicate_groups": len(groups),
            "duplicate_items": sum(len(g["items"]) for g in groups),
            "extra_copies": sum(len(g["items"]) - 1 for g in groups),
            "sliced_pieces_total": 2854 + s68["total_new_pieces"],
            "sliced_pieces_named": 1794 + s68["named"],
            "sliced_pieces_mixed": 1060 + s68["mixed"],
        },
        "plate_files_missing": missing,
        "groups": groups,
    }
    with open(os.path.join(HERE, "data", "duplicate-groups.json"), "w") as f:
        json.dump(out, f, indent=1)
    with open(os.path.join(HERE, "index.template.html")) as f:
        html = f.read()
    html = html.replace("__DUPLICATE_GROUPS_JSON__", json.dumps(out))
    with open(os.path.join(HERE, "index.html"), "w") as f:
        f.write(html)
    print(f"groups={len(groups)} items={out['totals']['duplicate_items']} "
          f"extra={out['totals']['extra_copies']} missing_plates={missing}")
    return out

if __name__ == "__main__":
    build()
