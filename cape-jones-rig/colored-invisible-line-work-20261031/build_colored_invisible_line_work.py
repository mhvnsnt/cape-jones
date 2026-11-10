"""Build COLORED INVISIBLE LINE WORK from existing CapeGP preset frames.

COLORED INVISIBLE LINE WORK (Mars, 2026-10-31 20:33 CDT) is a CapeGP
coloured outline-only state: coloured GP strokes, no fills, body invisible
except for its coloured outlines. It is a DIFFERENT invisible state from
the existing INVISIBLE LINE WORK (Silhouette Preset Pack Two, top row:
L1/L2/L3/L-depth/Sobel black-and-white lineart, invisibility powers).

What this script does, all in this folder, no existing file overwritten:
1. Reads capegp-presets-20261031/capegp_presets_frames.json (19 strokes
   per pose, traced outlines of existing v7c pieces, no new art).
2. Writes colored_invisible_line_work_frames.json: the same frames, with
   COLORED_INVISIBLE_LINE_WORK added as an alias of the NORMAL (apose)
   frame, plus a MODE note — the preset is a MODE, not a new pose: any
   source preset can be rendered in coloured-invisible mode.
3. Builds one single-preset .blend per source pose (6 blends, no
   multi-frame holdover) and renders each transparent, via Blender 5.2.3
   + xvfb-run (same as the CapeGP preset renders).
4. Composites each transparent render onto black (the "see him like
   that" view from the contact) and checks: alpha bbox, edge touch,
   stroke colour presence per layer colour, and that no fill exists
   (renders are strokes only by construction — GP fills are 0/1, not run).
5. Builds a contact sheet: default proof (apose, black) + all 6 mode
   variants + a distinction panel (existing black-and-white invisible
   lineart L3 vs new coloured outlines), and writes measurements JSON.

Usage:
  python3 build_colored_invisible_line_work.py
  python3 build_colored_invisible_line_work.py --source-preset FACE_SNAP
      (renders just that source pose in coloured-invisible mode)
"""
import json, os, subprocess, sys
from PIL import Image as P, ImageDraw as D

HERE = os.path.dirname(os.path.abspath(__file__))
RIG = os.path.expanduser("~/workspace/cape-jones-rig")
SRC = os.path.join(RIG, "capegp-presets-20261031", "capegp_presets_frames.json")
BL = os.path.expanduser("~/workspace/tools-industry/blender-5.2.3-linux-x64/blender")
LAYERS = ["FaceSnapArm", "Head", "CowlUpperArm", "Neck", "ChestSnapArm",
          "Torso", "Collar", "NormalArm", "Legs", "CapeBack"]
# RGBA 0-255 versions of the GP material colours in build_capegp.py.
COLOURS = {"FaceSnapArm": (255, 102, 51, 255), "Head": (140, 51, 179, 255),
           "CowlUpperArm": (255, 204, 51, 255), "Neck": (242, 179, 128, 255),
           "ChestSnapArm": (51, 204, 255, 255), "Torso": (230, 230, 242, 255),
           "Collar": (26, 26, 38, 255), "NormalArm": (217, 217, 230, 255),
           "Legs": (204, 217, 242, 255), "CapeBack": (38, 31, 51, 255)}
