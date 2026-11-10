"""Elbow FK rig chain + measurement + corrected walk builder.

Industry-standard methods, run vs mapping, stated plainly:
- RUN: FK (forward kinematics) parent-child chain, shoulder -> upper
  (bicep) -> elbow joint -> forearm -> wrist/hand. Elbow position is
  COMPUTED from the shoulder and the upper angle (same formula as
  snap_figure.py), the forearm piece is pasted AT the computed elbow,
  so moving/sliding/rotating the bicep moves the elbow, and the elbow
  moves the forearm, by construction, not by hand-placing pieces.
  This is the rig the walk builders already used implicitly; here it
  is a named, tested module instead of an implicit formula.
- RUN: elbow-pole constraint (gate). A key is legal only if the elbow
  apex is LATERAL (outward): L arm elbow x < shoulder x, R arm elbow
  x > shoulder x. A medial (inward) apex FAILS the gate. This is the
  rule that would have caught the backwards CONTACT-L key.
- MAPPING (not a solver run here): IK with an elbow pole vector, as
  in Harmony / Animate / Blender / Spine. This 2D piece rig has no IK
  solver (pieces are fixed-angle rotations, no inverse solve), so IK
  is a mapping for a future port, never claimed as a run. FK is the
  run; the pole DIRECTION (outward) is the same in both.
- MAPPING: human anatomy ranges. Elbow is a hinge: flexion 0-145 deg,
  no hyperextension past straight in a normal walk, elbow points
  lateral/posterior, never medial toward the sternum in front view.
  Used as the anatomical reason for the outward-pole rule, not as a
  measured medical claim for this character.

Angle convention, screen space, measured from the builders:
  0 deg = straight down. Positive = tilted toward viewer's right
  (east), negative = toward viewer's left (west). Same convention
  for upper and lower, because both use the same rotate call.
  Upper native vector (shoulder -> elbow ball) is (-16,192) for L
  and (23,192) for R, scaled 0.95, so upper 0 already sits slightly
  outward for both sides. That is why PASSING (upper 0) is outward.

The correction, stated plainly so Mars can overrule it:
  ONLY the backwards key is negated. CONTACT-L arms were the only
  inward-apex key in the walk (both sides). CONTACT-R and PASSING
  already point outward. Negating the WHOLE walk would make
  CONTACT-R backwards, which would be wrong, so it was NOT done.
  Corrected CONTACT-L arms = the opposite tilt of old CONTACT-L
  arms (upper L -20 / R +20, lower L +30 / R -30), legs, scale,
  timing, feet and ground unchanged. Forced change, plainly:
  inbetween frames on the two segments touching CONTACT-L
  (frames 0-9 and 31-40 in the 44f walk) change because they
  interpolate from the corrected key; no other frame's key changes.
  Snap table from the layer-fix walk is reused unchanged (chest
  rows 0,1,2,3,37,38,39,40,41,42,43) because the corrected arms
  still come down in front of the chest there.
"""
import os, sys, math, json, subprocess, importlib.util
from PIL import Image, ImageDraw
import numpy as np

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "coming-forward-walk-elbow-fix-20261031")
LAYER = os.path.join(RIG, "coming-forward-walk-layer-fix-20261031")
W, H = 1600, 1800
GROUND_Y = 1500
GREY = (128, 128, 128)
HERO_H = 700
CX = 550

