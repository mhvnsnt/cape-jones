#!/usr/bin/env python3
"""Exposure-strip split (sheets 1-9) + 09-hero-shot-black M1/M2 variants.
No original touched: all crops are pixel copies into the new folder.
Method per sheet is in MANIFEST: table-divider lines (dark/gradient counts)
for 1-8, FRAME-column lines for 7, gap-midpoints between alpha components
for 9. Sheet 10 is NOT band-split: figures overlap ~250px each, a band cut
would truncate torsos/capes; it is reported as still owed, not faked.
Hero M1/M2 are regenerated from the original plate with the same code as
honest-defects-10-methods (decontaminate sigma=2 edge band only; erode 1px),
numbers re-measured, not copied from that report.
"""
import json, os, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

BASE = os.path.expanduser("~/workspace/cape-jones-rig")
SRC = os.path.join(BASE, "transparent-plates-grok-full-sweep-20261031/plates/exposure-sheets")
HERO = os.path.join(BASE, "transparent-plates-grok-full-sweep-20261031/plates/root/09-hero-shot-black.png")
OUT = os.path.join(BASE, "art-owed-exposure-hero-20261031")
STRIPS = os.path.join(OUT, "exposure-strips")
HV = os.path.join(OUT, "hero-variants")
CT = os.path.join(OUT, "contacts")
for d in (STRIPS, HV, CT):
    os.makedirs(d, exist_ok=True)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# sheet -> (source file, [(y0,y1,label), ...], method note)
