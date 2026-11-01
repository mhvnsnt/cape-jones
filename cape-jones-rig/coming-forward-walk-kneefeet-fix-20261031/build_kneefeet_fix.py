"""Knee-feet fix for the coming-forward walk (elbow-fixed walk, 44f).

Audit first, then fix, then gate. The elbow-fixed walk is NOT edited:
it is read as the reference, and this builder re-renders the same
keys, scales, timing and snap table, changing ONLY the leg lower
piece per leg per frame (original vs FootIn), decided by the
universal per-leg gate. Arm angles, snap passes, canvas, ground and
feet_y are therefore identical by construction, and frames with no
leg inward must come out pixel-identical to the elbow-fixed walk.

Keys / timing / scales: exactly the elbow-fix builder.
  CONTACT-L (corrected arms) 0.70, PASSING 0.95, CONTACT-R 1.20,
  PASSING 1.40, CONTACT-L 1.60, then 4-frame hold at 1.60.
  SEG = 10 inbetweens per segment, smoothstep interpolation.
Leg keys (unchanged): CONTACT-L leg_upper L -28 / R +22,
PASSING 0 / +5, CONTACT-R +22 / -28. Leg lower keys are unchanged
in both old and new renders; only the lower PIECE switches.

Gate (per leg, per frame, exact sign, no deadband, no block range):
  L footin = leg_upper_L > 0 ; R footin = leg_upper_R < 0.
  Straight (0) -> original. A 0.6-degree crossing at f11 therefore
  flips the L toe, and that pop is stated plainly in the report
  instead of being hidden by a deadband: the universal rule is
  exact, so a future builder cannot silently reintroduce a
  near-zero mismatch.
"""
import os, sys, math, json, importlib.util
from PIL import Image, ImageDraw
import numpy as np

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "coming-forward-walk-kneefeet-fix-20261031")
ELBOW = os.path.join(RIG, "coming-forward-walk-elbow-fix-20261031")
LAYER = os.path.join(RIG, "coming-forward-walk-layer-fix-20261031")
W, H = 1600, 1800
GROUND_Y = 1500
GREY = (128, 128, 128)
HERO_H = 700

sys.path.insert(0, OUT)
from kneefeet_gate import leg_direction, required_footin, gate_table, knee_x

spec = importlib.util.spec_from_file_location("kf_fig", os.path.join(OUT, "kneefeet_figure.py"))
kf = importlib.util.module_from_spec(spec); spec.loader.exec_module(kf)

CONTACT_L = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": 30, "R": -30},
             "leg_upper": {"L": -28, "R": 22}, "leg_lower": {"L": 5, "R": 15}}
PASSING = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": -10, "R": 10},
           "leg_upper": {"L": 0, "R": 5}, "leg_lower": {"L": 15, "R": 5}}
CONTACT_R = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": 30, "R": -30},
             "leg_upper": {"L": 22, "R": -28}, "leg_lower": {"L": 15, "R": 5}}


def smooth(t):
    return t * t * (3 - 2 * t)


def interp_cfg(a, b, t):
    return {k: {s: a[k][s] + (b[k][s] - a[k][s]) * smooth(t) for s in ("L", "R")} for k in a}


def alpha_bbox(im):
    a = np.array(im.split()[3])
    rows = np.where(a.max(axis=1) > 10)[0]; cols = np.where(a.max(axis=0) > 10)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())