spec = importlib.util.spec_from_file_location("snap", os.path.join(RIG, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)

SHOULDERS = {"L": (CX - 120, 445), "R": (CX + 120, 445)}

def rot_vec(v, a):
    return snap.rot_vec(v, a)

class ArmChain:
    """FK chain: shoulder -> upper -> elbow -> forearm -> wrist.

    upper_angle / lower_angle are ABSOLUTE screen angles (the rig's
    convention). bend = lower - upper is the relative elbow bend.
    elbow() is computed, never hand-placed. wrist() is the forearm
    end using the measured lower-piece fist offset at angle 0,
    rotated by the lower angle in screen space.
    """
    def __init__(self, side, shoulder=None):
        self.side = side
        self.shoulder = shoulder if shoulder is not None else SHOULDERS[side]
        ball, anchor = snap.ARM[side]
        self.upper_vec = (ball[0] - anchor[0], ball[1] - anchor[1])
        # measured lower-piece fist-centroid offset at angle 0:
        # joint (550,600) -> centroid (565.7,824.8) in the test render
        self.lower_vec = (15.7, 224.8)

    def elbow(self, upper_angle):
        sh = self.shoulder
        v = rot_vec(self.upper_vec, upper_angle)
        return (sh[0] + v[0] * snap.SCALE, sh[1] + v[1] * snap.SCALE)

    def wrist(self, upper_angle, lower_angle):
        e = self.elbow(upper_angle)
        # screen rotation: PIL rotate(+a) moves a downward vector east
        r = math.radians(lower_angle)
        x, y = self.lower_vec
        wx = x * math.cos(r) + y * math.sin(r)
        wy = -x * math.sin(r) + y * math.cos(r)
        # note: lower piece native x offset is small; the dominant
        # term is y*sin(r), which is what the test render measured
        return (e[0] + wx, e[1] + wy)

    def apex(self, upper_angle):
        e = self.elbow(upper_angle)
        dx = e[0] - self.shoulder[0]
        if self.side == "L":
            return "OUTWARD" if dx < 0 else "INWARD (BACKWARDS)"
        return "OUTWARD" if dx > 0 else "INWARD (BACKWARDS)"

    def pole_pass(self, upper_angle):
        return self.apex(upper_angle) == "OUTWARD"

    def move_shoulder(self, dx, dy):
        return ArmChain(self.side, (self.shoulder[0] + dx, self.shoulder[1] + dy))

def measure_key(name, cfg):
    rows = []
    for side in ("L", "R"):
        ch = ArmChain(side)
        up = cfg["arm_upper"][side]; low = cfg["arm_lower"][side]
        e = ch.elbow(up); w = ch.wrist(up, low)
        rows.append({"key": name, "side": side, "bicep_angle_deg": up,
                     "forearm_angle_deg": low, "relative_bend_deg": low - up,
                     "shoulder_xy": [ch.shoulder[0], ch.shoulder[1]],
                     "elbow_xy": [round(e[0], 1), round(e[1], 1)],
                     "elbow_dx_px": round(e[0] - ch.shoulder[0], 1),
                     "wrist_approx_xy": [round(w[0], 1), round(w[1], 1)],
                     "elbow_apex": ch.apex(up), "pole_pass": ch.pole_pass(up)})
    return rows

# --- walk keys, old and corrected -------------------------------------
CONTACT_L_OLD = {"arm_upper": {"L": 20, "R": -20}, "arm_lower": {"L": -30, "R": 30},
                 "leg_upper": {"L": -28, "R": 22}, "leg_lower": {"L": 5, "R": 15}}
PASSING = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": -10, "R": 10},
           "leg_upper": {"L": 0, "R": 5}, "leg_lower": {"L": 15, "R": 5}}
CONTACT_R = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": 30, "R": -30},
             "leg_upper": {"L": 22, "R": -28}, "leg_lower": {"L": 15, "R": 5}}
CONTACT_L_NEW = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": 30, "R": -30},
                 "leg_upper": CONTACT_L_OLD["leg_upper"], "leg_lower": CONTACT_L_OLD["leg_lower"]}

def alpha_bbox(im):
    a = np.array(im.split()[3])
    rows = np.where(a.max(axis=1) > 10)[0]; cols = np.where(a.max(axis=0) > 10)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())

def anchor_layer(fig, scale):
    bx0, by0, bx1, by1 = alpha_bbox(fig); fig_h = by1 - by0 + 1
    plate_scale = (HERO_H * scale) / fig_h
    nw = max(1, int(fig.size[0] * plate_scale)); nh = max(1, int(fig.size[1] * plate_scale))
    scaled = fig.resize((nw, nh), Image.LANCZOS)
    sx0, sy0, sx1, sy1 = alpha_bbox(scaled)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx = W // 2 - (sx0 + sx1) // 2; top = GROUND_Y - sy1
    layer.alpha_composite(scaled, (cx, top))
    lx0, ly0, lx1, ly1 = alpha_bbox(layer)
    return layer, {"feet_y": ly1, "bbox": [lx0, ly0, lx1, ly1],
                   "touches_edge": (lx0 <= 0 or ly0 <= 0 or lx1 >= W - 1 or ly1 >= H - 1),
                   "margin": min(lx0, ly0, W - 1 - lx1, H - 1 - ly1)}

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

