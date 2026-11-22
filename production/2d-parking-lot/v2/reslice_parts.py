#!/usr/bin/env python3
"""reslice_parts.py — RE-SLICE rig parts with SHEET-LEVEL flood-fill alpha.

Root cause (2026-11-22 ~12:20 EST): make_part.py flooded each tight-cropped
part box. The white suit touches the box edges where the figure is cut, so the
flood leaked INTO the suit: torso chest pixel = RGBA [254,254,252,0] (suit
fully transparent), while opaque pixels in the box are the black cape/outlines
behind it. Result on render: dark navy/purple suit (background showing
through) + the opaque black box-backgrounds unioning into a flat black slab.

Fix: compute alpha on the FULL sheet (the figure never touches the sheet
border and its white suit is enclosed by black outlines there), then crop the
same boxes. Geometry (boxes, sizes, placement) is UNCHANGED — only alpha.
Parts are uploaded to branch v2-rig-parts (same paths, overwriting the broken
alpha); local copies are written to rig/parts/ when the disk wall allows.

Usage: python3 reslice_parts.py [--dry] [name ...]
  --dry: compute + print stats only, no upload.
  names: subset to re-slice (default: all flood-method sheet-01/08 parts).
Derived parts (forearm_*_out, shin_*_in, pupils) are regenerated from the
fixed bases by the same transforms make_part.py used.
"""
import cv2, numpy as np, sys, os, json, base64, subprocess

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
RIG = os.path.join(WD, "rig")
sys.path.insert(0, RIG)
import proof_composite as pc  # for LAYOUT/BOXES tables + gh_put

S01 = os.path.join(WD, "refs/01-tpose-turnaround.jpg")
S08 = os.path.join(WD, "refs/08-body-parts-limbs-capes.jpg")
BRANCH = "v2-rig-parts"
REPO = "mhvnsnt/cape-jones"

# name -> (sheet, box, key_bgr, tol): same boxes/keys as make_part.py PARTS,
# flood method only. Sheet-01 key WHITE (255,255,255) tol 18; sheet-08 GREY
# (193,193,193) tol 30.
SHEET_PARTS = {}
for n, b in [
    ("head", (935, 25, 1115, 265)), ("torso", (855, 225, 1195, 505)),
    ("pelvis", (875, 465, 1175, 625)),
    ("upper_arm_R", (650, 175, 920, 335)), ("forearm_R", (515, 180, 730, 325)),
    ("hand_glove_open_R", (415, 185, 585, 315)),
    ("upper_arm_L", (1130, 175, 1400, 335)), ("forearm_L", (1320, 180, 1535, 325)),
    ("hand_glove_open_L", (1470, 185, 1635, 315)),
    ("thigh_R", (875, 470, 1035, 810)), ("shin_foot_R", (875, 755, 1045, 1143)),
    ("thigh_L", (1015, 470, 1180, 810)), ("shin_foot_L", (1015, 755, 1185, 1143)),
]:
    SHEET_PARTS[n] = (S01, b, (255, 255, 255), 18)
for n, b in [
    ("cape_hang", (55, 630, 320, 1045)), ("cape_sweep", (595, 635, 1055, 990)),
    ("cape_billow", (320, 625, 660, 1045)), ("cape_diag", (985, 630, 1320, 1055)),
    ("fist_glove_h", (1060, 1135, 1225, 1220)), ("fist_glove_v", (1240, 1108, 1335, 1240)),
    ("hand_glove_point", (1465, 1118, 1595, 1225)),
    ("hand_glove_open_08", (1355, 1100, 1455, 1240)),
    ("belt_front", (465, 1875, 780, 1985)),
]:
    SHEET_PARTS[n] = (S08, b, (193, 193, 193), 30)


def clean_alpha(alpha):
    _, bw = cv2.threshold(alpha, 127, 255, cv2.THRESH_BINARY)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(bw, 8)
    if n > 1:
        keep = np.zeros_like(bw)
        for i in range(1, n):
            if stats[i, cv2.CC_STAT_AREA] >= 200:
                keep[lab == i] = 255
        bw = keep
    a = cv2.GaussianBlur(bw.astype(np.float32), (0, 0), 0.7)
    return np.clip(a, 0, 255).astype(np.uint8)


def sheet_alpha(src, keyc, tol):
    """Alpha for the WHOLE sheet: 0 where background (connected to the border
    through key-coloured pixels), 255 elsewhere."""
    im = cv2.imread(src)
    bgmask = (np.abs(im.astype(np.int16) - np.array(keyc, dtype=np.int16)).max(axis=2) <= tol)
    h, w = bgmask.shape
    padded = np.ones((h + 2, w + 2), np.uint8) * 255
    padded[1:-1, 1:-1] = bgmask.astype(np.uint8) * 255
    ff = np.zeros((h + 4, w + 4), np.uint8)
    tmp = padded.copy()
    cv2.floodFill(tmp, ff, (0, 0), 128)
    exterior = (tmp[1:-1, 1:-1] == 128)
    alpha = np.where(exterior, 0, 255).astype(np.uint8)
    return im, clean_alpha(alpha)


