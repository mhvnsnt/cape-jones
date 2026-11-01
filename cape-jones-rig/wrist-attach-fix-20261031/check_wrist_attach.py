"""WRIST-ATTACHMENT GATE — Cape Jones cutout rig.

Industry-standard rule wired here (anatomy + rigging):
  * The WRIST is the joint: carpus sits between forearm (radius/ulna) and
    hand. In a cutout rig the hand piece's WRIST END (cuff) must meet the
    forearm piece's distal (wrist) end. The fingertip end must be FARTHER
    from the forearm end than the wrist end is — fingertip-first = FAIL.
  * Harmony/Animate: hand is a separate drawing parented at the wrist
    pivot; the pivot, not the drawing centre, is placed on the forearm end.
  * Blender Grease Pencil / Spine: same — bone end = wrist pivot, hand
    drawing hangs off that pivot, never centred on the fist position.
  * Traditional animation: wrist overlap — the cuff overlaps the forearm
    end by ~one wrist width so the joint reads continuous, never a gap
    and never a fingertip-only touch.

Gate (measured on paste parameters, not on a flat PNG, because a flat PNG
cannot separate hand alpha from arm alpha):
  PASS iff  d_wrist <= 30 px  AND  d_wrist < d_tip
  where d_wrist = distance(wrist point after transform, forearm end),
        d_tip   = distance(fingertip point after transform, forearm end).
  30 px at 1100x1500 scale ~= one wrist width / one cuff height.

Hand registry: wrist/tip points measured from alpha (bottom-14-row cuff
centre / topmost-row centre). Offsets are from the IMAGE centre, because
builders paste by image centre. No hand is drawn here; all pieces are
pulled from sliced/.

  Hand_1_Fist    wrist (+? ) see HANDS below (measured 2026-10-31)
  All 7 canon hands have wrist at the BOTTOM, fingertips at the TOP
  in native orientation — so an unrotated paste centred on the fist
  puts the wrist ~1.7x the wrist offset BELOW the joint. That is the
  defect in the old dance-variant swaps and in the old Jeice serve.

Fix rule (Mars, 2026-10-31 ~18:52 CDT): MOVE the hand so its wrist lands
on the forearm end. NO MIRROR, NO FLIP. Where the hand as placed is
fingertip-first, the hand is turned IN-PLANE (rotation, not a mirror)
so the wrist end faces the forearm, then moved — a pure translation
cannot fix a fingertip-first hand, and the move-only control is kept in
the output so Mars can see that failure with his own eyes.

Usage:
  python3 check_wrist_attach.py --csv audit.csv   (prints PASS/FAIL table)
"""
import math, csv, sys

# name: (image size, wrist point, fingertip point) — measured from alpha
HANDS = {
    "Hand_1_Fist.png":    ((90, 108), (40.3, 95.6), (50.6, 4.0)),
    "Hand_2_FistBack.png":((94, 131), (46.4, 118.4), (58.1, 4.0)),
    "Hand_3_Open.png":    ((103, 141), (53.9, 128.6), (55.3, 4.0)),
    "Hand_4_Point.png":   ((83, 148), (40.5, 135.6), (41.0, 4.0)),
    "Hand_5_Point2.png":  ((97, 148), (45.6, 135.4), (56.8, 4.0)),
    "Hand_6_Relaxed.png": ((101, 142), (61.4, 129.4), (45.9, 4.0)),
    "Hand_7_Grip.png":    ((103, 129), (63.5, 116.5), (54.6, 4.0)),
}
TOL = 30.0

def rot_vec(v, a_deg):
    a = math.radians(a_deg); x, y = v
    return (x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a))

