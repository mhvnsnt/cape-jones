"""Mandatory pre-delivery snap gate for the coming-forward walk.
This is the wiring Mars ordered 2026-10-31 20:39 CDT: spot the defect
and fix it AHEAD of time, before showing Mars, not after.
Rules, in order (general rule + walk-specific Mars ruling):
  G1  FACE-SNAP (lower_vs_head > 5000) requires applied == face.
  G2  COWL-CANDIDATE requires eye-check; cowl-whole is BANNED, only
      cowl-upper. (No walk frame is a cowl candidate: elbow_dy is
      +164..+184, i.e. elbow BELOW shoulder, never >50px above.)
  G3  CHEST-SNAP (lower_vs_torso > 1000) + eye-check 'upper eaten'
      requires applied in (chest, face). In the general refined rule
      chest alone is a WARNING; in THIS walk Mars has already ruled
      (20:39) that biceps-under-torso in front arms IS wrong, so
      with that eye-check it is a FAIL, not a warning.
  G4  REPORT ONLY, NOT A FAIL: chest-masked upper-eaten px (upper
      pixels hidden under Torso_Chest alone, collar excluded) is
      reported per side per frame, but it is NOT a decision criterion.
      ARM-FRONT-SNAP-RULE.md, standing: 'Upper-arm overlap is NOT the
      test: upper arms always overlap the torso by 4000+ px at the
      shoulder attachment, crossed or not. Only forearm overlap
      discriminates.' A chest-masked rule would snap every frame and
      break side arms. The decision criterion stays G3 (forearm
      overlap > 1000 + Mars eye-check that the upper IS eaten).
  G5  applied == face with gate != FACE-SNAP is a FAIL (arm over the
      face for no reason). applied == chest with gate == NO SNAP is
      NOT a fail by itself (gate allows it); G3 (forearm gate + Mars eye-check) is what decides it.
Usage:
  python3 gate_walk_snap.py --table walk_snap_table.json --applied old|fixed
  Exit 0 = PASS, 1 = FAIL, 2 = table/applied mismatch or missing file.
The --applied mode selects the 'applied' column of the table:
  old   = what the original walk shipped (snap=None, both sides)
  fixed = what the fixed builder must use
A table row is: frame, side, gate_decision, lower_vs_torso,
chest_masked_upper_eaten_px, applied_old, applied_fixed, eye_check.
"""
import argparse, json, sys, os
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True)
    ap.add_argument("--applied", choices=["old", "fixed"], required=True)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    if not os.path.exists(a.table):
        print(f"MISSING TABLE {a.table}"); return 2
    rows = json.load(open(a.table))
    fails, warns = [], []
    for r in rows:
        applied = r[f"applied_{a.applied}"]
        dec = r["gate_decision"]
        eye = r.get("eye_check", "")
        chest_eaten = r.get("chest_masked_upper_eaten_px", 0)
        tag = f"f{r['frame']} {r['side']}"
        if dec == "FACE-SNAP" and applied != "face":
            fails.append(f"{tag}: FACE-SNAP required, applied={applied}")
        if applied == "cowl-whole":
            fails.append(f"{tag}: cowl-whole BANNED")
        if dec == "COWL-CANDIDATE" and applied not in ("cowl-upper",) and not eye:
            fails.append(f"{tag}: COWL-CANDIDATE with no eye-check")
        if dec == "CHEST-SNAP" and "upper eaten" in eye and applied not in ("chest", "face"):
            fails.append(f"{tag}: CHEST-SNAP + eye-check upper eaten, applied={applied} (G3, Mars 20:39 ruling)")
        if dec == "CHEST-SNAP" and "upper eaten" not in eye:
            warns.append(f"{tag}: CHEST-SNAP, no upper-eaten eye-check (general rule: warning only)")
        if chest_eaten > 1000:
            warns.append(f"{tag}: chest-masked upper eaten {chest_eaten}px reported (G4 report only, NOT a fail: upper overlap alone does not decide)")
        if dec == "NO SNAP" and applied == "face":
            fails.append(f"{tag}: face snap with NO SNAP gate reason")
    print(f"rows={len(rows)} applied={a.applied} fails={len(fails)} warns={len(warns)}")
    for f in fails: print(" FAIL:", f)
    for w in warns: print(" WARN:", w)
    if a.out:
        json.dump({"applied": a.applied, "rows": len(rows), "fails": fails, "warns": warns,
                   "result": "FAIL" if fails else "PASS"}, open(a.out, "w"), indent=2)
    print("FAIL" if fails else "PASS")
    return 1 if fails else 0
if __name__ == "__main__":
    sys.exit(main())
