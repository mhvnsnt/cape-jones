#!/usr/bin/env python3
"""No-clip gate: FAIL if a rendered figure touches the canvas edge.

Usage:
  python3 check_no_clip.py <image-or-dir> [...]
  python3 check_no_clip.py --compare <source.png> <rendered.png>  # also
      checks rendered alpha against a padded-truth transform (see notes)

Rules (NO-CROP-WINDOW RULE, Mars 2026-10-31 19:22 CDT):
  - FAIL if any alpha>0 pixel sits on the outermost row/column of the
    canvas (top, bottom, left or right edge touch > 0). A figure that
    touches the window may already be clipped; a whole figure never
    touches it, because trim() leaves PAD transparent pixels around it.
  - FAIL if the alpha bbox has a 0-px margin on any side (same test, in
    bbox terms).
  - PASS requires edge touch == 0 on all four sides.
  - With --compare, also FAIL if rendered alpha count is more than
    0.5% below the reference count. NOTE on resampling: a transform
    (rotate/shear) itself resamples pixels, so the reference must be
    the SAME transform run on a padded canvas (padded-truth), not the
    untransformed source. Comparing a sheared figure to the unsheared
    source and calling the resampling difference "loss" would be
    wrong; the padded-truth comparison is what separates clipping
    from resampling. Old-vs-new numbers in the report use padded-truth.

Exit code: 0 = all PASS, 1 = any FAIL. Prints one JSON object per file.
OpenCV cross-check: cv2.boundingRect is run when cv2 is installed
(it is, in the rig venv, cv2 5.0.0); if absent, the report says
"cv2": "not installed, numpy/Pillow bbox used" and does not fail on
that account.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from no_crop import alpha_bbox, alpha_count, edge_touch, margins, cv2_bbox
from PIL import Image


def check(path):
    im = Image.open(path).convert("RGBA")
    et = edge_touch(im); mg = margins(im)
    try:
        cb = cv2_bbox(im)
        cv2_note = list(cb) if cb else None
    except ImportError:
        cv2_note = "not installed, numpy/Pillow bbox used"
    fail = []
    if any(v > 0 for v in et.values()):
        fail.append("alpha touches canvas edge: %s" % et)
    if mg and min(mg.values()) <= 0:
        fail.append("alpha bbox margin <= 0: %s" % mg)
    return {
        "file": path, "size": list(im.size), "alpha_px": alpha_count(im),
        "bbox": list(alpha_bbox(im)) if alpha_bbox(im) else None,
        "edge_touch": et, "margins": mg, "cv2_bbox_xywh": cv2_note,
        "verdict": "FAIL" if fail else "PASS", "fail_reasons": fail,
    }


def main(argv):
    if argv[:1] == ["--compare"]:
        src, ren = argv[1], argv[2]
        r = check(ren)
        ref = alpha_count(Image.open(src).convert("RGBA"))
        r["reference_alpha_px"] = ref
        r["alpha_delta_vs_reference"] = r["alpha_px"] - ref
        if ref and r["alpha_px"] < ref * 0.995:
            r["verdict"] = "FAIL"
            r["fail_reasons"].append(
                "alpha more than 0.5%% below reference (%d vs %d)" % (r["alpha_px"], ref))
        print(json.dumps(r, indent=2)); return 0 if r["verdict"] == "PASS" else 1
    paths = []
    for a in argv:
        if os.path.isdir(a):
            paths += sorted(os.path.join(a, f) for f in os.listdir(a)
                            if f.lower().endswith(".png"))
        else:
            paths.append(a)
    results = [check(p) for p in paths]
    for r in results:
        print(json.dumps(r))
    bad = [r for r in results if r["verdict"] == "FAIL"]
    print("GATE: %d/%d PASS" % (len(results) - len(bad), len(results)),
          file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