def placed_points(hand, centre, angle, scale):
    """Return (wrist, tip) in canvas coords for a paste by image centre."""
    (W, H), wrist, tip = HANDS[hand]
    ic = (W / 2.0, H / 2.0)
    wo = ((wrist[0] - ic[0]) * scale, (wrist[1] - ic[1]) * scale)
    to = ((tip[0] - ic[0]) * scale, (tip[1] - ic[1]) * scale)
    wr = rot_vec(wo, angle); tr = rot_vec(to, angle)
    return ((centre[0] + wr[0], centre[1] + wr[1]),
            (centre[0] + tr[0], centre[1] + tr[1]))

def check(hand, centre, angle, scale, forearm_end):
    wrist, tip = placed_points(hand, centre, angle, scale)
    dw = math.dist(wrist, forearm_end); dt = math.dist(tip, forearm_end)
    ok = (dw <= TOL) and (dw < dt)
    return {"wrist": wrist, "tip": tip, "d_wrist": dw, "d_tip": dt,
            "pass": ok, "verdict": "PASS" if ok else "FAIL"}

def centre_for_wrist(hand, angle, scale, wrist_target):
    """Image centre that lands the wrist point exactly on wrist_target."""
    (W, H), wrist, _ = HANDS[hand]
    ic = (W / 2.0, H / 2.0)
    wo = ((wrist[0] - ic[0]) * scale, (wrist[1] - ic[1]) * scale)
    wr = rot_vec(wo, angle)
    return (wrist_target[0] - wr[0], wrist_target[1] - wr[1])

def angle_for_direction(D):
    """PIL angle that turns native wrist->tip (0,-1) onto unit vector D."""
    # rot_vec((0,-1), a) = (-sin a, -cos a) = D  =>  a = atan2(-Dx, -Dy)
    return math.degrees(math.atan2(-D[0], -D[1]))

if __name__ == "__main__":
    rows = []
    # --- Jeice serve (old vs fixed), forearm end = built-in fist centre
    F = (314.0, 517.0)
    old = check("Hand_3_Open.png", (314, 530), -20, 1.0, F)
    rows.append(["jei-01-serve-OLD", "Hand_3_Open", (314, 530), -20, 1.0, F,
                 round(old["d_wrist"], 1), round(old["d_tip"], 1), old["verdict"]])
    # fixed: arm direction elbow(382,268) -> F
    import math as _m
    D = ((F[0] - 382) / _m.dist((382, 268), F), (F[1] - 268) / _m.dist((382, 268), F))
    a = angle_for_direction(D)
    wt = (F[0] - D[0] * 25, F[1] - D[1] * 25)  # 25px overlap into forearm
    c = centre_for_wrist("Hand_3_Open.png", a, 1.0, wt)
    new = check("Hand_3_Open.png", c, a, 1.0, F)
    rows.append(["jei-01-serve-FIXED", "Hand_3_Open", tuple(round(v, 1) for v in c),
                 round(a, 1), 1.0, F, round(new["d_wrist"], 1),
                 round(new["d_tip"], 1), new["verdict"]])
    # move-only control for serve: wrist forced onto F, angle kept -20
    c2 = centre_for_wrist("Hand_3_Open.png", -20, 1.0, F)
    mo = check("Hand_3_Open.png", c2, -20, 1.0, F)
    rows.append(["jei-01-serve-MOVE-ONLY-CONTROL", "Hand_3_Open",
                 tuple(round(v, 1) for v in c2), -20, 1.0, F,
                 round(mo["d_wrist"], 1), round(mo["d_tip"], 1),
                 mo["verdict"] + " (numeric only; hand overlaps gauntlet, see crop)"])
    print("item, hand, centre, angle, scale, forearm_end, d_wrist, d_tip, verdict")
    for r in rows:
        print(", ".join(str(x) for x in r))
    if len(sys.argv) > 2 and sys.argv[1] == "--csv":
        with open(sys.argv[2], "w", newline="") as f:
            w = csv.writer(f); w.writerow(["item", "hand", "centre", "angle", "scale",
                                           "forearm_end", "d_wrist", "d_tip", "verdict"])
            w.writerows(rows)
