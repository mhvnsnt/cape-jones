#!/usr/bin/env python3
"""Build a Harmony-ready import pack from our locked sitting-pose manifest.

Runs WITHOUT Harmony installed. Output is a scene-folder skeleton +
node CSV + palette CSV + a QtScript stub. The stub is UNTESTED in Harmony
until activation; see README-20261101.md. No Toon Boom code is copied,
no proprietary binary is included, no piece is cropped here — pieces are
copied whole, by reference in the CSV, and the pack README tells Harmony
to import them as bitmap drawings.

Usage:
  python3 build_harmony_pack.py \
    --manifest ../../rig-34-locked-default-sitting-20261101/MANIFEST-DEFAULT-SITTING-POSE-20261101.json \
    --wired-manifest ../../rig-34-disassembled-wired-20261101/MANIFEST-20261101.json \
    --out ../templates/CapeJones_Sitting
"""
import argparse, csv, json, os, shutil, sys

PALETTE = [
    # name, r, g, b, role
    ("Cape_Outer_Black", 0, 0, 0, "outer cape, PMS BLACK"),
    ("Cape_Inner_Yellow", 255, 225, 82, "inner cape, PMS 115c"),
    ("Eyes_White", 255, 255, 255, "eyes, WHITE"),
    ("Suit_Green_336c", 0, 105, 80, "shirt/gloves/pants, PMS 336c (approx RGB; verify in-app)"),
    ("Shadow_Purple", 52, 22, 90, "coloured shadow, separate effect, NOT a rig"),
    ("Rim_Warm_Amber", 255, 180, 80, "rim default, L2 warm"),
    ("Rim_Bleed_Orange", 255, 120, 0, "bleed, L2 warm"),
]