def anchor_layer(fig, scale, ref=None):
    """Anchor a plate on the 1600x1800 canvas, feet on y=1500.
    ref=None: derive placement from this plate's own bbox (old behaviour).
    ref=(plate_scale, cx, top): reuse the reference frame's placement
    exactly, so a FootIn substitution cannot shift the rest of the
    figure by a pixel through bbox re-anchoring. Only the lower-piece
    pixels themselves may differ."""
    bx0, by0, bx1, by1 = alpha_bbox(fig); fig_h = by1 - by0 + 1
    if ref is None:
        plate_scale = (HERO_H * scale) / fig_h
        nw = max(1, int(fig.size[0] * plate_scale)); nh = max(1, int(fig.size[1] * plate_scale))
        scaled = fig.resize((nw, nh), Image.LANCZOS)
        sx0, sy0, sx1, sy1 = alpha_bbox(scaled)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cx = W // 2 - (sx0 + sx1) // 2; top = GROUND_Y - sy1
        layer.alpha_composite(scaled, (cx, top))
    else:
        # Hybrid (final): scale + horizontal placement from the reference
        # frame, vertical placement re-anchored so the feet stay planted
        # on y=1500. The FootIn foot's lowest row differs from the
        # original foot by up to 16 plate px on L-only frames, so a
        # fixed top would float that foot ~15 screen px; re-anchoring
        # keeps feet_y=1500 and the ground gate passing, at the cost
        # of the figure top shifting by that foot delta in those frames
        # (the walk's own ground rule taking precedence, stated plainly).
        plate_scale, cx, _top = ref
        nw = max(1, int(fig.size[0] * plate_scale)); nh = max(1, int(fig.size[1] * plate_scale))
        scaled = fig.resize((nw, nh), Image.LANCZOS)
        _sx0, _sy0, _sx1, _sy1 = alpha_bbox(scaled)
        top = GROUND_Y - _sy1
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(scaled, (cx, top))
    lx0, ly0, lx1, ly1 = alpha_bbox(layer)
    return layer, {"feet_y": ly1, "bbox": [lx0, ly0, lx1, ly1],
                   "touches_edge": (lx0 <= 0 or ly0 <= 0 or lx1 >= W - 1 or ly1 >= H - 1),
                   "margin": min(lx0, ly0, W - 1 - lx1, H - 1 - ly1),
                   "plate_scale": plate_scale, "cx": cx, "top": top}


def background(scale):
    bg = Image.new("RGB", (W, H), GREY); d = ImageDraw.Draw(bg)
    d.rectangle([0, GROUND_Y, W, H], fill=(96, 96, 96))
    d.line([(0, GROUND_Y), (W, GROUND_Y)], fill=(255, 255, 255), width=3)
    drift = int((scale - 1.0) * 0.3 * 400)
    for i, bx in enumerate([150, 450, 1050, 1350]):
        bw = 120 + 40 * (i % 2); x = bx - drift if bx < W // 2 else bx + drift
        d.rectangle([x, GROUND_Y - 180, x + bw, GROUND_Y], fill=(150, 150, 150))
    return bg


def compose(layer, scale):
    return Image.alpha_composite(background(scale).convert("RGBA"), layer).convert("RGB")


