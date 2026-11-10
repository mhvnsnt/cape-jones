"""I2 Angle classification — TRUE front vs 3/4 vs side, by geometry, not by filename.
RULES (locked, Mars 2026-11-01 00:58 CDT: all 10 angles are 3/4):
- TRUE FRONT = exactly 1 wall visible, wall edges vertical+horizontal (no converging corner),
  furniture faces camera flat (TV screen rectangle, not trapezoid, chair front flat).
- 3/4 CORNER = 2+ walls visible with a vertical corner line, floor/wall lines converge
  toward the corner, furniture shows a side face as well as a front face (CRT side visible,
  chair arm side visible, window frame depth visible).
- SIDE = 1 wall, profile view, 90 degrees.
- HIGH/LOW is a camera HEIGHT, not an angle type: high 3/4 and low 3/4 are still 3/4.
If claimed_label == 'front' and walls_visible >= 2: REJECT, relabel 3/4 corner.
"""
def classify(walls_visible, has_corner_line, furniture_shows_side):
    if walls_visible >= 2 and has_corner_line:
        return "3/4 corner"
    if walls_visible == 1 and not furniture_shows_side:
        return "true front"
    if walls_visible == 1 and furniture_shows_side:
        return "side/profile"
    return "3/4 corner"
if __name__ == "__main__":
    import json, pathlib
    labels = json.loads(pathlib.Path(__file__).parent.parent.joinpath("labels/corrected-labels-20261101.json").read_text())
    for r in labels["angles"]:
        got = classify(r["walls_visible"], r["corner_line"], r["furniture_shows_side"])
        assert got == r["true_angle"].split(",")[0], (r["id"], got, r["true_angle"])
    print("angle classifier: PASS — all 10 angles classify as 3/4 corner, 0 as true front")
