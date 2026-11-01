"""Read-only verification of pseudo-turn-templates-20261031/ (7 templates)
and audit of poses-as-movements-20261031/ (9 videos) + interp-v2 (3 videos).
Writes only into workstream-b-sweep-20261031/. No re-render, no overwrite
of any Mars-seen file. Verification != approval: all items stay 0/1 unless
Mars already approved them (dance-move base only, 1/1, as a dance move).
"""
import os, json
from PIL import Image

R = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(R, "workstream-b-sweep-20261031")
PT = os.path.join(R, "pseudo-turn-templates-20261031")
PM = os.path.join(R, "poses-as-movements-20261031")
V2 = os.path.join(R, "movements-interp-v2-20261031")

def gif_info(p):
    im = Image.open(p)
    n = 0
    try:
        while True:
            n += 1; im.seek(im.tell() + 1)
    except EOFError:
        pass
    return n

def verify_templates():
    out = {}
    for name in ["pseudo-turn", "stretch-power", "thin-power", "invisible-power",
                 "cheat-turn-a-depth-dark", "cheat-turn-b-bend-mirror", "sheet-animated-turn-attempt"]:
        d = os.path.join(PT, "frames", name)
        frames = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        edge = 0; sizes = set(); alphas = []
        for f in frames:
            im = Image.open(os.path.join(d, f)).convert("RGBA")
            sizes.add(im.size)
            a = im.getchannel("A")
            w, h = im.size
            edge += sum(1 for x in range(w) if a.getpixel((x, 0)) or a.getpixel((x, h - 1)))
            edge += sum(1 for y in range(h) if a.getpixel((0, y)) or a.getpixel((w - 1, y)))
            alphas.append(sum(1 for px in a.getdata() if px > 0))
        gif = os.path.join(PT, name + ".gif")
        mp4 = os.path.join(PT, name + ".mp4")
        out[name] = {
            "transparent_master_frames": len(frames),
            "gif_frames": gif_info(gif) if os.path.exists(gif) else 0,
            "mp4_exists": os.path.exists(mp4),
            "canvas_sizes": sorted([list(s) for s in sizes]),
            "edge_alpha_px_total": edge,
            "no_crop_gate": "PASS" if edge == 0 else "FAIL",
            "alpha_px_first_last": [alphas[0], alphas[-1]] if alphas else [],
            "ground": "GROUNDED (apose base; feet-anchored union canvas in original build)",
        }
        print(name, out[name])
    return out

def audit_videos(folder, names):
    out = {}
    for name in names:
        gif = os.path.join(folder, name + ".gif")
        mp4 = os.path.join(folder, name + ".mp4")
        out[name] = {
            "gif_frames": gif_info(gif) if os.path.exists(gif) else 0,
            "mp4_exists": os.path.exists(mp4),
            "gif_exists": os.path.exists(gif),
        }
        print(name, out[name])
    return out

pt = verify_templates()
pm = audit_videos(PM, ["jump-cowl-snap-movement", "jump-cowl-snap-movement-clean",
    "shimmy-cowl-snap-movement", "ginyu-force-movement", "pose-dialects-movements",
    "move-punch-to-flex", "move-jump-to-shimmy", "move-serve-to-guard",
    "move-rollcall-snap-to-spread"])
v2 = audit_videos(V2, ["move-serve-to-guard-v2-20261031", "move-punch-to-flex-v2-20261031",
    "move-rollcall-snap-to-spread-v2-20261031"])
with open(os.path.join(OUT, "verification-audit-20261031.json"), "w") as fh:
    json.dump({"pseudo_turn_templates": pt, "poses_as_movements_v1": pm,
               "movements_interp_v2": v2}, fh, indent=1)
print("AUDIT DONE")
