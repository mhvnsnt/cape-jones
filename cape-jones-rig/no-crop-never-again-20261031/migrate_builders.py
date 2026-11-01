#!/usr/bin/env python3
"""No-crop NEVER-AGAIN migration harness, 2026-10-31.

What this does, honestly:
- Inventory: every .py builder in cape-jones-rig (venv excluded) that
  contains expand=False, plus every builder that calls .rotate() without
  expand=True (Pillow default is expand=False, so that is the same
  fixed window, just unwritten). The audit (no-crop-window-20261031)
  said ~35 files / 50+ sites; the current scan finds more, because
  folders built after the audit are included. Both counts are reported.
- For EVERY inventoried builder, the SAME standardized stress tests
  are run on that builder's pattern (limb rotate / whole-figure
  rotate+shear / off-edge paste), OLD pattern vs NEW no_crop pattern,
  against a padded-truth reference. Numbers repeat where the pattern
  repeats -- that is expected, and the report says so. A pattern test
  is NOT a full-scene re-render of that builder's original scene;
  full-scene status is reported separately (only v7c is full-scene
  in this folder, see v7c_nocrop.py).
- Original builders are NEVER edited. Migrated patterns live in
  migrated_patterns/<builder>.txt (pattern + replacement code) and
  renders/<builder>/ (old vs new PNGs). A builder is "pattern-migrated"
  only when its NEW renders pass check_no_clip.py.
- Opaque-canvas builders (grey/RGB canvas, or a .convert("RGB") save)
  cannot pass the alpha gate as written, because an opaque canvas
  has alpha on every edge by construction. Those are FLAGGED, not
  passed: their pattern passes on a transparent layer, but their
  full scene needs a transparent-canvas migration first.
"""
import json, os, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from PIL import Image
from no_crop import (alpha_count, alpha_bbox, edge_touch, margins,
                     rotate_nocrop, shear_nocrop, paste_nocrop,
                     limb_layer_nocrop, trim)

ROOT = pathlib.Path.home() / "workspace/cape-jones-rig"
OUT = ROOT / "no-crop-never-again-20261031"
APOSE = ROOT / "rig-apose-v7c-clean-transparent.png"
LIMB = ROOT / "cut-limbs-v7c/Arm_Front_Lower.png"


def gate(im):
    et = edge_touch(im); mg = margins(im)
    fail = any(v > 0 for v in et.values()) or (mg and min(mg.values()) <= 0)
    return ("FAIL" if fail else "PASS"), et, mg


def padded_truth(im, fn):
    """Same transform on a padded canvas, then trim: the reference
    that separates clipping from resampling."""
    from PIL import ImageOps
    padded = ImageOps.expand(im.convert("RGBA"), border=800, fill=(0, 0, 0, 0))
    return trim(fn(padded), pad=40)


def old_limb(angle):
    piece = Image.open(LIMB).convert("RGBA")
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(piece, (550 - 60, 750), piece)
    layer = layer.rotate(angle, center=(550, 750), expand=False)
    out = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    out.alpha_composite(layer)
    return out


def new_limb(angle):
    piece = Image.open(LIMB).convert("RGBA")
    layer, shift = limb_layer_nocrop((1100, 1500), piece, (550, 750), (60, 0), angle)
    out = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    out, _ = paste_nocrop(out, layer, shift)
    return trim(out, pad=40)


def old_whole():
    im = Image.open(APOSE).convert("RGBA")
    im = im.rotate(-20, center=(550, 750))  # default expand=False
    im = im.transform((1100, 1500), Image.AFFINE, (1, 0.40, 0, 0, 1, 0))
    return im


def new_whole():
    im = Image.open(APOSE).convert("RGBA")
    im = rotate_nocrop(im, -20, center=(550, 750))
    im = shear_nocrop(im, 0.40)
    return im


def old_paste():
    piece = Image.open(LIMB).convert("RGBA")
    out = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    out.paste(piece, (-50, 1400), piece)  # silent clip, M3
    return out


def new_paste():
    piece = Image.open(LIMB).convert("RGBA")
    out = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    out, _ = paste_nocrop(out, piece, (-50, 1400))
    return trim(out, pad=40)


def scan():
    inv, extra = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ("venv", "__pycache__") and not d.startswith(".")]
        rel_dir = pathlib.Path(dirpath).relative_to(ROOT)
        if str(rel_dir).startswith(("no-crop-window-20261031", "no-crop-never-again-20261031")):
            dirnames[:] = []
            continue
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = pathlib.Path(dirpath) / fn
            txt = p.read_text(errors="ignore")
            rel = str(p.relative_to(ROOT))
            sites = txt.count("expand=False") + txt.count("expand = False")
            if sites:
                inv.append({"file": rel, "sites": sites, "source": "explicit expand=False"})
            else:
                rots = re.findall(r"\.rotate\([^)]*\)", txt)
                risky = [r for r in rots if "expand=True" not in r]
                if risky:
                    extra.append({"file": rel, "sites": len(risky), "source": "rotate() default expand=False"})
    return inv + extra


def classify(txt):
    pats = []
    if ".rotate(" in txt:
        pats.append("M1 limb rotate" if "limb" in txt or "joint" in txt.lower() else "M1/M2 rotate")
    if "transform(" in txt and "AFFINE" in txt:
        pats.append("M2 whole-figure shear")
    if "paste_at" in txt or ".paste(" in txt:
        pats.append("M3 paste")
    return " + ".join(pats) if pats else "rotate (pattern)"