# Node rows: (z, piece_id, node_name, peg_name, pivot_ox, pivot_oy, notes)
# Pivots from the widget inspection; cape/pelvis/head centre is ASSUMED,
# flagged in the bridge doc — verify in-app before first render.
NODES = [
    (0, "cape", "Cape", "Cape-P", 0.5, 0.5, "backmost, shoulders-back, collar fused in torso"),
    (1, "upperArmL", "Arm1-Upper", "Arm1-Upper-P", 0.5, 0, "LEFT arm, behind torso"),
    (2, "thighR", "Leg2-Thigh", "Leg2-Thigh-P", 0.5, 0, "RIGHT leg"),
    (3, "thighL", "Leg1-Thigh", "Leg1-Thigh-P", 0.5, 0, "LEFT leg"),
    (4, "forearmL", "Arm1-Forearm", "Arm1-Forearm-P", 0.39, 0.11, "LEFT forearm, whole, fist attached"),
    (4, "pelvis", "Pelvis", "Pelvis-P", 0.5, 0.5, "ASSUMED centre pivot — verify in-app"),
    (4, "kneeL", "Leg1-Knee", "Leg1-Knee-P", 0.5, 0.5, "knee pivot, NOT a secondary knee"),
    (5, "elbowCapL", "Arm1-ElbowCap", "Arm1-ElbowCap-P", 0.5, 0.5, "LEFT elbow cap"),
    (6, "shinL", "Leg1-Shin", "Leg1-Shin-P", 0.5, 0, "LEFT shin"),
    (6, "shinR", "Leg2-Shin", "Leg2-Shin-P", 0.5, 0, "RIGHT shin"),
    (7, "kneeR", "Leg2-Knee", "Leg2-Knee-P", 0.5, 0.5, "knee pivot"),
    (8, "torso", "Torso", "Torso-P", 0.5, 0, "collar fused, locked"),
    (8.5, "neck", "Neck", "Neck-P", 0.5, 0.5, "front-view neck, 101x82 rendered, 1.05x, NOT squashed"),
    (9, "head", "Head", "Head-P", 0.5, 0.5, "ASSUMED centre pivot — verify in-app"),
    (10, "upperArmR", "Arm2-Upper", "Arm2-Upper-P", 0.5, 0, "RIGHT arm, PERFECT, do not move"),
    (11, "forearmR", "Arm2-Forearm", "Arm2-Forearm-P", 0.63, 0.11, "RIGHT forearm, whole, fist attached"),
    (12, "elbowCapR", "Arm2-ElbowCap", "Arm2-ElbowCap-P", 0.5, 0.5, "RIGHT elbow cap"),
    (13, "handL", "Arm1-Hand", "Arm1-Hand-P", 0.5, 0.5, "LEFT hand, as-is, thumb east"),
    (13, "handR", "Arm2-Hand", "Arm2-Hand-P", 0.5, 0.5, "RIGHT hand, mirrored whole, thumb west"),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="")
    ap.add_argument("--wired-manifest", default="")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "elements"), exist_ok=True)
    os.makedirs(os.path.join(a.out, "palette"), exist_ok=True)

    # Saved pose, read-only: pull xy/rotation for each piece id if available.
    pose = {}
    for path in (a.manifest, a.wired_manifest):
        if path and os.path.exists(path):
            try:
                d = json.load(open(path))
                pieces = d.get("pieces", {})
                if isinstance(pieces, dict):
                    for k, v in pieces.items():
                        if isinstance(v, dict) and "xy" in v:
                            pose.setdefault(k, v)
                elif isinstance(pieces, list):
                    for v in pieces:
                        if isinstance(v, dict) and v.get("id"):
                            pose.setdefault(v["id"], v)
            except Exception as e:
                print(f"WARN manifest {path}: {e}", file=sys.stderr)

    rows = []
    for z, pid, node, peg, ox, oy, note in NODES:
        p = pose.get(pid, {})
        # Locked manifest uses xy=[x,y]; wired manifest uses x/y separately.
        # Prefer xy (locked, Mars-authored pose) when present.
        if "xy" in p:
            xy = p["xy"]
        elif "x" in p:
            xy = [p["x"], p.get("y", "")]
        else:
            xy = ["", ""]
        rot = p.get("rotation", "")
        rows.append({
            "z": z, "piece_id": pid, "drawing_node": node, "peg_node": peg,
            "pivot_ox": ox, "pivot_oy": oy, "saved_x": xy[0] if len(xy) > 0 else "",
            "saved_y": xy[1] if len(xy) > 1 else "", "saved_rotation": rot,
            "chain_note": note,
        })
    with open(os.path.join(a.out, "nodes.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    with open(os.path.join(a.out, "palette", "cape-jones-palette.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["name", "r", "g", "b", "role"]); w.writerows(PALETTE)

    with open(os.path.join(a.out, "README.md"), "w") as f:
        f.write("""# CapeJones_Sitting — Harmony import pack (skeleton)
1. In Harmony 27 Premium (activated, Windows/Mac): File > New Scene, 24 fps.
2. Import each piece in nodes.csv as a bitmap drawing (whole piece, no crop),
   create its peg, set pivot to pivot_ox/pivot_oy, set saved x/y/rotation.
   Verify cape/pelvis/head pivots (assumed centre) via Show Attribute Information.
3. Import palette/cape-jones-palette.csv via the palette editor, verify RGB
   against CAPE-JONES-HARMONY-BRIDGE-20261101.md before first render.
4. Run scripts/cape_jones_import_stub.js from Harmony's scripting interface.
   It is UNTESTED until activation — check its log against nodes.csv.
5. Save the rig as a Template (.tpl) in your CapeJones library. Do NOT
   overwrite the original default sitting pose; save new poses as new versions.
""")
    # Copy the QtScript stub alongside the pack for in-app use.
    stub_src = os.path.join(os.path.dirname(__file__), "cape_jones_import_stub.js")
    if os.path.exists(stub_src):
        shutil.copy(stub_src, os.path.join(a.out, "cape_jones_import_stub.js"))
    print(f"nodes: {len(rows)}")
    print(f"palette colours: {len(PALETTE)}")
    print(f"out: {a.out}")
    print("STATUS: pack skeleton built, UNTESTED in Harmony until activation.")

if __name__ == "__main__":
    main()
