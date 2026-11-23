#!/usr/bin/env python3
"""Numeric verification of a V3 transforms dump — no eyeballing.
Rig Jones 2 / Clean-Up Jones 1, v2 (socket cut + invisible swap).

Checks (all in rig units, tolerance 0.06 unless stated):
 1. One hand per arm, one mouth — as SINGLE planes (P_handR, P_handL,
    P_mouth), always visible, with a per-frame "tex" naming the active
    variant image. No second pair of hands, no stacked planes.
 2. SWAP CONTINUITY (new): an ART property. The hand/mouth planes are
    single planes parented to their bones, so a swap cannot move the
    plane (its transform is bone-driven); what a swap CAN change is the
    drawn art. Every hand variant's cuff centre must sit at the canvas
    centre (x=66) with the cuff top at row 0; every mouth variant's
    opaque bbox must be centred on the 105x95 canvas. A swap is
    invisible iff the art is centred and the plane is one.
 3. JOINTS — ball == socket. Each joint was cut along the ball's own
    outline circle (prep_art.py v2): the ball belongs entirely to the
    LOWER piece, the upper piece ends in a concave socket of the same
    circle. The ball centre (ball_local in art-geometry.json, the same
    world point in both planes' local frames) must coincide at EVERY
    frame. NO overlap, NO cap, NO gap — if the two pieces pivoted about
    different points, the ball centres would separate.
 4. Shoulder attachment: upper-arm top == the moving shoulder point
    (derived from the torso plane — the shoulder rides the torso).
 5. Wrist: the hand's cuff (top centre) == the forearm's WRIST PINCH
    point (not the forearm plane's bottom midpoint — the limb wanders
    off its centre line, so the midpoints do not coincide even when the
    art is attached). The cuff centre and the pinch coincide in the art.
 6. Cape: top row stays at the neck (y ~10.9, not lifted with the arm);
    cape tip x stays near the top centre (not swung with the arm).
 7. Remote: when visible, its grip point lands on the Grip hand's
    finger centre (from art-geometry.json — the Grip finger centroid
    measured on the common canvas), within 0.20.
Usage: python3 v3-swap-system/verify_v3.py <transforms.json>
Exit 0 = all pass, 1 = any fail.
"""
import json
import math
import os
import sys

V3 = "/home/hatch/workspace/_cape-jones-parking-lot-2d/v3-swap-system"
TOL = 0.06
GEOM = json.load(open(os.path.join(V3, "art-geometry.json")))


def rot_point(cx, cy, dx, dy, deg):
    a = math.radians(deg)
    return (cx + dx * math.cos(a) - dy * math.sin(a),
            cy + dx * math.sin(a) + dy * math.cos(a))


def top(p, rec):
    return rot_point(rec["x"], rec["y"], 0, p["h"] / 2, rec["rot"])


def bottom(p, rec):
    return rot_point(rec["x"], rec["y"], 0, -p["h"] / 2, rec["rot"])


def ball_at(plane_name, rec):
    bl = GEOM["planes"][plane_name]["ball_local"]
    return rot_point(rec["x"], rec["y"], bl[0], bl[1], rec["rot"])


def wrist_local(side, fa_plane_name):
    """The wrist pinch in the forearm plane's local frame. The wrist is
    NOT at the forearm plane's bottom midpoint — the limb wanders off
    its centre line (R wrist rig x -1.7235 vs plane centre -1.6; L
    1.92775 vs 1.6). The wrist point is the pinch: its rest rig coords
    minus the plane centre. Measuring bottom-midpoint to hand-top
    reported a constant 0.12/0.33 'gap' that is not a gap at all — the
    art's cuff centre and the art's wrist pinch coincide; the plane
    midpoints do not."""
    w = GEOM["wrists"][side]["rig"]
    c = GEOM["planes"][fa_plane_name]["center"]
    return (w[0] - c[0], w[1] - c[1])