def smooth(t): return t * t * (3 - 2 * t)

def interp_cfg(a, b, t):
    return {k: {s: a[k][s] + (b[k][s] - a[k][s]) * smooth(t) for s in ("L", "R")} for k in a}

def mark_elbows(img, cfg, plate_scale, plate_origin, label=True):
    """Draw elbow markers + shoulder-elbow-forearm lines on a composed
    walk frame. plate_origin = (cx, top) of the scaled figure layer."""
    d = ImageDraw.Draw(img)
    cx0, top = plate_origin
    # figure plate is 1100x1500 scaled by plate_scale, centred at W/2:
    # layer placement in anchor_layer: cx = W//2 - (sx0+sx1)//2, top = GROUND_Y - sy1
    # recompute from the figure bbox instead: caller passes the layer bbox.
    return d

def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "frames-fixed"), exist_ok=True)
    # 1. measurements, old keys + corrected key
    meas = []
    for name, cfg in [("CONTACT-L-OLD", CONTACT_L_OLD), ("PASSING", PASSING),
                      ("CONTACT-R", CONTACT_R), ("CONTACT-L-CORRECTED", CONTACT_L_NEW)]:
        meas.extend(measure_key(name, cfg))
    # 2. rig-follow test, measured
    base = ArmChain("L")
    tests = []
    for label, ch, up, low in [
        ("base CONTACT-R L", base, -20, 30),
        ("bicep rotated +20 (upper -20 -> 0), bend kept", base, 0, 50),
        ("bicep rotated +20 (upper -20 -> 0), absolute forearm kept", base, 0, 30),
        ("shoulder slid +30 east", base.move_shoulder(30, 0), -20, 30),
        ("shoulder slid -40 west, +10 down", base.move_shoulder(-40, 10), -20, 30),
    ]:
        e = ch.elbow(up); w = ch.wrist(up, low)
        tests.append({"test": label, "shoulder_xy": [ch.shoulder[0], ch.shoulder[1]],
                      "upper_deg": up, "lower_deg": low, "bend_deg": low - up,
                      "elbow_xy": [round(e[0], 1), round(e[1], 1)],
                      "wrist_approx_xy": [round(w[0], 1), round(w[1], 1)],
                      "apex": ch.apex(up)})
    # pole gate on old walk keys
    gate = []
    for name, cfg in [("CONTACT-L-OLD", CONTACT_L_OLD), ("PASSING", PASSING), ("CONTACT-R", CONTACT_R)]:
        for side in ("L", "R"):
            gate.append({"key": name, "side": side,
                         "upper": cfg["arm_upper"][side], "lower": cfg["arm_lower"][side],
                         "pole_pass": ArmChain(side).pole_pass(cfg["arm_upper"][side])})
    gate_new = [{"key": "CONTACT-L-CORRECTED", "side": s,
                 "upper": CONTACT_L_NEW["arm_upper"][s], "lower": CONTACT_L_NEW["arm_lower"][s],
                 "pole_pass": ArmChain(s).pole_pass(CONTACT_L_NEW["arm_upper"][s])} for s in ("L", "R")]
    json.dump({"measurements": meas, "rig_follow_tests": tests,
               "pole_gate_old": gate, "pole_gate_corrected": gate_new},
              open(os.path.join(OUT, "elbow-measurements-20261031.json"), "w"), indent=2)
    for r in meas:
        print(r)
    print("TESTS")
    for t in tests:
        print(t)

    # 3. corrected walk, same structure as layer-fix builder
    table = json.load(open(os.path.join(LAYER, "walk_snap_table.json")))
    snap_by_frame = {}
    for r in table:
        snap_by_frame.setdefault(r["frame"], {})[r["side"]] = r["applied_fixed"]
    walk_keys = [(CONTACT_L_NEW, 0.70, "CONTACT-L-CORRECTED"), (PASSING, 0.95, "PASSING"),
                 (CONTACT_R, 1.20, "CONTACT-R"), (PASSING, 1.40, "PASSING"),
                 (CONTACT_L_NEW, 1.60, "CONTACT-L-CORRECTED")]
    frames, meas_w, phases = [], [], []
    SEG = 10
    for ki in range(len(walk_keys) - 1):
        cfg_a, s_a, lab_a = walk_keys[ki]; cfg_b, s_b, lab_b = walk_keys[ki + 1]
        for i in range(SEG):
            t = i / SEG; cfg = interp_cfg(cfg_a, cfg_b, t); s = s_a + (s_b - s_a) * smooth(t)
            fi = len(frames)
            snapd = {side: v for side, v in snap_by_frame.get(fi, {}).items() if v != "none"}
            fig = snap.figure(550, cfg, snap=snapd)
            layer, m = anchor_layer(fig, s)
            frames.append(compose(layer, s)); phases.append(lab_a if i == 0 else "INBETWEEN")
            m.update({"frame": fi, "scale": round(s, 4), "phase": phases[-1], "snap": snapd,
                      "arm_upper": cfg["arm_upper"], "arm_lower": cfg["arm_lower"]})
            meas_w.append(m)
    fig = snap.figure(550, CONTACT_L_NEW, snap={s: v for s, v in snap_by_frame.get(40, {}).items() if v != "none"})
    for _ in range(4):
        fi = len(frames); layer, m = anchor_layer(fig, 1.60)
        frames.append(compose(layer, 1.60)); phases.append("CONTACT-L-CORRECTED-HOLD")
        m.update({"frame": fi, "scale": 1.60, "phase": "CONTACT-L-CORRECTED-HOLD",
                  "snap": snap_by_frame.get(40, {}),
                  "arm_upper": CONTACT_L_NEW["arm_upper"], "arm_lower": CONTACT_L_NEW["arm_lower"]})
        meas_w.append(m)
    for i, f in enumerate(frames):
        f.save(os.path.join(OUT, "frames-fixed", f"f{i:03d}.jpg"), quality=92)
    gif = os.path.join(OUT, "coming-forward-walk-ELBOW-FIXED-20261031.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=int(1000 / 24), loop=0)
    feet = [m["feet_y"] for m in meas_w]
    report = {"frames": len(frames), "fps": 24, "feet_y_min": min(feet), "feet_y_max": max(feet),
              "feet_y_spread_px": max(feet) - min(feet),
              "touches_edge_frames": [m["frame"] for m in meas_w if m["touches_edge"]],
              "min_margin_px": min(m["margin"] for m in meas_w),
              "PASS": (max(feet) - min(feet) <= 1) and not any(m["touches_edge"] for m in meas_w),
              "measurements": meas_w}
    json.dump(report, open(os.path.join(OUT, "corrected_walk_measurements.json"), "w"), indent=2)
    print("BUILT", len(frames), "feet spread", max(feet) - min(feet), "PASS", report["PASS"])

    # 4. before/after contact with angle labels + elbow markers.
    # Elbow markers are drawn on the PLATE (1100x1500) before scaling,
    # using the analytic elbow positions, then the plate is anchored
    # the same way as the walk frames, so markers land on the caps.
    def plate_with_markers(cfg, snapd):
        fig = snap.figure(550, cfg, snap=snapd)
        d = ImageDraw.Draw(fig)
        for side in ("L", "R"):
            ch = ArmChain(side); e = ch.elbow(cfg["arm_upper"][side])
            r = 22
            d.ellipse([e[0] - r, e[1] - r, e[0] + r, e[1] + r], outline=(255, 0, 0), width=6)
            d.line([ch.shoulder, e], fill=(255, 0, 0), width=4)
            w = ch.wrist(cfg["arm_upper"][side], cfg["arm_lower"][side])
            d.line([e, w], fill=(255, 128, 0), width=4)
            d.ellipse([w[0] - 10, w[1] - 10, w[0] + 10, w[1] + 10], outline=(255, 128, 0), width=4)
        return fig

    def anchored_marked(cfg, snapd, scale):
        fig = plate_with_markers(cfg, snapd)
        layer, m = anchor_layer(fig, scale)
        return compose(layer, scale)

    # old vs new at CONTACT-L scale 0.70 (frame 0) and CONTACT-R scale 1.20 (frame 20, unchanged)
    pairs = []
    for lab, old_cfg, new_cfg, scale, snapd in [
        ("f00 CONTACT-L", CONTACT_L_OLD, CONTACT_L_NEW, 0.70, {"L": "chest", "R": "chest"}),
        ("f20 CONTACT-R (unchanged)", CONTACT_R, CONTACT_R, 1.20, {}),
        ("f40 CONTACT-L HOLD", CONTACT_L_OLD, CONTACT_L_NEW, 1.60, {"L": "chest", "R": "chest"}),
    ]:
        pairs.append((lab, anchored_marked(old_cfg, snapd, scale), anchored_marked(new_cfg, snapd, scale)))
    # contact sheet: 3 rows x 2 cols, downscaled
    tw, th = 500, 562
    sheet = Image.new("RGB", (tw * 2, th * 3 + 90), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    d.text((10, 5), "BEFORE (old elbows) LEFT  |  AFTER (corrected elbows) RIGHT  -- red ring = elbow, red line = bicep, orange = forearm", fill=(255, 255, 0))
    y = 30
    for lab, old_im, new_im in pairs:
        d.text((10, y), f"OLD {lab}", fill=(255, 180, 180))
        d.text((tw + 10, y), f"NEW {lab}", fill=(180, 255, 180))
        sheet.paste(old_im.resize((tw, th), Image.LANCZOS), (0, y + 20))
        sheet.paste(new_im.resize((tw, th), Image.LANCZOS), (tw, y + 20))
        y += th + 20
    sheet.save(os.path.join(OUT, "elbow-before-after-contact-20261031.png"))
    # rig-follow test contact: 3 plates, L arm only, shoulder/elbow/wrist lines
    def rig_plate(ch, up, low, title):
        fig = snap.figure(550, {"arm_upper": {"L": up, "R": 20}, "arm_lower": {"L": low, "R": -30},
                                    "leg_upper": {"L": 0, "R": 5}, "leg_lower": {"L": 15, "R": 5}})
        d = ImageDraw.Draw(fig)
        e = ch.elbow(up); w = ch.wrist(up, low)
        d.line([ch.shoulder, e], fill=(255, 0, 0), width=5)
        d.line([e, w], fill=(255, 128, 0), width=5)
        d.ellipse([e[0] - 24, e[1] - 24, e[0] + 24, e[1] + 24], outline=(255, 0, 0), width=6)
        d.ellipse([ch.shoulder[0] - 16, ch.shoulder[1] - 16, ch.shoulder[0] + 16, ch.shoulder[1] + 16], outline=(0, 255, 0), width=5)
        return fig
    rigs = [
        ("BASE upper -20", base, -20, 30),
        ("BICEP +20 -> upper 0, bend kept (lower 50)", base, 0, 50),
        ("SHOULDER +30 east, upper -20", base.move_shoulder(30, 0), -20, 30),
    ]
    rw, rh = 366, 500
    rsheet = Image.new("RGB", (rw * 3, rh + 60), (0, 0, 0))
    rd = ImageDraw.Draw(rsheet)
    rd.text((10, 5), "RIG FOLLOW TEST, L arm: green = shoulder, red ring = elbow, red = bicep, orange = forearm", fill=(255, 255, 0))
    for i, (title, ch, up, low) in enumerate(rigs):
        fig = rig_plate(ch, up, low, title)
        crop = fig.crop((250, 350, 800, 1000)).resize((rw, rh), Image.LANCZOS)
        bg = Image.new("RGBA", crop.size, (128, 128, 128, 255)); bg.alpha_composite(crop)
        rsheet.paste(bg.convert("RGB"), (i * rw, 30))
        rd.text((i * rw + 10, 35), title, fill=(255, 255, 0))
    rsheet.save(os.path.join(OUT, "rig-follow-test-contact-20261031.png"))
    print("CONTACTS SAVED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
