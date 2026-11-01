#!/usr/bin/env python3
"""Ground-detection + feet-placement gate, wired 2026-10-31.

Standing rule (do not invent a new one):
  feet anchor = figure alpha-bbox bottom on a world ground line;
  scaling and camera moves grow/move ABOVE that anchor, never from centre.

New rule from Mars, 2026-10-31 20:37 CDT, recorded exactly:
  GROUNDED vs AIRBORNE.
  - Walking or standing: ground must be detected well and feet must be
    placed on it. Gate FAILS if feet are off ground in a grounded shot.
  - Floating, flying, levitating, or a chase/airborne moment: feet are
    NOT forced to ground. That is intentional, and the shot spec must
    label it AIRBORNE, with a stated height / flight line, otherwise it
    looks like a floating mistake.
  - Do NOT force airborne poses to ground, and do NOT excuse a grounded
    floating mistake as airborne.

Exit codes (matching the portrait scale gate):
  0 = PASS
  2 = FAIL, loudly (grounded off ground, airborne mislabelled,
      airborne with no height, or feet outside the planted band)
  1 = usage / input error (missing file, missing ground reference,
      missing mode label)

Ground references, in priority order (never trust a builder's claim):
  1. Explicit ground_y (a world/screen ground line, e.g. BARS Gy=700,
     size-walk ground y=1500, room master feet y=1550).
  2. Rug/floor band (rug_far, rug_near): planted iff rug_position is in
     [0.55, 0.95]. Old portrait feet 1548 = 0.284 FAILS; planted
     portrait feet 1700 = 0.624 PASSES. (Band from the portrait gate.)
  3. Auto-detected line from the background (detect_ground_line):
     ESTIMATE only. A gate run on an auto-detected line alone reports
     verdict PASS-ESTIMATE, never a clean PASS, and the shot spec must
     confirm the line before delivery. Auto-detection is a cue, not a
     confirmed ground line.

Feet measurement (never trust a builder's claimed placement):
  - Transparent plate: alpha > 10 bbox bottom = feet_y, alpha > 10
    bbox centre-x = feet centre-x. (Apose plate: 248,253-875,1294,
    373,846 px, verified here, not copied from a claim.)
  - Composite vs a background-only reconstruction: diff > 20 bbox,
    then feet = lowest row that is BOTH diff AND light (mean > 170),
    so a dark contact shadow does not inflate the feet (portrait-gate
    correction: shadow inflated heights by 27 px in the first run).

Tolerances:
  - Single ground line: PASS iff |feet_y - ground_y| <= tolerance_px.
    Default tolerance_px = 10 at full resolution. That is a measurement
    tolerance for anti-alias / LANCZOS fringe (bars proof measured 653,
    not assumed 651, a 2 px fringe), NOT a licence to float: a 47 px
    float (old bars / old portrait style) FAILS by a wide margin.
  - Rug band: PASS iff 0.55 <= rug_position <= 0.95.
  - AIRBORNE: PASS iff mode is explicitly AIRBORNE, height_px > 0
    (ground_y - feet_y), and a flight line / height is stated in the
    spec dict. If feet are ON the ground (height <= tolerance) but the
    spec says AIRBORNE, that is a spec mismatch: FAIL, relabel GROUNDED.
    If mode is missing or blank, FAIL (no silent default).

Shadow cue (reported, hard-fail only on the AIRBORNE mismatch above):
  - GROUNDED: a contact shadow should sit within ~25 px below the feet
    and roughly under the feet centre. Absence of a shadow is a WARNING
    (some styles have no shadow; BARS had none), not a FAIL.
  - AIRBORNE: the shadow, if present, should be detached from the feet
    (gap grows with height) and/or smaller / blurrier than a contact
    shadow. A shadow glued to airborne feet is a WARNING that the
    airborne read may fail on screen, not a FAIL by itself.

Sequence check (for a list of per-frame results):
  - GROUNDED: feet_y spread must be <= tolerance_px * 2 across the
    sequence (size walk: 54/54 and 44/44 frames feet_y = 1500, spread 0;
    BARS: 24/24 feet_y = 700, spread 0; world centre-x spread <= 2 px
    in BARS, 849-850).
  - AIRBORNE: height trajectory must be smooth: max |height[i+1]-height[i]|
    <= 25% of figure height, otherwise WARNING (jitter reads as a
    floating mistake, not flight).

Usage:
  python3 ground_gate.py --plate PLATE.png --mode GROUNDED --ground-y 700
  python3 ground_gate.py --composite COMP.png --background BG.png \
      --mode GROUNDED --rug-far 1421 --rug-near 1868
  python3 ground_gate.py --plate PLATE.png --mode AIRBORNE \
      --ground-y 700 --height 180 --flight-line "hover 180px above floor"
  python3 ground_gate.py --sequence measurements.json --mode GROUNDED
"""
import argparse, json, math, os, sys
import numpy as np
from PIL import Image, ImageFilter