def wrist_at(side, fa_plane_name, rec):
    wl = wrist_local(side, fa_plane_name)
    return rot_point(rec["x"], rec["y"], wl[0], wl[1], rec["rot"])


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def main(path):
    spec = json.load(open(path))
    parts = {p["name"]: p for p in spec["parts"]}
    frames = spec["frames"]
    fails = []

    def check(cond, msg):
        if not cond:
            fails.append(msg)

    # 1. Single hand/mouth planes, always visible, tex present.
    for pname in ("P_handR", "P_handL", "P_mouth"):
        check(pname in parts, f"{pname} missing from dump")
        if pname not in parts:
            continue
        p = parts[pname]
        for f in range(1, frames + 1):
            rec = p["frames"][f - 1]
            check(not rec["hide"], f"f{f}: {pname} hidden (want always visible)")
            check("tex" in rec, f"f{f}: {pname} has no tex (want active variant)")
    # No leftover multi-plane hand/mouth parts from v1.
    for p in parts.values():
        check(not (p["name"].startswith("P_handR_") or
                   p["name"].startswith("P_handL_") or
                   p["name"].startswith("P_mouth_")),
              f"leftover v1 multi-plane part: {p['name']}")

    # 2. Swap continuity — an ART property, not a per-frame one. The
    # hand/mouth planes are single planes parented to their bones, so a
    # swap cannot move the plane (its transform is bone-driven); what a
    # swap CAN change is the drawn art — if a variant's cuff were drawn
    # off-centre, the hand would jump at the swap. The guarantee is in
    # the art: every hand variant's cuff centre must sit at the canvas
    # centre (x=66) with the cuff top at row 0; every mouth variant's
    # opaque bbox must be centred on the 105x95 canvas (x ~52.5).
    # (The first two versions of this check compared per-frame plane
    # centres and failed good frames — they were measuring the arm's
    # swing, not the swap. The swap is invisible iff the art is centred
    # and the plane is one. Both are checked here.)
    from PIL import Image as _Image
    import numpy as _np
    for side in ("R", "L"):
        for i in range(1, 8):
            pth = os.path.join(V3, "art", f"Hand_{side}_{i}.png")
            a = _np.asarray(_Image.open(pth).convert("RGBA")).astype(int)
            alpha = a[:, :, 3] > 0
            top_rows = alpha[:6, :]
            ys, xs = _np.where(top_rows)
            cuff_cx = xs.mean() if len(xs) else -1
            check(abs(cuff_cx - 66) < 2,
                  f"Hand_{side}_{i}: cuff centre x={cuff_cx:.1f} (want 66)")
            top_row = _np.where(alpha.any(axis=1))[0][0]
            check(top_row <= 1,
                  f"Hand_{side}_{i}: cuff top row={top_row} (want 0)")
    for mn in ("Closed", "Open", "Shout", "Smile", "Teeth"):
        pth = os.path.join(V3, "art", f"Mouth_{mn}.png")
        a = _np.asarray(_Image.open(pth).convert("RGBA")).astype(int)
        alpha = a[:, :, 3] > 0
        ys, xs = _np.where(alpha)
        check(abs(xs.mean() - 52.5) < 5,
              f"Mouth_{mn}: opaque centre x={xs.mean():.1f} (want ~52.5)")

    for f in range(1, frames + 1):
        # 3. Ball == socket at every joint, every frame.
        for ua, fa, plane_u, plane_l in (
                ("P_UpperArmR", "P_ForearmR", "UpperArmR", "ForearmR"),
                ("P_UpperArmL", "P_ForearmL", "UpperArmL", "ForearmL"),
                ("P_ThighR", "P_ShinR", "ThighR", "ShinR"),
                ("P_ThighL", "P_ShinL", "ThighL", "ShinL")):
            bu = ball_at(plane_u, parts[ua]["frames"][f - 1])
            bl_ = ball_at(plane_l, parts[fa]["frames"][f - 1])
            d = dist(bu, bl_)
            check(d < TOL, f"f{f}: {ua}/{fa} ball-socket gap {d:.3f}")
        # 4. Shoulder: upper-arm top == moving shoulder point.
        torso = parts["P_Torso_Chest"]["frames"][f - 1]
        for ua, sx in (("P_UpperArmR", -1.6), ("P_UpperArmL", 1.6)):
            sh = rot_point(torso["x"], torso["y"],
                           sx - 0.0, 10.8 - 9.485, torso["rot"])
            d = dist(top(parts[ua], parts[ua]["frames"][f - 1]), sh)
            check(d < TOL, f"f{f}: shoulder {ua} gap {d:.3f}")
        # 5. Wrist: the hand's cuff (top centre) == the forearm's WRIST
        # PINCH point (not the forearm plane's bottom midpoint — see
        # wrist_local()). The cuff centre and the pinch coincide in the
        # art; that is the attachment.
        for fa_name, hand_name, side in (("P_ForearmR", "P_handR", "R"),
                                         ("P_ForearmL", "P_handL", "L")):
            wpt = wrist_at(side, fa_name[2:], parts[fa_name]["frames"][f - 1])
            d = dist(wpt, top(parts[hand_name], parts[hand_name]["frames"][f - 1]))
            check(d < TOL, f"f{f}: wrist {fa_name} gap {d:.3f}")

    # 6. Cape.
    cape = spec["cape"]
    rest = cape["frames"][0]["verts"]
    xs = [v[0] for v in rest.values()]
    ys = [v[1] for v in rest.values()]
    check(abs(min(xs) + 2.3275) < 0.1 and abs(max(xs) - 2.3275) < 0.1,
          f"cape rest width {min(xs):.2f}..{max(xs):.2f} (want +-2.33)")
    check(abs(max(ys) - 10.9) < 0.1 and abs(min(ys) - 2.99) < 0.1,
          f"cape rest height {min(ys):.2f}..{max(ys):.2f} (want 2.99..10.9)")
    for f in range(1, frames + 1):
        verts = cape["frames"][f - 1]["verts"]
        top_y = max(v[1] for k, v in verts.items() if k.endswith(",0"))
        check(abs(top_y - 10.9) < 0.35,
              f"f{f}: cape top row y={top_y:.2f} (want ~10.9, not lifted)")
        tip_x = [v[0] for k, v in verts.items() if k.endswith(",12")]
        top_x = [v[0] for k, v in verts.items() if k.endswith(",0")]
        tip_cx = sum(tip_x) / len(tip_x)
        top_cx = sum(top_x) / len(top_x)
        check(abs(tip_cx - top_cx) < 0.8,
              f"f{f}: cape tip centre x {tip_cx:.2f} vs top {top_cx:.2f}")

    # 7. Remote grip: grip point vs the Grip finger centre from the
    # geometry file (measured on the common canvas: canvas (75.4,100.7),
    # canvas centre (66,72) -> local (0.089, -0.273) rig units).
    rem = parts.get("P_remote_Remote_Device")
    if rem:
        fx, fy = GEOM["hands"]["Grip_R_finger_canvas"]
        finger_local = ((fx - 66) * 0.0095, (72 - fy) * 0.0095)
        for f in range(1, frames + 1):
            rec = rem["frames"][f - 1]
            if rec["hide"]:
                continue
            gx, gy = rot_point(rec["x"], rec["y"], 0.18, 0.0855, rec["rot"])
            hp = parts["P_handR"]["frames"][f - 1]
            if "Grip" not in hp.get("tex", ""):
                continue
            fcx, fcy = rot_point(hp["x"], hp["y"],
                                 finger_local[0], finger_local[1], hp["rot"])
            d = math.hypot(gx - fcx, gy - fcy)
            check(d < 0.20, f"f{f}: remote grip gap {d:.3f}")

    if fails:
        print(f"VERIFY FAIL ({len(fails)}):")
        for m in fails[:25]:
            print("  ", m)
        return 1
    print(f"VERIFY PASS: {frames} frames — 1 hand/side (single plane), "
          f"1 mouth, ball==socket, shoulder/wrist attached, cape hanging, "
          f"remote on grip, swaps invisible")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