def main():
    os.makedirs(os.path.join(OUT, "frames-fixed"), exist_ok=True)
    # 1. Audit: rebuild the 44-frame leg_upper table, old toe = original always.
    table = json.load(open(os.path.join(LAYER, "walk_snap_table.json")))
    snap_by_frame = {}
    for r in table:
        snap_by_frame.setdefault(r["frame"], {})[r["side"]] = r["applied_fixed"]
    walk_keys = [(CONTACT_L, 0.70, "CONTACT-L"), (PASSING, 0.95, "PASSING"),
                 (CONTACT_R, 1.20, "CONTACT-R"), (PASSING, 1.40, "PASSING"),
                 (CONTACT_L, 1.60, "CONTACT-L")]
    cfgs, scales, phases = [], [], []
    for ki in range(len(walk_keys) - 1):
        cfg_a, s_a, lab_a = walk_keys[ki]; cfg_b, s_b, _ = walk_keys[ki + 1]
        for i in range(10):
            t = i / 10; cfgs.append(interp_cfg(cfg_a, cfg_b, t))
            scales.append(s_a + (s_b - s_a) * smooth(t))
            phases.append(lab_a if i == 0 else "INBETWEEN")
    for _ in range(4):
        cfgs.append(CONTACT_L); scales.append(1.60); phases.append("CONTACT-L-HOLD")
    assert len(cfgs) == 44, len(cfgs)

    rows_old, rows_new = [], []
    for fi, cfg in enumerate(cfgs):
        lu, ru = cfg["leg_upper"]["L"], cfg["leg_upper"]["R"]
        kxl, kxr = knee_x("L", lu), knee_x("R", ru)
        crossed = kxl > kxr
        fl, fr = required_footin("L", lu, crossed=crossed), required_footin("R", ru, crossed=crossed)
        base = {"frame": fi, "leg_upper_L": round(lu, 2), "leg_upper_R": round(ru, 2),
                "knee_L": leg_direction("L", lu), "knee_R": leg_direction("R", ru),
                "knee_x_L": round(kxl, 1), "knee_x_R": round(kxr, 1), "crossed": crossed,
                "phase": phases[fi], "scale": round(scales[fi], 4)}
        rows_old.append({**base, "footin_L": False, "footin_R": False})
        rows_new.append({**base, "footin_L": fl, "footin_R": fr})
    ok_old, fail_old, cnt_old = gate_table(rows_old)
    ok_new, fail_new, cnt_new = gate_table(rows_new)
    print("OLD GATE:", ok_old, cnt_old)
    print("NEW GATE:", ok_new, cnt_new)
    assert not ok_old and ok_new, "gate proof must be OLD=FAIL, NEW=PASS"
    # 2. Gate is pre-build: if the new table failed, refuse to render.
    if not ok_new:
        print("GATE FAILS ON NEW TABLE — refusing build"); return 1

    # 3. Render with per-leg footin.
    frames, meas = [], []
    for fi, cfg in enumerate(cfgs):
        snapd = {s: v for s, v in snap_by_frame.get(fi, {}).items() if v != "none"}
        footin = {"L": rows_new[fi]["footin_L"], "R": rows_new[fi]["footin_R"]}
        old_fig = kf.figure(550, cfg, snap=snapd, footin={"L": False, "R": False})
        _old_layer, _old_m = anchor_layer(old_fig, scales[fi])
        ref = (_old_m["plate_scale"], _old_m["cx"], _old_m["top"])
        fig = kf.figure(550, cfg, snap=snapd, footin=footin)
        layer, m = anchor_layer(fig, scales[fi], ref=ref)
        frames.append(compose(layer, scales[fi]))
        m.update({"frame": fi, "scale": round(scales[fi], 4), "phase": phases[fi],
                  "snap": snapd, "arm_upper": cfg["arm_upper"], "arm_lower": cfg["arm_lower"],
                  "leg_upper": cfg["leg_upper"], "footin": footin})
        meas.append(m)
    gif = os.path.join(OUT, "coming-forward-walk-KNEEFEET-FIXED-20261031.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=int(1000 / 24), loop=0)
    feet = [m["feet_y"] for m in meas]
    # 4. Elbow preservation + changed-frame proof vs elbow-fixed walk.
    # Compare SAVED JPGs (both decoded), not in-memory RGB vs JPG, so
    # JPEG noise cannot masquerade as a change.
    changed, identical = [], []
    for fi in range(44):
        old = Image.open(os.path.join(ELBOW, "frames-fixed", f"f{fi:03d}.jpg")).convert("RGB")
        new = frames[fi]
        new.save(os.path.join(OUT, "frames-fixed", f"f{fi:03d}.jpg"), quality=92)
        new_j = Image.open(os.path.join(OUT, "frames-fixed", f"f{fi:03d}.jpg")).convert("RGB")
        arr_o = np.array(old, dtype=np.int16); arr_n = np.array(new_j, dtype=np.int16)
        ndiff = int((np.abs(arr_o - arr_n).sum(axis=2) > 30).sum())
        (changed if ndiff > 0 else identical).append(fi)
        meas[fi]["diff_px_vs_elbow_fixed"] = ndiff
    print("CHANGED FRAMES:", changed)
    print("IDENTICAL FRAMES:", identical)
    feet = [m["feet_y"] for m in meas]
    print("FEET:", min(feet), max(feet), "EDGE:", [m["frame"] for m in meas if m["touches_edge"]])
    json.dump({"frames": 44, "fps": 24, "feet_y_min": min(feet), "feet_y_max": max(feet),
               "feet_y_spread_px": max(feet) - min(feet),
               "touches_edge_frames": [m["frame"] for m in meas if m["touches_edge"]],
               "min_margin_px": min(m["margin"] for m in meas),
               "old_gate": {"PASS": ok_old, "counts": cnt_old, "failures": fail_old},
               "new_gate": {"PASS": ok_new, "counts": cnt_new, "failures": fail_new},
               "changed_frames": changed, "identical_frames": identical,
               "audit": rows_new, "measurements": meas},
              open(os.path.join(OUT, "kneefeet_measurements.json"), "w"), indent=2)
    with open(os.path.join(OUT, "kneefeet_audit.csv"), "w") as fh:
        fh.write("frame,phase,leg_upper_L,leg_upper_R,knee_L,knee_R,knee_x_L,knee_x_R,crossed,footin_L,footin_R,changed_vs_elbow\n")
        for r, m in zip(rows_new, meas):
            fh.write(f"{r['frame']},{r['phase']},{r['leg_upper_L']},{r['leg_upper_R']},{r['knee_L']},{r['knee_R']},{r['knee_x_L']},{r['knee_x_R']},{r['crossed']},{r['footin_L']},{r['footin_R']},{r['frame'] in changed}\n")

    # 5. Contacts: full-frame old vs new + foot crops, for f11 (L-only),
    #    f13 (first both-inward), f20 (CONTACT-R key), f27 (last both-inward).
    def foot_crop(im):
        return im.crop((560, 1260, 1040, 1500)).resize((960, 480), Image.LANCZOS)
    picks = [11, 13, 20, 24]
    tw, th = 800, 900
    sheet = Image.new("RGB", (tw * 2, th * len(picks) + 60), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    d.text((10, 5), "KNEE-FEET FIX: OLD (elbow-fixed, original lowers) LEFT | NEW (FootIn lowers) RIGHT -- feet cropped below each full frame", fill=(255, 255, 0))
    y = 30
    for f in picks:
        old = Image.open(os.path.join(ELBOW, "frames-fixed", f"f{f:03d}.jpg")).convert("RGB")
        new = frames[f]
        r = rows_new[f]
        d.text((10, y), f"f{f:02d} OLD  L{ r['leg_upper_L']:+.1f} {r['knee_L']} / R{ r['leg_upper_R']:+.1f} {r['knee_R']}  toes original", fill=(255, 180, 180))
        d.text((tw + 10, y), f"f{f:02d} NEW  footin L={r['footin_L']} R={r['footin_R']}", fill=(180, 255, 180))
        sheet.paste(old.resize((tw // 2, th // 2), Image.LANCZOS), (0, y + 20))
        sheet.paste(new.resize((tw // 2, th // 2), Image.LANCZOS), (tw // 2, y + 20))
        sheet.paste(foot_crop(old), (tw, y + 20))
        # foot crop of new goes under? place as second row in right half: use lower half
        sheet.paste(foot_crop(new), (tw, y + 20 + 480))
        y += th + 20
    # The sheet layout above overlaps foot crops; rebuild cleanly instead:
    sheet = Image.new("RGB", (800, 480 * len(picks) * 2 + 60), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    d.text((10, 5), "KNEE-FEET FIX, FOOT CROPS ONLY: OLD top, NEW bottom per frame (f11 L-only, f13 first both-in, f20 CONTACT-R crossed=unchanged, f24 both-in after crossing)", fill=(255, 255, 0))
    y = 30
    for f in picks:
        old = Image.open(os.path.join(ELBOW, "frames-fixed", f"f{f:03d}.jpg")).convert("RGB")
        r = rows_new[f]
        d.text((10, y), f"f{f:02d} OLD feet  L{ r['leg_upper_L']:+.1f} {r['knee_L']} / R{ r['leg_upper_R']:+.1f} {r['knee_R']}", fill=(255, 180, 180))
        sheet.paste(foot_crop(old), (0, y + 20))
        y += 500
        d.text((10, y), f"f{f:02d} NEW feet  footin L={r['footin_L']} R={r['footin_R']}", fill=(180, 255, 180))
        sheet.paste(foot_crop(frames[f]), (0, y + 20))
        y += 500
    sheet.save(os.path.join(OUT, "kneefeet-before-after-contact-20261031.png"))
    # full-frame contact f20 + f13
    fsheet = Image.new("RGB", (800, 900 * 2 + 60), (0, 0, 0))
    fd = ImageDraw.Draw(fsheet)
    fd.text((10, 5), "KNEE-FEET FIX, FULL FRAMES: OLD left, NEW right", fill=(255, 255, 0))
    y = 30
    for f in (13, 20):
        old = Image.open(os.path.join(ELBOW, "frames-fixed", f"f{f:03d}.jpg")).convert("RGB")
        fd.text((10, y), f"f{f:02d} OLD", fill=(255, 180, 180)); fd.text((410, y), f"f{f:02d} NEW", fill=(180, 255, 180))
        fsheet.paste(old.resize((400, 450), Image.LANCZOS), (0, y + 20))
        fsheet.paste(frames[f].resize((400, 450), Image.LANCZOS), (400, y + 20))
        y += 470
    fsheet.save(os.path.join(OUT, "kneefeet-fullframe-contact-20261031.png"))
    print("BUILT 44f, GIF:", gif)
    return 0


if __name__ == "__main__":
    sys.exit(main())
