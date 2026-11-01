"""Build + test Cape Jones Toon own version. Exit 0 = all tests pass.

Usage:
  python3 build_own_version.py
Outputs (in ../output/, numbers only, NO PNGs):
  scene.cjstage.json, harmony_check.js, animation_keys.json, test_report.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cjtoon import (CHAINS, FPS, GROUND_Y, build_scene, export_harmony_check_script,
                    inbetween, load_nodes, load_palette, onion_weights,
                    roundtrip_check, validate_chains)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
WIRE = Path.home() / "workspace/cape-jones-rig/toon-boom-wire100-20261101"
NODES_CSV = WIRE / "templates/CapeJones_Sitting/nodes.csv"
PALETTE_CSV = WIRE / "templates/CapeJones_Sitting/palette/cape-jones-palette.csv"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = load_nodes(NODES_CSV)
    palette = load_palette(PALETTE_CSV)
    chains = validate_chains(nodes)
    assert chains["ok"], f"chain members missing: {chains['missing']}"
    assert len(nodes) == 19, f"expected 19 nodes, got {len(nodes)}"
    assert len(palette) == 7, f"expected 7 palette colours, got {len(palette)}"

    scene = build_scene(nodes, palette)
    rt = roundtrip_check(scene)
    assert rt["count_ok"] and rt["values_exact"], rt

    # Animation test: sit-idle bob, from locked pose (key A) to bob key (key B).
    # Key B = upper chains +3px y, head +2 deg; pelvis/legs static.
    upper = {"head", "neck", "torso", "upperArmL", "forearmL", "handL",
             "upperArmR", "forearmR", "handR"}
    key_a = {n["piece_id"]: (n["saved_x"], n["saved_y"], n["saved_rotation"]) for n in nodes}
    key_b = {}
    for n in nodes:
        x, y, r = key_a[n["piece_id"]]
        if n["piece_id"] in upper:
            y = y + 3
        if n["piece_id"] == "head":
            r = r + 2
        key_b[n["piece_id"]] = (x, y, r)
    total = 24  # 1 second at 24fps, A -> B
    mid = inbetween(key_a, key_b, 12, total)  # smoothstep(0.5) = 0.5 exactly
    end = inbetween(key_a, key_b, 24, total)
    assert mid["head"] == (key_a["head"][0], key_a["head"][1] + 1.5, 1.0), mid["head"]
    assert end["head"] == key_b["head"], end
    assert mid["shinL"] == key_a["shinL"], "legs must stay static in sit-idle"
    assert mid["pelvis"] == key_a["pelvis"]
    # Onion skin: frame 12 between keys 0 and 24 -> both neighbours at 0.35.
    ow = onion_weights(12, [0, 24, 48])
    assert ow == {0: 0.35, 24: 0.35}, ow
    # Ground gate, numeric only: lowest saved_y + piece height is unknown
    # from nodes.csv (no display size), so gate reports saved ground as
    # carried from locked pose (1410) vs stage ground 1475, NOT faked.
    ground = {"stage_ground_y": GROUND_Y, "locked_pose_bottom_carried": 1410,
              "planted_at_1475": False,
              "note": "Planting is a further drag in the widget, not a builder shift."}

    (OUT / "scene.cjstage.json").write_text(json.dumps(scene, indent=2), encoding="utf-8")
    (OUT / "harmony_check.js").write_text(export_harmony_check_script(nodes), encoding="utf-8")
    (OUT / "animation_keys.json").write_text(json.dumps({
        "fps": FPS, "key_a": "locked sitting pose", "key_b": "sit-idle bob +3px, head +2deg",
        "frames_A_to_B": total, "mid_frame_12_head": mid["head"],
        "end_frame_24_head": end["head"], "legs_static": True,
        "onion_weights_frame_12": ow,
    }, indent=2), encoding="utf-8")

    report = {
        "exit": 0, "nodes": len(nodes), "palette_colours": len(palette),
        "chains": chains, "roundtrip": rt, "ground": ground,
        "harmony_check_script_lines": len(export_harmony_check_script(nodes).splitlines()),
        "animation_test": "PASS: smoothstep mid = 0.5, end = key B, legs static, onion 0.35/0.35",
        "what_this_proves": "Own version loads, validates, inbetweens, and round-trips the sitting pose with numbers only, no Harmony installed.",
        "what_this_does_NOT_prove": "In-Harmony execution of harmony_check.js, .tpl/.plt export, and in-app rendering — those still need Harmony activation on Windows/Mac.",
    }
    (OUT / "test_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