SHEETS = {
 "exposure-sheet-1-walk": ("exposure-sheet-1-walk.png",
   [(115,295,"frame-1"),(297,483,"frame-2"),(485,671,"frame-3"),(673,846,"frame-4"),
    (848,1019,"frame-5"),(1021,1194,"frame-6"),(1196,1358,"frame-7"),(1360,1527,"frame-8")],
   "table-divider dark lines at 114,296,484,672,847,1020,1195,1359,1528 (dark count >770/1264)"),
 "exposure-sheet-2-jump": ("exposure-sheet-2-jump.png",
   [(149,312,"frame-1"),(314,480,"frame-2"),(482,616,"frame-3"),(618,759,"frame-4"),
    (761,901,"frame-5"),(903,1053,"frame-6"),(1055,1216,"frame-7"),(1218,1349,"frame-8"),(1351,1527,"frame-9")],
   "gradient dividers at 148,313,481,617,760,902,1054,1217,1350,1528 (action-column gradient >128; dark-count alone misses 313,760,1054,1350)"),
 "exposure-sheet-3-punch": ("exposure-sheet-3-punch.png",
   [(157,311,"frame-1"),(313,465,"frame-2"),(467,620,"frame-3"),(622,772,"frame-4"),
    (774,925,"frame-5"),(927,1077,"frame-6"),(1079,1227,"frame-7"),(1229,1377,"frame-8"),
    (1379,1520,"frame-9"),(1522,1688,"frame-10")],
   "table-divider dark lines at 156,312,466,621,773,926,1078,1228,1378,1521,1689; header band 114-155 excluded"),
 "exposure-sheet-4-flight": ("exposure-sheet-4-flight.png",
   [(158,312,"frame-1"),(314,463,"frame-2"),(465,616,"frame-3"),(618,769,"frame-4"),
    (771,920,"frame-5"),(922,1066,"frame-6"),(1068,1216,"frame-7"),(1218,1370,"frame-8"),
    (1372,1516,"frame-9"),(1518,1661,"frame-10")],
   "table-divider dark lines at 114,157,313,464,617,770,921,1067,1217,1371,1517,1662; header band 115-156 excluded"),
 "exposure-sheet-5-reaction": ("exposure-sheet-5-reaction.png",
   [(153,358,"frame-1"),(360,552,"frame-2"),(554,728,"frame-3"),(730,916,"frame-4"),
    (918,1096,"frame-5"),(1098,1282,"frame-6"),(1284,1472,"frame-7"),(1474,1673,"frame-8")],
   "table-divider dark lines at 98,152,359,553,729,917,1097,1283,1473,1674; header band 99-151 excluded"),
 "exposure-sheet-6-sit": ("exposure-sheet-6-sit.png",
   [(224,276,"frame-1"),(278,329,"frame-2"),(331,382,"frame-3"),(384,434,"frame-4"),
    (436,486,"frame-5"),(488,538,"frame-6"),(540,590,"frame-7"),(592,641,"frame-8"),
    (643,693,"frame-9"),(695,745,"frame-10"),(747,796,"frame-11"),(798,848,"frame-12"),
    (850,900,"frame-13"),(902,952,"frame-14"),(954,1004,"frame-15"),(1006,1057,"frame-16")],
   "table-divider dark lines every ~52px at 171,223,277,330,383,435,487,539,591,642,694,746,797,849,901,953,1005,1057; first band 172-222 is the header, excluded"),
 "exposure-sheet-7-cape": ("exposure-sheet-7-cape.png",
   [(155,322,"frame-1"),(324,484,"frame-4"),(486,663,"frame-8"),(665,828,"frame-12"),
    (830,997,"frame-16"),(999,1152,"frame-20"),(1154,1300,"frame-24"),(1302,1530,"frame-28")],
   "FRAME-column dark lines at 154,323,485,664,829,998,1153,1301,1531 (count 113/115 in x20-135); ACTION column has no lines, FRAME lines are the row boundaries; frame numbers as printed: 1,4,8,12,16,20,24,28"),
 "exposure-sheet-8-turnaround": ("exposure-sheet-8-turnaround.png",
   [(87,116,"frame-1"),(118,149,"frame-2"),(151,184,"frame-3"),(186,216,"frame-4"),
    (218,250,"frame-5"),(252,285,"frame-6"),(287,319,"frame-7"),(321,353,"frame-9"),
    (355,387,"frame-10"),(389,421,"frame-12"),(423,455,"frame-13"),(457,487,"frame-14"),
    (489,518,"frame-15"),(520,549,"frame-16"),(551,580,"frame-17"),(582,610,"frame-18"),
    (612,640,"frame-20"),(642,670,"frame-21"),(672,702,"frame-22"),(704,732,"frame-24"),
    (734,761,"frame-25"),(763,791,"frame-26"),(793,823,"frame-27"),(825,853,"frame-28"),
    (855,883,"frame-29"),(885,912,"frame-30"),(914,971,"frame-39")],
   "FR-column gradient dividers at ~117,150,185,217,251,286,320,354,388,422,456,488,519,550,581,611,641,671,703,733,762,792,824,854,884,913 (spacing ~32-33px); top 86, bottom 972. ROW strips, not figure strips: the turnaround column is drawn across rows in the original, so each strip contains a slice of it - documented, not a standalone figure"),
 "exposure-sheet-9-run": ("exposure-sheet-9-run.png",
   [(155,347,"run-01"),(348,498,"run-02"),(499,653,"run-03"),(654,814,"run-04"),
    (815,970,"run-05"),(971,1111,"run-06"),(1112,1238,"run-07"),(1239,1358,"run-08"),
    (1359,1502,"run-09"),(1503,1727,"run-10")],
   "gap-midpoints between the 10 alpha components (area 10.7k-13.2k px) at y 192-339,356-487,510-641,665-807,821-963,978-1107,1115-1234,1242-1355,1361-1498,1506-1638; midpoints 347,498,653,814,970,1111,1238,1358,1502; no figure pixel crosses a cut (figure bboxes end/start >=8px from every cut); first band top 155 excludes the title block, last band runs to sheet bottom 1727"),
}

manifest = {"sheets": [], "hero": {}, "original_sha256": {}}
total = 0
for key, (srcfile, bands, method) in SHEETS.items():
    src = os.path.join(SRC, srcfile)
    im = Image.open(src).convert("RGBA")
    W, H = im.size
    manifest["original_sha256"][srcfile] = sha(src)
    entries = []
    for i, (y0, y1, lab) in enumerate(bands, 1):
        strip = im.crop((0, y0, W, y1 + 1))
        name = f"{key}-strip-{i:02d}-{lab}.png"
        outp = os.path.join(STRIPS, name)
        strip.save(outp)
        # pixel-equality gate: strip == original crop
        arr_s = np.array(strip); arr_o = np.array(im.crop((0, y0, W, y1 + 1)))
        assert (arr_s == arr_o).all(), name
        entries.append({"file": name, "label": lab, "y0": y0, "y1": y1, "height": y1 - y0 + 1,
                        "width": W, "size_bytes": os.path.getsize(outp)})
    manifest["sheets"].append({"source": srcfile, "source_size": [W, H], "method": method,
                               "strip_count": len(entries), "strips": entries})
    total += len(entries)
    print(key, len(entries))

