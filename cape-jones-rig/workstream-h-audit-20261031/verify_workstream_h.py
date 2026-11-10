"""Workstream H audit verifier — recomputes counts from disk, no files overwritten."""
import json, glob
from pathlib import Path
from PIL import Image
R = Path(__file__).resolve().parent.parent
out = {}
# PLY vertices
for p in sorted(R.glob("gaussian-splatting-20261031/*.ply")) + sorted(R.glob("gaussian-splatting-upgrade-20261031/8BIT-V*/*.ply")):
    for line in open(p, 'rb'):
        s = line.decode('utf-8','ignore').strip()
        if s.startswith("element vertex"): out[str(p.relative_to(R))] = int(s.split()[-1])
        if s == "end_header": break
# CapeGP strokes
d = json.load(open(R/"capegp-presets-20261031/capegp_presets_frames.json"))
out["capegp_strokes"] = {k: sum(len(v) for v in val.values()) for k, val in d.items()}
out["capegp_total_strokes"] = sum(out["capegp_strokes"].values())
# GIF frames
for f in ["gaussian-splatting-20261031/splat-turn-sequence-20261031.gif",
          "gaussian-splatting-upgrade-20261031/8BIT-V2/8bit-V2-turn-sequence-20261031.gif",
          "gaussian-splatting-upgrade-20261031/8BIT-V3/8bit-V3-turn-sequence-20261031.gif",
          "gaussian-splatting-upgrade-20261031/8BIT-V4/8bit-V4-turn-sequence-20261031.gif",
          "invisible-power-v1-nocrop-fix-20261031/invisible-power-v1-NOCROP-FIXED-20261031.gif"]:
    out[f] = Image.open(R/f).n_frames
out["invisible_fixed_masters"] = len(list((R/"invisible-power-v1-nocrop-fix-20261031/frames").glob("*.png")))
out["invisible_draft_masters"] = len(list((R/"invisible-power-v1-nocrop-fix-20261031/draft/frames").glob("*.png")))
out["pack_two_effects"] = sorted(p.name for p in (R/"drawing-masters-upgrade-20261031/effects").glob("*.png"))
out["colored_variants"] = len(list((R/"colored-invisible-line-work-20261031/variants").glob("*.png")))
out["colored_blends"] = len(list((R/"colored-invisible-line-work-20261031/blends").glob("*.blend")))
out["capegp_single_blends"] = len(list((R/"capegp-presets-20261031").glob("single-*.blend")))
out["capegp_proofs"] = len(list((R/"capegp-presets-20261031").glob("preset-000*.png")))
out["methods"] = len(list((R/"gaussian-splatting-upgrade-20261031/methods").glob("method-*.png")))
print(json.dumps(out, indent=1))
(Path(__file__).resolve().parent/"counts-20261031.json").write_text(json.dumps(out, indent=1))
