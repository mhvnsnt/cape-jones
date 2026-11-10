#!/usr/bin/env python3
"""ARM-FRONT-SNAP AUTOMATIC SENSOR — Mars 2026-11-01 11:25 CST.

Standing rule (ARM-FRONT-SNAP-RULE.md, Mars 2026-10-31 17:58, wire100
2026-10-31): when an arm crosses down across the chest in front of
him, that WHOLE arm chain (upper + forearm + fist + elbow cap) must
go to the TOP layer for exactly as long as it is crossing, so it is
not eaten by the chest. When it goes back out to the sides, snap OFF.

This script is the automatic sense, not a manual per-frame decision:
  SENSE (angles, mandatory BEFORE rendering):
    render that side's forearm alone, count alpha overlap with the
    Torso_Chest alpha mask at 1100x1500.  snap = overlap > 1000 px.
    Measured gap (dance-arm-snap audit, 63 frames): out-to-side
    0-268 px, crossed 1538-8969 px. 1000 sits in the empty middle,
    so the sensor does not flicker on shoulder-edge contact.
    Upper-arm overlap is NOT the test (always 4000+ px at the
    shoulder attachment, crossed or not).
  APPLY (builder):
    chest snap: whole chain above torso, BELOW head
      (torso < arm < head) — snap_figure.py chest pass.
    face snap (lower_vs_head > 5000): whole chain above head.
    cowl: UPPER ONLY above collar, candidate + eye-check only,
      never automatic, whole-chain cowl BANNED (JoJo 02 L).
  CHEST IS A WARNING, not an automatic FAIL by itself (wire100):
    lower_vs_torso > 1000 flags a pose for eye-check; it FAILs
    only if the eye-check says the upper IS eaten and no snap
    was applied. This script therefore outputs the measured
    overlap + a candidate flag, and the eye-check verdict is
    recorded alongside it, never guessed.

  FLAT-VIDEO PROXY (for already-rendered MP4s, second-best):
    A flat PNG cannot prove layer order after the fact (rule file,
    pipeline step). The proxy below therefore does NOT claim a
    layer verdict: it extracts frames, finds the hero bbox and
    chest band, and reports chest-band white coverage + whether
    a white arm run crosses the chest centre column. A candidate
    is flagged for eye-check; only an eye-checked eaten arm is a
    FAIL, and a flat video with an eaten arm CANNOT be fixed by
    re-layering pixels (the hidden pixels are gone) — it must be
    re-rendered from the rig with the angle-mode sensor ON.
    That limit is stated in every proxy CSV, not hidden.
    RETIRED AS A DISCRIMINATOR, 2026-11-01: run over 8 movement
    clips + dance-test at 6 fps, the proxy flagged 100% of
    frames as candidates, because the white torso itself fills
    the chest band on every frame. It cannot separate arm-white
    from torso-white, so its candidate count is NOT a snap count
    and is NOT used as a verdict anywhere in this task. The
    verdicts in CLIP-SNAP-AUDIT-20261101.csv come from
    eye-checked contact sheets (3 fps) + source-builder audits,
    per the rule's own eye-check-decides clause for chest cases.
    The proxy code is kept for its frame-extraction plumbing
    only; do not quote its candidate numbers as findings.

Usage:
  python3 arm_front_snap_sensor.py --angles   # crossed-down test pose
  python3 arm_front_snap_sensor.py --video <mp4> --out <csv>
"""
import os, sys, csv, math, argparse
from PIL import Image
import numpy as np

BASE = os.path.expanduser("~/workspace/cape-jones-rig/sliced")
CUT = os.path.expanduser("~/workspace/cape-jones-rig/cut-limbs-v7c")
SCALE = 0.95
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
SHOULDER = {"L": (430, 445), "R": (670, 445)}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)

def rot_vec(v, a):
    r = math.radians(a); x, y = v
    return (x*math.cos(r) + y*math.sin(r), -x*math.sin(r) + y*math.cos(r))

def limb_layer(path, joint, angle, anchor, scale=SCALE):
    im = load(path, scale); ax, ay = anchor[0]*scale, anchor[1]*scale
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    return layer.rotate(angle, center=joint, expand=False)

_TORSO = None
def torso_mask():
    global _TORSO
    if _TORSO is None:
        t = load(os.path.join(BASE, "Torso_Chest.png"))
        m = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
        m.paste(t, (int(550-t.size[0]/2), 400), t)
        _TORSO = np.array(m.split()[3]) > 0
    return _TORSO