def slice_from_sheet(name):
    src, box, keyc, tol = SHEET_PARTS[name]
    if not hasattr(slice_from_sheet, "_cache"):
        slice_from_sheet._cache = {}
    if src not in slice_from_sheet._cache:
        im, alpha = sheet_alpha(src, keyc, tol)
        slice_from_sheet._cache[src] = (im, alpha)
        print(f"sheet {os.path.basename(src)}: {im.shape[1]}x{im.shape[0]} "
              f"fg%={100*(alpha > 127).mean():.1f}", flush=True)
    im, alpha = slice_from_sheet._cache[src]
    x0, y0, x1, y1 = box
    crop = im[y0:y1, x0:x1]
    rgba = cv2.cvtColor(crop, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = alpha[y0:y1, x0:x1]
    return rgba


def encode_png(rgba):
    ok, buf = cv2.imencode(".png", rgba)
    assert ok
    return buf.tobytes()


def derive(name, bases):
    """Regenerate a derived part from (already fixed) base images."""
    if name in ("forearm_R_out", "forearm_L_out"):
        src_name = "forearm_R" if name == "forearm_R_out" else "forearm_L"
        img = bases[src_name].copy()
        h = img.shape[0]
        y0, y1 = int(0.55 * h), int(0.90 * h)
        for y in range(y0, y1):
            row = img[y]
            xs = np.where(row[:, 3] > 127)[0]
            if len(xs) < 4:
                continue
            a, b = xs.min(), xs.max()
            img[y, a:b + 1] = row[a:b + 1][::-1]
        return img
    if name in ("shin_foot_R_in", "shin_foot_L_in"):
        src_name = "shin_foot_R" if name == "shin_foot_R_in" else "shin_foot_L"
        return cv2.flip(bases[src_name], 1)
    if name in ("eyes_pupil_center", "eyes_pupil_audience"):
        base = bases["eyes_white_default"].copy()
        alpha = base[:, :, 3]
        _, bw = cv2.threshold(alpha, 127, 255, cv2.THRESH_BINARY)
        n, lab, stats, cent = cv2.connectedComponentsWithStats(bw, 8)
        centres = []
        for i in range(1, n):
            if stats[i, cv2.CC_STAT_AREA] > 200:
                centres.append((cent[i][0], cent[i][1], stats[i, cv2.CC_STAT_HEIGHT]))
        centres.sort()
        img = base.copy()
        dy = 0.05 if name == "eyes_pupil_audience" else 0.0
        for (cx, cy, hh) in centres:
            r = max(4, int(0.30 * hh))
            cv2.circle(img, (int(cx), int(cy + dy * hh)), r, (0, 0, 0, 255), -1, cv2.LINE_AA)
        return img
    raise ValueError(name)


def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    names = [a for a in args if not a.startswith("--")]
    if not names:
        names = list(SHEET_PARTS.keys())
    derived = [n for n in names if n not in SHEET_PARTS]
    base_names = [n for n in names if n in SHEET_PARTS]
    results = {}
    for name in base_names:
        rgba = slice_from_sheet(name)
        a = rgba[:, :, 3]
        print(f"{name}: {rgba.shape[1]}x{rgba.shape[0]} "
              f"opaque%={100*(a > 250).mean():.0f} transparent%={100*(a <= 10).mean():.0f} "
              f"centreRGBA={rgba[rgba.shape[0]//2, rgba.shape[1]//2].tolist()}", flush=True)
        results[name] = rgba
    # derived parts need their bases (fetch from branch if not re-sliced here)
    for name in derived:
        bases = {}
        for bn in ("forearm_R", "forearm_L", "shin_foot_R", "shin_foot_L",
                   "eyes_white_default"):
            if bn in results:
                bases[bn] = results[bn]
            else:
                bases[bn] = pc.part(bn)  # branch copy (BGRA after the channel fix)
        results[name] = derive(name, bases)
        print(f"{name}: derived {results[name].shape[1]}x{results[name].shape[0]}", flush=True)
    if dry:
        print("DRY RUN — nothing uploaded", flush=True)
        return
    for name, rgba in results.items():
        data = encode_png(rgba)
        # sanity: size must match the old part's dimensions
        old = pc.part(name)
        assert old.shape[0] == rgba.shape[0] and old.shape[1] == rgba.shape[1], \
            f"{name}: size changed {old.shape} -> {rgba.shape}"
        ok = pc.gh_put(f"production/2d-parking-lot/v2/rig-parts/{name}.png", data,
                       f"V2 rig parts: re-slice {name} (sheet-level flood alpha fix)")
        print(f"{name}: upload={'OK' if ok else 'FAIL'} ({len(data)} B)", flush=True)
        # local copy when the wall allows (branch is canonical; local is convenience)
        try:
            with open(os.path.join(RIG, "parts", name + ".png"), "wb") as f:
                f.write(data)
        except Exception as e:
            print(f"{name}: local write failed ({e}) — branch copy is canonical", flush=True)
    print("RESLICE DONE", flush=True)


if __name__ == "__main__":
    main()
