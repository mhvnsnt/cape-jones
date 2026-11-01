"""Honesty fix, 2026-10-31: the first banding let a disagreeing pair score
MEDIUM. Eye-checking sheets 1-2 showed most MEDIUM proposals were wrong
(foot -> cape_collar, torso -> hand_fist, head -> pelvis). Correct rule:
agree + conf>=0.8 = HIGH; agree only = MEDIUM; disagree = NEEDS-MARS-EYE.
This script re-bands proposals.json and regenerates contact sheets
(4 columns, wrapped labels, no truncation) without re-running the tools."""
import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont
OUT = "batch-60-20261031"
d = json.load(open(os.path.join(OUT, "proposals.json")))
for p in d["proposals"]:
    if p["status"] == "reject":
        p["band"] = "REJECT"
    elif p["agree"] and p["confidence"] >= 0.8:
        p["band"] = "HIGH"
    elif p["agree"]:
        p["band"] = "MEDIUM"
    else:
        p["band"] = "NEEDS-MARS-EYE"
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
except Exception:
    font = small = ImageFont.load_default()
sheets = []
per, cols, W, cell = 8, 4, 1600, 400
for si in range(0, len(d["proposals"]), per):
    chunk = d["proposals"][si:si+per]
    rows = (len(chunk) + cols - 1)//cols
    sheet = Image.new("RGB", (W, 50 + rows*cell), (128,128,128))
    dr = ImageDraw.Draw(sheet)
    dr.text((20,12), f"PIECE LABELLING — sheet {si//per+1} — labels on SHEET ONLY, never baked into pieces", fill=(255,255,255), font=font)
    for i,p in enumerate(chunk):
        x, y = (i%cols)*cell+10, 50+(i//cols)*cell+10
        try:
            im = Image.open(p["piece"]).convert("RGBA"); im.thumbnail((360,250))
            bg = Image.new("RGBA",(360,250),(128,128,128,255)); bg.alpha_composite(im,((360-im.width)//2,(250-im.height)//2))
            sheet.paste(bg.convert("RGB"),(x,y))
        except Exception as e:
            dr.text((x,y), f"unreadable {e}", fill=(255,0,0), font=small)
        txt = "\n".join(textwrap.wrap(p["piece_id"], 38) + textwrap.wrap("-> "+p["canonical"], 38) + [f"{p['band']} conf {p['confidence']} agree={p['agree']}"])
        dr.multiline_text((x, y+255), txt, fill=(255,255,255), font=small)
    fn = os.path.join(OUT, f"contact-sheet-{si//per+1:02d}-20261031.png"); sheet.save(fn); sheets.append(fn)
d["sheets"] = sheets
json.dump(d, open(os.path.join(OUT,"proposals.json"),"w"), indent=2)
with open(os.path.join(OUT,"mars_corrections.txt"),"w") as f:
    f.write("# MARS EYE CORRECTIONS — edit ONLY the right-hand side, one line per piece.\n# Format: piece_id = canonical_name | status\n# status: keep | rename | reject | good\n# Lines starting with # are ignored. Do not edit the piece_id.\n")
    for p in d["proposals"]:
        f.write(f"{p['piece_id']} = {p['canonical']} | keep\n")
import collections
print(json.dumps({"total": len(d["proposals"]), **dict(collections.Counter(p["band"] for p in d["proposals"])), "agree": sum(p["agree"] for p in d["proposals"]), "sheets": sheets}, indent=2))