def sense_from_angles(cfg):
    """cfg: arm_upper/arm_lower dicts L/R. Returns {side: (snap, overlap_px)}.
    Elbows computed exactly as build_arm_snap.py does."""
    ta = torso_mask(); out = {}
    for side in ("L", "R"):
        ball, sh_anchor = ARM[side]
        vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
        sh = SHOULDER[side]
        elbow = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE,
                 sh[1] + rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
        _, low, _ = ARM_PIECES[side]
        lay = limb_layer(os.path.join(CUT, low), elbow, cfg["arm_lower"][side], (ball[0], 0))
        ov = int(((np.array(lay.split()[3]) > 0) & ta).sum())
        out[side] = (ov > 1000, ov)
    return out

def sense_flat_frame(im):
    """Proxy only. Returns dict with hero bbox, chest-band white px,
    and centre-column white-run length. Candidate, not a verdict."""
    a = np.array(im.convert("RGB")).astype(int)
    # hero = pixels far from the frame's modal background colour
    flat = a.reshape(-1, 3)
    # modal bg: most common colour in corners
    corners = np.concatenate([flat[:1000], flat[-1000:]])
    bg = np.median(corners, axis=0)
    diff = np.abs(a - bg).sum(axis=2)
    mask = diff > 60
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return dict(hero_bbox=None, chest_white_px=0, centre_run=0, candidate=False)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    h = max(1, y1-y0); w = max(1, x1-x0)
    # chest band: 28%-47% of hero height (pecs/ribs zone, scaled)
    cy0, cy1 = int(y0 + 0.28*h), int(y0 + 0.47*h)
    band = mask[cy0:cy1, :]
    chest_white = int(band[:, x0:x1].sum())
    # centre column: white run across the chest centre line
    cx = (x0+x1)//2
    col = mask[cy0:cy1, cx-2:cx+3].any(axis=1)
    # longest run of True in col
    best = cur = 0
    for v in col:
        cur = cur+1 if v else 0; best = max(best, cur)
    return dict(hero_bbox=(int(x0), int(y0), int(x1), int(y1)),
                chest_white_px=chest_white, centre_run=int(best),
                candidate=bool(best >= 5 and chest_white > 500))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--angles", action="store_true")
    ap.add_argument("--video", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--fps", type=int, default=6)
    args = ap.parse_args()
    if args.angles:
        poses = {
            "crossed-down-across-chest": {"arm_upper": {"L": 20, "R": -20},
                                          "arm_lower": {"L": 90, "R": -90}},
            "stride-B-crossed (dance f015 lineage)": {"arm_upper": {"L": 35, "R": -35},
                                                       "arm_lower": {"L": 30, "R": -30}},
            "arms-out-control (dance f028 lineage)": {"arm_upper": {"L": -35, "R": 35},
                                                      "arm_lower": {"L": -30, "R": 30}},
        }
        for name, cfg in poses.items():
            s = sense_from_angles(cfg)
            print(f"{name}: L snap={s['L'][0]} overlap={s['L'][1]} px | "
                  f"R snap={s['R'][0]} overlap={s['R'][1]} px")
        return
    if args.video:
        import subprocess, tempfile
        out = args.out or "snap-proxy.csv"
        tmp = tempfile.mkdtemp(dir=os.path.expanduser("~/workspace/cape-jones-rig/arm-front-snap-auto-20261101/work"))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", args.video,
                        "-vf", f"fps={args.fps}", os.path.join(tmp, "f%04d.png")], check=True)
        rows = []
        for fn in sorted(os.listdir(tmp)):
            im = Image.open(os.path.join(tmp, fn))
            r = sense_flat_frame(im)
            rows.append(dict(frame=fn, hero_bbox=r["hero_bbox"],
                             chest_white_px=r["chest_white_px"],
                             centre_run=r["centre_run"],
                             candidate=r["candidate"],
                             note="PROXY ONLY: flat PNG cannot prove layer order; "
                                  "candidate = eye-check required, not a FAIL by itself"))
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        print(f"{args.video}: {len(rows)} frames, "
              f"{sum(r['candidate'] for r in rows)} candidates -> {out}")
        return
    ap.print_help()

if __name__ == "__main__":
    main()