ORDER = ["NORMAL", "APOSE_FLEX", "FACE_SNAP", "COWL_SNAP", "CHEST_SNAP", "JOINT_SMOOTH"]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit(f"FAILED: {' '.join(cmd)}")
    return r.stdout

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-preset", default=None)
    args = ap.parse_args()
    presets = [args.source_preset] if args.source_preset else ORDER
    with open(SRC) as f:
        frames = json.load(f)
    # 1-2. Preset frames file: source frames + named default preset.
    out_frames = dict(frames)
    out_frames["COLORED_INVISIBLE_LINE_WORK"] = frames["NORMAL"]
    out_frames["_MODE"] = ("MODE, not a pose: render any source preset with "
                           "coloured GP strokes only, no fills, transparent "
                           "background. Default source pose = NORMAL (apose).")
    frames_path = os.path.join(HERE, "colored_invisible_line_work_frames.json")
    with open(frames_path, "w") as f:
        json.dump(out_frames, f)
    meas = {"preset": "COLORED_INVISIBLE_LINE_WORK", "default_source": "NORMAL",
            "mode": "coloured GP strokes only, no fills, transparent background",
            "layers": LAYERS, "colours_rgba": COLOURS, "variants": {}}
    for name in presets:
        blend = os.path.join(HERE, "blends", f"colored-invisible-{name}.blend")
        run(["xvfb-run", "-a", BL, "-b", "--python",
             os.path.join(HERE, "blender_build.py"), "--",
             "--frames", frames_path, "--preset", name, blend])
        trans = os.path.join(HERE, "variants", f"colored-invisible-{name}-transparent.png")
        run(["xvfb-run", "-a", BL, "-b", "--python",
             os.path.join(HERE, "blender_render.py"), "--",
             "--blend", blend, "--out", trans])
        im = P.open(trans).convert("RGBA")
        black = P.new("RGBA", im.size, (0, 0, 0, 255))
        black.alpha_composite(im)
        black_path = os.path.join(HERE, "variants", f"colored-invisible-{name}-on-black.png")
        black.save(black_path)
        alpha = im.split()[3]
        bbox = alpha.getbbox()
        # Edge touch: any opaque alpha on the outermost row/column.
        import numpy as np
        a = np.array(alpha)
        edge = int(((a[0] > 10).sum() + (a[-1] > 10).sum() +
                    (a[:, 0] > 10).sum() + (a[:, -1] > 10).sum()))
        # Colour presence: count pixels near each layer colour (tolerance 40).
        arr = np.array(im.convert("RGB")).astype(int)
        amask = a > 10
        present = {}
        for layer, c in COLOURS.items():
            d = (abs(arr[:, :, 0] - c[0]) + abs(arr[:, :, 1] - c[1]) +
                 abs(arr[:, :, 2] - c[2]))
            present[layer] = int(((d < 120) & amask).sum())
        meas["variants"][name] = {
            "strokes": {k: len(v) for k, v in frames[name].items() if v},
            "total_strokes": sum(len(v) for v in frames[name].values()),
            "render_size": list(im.size), "alpha_bbox": list(bbox) if bbox else None,
            "alpha_px": int(amask.sum()), "edge_touch_px": edge,
            "colour_px_near_layer_colour": present,
            "blend": os.path.basename(blend), "transparent": os.path.basename(trans),
            "on_black": os.path.basename(black_path)}
        print(name, "strokes", meas["variants"][name]["total_strokes"],
              "alpha_px", meas["variants"][name]["alpha_px"], "edge", edge)
    # Contact: default proof large on top, 6 variants below, distinction strip.
    def tile(path, w, h):
        im = P.open(path).convert("RGBA")
        bg = P.new("RGBA", (w, h), (0, 0, 0, 255))
        im.thumbnail((w, h))
        bg.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
        return bg
    W, H = 1650, 1100
    contact = P.new("RGBA", (W, H), (20, 20, 20, 255))
    dr = D.Draw(contact)
    dr.text((10, 5), "COLORED INVISIBLE LINE WORK — default: NORMAL (apose), on black",
            fill=(255, 255, 0))
    contact.paste(tile(os.path.join(HERE, "variants", "colored-invisible-NORMAL-on-black.png"), 550, 700), (550, 30))
    # Existing invisible linework, for distinction, shrunk into the top-left.
    l3 = os.path.join(RIG, "drawing-masters-upgrade-20261031", "effects",
                      "LINEART-INVISIBLE-L3-visible-3px-a180.png")
    if os.path.exists(l3):
        contact.paste(tile(l3, 520, 700), (10, 30))
        dr.text((10, 735), "LEFT: EXISTING invisible line work (Pack Two top row, B/W lineart)",
                fill=(255, 255, 255))
    dr.text((560, 735), "CENTRE: NEW Colored Invisible Line Work (CapeGP, coloured strokes, no fills)",
            fill=(255, 255, 255))
    # 6 variants in a row at the bottom.
    y0 = 780
    for i, name in enumerate(ORDER):
        x = 10 + i * 272
        contact.paste(tile(os.path.join(HERE, "variants", f"colored-invisible-{name}-on-black.png"), 262, 300), (x, y0))
        dr.text((x, y0 + 305), name, fill=(255, 255, 255))
    contact.convert("RGB").save(os.path.join(HERE, "colored-invisible-line-work-contact-20261031.png"))
    # Default proof copy at the folder root for easy showing.
    P.open(os.path.join(HERE, "variants", "colored-invisible-NORMAL-on-black.png")).save(
        os.path.join(HERE, "colored-invisible-line-work-default-proof-20261031.png"))
    with open(os.path.join(HERE, "measurements-20261031.json"), "w") as f:
        json.dump(meas, f, indent=2)
    print("DONE", frames_path)

if __name__ == "__main__":
    main()