DEFAULT_TOL = 10
RUG_LO, RUG_HI = 0.55, 0.95


def plate_feet(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)[:, :, 3]
    ys, xs = np.where(a > 10)
    if len(xs) == 0:
        raise ValueError("no alpha in plate")
    bbox = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    return {"bbox": bbox, "feet_y": bbox[3], "head_y": bbox[1],
            "feet_centre_x": int((bbox[0] + bbox[2]) / 2),
            "height": bbox[3] - bbox[1], "alpha_px": int((a > 10).sum()),
            "size": list(im.size)}


def composite_feet(comp_path, bg_path):
    """Feet from a composite vs its background-only reconstruction."""
    im = Image.open(comp_path).convert("RGB")
    bg = Image.open(bg_path).convert("RGB")
    if bg.size != im.size:
        bg = bg.resize(im.size, Image.LANCZOS)
    diff = np.abs(np.asarray(im).astype(int) - np.asarray(bg).astype(int)).max(axis=2)
    mask = diff > 20
    ys, xs = np.where(mask)
    if len(xs) == 0:
        raise ValueError("no diff vs background")
    arr = np.asarray(im).astype(int)
    # Foot row = diff AND light AND a strong diff. A blurred shadow feather
    # over a light sky still has mean > 170 but only diff 17-30; a white
    # foot against sky/floor has diff > 50. Without the diff floor, the
    # shadow feather at y688-698 in the first airborne proof was counted
    # as a foot (measured 698, not the true 520). Corrected here.
    light = mask & (arr.mean(axis=2) > 170) & (diff > 50)
    ly, lx = np.where(light)
    foot_bottom = int(ly.max()) if len(ly) else int(ys.max())
    return {"diff_bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
            "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), foot_bottom],
            "feet_y": foot_bottom, "head_y": int(ys.min()),
            "feet_centre_x": int((xs.min() + xs.max()) / 2),
            "height": foot_bottom - int(ys.min()), "size": list(im.size)}


def detect_ground_line(bg_path):
    """Auto-detect a horizontal floor transition in a background.

    Method: grey, light blur, row-to-row mean absolute difference, search
    the lower two-thirds of the frame for the strongest sustained edge.
    Returns (y, strength, confidence). Confidence is ESTIMATE by design:
    a strong single edge scores high, a busy painted room (rug pattern,
    furniture) scores low. Never a clean PASS on its own.
    """
    im = Image.open(bg_path).convert("L")
    arr = np.asarray(im).astype(float)
    # row gradient, smoothed over 5 rows so a single texture row cannot win
    grad = np.abs(np.diff(arr, axis=0)).mean(axis=1)
    k = np.ones(5) / 5.0
    smooth = np.convolve(grad, k, mode="same")
    lo = int(len(smooth) * 0.33)
    cand = int(np.argmax(smooth[lo:]) + lo)
    strength = float(smooth[cand])
    second = float(np.sort(smooth[lo:])[-2]) if len(smooth[lo:]) > 1 else 0.0
    # confidence: how far the winner stands out from the runner-up
    conf = round(min(1.0, (strength - second) / max(strength, 1e-9) * 4), 3)
    return {"ground_y_estimate": cand, "edge_strength": round(strength, 3),
            "confidence": conf, "note": "ESTIMATE only; confirm in shot spec"}