# sheet 10: NOT split, recorded explicitly
manifest["sheets"].append({"source": "exposure-sheet-10-flex.png", "source_size": [1152, 1728],
    "method": "NOT SPLIT. Flex figures are ~375px tall, spaced ~155px apart (frame ticks at 190,344,497,650,800,954,1108,1262,1425,1571), so each figure overlaps the next by ~220px; a horizontal band cut at tick midpoints would truncate torsos/capes. A figure-extraction pass (not a band split) is still owed for this sheet.",
    "strip_count": 0, "strips": []})
manifest["original_sha256"]["exposure-sheet-10-flex.png"] = sha(os.path.join(SRC, "exposure-sheet-10-flex.png"))
manifest["total_strips"] = total
manifest["sheets_split"] = 9
manifest["sheets_total"] = 10
print("total strips", total)

# ---- hero M1/M2, regenerated ----
def load_rgba(p):
    return np.array(Image.open(p).convert("RGBA")).astype(np.float64)

def fringe(arr):
    a = arr[:, :, 3]; kept = a > 10
    dist = ndimage.distance_transform_edt(kept)
    edge = kept & (dist <= 3.5)
    rgb = arr[:, :, :3]; mx = rgb.max(axis=2); mn = rgb.min(axis=2)
    sat = (mx - mn) > 60
    blue = (rgb[:, :, 2] - rgb[:, :, 0]) > 40
    red = (rgb[:, :, 0] - rgb[:, :, 2]) > 40
    return int((edge & sat & (blue | red)).sum()), int((kept & sat & (blue | red)).sum()), int(kept.sum())

def decontaminate(arr, sigma=2.0):
    a = arr[:, :, 3:4] / 255.0
    prem = arr[:, :, :3] * a
    blur_prem = np.array(Image.fromarray(np.clip(prem, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sigma))).astype(np.float64)
    blur_a = np.array(Image.fromarray(np.clip(a[:, :, 0] * 255, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sigma))).astype(np.float64) / 255.0
    blur_a = np.maximum(blur_a, 1e-6)
    decon = blur_prem / blur_a[:, :, None]
    kept = arr[:, :, 3] > 10
    dist = ndimage.distance_transform_edt(kept)
    edge = kept & (dist <= 3.5)
    out = arr.copy(); out[edge, :3] = decon[edge, :3]
    return out

def erode(arr):
    mask = arr[:, :, 3] > 10
    er = ndimage.binary_erosion(mask, iterations=1)
    out = arr.copy(); out[~er, 3] = 0
    return out

hero = load_rgba(HERO)
manifest["hero"]["original"] = "09-hero-shot-black.png"
manifest["hero"]["original_sha256"] = sha(HERO)
manifest["hero"]["original_size"] = [921, 2047]
base_f = fringe(hero)
manifest["hero"]["baseline"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], base_f))
print("baseline", manifest["hero"]["baseline"])
m1 = decontaminate(hero)
Image.fromarray(np.clip(m1, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(HV, "hero-09-M1-decontaminate.png"))
manifest["hero"]["M1_decontaminate"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], fringe(m1)))
print("M1", manifest["hero"]["M1_decontaminate"])
m2 = erode(hero)
Image.fromarray(np.clip(m2, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(HV, "hero-09-M2-erode1.png"))
manifest["hero"]["M2_erode1"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], fringe(m2)))
print("M2", manifest["hero"]["M2_erode1"])

# densest fringe window (400x400) for the zoom crop
a = hero[:, :, 3]; kept = a > 10
dist = ndimage.distance_transform_edt(kept)
edge = kept & (dist <= 3.5)
rgb = hero[:, :, :3]; mx = rgb.max(axis=2); mn = rgb.min(axis=2)
sat = (mx - mn) > 60
fr = edge & sat & ((rgb[:, :, 2] - rgb[:, :, 0]) > 40 | ((rgb[:, :, 0] - rgb[:, :, 2]) > 40))
fr = edge & sat & (((rgb[:, :, 2] - rgb[:, :, 0]) > 40) | ((rgb[:, :, 0] - rgb[:, :, 2]) > 40))
best = (0, 0, 0)
H, W = fr.shape
for y in range(0, H - 400, 20):
    for x in range(0, W - 400, 20):
        c = int(fr[y:y+400, x:x+400].sum())
        if c > best[0]:
            best = (c, x, y)
manifest["hero"]["zoom_crop"] = {"fringe_px_in_crop": best[0], "x": best[1], "y": best[2], "w": 400, "h": 400}
print("zoom crop", manifest["hero"]["zoom_crop"])

json.dump(manifest, open(os.path.join(OUT, "MANIFEST-20261031.json"), "w"), indent=1)
print("manifest written")