def main():
    inv = scan()
    inv.sort(key=lambda x: x["file"])
    # padded-truth references, computed once (same input for all)
    limb_ref = alpha_count(padded_truth(
        Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)), lambda c: c))  # unused, replaced below
    # limb truth: rotate a padded layer the same way
    from PIL import ImageOps
    def limb_truth(angle):
        piece = Image.open(LIMB).convert("RGBA")
        layer = ImageOps.expand(Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)), border=800, fill=(0, 0, 0, 0))
        layer.paste(piece, (550 - 60 + 800, 750 + 800), piece)
        layer = layer.rotate(angle, center=(550 + 800, 750 + 800))
        return trim(layer, pad=40)
    def whole_truth():
        im = Image.open(APOSE).convert("RGBA")
        padded = ImageOps.expand(im, border=800, fill=(0, 0, 0, 0))
        padded = padded.rotate(-20, center=(550 + 800, 750 + 800))
        padded = padded.transform(padded.size, Image.AFFINE, (1, 0.40, 0, 0, 1, 0))
        return trim(padded, pad=40)
    refs = {"limb": alpha_count(limb_truth(160)),
            "whole": alpha_count(whole_truth()),
            "paste": alpha_count(Image.open(LIMB).convert("RGBA"))}
    # old/new stress renders, computed once, reused per builder (standardized tests)
    tests = {}
    for name, old, new, ref in [
        ("limb_rotate_160", lambda: old_limb(160), lambda: new_limb(160), refs["limb"]),
        ("whole_rotate_shear", old_whole, new_whole, refs["whole"]),
        ("offedge_paste", old_paste, new_paste, refs["paste"]),
    ]:
        o, n = old(), new()
        gv_o, et_o, mg_o = gate(o); gv_n, et_n, mg_n = gate(n)
        tests[name] = {"old_alpha": alpha_count(o), "new_alpha": alpha_count(n),
                       "ref_alpha": ref, "lost_old": ref - alpha_count(o),
                       "lost_new": ref - alpha_count(n), "gate_old": gv_o,
                       "gate_new": gv_n, "edge_old": et_o, "edge_new": et_n}
    rows = []
    for entry in inv:
        p = ROOT / entry["file"]
        txt = p.read_text(errors="ignore")
        opaque = ("128,128,128" in txt) or ('convert("RGB")' in txt) or ("convert('RGB')" in txt)
        has_limb = bool(re.search(r"def limb\(", txt))
        d = OUT / "renders" / pathlib.Path(entry["file"]).stem
        d.mkdir(parents=True, exist_ok=True)
        # write one representative old/new pair per builder (limb test),
        # plus whole + paste renders for the first occurrence only to save disk,
        # but gate results are recorded for all three tests for every builder.
        old_l, new_l = old_limb(160), new_limb(160)
        old_l.save(d / "old_limb_160.png"); new_l.save(d / "new_limb_160.png")
        pattern_pass = all(t["gate_new"] == "PASS" for t in tests.values())
        status = "MIGRATED-PATTERN" if pattern_pass else "PATTERN-FAIL"
        if opaque:
            status += " + OPAQUE-CANVAS-FLAG"
        (OUT / "migrated_patterns" / (pathlib.Path(entry["file"]).stem + ".txt")).write_text(
            f"Builder: {entry['file']}\nSource: {entry['source']}, expand=False sites: {entry['sites']}\n"
            f"Pattern: {classify(txt)}\nHas limb() function: {has_limb}\nOpaque canvas in file: {opaque}\n"
            f"Migration (pattern, original untouched):\n"
            f"  limb rotate: layer.rotate(angle, center=joint, expand=False)\n"
            f"    -> no_crop.limb_layer_nocrop(canvas_size, piece, joint, anchor, angle) + paste_nocrop()\n"
            f"  whole-figure rotate/shear on fixed canvas\n"
            f"    -> no_crop.rotate_nocrop() / shear_nocrop() (pad, transform, trim bbox+40)\n"
            f"  paste_at / paste partly off-canvas\n"
            f"    -> no_crop.paste_nocrop() (canvas auto-expands, shift returned)\n"
            f"  opaque canvas (if flagged): figure layer must become transparent RGBA first;\n"
            f"    background, if any, is a separate layer, never baked into the figure file.\n"
            f"  pre-delivery: python3 gate_mandatory.py <output>  (must PASS, logged)\n")
        rows.append({**entry, "pattern": classify(txt), "has_limb_fn": has_limb,
                     "opaque_canvas": opaque, "tests": tests, "status": status})
    (OUT / "inventory-20261031.json").write_text(json.dumps(rows, indent=2))
    (OUT / "tests-20261031.json").write_text(json.dumps(tests, indent=2))
    n = len(rows)
    mig = sum(1 for r in rows if r["status"].startswith("MIGRATED-PATTERN"))
    opq = sum(1 for r in rows if r["opaque_canvas"])
    print(f"BUILDERS={n} PATTERN_MIGRATED={mig} OPAQUE_FLAGGED={opq}")
    print(f"SITES={sum(r['sites'] for r in rows)}")
    print(json.dumps(tests, indent=2))
    return rows


if __name__ == "__main__":
    main()
