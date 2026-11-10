#!/usr/bin/env python3
"""Build APPROVAL PACK contact sheets, 2026-10-31. New files only; never overwrites Mars-seen versions.
Grey-128 background for transparency checks. No red anywhere (sheet titles only, white on dark grey).
Status: 0 = UNAPPROVED / for approval, 1 = ALREADY APPROVED (eyes in-mask reference strip only).
"""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "approval-pack-20261031")
os.makedirs(OUT, exist_ok=True)
GREY = (128, 128, 128)
DARK = (34, 34, 34)
CAPBAR = (52, 52, 52)
WHITE = (255, 255, 255)
LIGHT = (232, 232, 232)

def font(sz, bold=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(p, sz)
    except Exception:
        return ImageFont.load_default()

def shortlabel(path):
    b = os.path.basename(path)
    # strip common date suffix for readability, keep recognisable stem
    return b.replace("-20261031", "")

def load_cell(path, cw, ch):
    """Fit image into cw x ch on grey-128, preserving aspect. Returns RGB image."""
    im = Image.open(path).convert("RGBA")
    im.thumbnail((cw - 16, ch - 16), Image.LANCZOS)
    canvas = Image.new("RGBA", (cw, ch), GREY + (255,))
    canvas.alpha_composite(im, ((cw - im.width) // 2, (ch - im.height) // 2))
    return canvas.convert("RGB")

def sheet(title, subtitle, cells, cols, cell_w, cell_h, outname, extra_sections=None):
    """cells: list of (path, label). extra_sections: list of (kind, ...) rendered below grid.
       kind 'approved_ref': (path, label) small reference strip. kind 'note': (text,) wrapped text block."""
    W = 1600
    pad = 16
    gap = 12
    title_h = 110
    # grid width
    grid_w = W - 2 * pad
    # recompute cell_w to fit cols exactly
    cw = (grid_w - gap * (cols - 1)) // cols
    rows = (len(cells) + cols - 1) // cols if cells else 0
    cap_h = 44
    grid_h = rows * (cell_h + cap_h) + (rows - 1) * gap if rows else 0
    extra_h = 0
    extra_plan = []
    if extra_sections:
        for sec in extra_sections:
            if sec[0] == "approved_ref":
                extra_h += 16 + 44 + 340 + 44
            elif sec[0] == "note":
                lines = textwrap.wrap(sec[1], width=105)
                extra_h += 16 + 44 + len(lines) * 28 + 20
    H = title_h + pad + grid_h + extra_h + pad
    img = Image.new("RGB", (W, H), GREY)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, title_h], fill=DARK)
    d.text((pad, 14), title, font=font(34, True), fill=WHITE)
    d.text((pad, 62), subtitle, font=font(20), fill=LIGHT)
    y = title_h + pad
    missing = []
    for i, (path, label) in enumerate(cells):
        r, c = divmod(i, cols)
        x = pad + c * (cw + gap)
        yy = y + r * (cell_h + cap_h + gap)
        if not os.path.exists(path):
            missing.append(path)
            d.rectangle([x, yy, x + cw, yy + cell_h], fill=(96, 96, 96))
            d.text((x + 12, yy + cell_h // 2), "MISSING: " + shortlabel(path), font=font(18, True), fill=WHITE)
        else:
            img.paste(load_cell(path, cw, cell_h), (x, yy))
        d.rectangle([x, yy + cell_h, x + cw, yy + cell_h + cap_h], fill=CAPBAR)
        # NOTE: do NOT basename() an explicit label — labels may contain '/' (e.g. 'before / after')
        lab = label.replace("-20261031", "") if label else shortlabel(path)
        # shrink font if too long
        f = font(18)
        while d.textlength(lab, font=f) > cw - 16 and f.size > 12:
            f = font(f.size - 1)
        d.text((x + 8, yy + cell_h + 11), lab, font=f, fill=WHITE)
    y2 = y + grid_h
    if extra_sections:
        for sec in extra_sections:
            y2 += 16
            if sec[0] == "approved_ref":
                _, path, label = sec
                d.rectangle([pad, y2, W - pad, y2 + 44], fill=(20, 60, 20))
                d.text((pad + 12, y2 + 10), "ALREADY APPROVED  |  STATUS 1  |  REFERENCE ONLY — NOT FOR APPROVAL", font=font(19, True), fill=WHITE)
                y2 += 44
                rw = W - 2 * pad
                if os.path.exists(path):
                    img.paste(load_cell(path, rw, 340), (pad, y2))
                else:
                    missing.append(path)
                d.rectangle([pad, y2 + 340, W - pad, y2 + 340 + 44], fill=CAPBAR)
                d.text((pad + 12, y2 + 340 + 11), label, font=font(18), fill=WHITE)
                y2 += 340 + 44
            elif sec[0] == "note":
                lines = textwrap.wrap(sec[1], width=105)
                bh = 44 + len(lines) * 28 + 20
                d.rectangle([pad, y2, W - pad, y2 + bh], fill=(240, 240, 240))
                d.rectangle([pad, y2, W - pad, y2 + 44], fill=CAPBAR)
                d.text((pad + 12, y2 + 10), "NOTE", font=font(19, True), fill=WHITE)
                for j, ln in enumerate(lines):
                    d.text((pad + 12, y2 + 52 + j * 28), ln, font=font(19), fill=(20, 20, 20))
                y2 += bh
    out = os.path.join(OUT, outname)
    img.save(out)
    print(f"{outname}  {img.size}  cells={len(cells)} missing={missing}")
    return out, missing

S = "STATUS 0 — UNAPPROVED / FOR MARS APPROVAL"
all_missing = []
def run(*a, **k):
    o, m = sheet(*a, **k)
    all_missing.extend(m)
    return o

B = RIG + "/"
# 1 visemes
run("01 — VISEMES v2", S + "  |  14 heads (rest → gk)",
    [(f"{B}visemes-v2-20261031/head-v2-{i:02d}-{n}-20261031.png", f"{i:02d} {n}") for i, n in enumerate(
        ["rest","ee","eh","ah","oh","oo","mbp","fv","l","sz","th","r","w","gk"], start=1)],
    5, 0, 420, "01-visemes-v2-20261031.png")
# 2 cape styles
run("02 — CAPE STYLES v2", S + "  |  15 styles",
    [(f"{B}cape-styles-v2-20261031/cape-{i:02d}-{n}-20261031.png", f"{i:02d} {n}") for i, n in enumerate(
        ["draped","lying-flat","swinging","billowing","wind-left","wind-right","lifted-up","hanging-heavy","twisted","over-shoulder","wrapped-front","trailing-behind","flying-spread","sitting-pooled","raised-high"], start=1)],
    5, 0, 460, "02-cape-styles-v2-20261031.png")
# 3 device prop v2
run("03 — DEVICE PROP v2", S + "  |  prop sheet + in final shot",
    [(f"{B}device-prop-v2-20261031/device-prop-sheet-v2-20261031.png", "prop sheet v2"),
     (f"{B}device-prop-v2-20261031/device-in-final-shot-v2-20261031.png", "in final shot v2")],
    2, 0, 560, "03-device-prop-v2-20261031.png")
# 4 forearm fist v5 + correction
run("04 — FOREARM / FIST v5 + v5 CORRECTION", S + "  |  v5 punch + correction: flipped forward punch + uppercut",
    [(f"{B}forearm-fist-v5-20261031/forearm-v5-arm1-front-punch-fist-20261031.png", "v5 arm1 front punch"),
     (f"{B}forearm-fist-v5-20261031/forearm-v5-arm2-front-punch-fist-20261031.png", "v5 arm2 front punch"),
     (f"{B}forearm-fist-v5-20261031/fist-left-v5-20261031.png", "v5 fist left"),
     (f"{B}forearm-fist-v5-20261031/fist-right-v5-20261031.png", "v5 fist right"),
     (f"{B}forearm-fist-v5-correction-20261031/forearm-v5-arm1-forward-punch-flipped-20261031.png", "CORR arm1 fwd punch flipped"),
     (f"{B}forearm-fist-v5-correction-20261031/forearm-v5-arm2-forward-punch-flipped-20261031.png", "CORR arm2 fwd punch flipped"),
     (f"{B}forearm-fist-v5-correction-20261031/forearm-v5-arm1-uppercut-20261031.png", "CORR arm1 uppercut"),
     (f"{B}forearm-fist-v5-correction-20261031/forearm-v5-arm2-uppercut-20261031.png", "CORR arm2 uppercut"),
     (f"{B}forearm-fist-v5-correction-20261031/proof-v5-correction-forward-vs-uppercut-20261031.png", "proof: forward vs uppercut")],
    3, 0, 380, "04-forearm-fist-v5-correction-20261031.png")
# 5 eyes v4 — strips only + small approved ref
run("05 — EYES NORMAL SUPERHERO v4 — STRIPS ONLY", S + "  |  strips only in main grid; in-mask fit is NOT re-approved here",
    [(f"{B}eyes-normal-superhero-v4-20261031/strips-alone-v4-20261031.png", "strips alone v4 (all)"),
     (f"{B}eyes-normal-superhero-v4-20261031/eye-normal-v4-01-neutral-20261031.png", "01 neutral"),
     (f"{B}eyes-normal-superhero-v4-20261031/eye-normal-v4-02-determined-focused-20261031.png", "02 determined / focused"),
     (f"{B}eyes-normal-superhero-v4-20261031/eye-normal-v4-03-angry-scowling-20261031.png", "03 angry / scowling"),
     (f"{B}eyes-normal-superhero-v4-20261031/eye-normal-v4-04-surprised-alarmed-20261031.png", "04 surprised / alarmed"),
     (f"{B}eyes-normal-superhero-v4-20261031/eye-normal-v4-05-concentrating-20261031.png", "05 concentrating")],
    2, 0, 380, "05-eyes-normal-superhero-v4-strips-20261031.png",
    extra_sections=[("approved_ref", f"{B}eyes-normal-superhero-v4-20261031/proof-eyes-in-own-mask-v4-20261031.png",
                     "proof-eyes-in-own-mask v4 — SMALL REFERENCE ONLY (already approved in-mask fit)")])
# 6 wrap v2
run("06 — BLENDER COMPOSITE WRAP v2", S,
    [(f"{B}blender-composite-wrap-v2-20261031/wrap-v2-apose-20261031.png", "wrap v2 apose"),
     (f"{B}blender-composite-wrap-v2-20261031/wrap-v2-armsup-20261031.png", "wrap v2 arms-up"),
     (f"{B}blender-composite-wrap-v2-20261031/control-no-wrap-apose-20261031.png", "control no-wrap apose"),
     (f"{B}blender-composite-wrap-v2-20261031/control-no-wrap-armsup-20261031.png", "control no-wrap arms-up"),
     (f"{B}blender-composite-wrap-v2-20261031/proof-v1-vs-v2-wrap-20261031.png", "proof v1 vs v2 wrap")],
    3, 0, 300, "06-blender-composite-wrap-v2-20261031.png")
# 7 wrap v3
run("07 — BLENDER COMPOSITE WRAP v3", S,
    [(f"{B}blender-composite-wrap-v3-20261031/wrap-v3-apose-20261031.png", "wrap v3 apose"),
     (f"{B}blender-composite-wrap-v3-20261031/wrap-v3-armsup-20261031.png", "wrap v3 arms-up"),
     (f"{B}blender-composite-wrap-v3-20261031/wrap-v3-fighting-20261031.png", "wrap v3 fighting"),
     (f"{B}blender-composite-wrap-v3-20261031/proof-v2-vs-v3-wrap-20261031.png", "proof v2 vs v3"),
     (f"{B}blender-composite-wrap-v3-20261031/proof-rim-variants-20261031.png", "proof rim variants"),
     (f"{B}blender-composite-wrap-v3-20261031/proof-interior-detail-20261031.png", "proof interior detail")],
    3, 0, 300, "07-blender-composite-wrap-v3-20261031.png")
# 8 wrap v4 — relit plates only
run("08 — BLENDER COMPOSITE WRAP v4", S + "  |  RELIT PLATES ONLY — no final v4 composite render found in folder",
    [(f"{B}blender-composite-wrap-v4-20261031/scratch/plate-apose-relit-v4.png", "plate apose relit v4"),
     (f"{B}blender-composite-wrap-v4-20261031/scratch/plate-armsup-relit-v4.png", "plate arms-up relit v4"),
     (f"{B}blender-composite-wrap-v4-20261031/scratch/plate-fighting-relit-v4.png", "plate fighting relit v4")],
    3, 0, 620, "08-blender-composite-wrap-v4-20261031.png",
    extra_sections=[("note", "No final wrap-v4 composite render was found in blender-composite-wrap-v4-20261031 (only relight_normal_v4.py + scratch plates/normals/depth). This sheet shows the three relit plates only; nothing has been substituted.")])
# 9 godray L3
run("09 — GODRAY LEVEL 3", S,
    [(f"{B}godray-level3-20261031/v5-level3-20261031.png", "v5 level 3"),
     (f"{B}godray-level3-20261031/v4-level3-20261031.png", "v4 level 3"),
     (f"{B}godray-level3-20261031/proof-before-after-l3-20261031.png", "proof before / after L3"),
     (f"{B}godray-level3-20261031/godray-bg-v2-20261031.png", "godray bg v2")],
    2, 0, 620, "09-godray-level3-20261031.png")
# 10 godray L4
run("10 — GODRAY LEVEL 4", S,
    [(f"{B}godray-level4-20261031/l4-candidate-20261031.png", "L4 candidate"),
     (f"{B}godray-level4-20261031/gold-preserved-v5-20261031.png", "gold preserved v5"),
     (f"{B}godray-level4-20261031/gold-preserved-v4-20261031.png", "gold preserved v4"),
     (f"{B}godray-level4-20261031/proof-l3-vs-l4-vs-gold-preserved-20261031.png", "proof L3 vs L4 vs gold")],
    2, 0, 620, "10-godray-level4-20261031.png")
# 11 afterglow
run("11 — AFTERGLOW", S + "  |  stills only; motion file is a GIF (see manifest)",
    [(f"{B}afterglow-20261031/afterglow-at-rest-final-frame-20261031.png", "at-rest final frame"),
     (f"{B}afterglow-20261031/afterglow-proof-contact-20261031.png", "proof contact (existing)")],
    2, 0, 420, "11-afterglow-20261031.png")
# 12 dance kneefeet correction
kf = [f"{B}dance-kneefeet-fix-correction-20261031/frames/dance-kneefeet-corrected-f{f:03d}.png" for f in (1, 17, 28, 43, 60, 77, 93)]
run("12 — DANCE KNEE / FEET FIX — CORRECTION", S + "  |  sampled corrected frames + before/after + foot crops",
    [(p, f"corrected f{f:03d}") for p, f in zip(kf, (1, 17, 28, 43, 60, 77, 93))] +
    [(f"{B}dance-kneefeet-fix-correction-20261031/dance-kneefeet-corrected-before-after-20261031.png", "before / after"),
     (f"{B}dance-kneefeet-fix-correction-20261031/dance-kneefeet-corrected-foot-crops-f028-20261031.png", "foot crops f028")],
    3, 0, 380, "12-dance-kneefeet-fix-correction-20261031.png")
# 13 dance improved
di = [f"{B}dance-improved-20261031/frames/dance-improved-f{f:03d}.png" for f in (1, 11, 21, 28, 36, 43, 50, 60)]
run("13 — DANCE IMPROVED", S + "  |  sampled frames (full sequence is GIF/MP4 — see manifest)",
    [(p, f"f{f:03d}") for p, f in zip(di, (1, 11, 21, 28, 36, 43, 50, 60))],
    4, 0, 380, "13-dance-improved-20261031.png")
# 14 mochiichao combine
run("14 — MOCHII / CHAO COMBINE BUILD", S + "  |  sampled dance frames + room/device stills (GIFs in manifest)",
    [(f"{B}mochiichao-combine-build-20261031/frames/dance-f{f:03d}.png", f"dance f{f:03d}") for f in (0, 12, 24, 36)] +
    [(f"{B}mochiichao-combine-build-20261031/device-in-final-shot-room-20261031.png", "device in final shot (room)"),
     (f"{B}mochiichao-combine-build-20261031/device-prop-sheet-20261031.png", "device prop sheet (combine)")],
    3, 0, 380, "14-mochiichao-combine-build-20261031.png")
# 15 show templates — TEXT ONLY (no images exist)
templates = []
import glob
for md in sorted(glob.glob(f"{B}show-templates-world-interactions-20261031/*.md")):
    with open(md, encoding="utf-8", errors="replace") as fh:
        first = next((ln.strip() for ln in fh if ln.strip()), os.path.basename(md))
    templates.append(f"{os.path.basename(md)} — {first}")
note15 = ("NO IMAGES EXIST for this group: show-templates-world-interactions-20261031 contains only 7 Markdown template specs, "
          "no renders, frames or stills. Nothing has been substituted. Templates: " + " | ".join(templates))
run("15 — SHOW TEMPLATES / WORLD INTERACTIONS", S + "  |  TEXT SPECS ONLY — NO IMAGES EXIST",
    [], 1, 0, 100, "15-show-templates-world-interactions-20261031.png",
    extra_sections=[("note", note15)])
# 16 clean-100 layouts + shots
run("16 — CLEAN-100: LAYOUTS + SHOTS", S + "  |  4 layout passes shown; SHOTS are SPECS ONLY — 0/30 rendered",
    [(f"{B}clean-100-20261031/layouts/layout-pass-{n}-painted-20261031.jpg", f"layout {n}") for n in ("alley", "desk", "flying", "rooftop")],
    2, 0, 560, "16-clean-100-layouts-shots-20261031.png",
    extra_sections=[("note", "SHOTS: 30 shot specs, 0/30 rendered. Spec docs: clean-100-20261031/shots/shot-specs-30-20261031.md + .json, god-ray-placement-30-20261031.md + .json, DELIVERY-SPECS-20261031.md. Per the spec header itself: 'SPECIFICATIONS ONLY. No shot approval is claimed for any of the 30 shots.' No renders have been substituted; layout passes above are the only images in this sheet.")])
# 17 joint cleanup
run("17 — JOINT CLEANUP", S,
    [(f"{B}joint-cleanup-20261031/joint-cleanup-before-after-20261031.png", "before / after"),
     (f"{B}joint-cleanup-20261031/true-final-flex-wrist-polish-20261031.png", "true-final flex wrist polish"),
     (f"{B}joint-cleanup-20261031/deep-squat-flex-wrist-polish-20261031.png", "deep-squat flex wrist polish"),
     (f"{B}joint-cleanup-20261031/over-exaggerated-flex-wrist-polish-20261031.png", "over-exaggerated flex wrist polish"),
     (f"{B}joint-cleanup-20261031/cap-omit-test-true-final-20261031.png", "cap-omit test true-final"),
     (f"{B}joint-cleanup-20261031/crop-capomit-elbowL-before-after-20261031.png", "cap-omit elbow L crop"),
     (f"{B}joint-cleanup-20261031/crop-capomit-elbowR-before-after-20261031.png", "cap-omit elbow R crop")],
    3, 0, 420, "17-joint-cleanup-20261031.png")
# 18 forearm arm2 aligned
run("18 — FOREARM ARM2 ALIGNED", S,
    [(f"{B}forearm-arm2-aligned-20261031/forearm-v3-arm2-back-aligned-20261031.png", "arm2 back aligned (piece)"),
     (f"{B}forearm-arm2-aligned-20261031/proof-arm2-alignment-before-after-20261031.png", "proof before / after")],
    2, 0, 420, "18-forearm-arm2-aligned-20261031.png")
# 19 hip-lower flex
run("19 — HIP / LOWER FLEX", S + "  |  build_hip_lower.py output folder: reposes-v7c-clean (*hip*)",
    [(f"{B}reposes-v7c-clean/deep-squat-hip-lower-before-after-20261031.png", "deep-squat hip-lower before/after"),
     (f"{B}reposes-v7c-clean/over-exaggerated-hip-lower-before-after-20261031.png", "over-exaggerated hip-lower before/after"),
     (f"{B}reposes-v7c-clean/deep-squat-hip-lower-leg-crops-20261031.png", "deep-squat hip-lower leg crops"),
     (f"{B}reposes-v7c-clean/over-exaggerated-hip-lower-leg-crops-20261031.png", "over-exaggerated hip-lower leg crops"),
     (f"{B}reposes-v7c-clean/full-final-flex-exaggerated-deep-squat-hip-lower-20261031.png", "full final flex exaggerated deep-squat hip-lower"),
     (f"{B}reposes-v7c-clean/full-final-flex-over-exaggerated-hip-lower-20261031.png", "full final flex over-exaggerated hip-lower")],
    3, 0, 520, "19-hip-lower-flex-20261031.png")

print("ALL MISSING:", all_missing if all_missing else "none")