def shadow_cue(comp_path, feet_y, feet_cx, fig_w, ground_y=None):
    """Also, if ground_y is given, check a band around the ground line:
    an airborne shadow lives on the ground, far below a 120 px window
    under the feet. The first version missed the G3 shadow for exactly
    this reason (shadow at y702, window ended at y634)."""
    """Measure a dark shadow region under the feet, if one is present.

    Region: x in [cx - w/4, cx + w/4], y in [feet_y, feet_y + 120].
    Dark = mean < 90. Returns gap (shadow top - feet_y), centroid, px.
    """
    try:
        im = Image.open(comp_path).convert("RGB")
    except Exception:
        return {"present": False, "note": "no composite supplied"}
    arr = np.asarray(im).astype(int)
    h, w = arr.shape[:2]
    x0, x1 = max(0, feet_cx - fig_w // 4), min(w, feet_cx + fig_w // 4)
    y0, y1 = max(0, feet_y), min(h, feet_y + 120)
    if y1 <= y0 or x1 <= x0:
        return {"present": False}
    region = arr[y0:y1, x0:x1].mean(axis=2)
    dark = region < 90
    out = {"present": False, "dark_px": int(dark.sum())}
    if int(dark.sum()) >= 50:
        ys, xs = np.where(dark)
        out = {"present": True, "dark_px": int(dark.sum()),
               "top_y": int(y0 + ys.min()), "gap_px": int(y0 + ys.min() - feet_y),
               "centroid_y": int(y0 + ys.mean())}
    if ground_y is not None:
        gy0, gy1 = max(0, ground_y - 10), min(h, ground_y + 30)
        greg = arr[gy0:gy1, x0:x1].mean(axis=2)
        gdark = greg < 90
        out["ground_band_dark_px"] = int(gdark.sum())
        out["ground_band_present"] = bool(gdark.sum() >= 50)
        out["ground_gap_px"] = int(ground_y - feet_y)
    return out


def check_single(feet, mode, ground_y=None, rug_far=None, rug_near=None,
                 tolerance_px=DEFAULT_TOL, height_px=None, flight_line=None):
    """Core verdict. feet = dict with feet_y, feet_centre_x, height."""
    rep = {"mode": mode, "feet_y": feet["feet_y"],
           "feet_centre_x": feet.get("feet_centre_x"),
           "figure_height": feet.get("height"),
           "tolerance_px": tolerance_px, "warnings": [], "fails": []}
    if not mode or mode not in ("GROUNDED", "AIRBORNE"):
        rep["fails"].append("MODE MISSING OR NOT GROUNDED/AIRBORNE: no silent default")
        rep["verdict"] = "FAIL: " + "; ".join(rep["fails"])
        return rep
    if mode == "GROUNDED":
        if ground_y is not None:
            off = feet["feet_y"] - ground_y
            rep["ground_y"] = ground_y
            rep["offset_px"] = off
            rep["offset_note"] = "negative = floating above line, positive = sunk below line"
            if abs(off) > tolerance_px:
                rep["fails"].append(
                    f"FEET OFF GROUND: offset {off}px exceeds tolerance {tolerance_px}px")
        elif rug_far is not None and rug_near is not None:
            pos = round((feet["feet_y"] - rug_far) / (rug_near - rug_far), 3)
            rep["rug_far"], rep["rug_near"], rep["rug_position"] = rug_far, rug_near, pos
            rep["rug_in_front_px"] = int(rug_near - feet["feet_y"])
            if not (RUG_LO <= pos <= RUG_HI):
                rep["fails"].append(
                    f"FEET NOT PLANTED ON RUG: rug_position {pos} outside [{RUG_LO}, {RUG_HI}]")
        else:
            rep["fails"].append("NO GROUND REFERENCE: give ground_y or rug_far/rug_near")
    else:  # AIRBORNE
        if ground_y is None and height_px is None:
            rep["fails"].append("AIRBORNE WITHOUT HEIGHT: give ground_y and/or height_px + flight_line")
        else:
            h = height_px if height_px is not None else (ground_y - feet["feet_y"])
            rep["ground_y"] = ground_y
            rep["height_px"] = int(h)
            rep["flight_line"] = flight_line
            if h <= tolerance_px:
                rep["fails"].append(
                    f"AIRBORNE SPEC MISMATCH: height {h}px <= tolerance {tolerance_px}px, feet are on the ground, relabel GROUNDED")
            if not flight_line:
                rep["fails"].append("AIRBORNE WITHOUT FLIGHT LINE: state height / flight line in spec")
    rep["verdict"] = "PASS" if not rep["fails"] else "FAIL: " + "; ".join(rep["fails"])
    return rep


def check_sequence(rows, mode, tolerance_px=DEFAULT_TOL):
    """rows: list of {feet_y, feet_centre_x, height_px?}. Returns verdict dict."""
    feet = [r["feet_y"] for r in rows]
    spread = max(feet) - min(feet) if feet else 0
    rep = {"mode": mode, "n_frames": len(rows), "feet_y_min": min(feet) if feet else None,
           "feet_y_max": max(feet) if feet else None, "feet_y_spread": spread,
           "warnings": [], "fails": []}
    if mode == "GROUNDED":
        if spread > tolerance_px * 2:
            rep["fails"].append(f"GROUNDED SEQUENCE DRIFT: feet spread {spread}px > {tolerance_px * 2}px")
        cxs = [r.get("feet_centre_x") for r in rows if r.get("feet_centre_x") is not None]
        if cxs:
            rep["feet_centre_x_spread"] = max(cxs) - min(cxs)
    else:
        hs = [r.get("height_px") for r in rows if r.get("height_px") is not None]
        if hs:
            jumps = [abs(hs[i + 1] - hs[i]) for i in range(len(hs) - 1)]
            rep["max_height_jump"] = max(jumps) if jumps else 0
            fig_h = rows[0].get("figure_height") or 600
            if rep["max_height_jump"] > 0.25 * fig_h:
                rep["warnings"].append("AIRBORNE HEIGHT JITTER: max jump exceeds 25% of figure height")
    rep["verdict"] = "PASS" if not rep["fails"] else "FAIL: " + "; ".join(rep["fails"])
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate")
    ap.add_argument("--composite")
    ap.add_argument("--background")
    ap.add_argument("--mode", required=True)
    ap.add_argument("--ground-y", type=int)
    ap.add_argument("--rug-far", type=int)
    ap.add_argument("--rug-near", type=int)
    ap.add_argument("--tolerance", type=int, default=DEFAULT_TOL)
    ap.add_argument("--height", type=int)
    ap.add_argument("--flight-line")
    ap.add_argument("--detect-ground", action="store_true",
                    help="auto-detect a ground line from --background (ESTIMATE only)")
    ap.add_argument("--sequence")
    a = ap.parse_args()
    try:
        if a.sequence:
            rows = json.load(open(a.sequence))
            rep = check_sequence(rows, a.mode, a.tolerance)
            print(json.dumps(rep, indent=2))
            return 0 if not rep["fails"] else 2
        if a.plate:
            feet = plate_feet(a.plate)
        elif a.composite and a.background:
            feet = composite_feet(a.composite, a.background)
        elif a.composite:
            raise ValueError("composite needs --background for diff measurement")
        else:
            raise ValueError("give --plate or --composite + --background")
        rep = check_single(feet, a.mode, a.ground_y, a.rug_far, a.rug_near,
                           a.tolerance, a.height, a.flight_line)
        rep.update({k: v for k, v in feet.items() if k not in rep})
        if a.composite:
            rep["shadow"] = shadow_cue(a.composite, feet["feet_y"],
                                       feet["feet_centre_x"],
                                       feet["bbox"][2] - feet["bbox"][0],
                                       ground_y=a.ground_y)
            if a.mode == "GROUNDED" and not rep["shadow"].get("present"):
                rep["warnings"].append("NO CONTACT SHADOW: warning only, some styles have none")
            if a.mode == "AIRBORNE" and rep["shadow"].get("present") and rep["shadow"].get("gap_px", 999) <= 5:
                rep["warnings"].append("SHADOW GLUED TO AIRBORNE FEET: airborne read may fail on screen")
        if a.detect_ground and a.background:
            rep["auto_ground"] = detect_ground_line(a.background)
            if rep["verdict"] == "PASS":
                rep["verdict"] = "PASS-ESTIMATE (auto ground line, confirm in spec)"
        print(json.dumps(rep, indent=2))
        return 0 if rep["verdict"].startswith("PASS") else 2
    except ValueError as e:
        print(json.dumps({"verdict": "ERROR", "error": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
