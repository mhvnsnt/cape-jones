"""Build walk_snap_table.json: one row per frame per side (44x2=88).
Gate decisions are transcribed from check_face_cowl_snap.py output run
on the exact walk configs (see gate_output.txt, copied below).
lower_vs_head = 0 on every side-frame (no face snap anywhere).
elbow_dy = +164..+184 (elbow BELOW shoulder, never a cowl candidate).
Decision rule: CHEST-SNAP iff lower_vs_torso > 1000, else NO SNAP.
applied_old = none (original walk shipped snap=None).
applied_fixed = chest iff CHEST-SNAP, else none.
eye_check: on CHEST-SNAP rows, Mars's 20:39 ruling that the upper IS
eaten in front arms, which turns the general chest WARNING into a
FAIL for the old walk under gate_walk_snap.py G3.
chest_masked_upper_eaten_px is merged from chest_masked_measurements.json
(torso-only diff, collar excluded) -- report only, NOT a decision
criterion, per ARM-FRONT-SNAP-RULE.md.
"""
import json, os
OUT = os.path.expanduser("~/workspace/cape-jones-rig/coming-forward-walk-layer-fix-20261031")
# (frame: (L_lower_vs_torso, R_lower_vs_torso))
GATE = {
 0:(2200,1383), 1:(2010,1285), 2:(1656,989), 3:(1236,651), 4:(778,308),
 5:(360,99), 6:(130,8), 7:(3,0), 8:(0,0), 9:(0,0), 10:(0,0), 11:(0,0),
 12:(0,0), 13:(0,0), 14:(0,0), 15:(0,0), 16:(0,0), 17:(0,0), 18:(0,0),
 19:(0,0), 20:(0,0), 21:(0,0), 22:(0,0), 23:(0,0), 24:(0,0), 25:(0,0),
 26:(0,0), 27:(0,0), 28:(0,0), 29:(0,0), 30:(0,0), 31:(0,0), 32:(0,0),
 33:(3,0), 34:(130,8), 35:(360,99), 36:(778,308), 37:(1236,651),
 38:(1656,989), 39:(2010,1285), 40:(2200,1383), 41:(2200,1383),
 42:(2200,1383), 43:(2200,1383)}
upper = {r["frame"]: r for r in json.load(open(os.path.join(OUT, "upper_eaten_measurements.json")))}
chest = {}
for r in json.load(open(os.path.join(OUT, "chest_masked_measurements.json"))):
    chest[(r["frame"], r["side"])] = r
rows = []
for f in range(44):
    for si, side in enumerate(("L", "R")):
        lv = GATE[f][si]
        dec = "CHEST-SNAP" if lv > 1000 else "NO SNAP"
        c = chest[(f, side)]
        rows.append({
            "frame": f, "side": side, "gate_decision": dec,
            "lower_vs_head": 0, "lower_vs_torso": lv,
            "upper_eaten_total_px": upper[f][f"upper_eaten_{side}_px"],
            "chest_masked_upper_eaten_px": c["diff_torso_only"] + c["diff_both"],
            "chest_masked_torso_only_px": c["diff_torso_only"],
            "chest_masked_both_px": c["diff_both"],
            "chest_masked_collar_only_px": c["diff_collar_only"],
            "applied_old": "none",
            "applied_fixed": "chest" if dec == "CHEST-SNAP" else "none",
            "eye_check": "upper eaten in front arms, Mars 2026-10-31 20:39" if dec == "CHEST-SNAP" else "",
            "snap_order_fixed": "torso < arm < head" if dec == "CHEST-SNAP" else "normal (upper < torso < lower < head)",
        })
json.dump(rows, open(os.path.join(OUT, "walk_snap_table.json"), "w"), indent=2)
n_chest = sum(1 for r in rows if r["applied_fixed"] == "chest")
print(f"rows={len(rows)} chest_snaps={n_chest} (L={sum(1 for r in rows if r['side']=='L' and r['applied_fixed']=='chest')}, R={sum(1 for r in rows if r['side']=='R' and r['applied_fixed']=='chest')})")
print("chest frames L:", [r["frame"] for r in rows if r["side"]=="L" and r["applied_fixed"]=="chest"])
print("chest frames R:", [r["frame"] for r in rows if r["side"]=="R" and r["applied_fixed"]=="chest"])
