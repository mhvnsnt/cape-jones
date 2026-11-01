#!/usr/bin/env python3
"""COMBINED PIPELINE — Tools 1+2+3 merged, Tools 4+5 as provenance checks.
For each piece: Tool 1 (shape) + Tool 2 (colour/proportion) propose a
template; if they AGREE, confidence is high; if they DISAGREE, the piece
goes to Mars's eye as low-confidence/needs-eye. Tool 3 turns the winning
template into a canonical name + warnings (CLEAN/GRAFTED traps, folder
mismatch, Front/Back limb trap). Reject: no opaque pixels, or a GRAFTED
winner, or a piece whose alpha bbox is a full sheet (not a piece).
Usage: label_pieces.py <piece1.png> [piece2.png ...] --out <dir>
Outputs in <dir>: proposals.json, contact sheets, mars_corrections.txt
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(__file__))
from tool1_opencv_match import match as shape_match
from tool2_embedding_knn import classify as knn_classify
from tool3_naming_schema import canonical
from PIL import Image, ImageDraw, ImageFont

def propose(path):
    s = shape_match(path)
    k = knn_classify(path)
    agree = s.get("best") == k.get("best")
    winner = s["best"] if agree else s["best"]  # shape breaks ties, stated
    conf = min(1.0, (s.get("confidence", 0) + k.get("confidence", 0)) / 2 + (0.2 if agree else -0.2))
    conf = max(0.05, min(0.95, round(conf, 2)))
    # Honesty rule (fixed 2026-10-31 after eye-checking sheets 1-2: disagreeing
    # pairs scored MEDIUM but were mostly wrong): disagree = NEEDS-MARS-EYE.
    band = "HIGH" if agree and conf >= 0.8 else ("MEDIUM" if agree else "NEEDS-MARS-EYE")
    folder = os.path.basename(os.path.dirname(path))
    can = canonical(winner or "", folder)
    status = "proposed"
    if s.get("best") is None:
        status, band = "reject", "REJECT"
    elif "REJECT" in can["canonical"]:
        status, band = "reject", "REJECT"
    return {"piece": path, "piece_id": os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path),
            "folder": folder, "tool1_shape": s, "tool2_knn": k, "agree": agree,
            "proposed_template": winner, "canonical": can["canonical"],
            "description": can["description"], "warnings": can["warnings"],
            "confidence": conf, "band": band, "status": status}

def contact_sheets(proposals, outdir, per_sheet=10):
    from PIL import Image
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font, small = ImageFont.load_default(), ImageFont.load_default()
    sheets = []
    for si in range(0, len(proposals), per_sheet):
        chunk = proposals[si:si + per_sheet]
        W, cell = 1600, 320
        rows = (len(chunk) + 4) // 5
        sheet = Image.new("RGB", (W, 60 + rows * cell), (128, 128, 128))
        d = ImageDraw.Draw(sheet)
        d.text((20, 15), f"PIECE LABELLING — sheet {si // per_sheet + 1} — labels on SHEET ONLY, never baked into pieces", fill=(255, 255, 255), font=font)
        for i, p in enumerate(chunk):
            x, y = (i % 5) * cell + 10, 60 + (i // 5) * cell + 10
            try:
                im = Image.open(p["piece"]).convert("RGBA")
                im.thumbnail((300, 240))
                bg = Image.new("RGBA", (300, 240), (128, 128, 128, 255))
                bg.alpha_composite(im, ((300 - im.width) // 2, (240 - im.height) // 2))
                sheet.paste(bg.convert("RGB"), (x, y))
            except Exception as e:
                d.text((x, y), f"unreadable: {e}", fill=(255, 0, 0), font=small)
            label = f"{p['piece_id']}\n-> {p['canonical']}\n{p['band']} conf {p['confidence']} agree={p['agree']}"
            d.multiline_text((x, y + 245), label, fill=(255, 255, 255), font=small)
        fn = os.path.join(outdir, f"contact-sheet-{si // per_sheet + 1:02d}-20261031.png")
        sheet.save(fn)
        sheets.append(fn)
    return sheets

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pieces", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    props = [propose(p) for p in a.pieces]
    sheets = contact_sheets(props, a.out)
    with open(os.path.join(a.out, "proposals.json"), "w") as f:
        json.dump({"count": len(props), "sheets": sheets, "proposals": props}, f, indent=2)
    with open(os.path.join(a.out, "mars_corrections.txt"), "w") as f:
        f.write("# MARS EYE CORRECTIONS — edit ONLY the right-hand side, one line per piece.\n"
                "# Format: piece_id = canonical_name | status\n"
                "# status: keep | rename | reject | good\n"
                "# Example: fla-front/Row1_1.png = capejones_hand_open_front | keep\n"
                "# Lines starting with # are ignored. Do not edit the piece_id.\n")
        for p in props:
            f.write(f"{p['piece_id']} = {p['canonical']} | keep\n")
    n_high = sum(1 for p in props if p["band"] == "HIGH")
    n_med = sum(1 for p in props if p["band"] == "MEDIUM")
    n_eye = sum(1 for p in props if p["band"] == "NEEDS-MARS-EYE")
    n_rej = sum(1 for p in props if p["status"] == "reject")
    print(json.dumps({"total": len(props), "high": n_high, "medium": n_med,
                      "needs_mars_eye": n_eye, "reject": n_rej, "sheets": sheets}, indent=2))

if __name__ == "__main__":
    main()
