"""Universal knee-feet gate + leg chain.

Standing rule (KNEE-FEET-RULE.md, bidirectional):
  knees INWARD  -> toes INWARD  (FootIn mirrored lower)
  knees OUTWARD -> toes OUTWARD (original lower)
  knees STRAIGHT (thigh angle 0) -> toes STRAIGHT (original lower, do not flip)

Angle convention (same as the rig builders): 0 deg = straight down,
positive = toward viewer's right (east), negative = toward viewer's
left (west). A leg's thigh is INWARD when it angles toward the
midline: L upper > 0, R upper < 0. OUTWARD is the reverse sign.
STRAIGHT is exactly 0. This is the thigh-angle sign, NOT knee-x minus
hip-x: at rest the thigh piece already sits slightly inboard of the
hip, so x-offset alone misreads straight legs as inward.

The gate is PER FRAME and PER LEG. A block range (e.g. "FootIn on
frames 15-55") FAILS by construction: knee direction changes inside a
segment, so a block flips outward-knee frames inward and misses
inward-knee frames outside the block. That was the v1 dance mistake,
corrected 2026-10-31 16:58 CDT, and it must not be repeated.

Usage: gate_table(rows) where each row has frame, leg_upper_L,
leg_upper_R, footin_L, footin_R. Returns (pass_bool, failures).
Exit code: 0 = PASS, 1 = FAIL, 2 = usage error.
A movement builder MUST call this BEFORE rendering and refuse the
build on FAIL. That is the universal wiring: no builder in any lane
ships a movement without passing this gate first.
"""
import json, sys


def leg_direction(side, upper_deg):
    """INWARD / OUTWARD / STRAIGHT for one leg from its thigh angle."""
    if upper_deg == 0:
        return "STRAIGHT"
    if side == "L":
        return "INWARD" if upper_deg > 0 else "OUTWARD"
    return "INWARD" if upper_deg < 0 else "OUTWARD"


def required_footin(side, upper_deg, crossed=False):
    """True iff this leg's toe must be the FootIn (inward) piece.
    crossed=True is the measured crossed-leg exception: when the
    knees cross (L knee screen-x > R knee screen-x), the legs have
    swapped screen sides, so the original feet already point inward
    by crossing (verified at CONTACT-R f20: old feet point toward
    each other). Mirroring them there would point toes OUTWARD and
    break the frame, so crossed frames keep original lowers.
    crossed is measured per frame from analytic knee x, never a
    block range."""
    if crossed:
        return False
    return leg_direction(side, upper_deg) == "INWARD"


def knee_x(side, upper_deg):
    """Analytic knee screen-x in the 1100x1500 plate, from snap.figure
    hips and leg vectors (SCALE 0.95). L hip (470,740), vector
    (18,274); R hip (615,740), vector (16,274)."""
    import math
    hip, vec = (470, (18, 274)) if side == "L" else (615, (16, 274))
    r = math.radians(upper_deg); x, y = vec
    return hip + (x * math.cos(r) + y * math.sin(r)) * 0.95


class LegChain:
    """FK leg chain, mirror of the arm chain: hip -> thigh -> knee
    -> lower -> foot/toe. The knee is COMPUTED from the hip and the
    thigh angle, never hand-placed; the lower piece is pasted AT the
    computed knee; the toe direction is then DECIDED by the gate
    (original vs FootIn), never by bending the knee sideways. The
    knee is a hinge: it cannot bend sideways, so any knee/foot
    direction mismatch reads as a broken joint, whichever way it
    points (valgus = knee-in/toe-out, varus = knee-out/toe-in)."""

    def __init__(self, side, hip):
        self.side, self.hip = side, hip

    def knee_direction(self, upper_deg):
        return leg_direction(self.side, upper_deg)

    def footin_required(self, upper_deg):
        return required_footin(self.side, upper_deg)


def gate_table(rows):
    """rows: list of dicts with frame, leg_upper_L, leg_upper_R,
    footin_L, footin_R. Returns (ok, failures, counts)."""
    failures, n_leg = [], 0
    for r in rows:
        crossed = bool(r.get("knee_x_L", 0) > r.get("knee_x_R", 0)) if "knee_x_L" in r else False
        for side, ukey, fkey in (("L", "leg_upper_L", "footin_L"),
                                 ("R", "leg_upper_R", "footin_R")):
            n_leg += 1
            want = required_footin(side, r[ukey], crossed=crossed)
            got = bool(r[fkey])
            if want != got:
                failures.append({
                    "frame": r["frame"], "side": side,
                    "leg_upper_deg": r[ukey],
                    "knee_direction": leg_direction(side, r[ukey]),
                    "footin_required": want, "footin_used": got,
                    "defect": "knee INWARD, toe NOT switched"
                              if want else "knee NOT inward, toe switched wrongly",
                })
    frames_bad = sorted({f["frame"] for f in failures})
    counts = {"leg_frames": n_leg, "mismatches": len(failures),
              "frames_with_any_mismatch": len(frames_bad),
              "frames_bad": frames_bad}
    return (not failures), failures, counts


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: kneefeet_gate.py <table.json>  (rows: frame, leg_upper_L, leg_upper_R, footin_L, footin_R)")
        sys.exit(2)
    rows = json.load(open(sys.argv[1]))
    ok, failures, counts = gate_table(rows)
    print(json.dumps({"PASS": ok, "counts": counts, "failures": failures}, indent=2))
    sys.exit(0 if ok else 1)
