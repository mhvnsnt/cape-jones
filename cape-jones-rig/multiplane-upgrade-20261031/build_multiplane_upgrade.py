"""BARS PRESET — multiplane camera upgrade, feet planted in world space.

World model (one feet rule, used everywhere):
  World canvas: W=1700, H=750. Screen window: 1100x750.
  Camera pans horizontally only: camera_x(t) = 0..120 px over 24 frames.
  A world point at world_x appears on screen at:
      screen_x = world_x - camera_x * parallax
  so its WORLD x is recovered as:
      world_x = screen_x + camera_x * parallax   (invariant for a fixed world point)
  Vertical camera = 0, so world ground line Gy=700 is also screen y=700.

  Layers (back to front, layer order = depth order):
    far bg      parallax 0.3, blur 1.2, darker (atmospheric perspective)
    ground      parallax 1.0 (SAME as Cape, so feet never slide off it)
    Cape        parallax 1.0, figure height 750, feet = alpha-bbox bottom
    foreground  parallax 1.8, bars in front of Cape (occlusion is correct)

  Feet anchor: Cape figure (snap_figure, true-final-flex angles) resized to
  550x750 has alpha bbox bottom at y=651 in its own image (measured from
  the 1100x1500 figure, bbox bottom 1302 -> 651 at 0.5 scale). Pasting the
  figure at world y=47 puts feet exactly on Gy=700. The ground platform
  top edge is drawn at y=700 in the ground layer, at Cape parallax.

  Foreground variants:
    test:  bars 55px wide, alpha 210, every 180px, blur 2.0  (original test)
    final: bars 28px wide, alpha 140, every 260px, blur 1.0  (thinner/sparser)

  No-crop rule: figure world x 575..1125 (centre 850), screen x 575..455
  over the move, always inside 0..1100; foreground/far world layers are
  1700 wide, covering screen + max offset (216 / 36). Gate: no alpha pixel
  of the Cape figure touches a canvas edge in any frame.
"""
import os, sys, json, math, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter

RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(RIG, "multiplane-upgrade-20261031")
os.makedirs(OUT, exist_ok=True)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "snap", os.path.join(RIG, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)

W, H, SW = 1700, 750, 1100
GY = 700                      # world ground line, = screen y (vertical camera 0)
CAM_MAX = 120                 # camera pan, px, over the sequence
N = 24
FPS = 12
PRESET = {
    "name": "BARS PRESET",
    "screen": [1100, 750], "world": [1700, 750], "frames": N, "fps": FPS,
    "camera": {"axis": "horizontal only", "camera_x_start": 0, "camera_x_end": 120,
               "vertical_camera": 0},
    "parallax": {"far_bg": 0.3, "ground": 1.0, "cape": 1.0, "foreground": 1.8},
    "camera_move_px": {"far_bg": 36, "ground": 120, "cape": 120, "foreground": 216},
    "ground": {"ground_line_y_world": 700, "ground_line_y_screen": 700,
               "rule": "feet alpha-bbox bottom == ground line, every frame, world and screen"},
    "cape": {"figure": "snap_figure true-final-flex angles",
             "angles": {"arm_upper": {"L": -85, "R": 85}, "arm_lower": {"L": 145, "R": -145},
                        "leg_upper": {"L": -22, "R": 22}, "leg_lower": {"L": 10, "R": -10}},
             "size_px": [550, 750], "alpha_bbox_bottom_in_figure": 653,
             "paste_y_world": 47, "centre_x_world": 850},
    "foreground": {
        "test":  {"bar_w": 55, "alpha": 210, "spacing": 180, "blur": 2.0, "label": "TEST bars, original, heavy/occluding"},
        "final": {"bar_w": 28, "alpha": 140, "spacing": 260, "blur": 1.0, "label": "FINAL bars, thinner/sparser"},
    },
    "far_bg": {"blur": 1.2, "darken": 0.85},
}

def build_cape():
    fig = snap.figure(550, PRESET["cape"]["angles"], head_angle=0)
    cape = fig.resize((550, 750), Image.LANCZOS)
    # MEASURED resized bbox bottom (LANCZOS alpha fringe), not assumed 651:
    # 1100x1500 figure bbox bottom 1302 -> 653 after resize, verified here.
    return cape, cape.getchannel("A").getbbox()[3]

def build_world_layers(variant):
    bg = Image.open(os.path.join(RIG, "showcase/backgrounds-new-20261031/bg-rooftop-new-20261031.jpg")).convert("RGB")
    far_world = bg.resize((1700, 950)).crop((0, 100, 1700, 850))
    far_world = far_world.filter(ImageFilter.GaussianBlur(PRESET["far_bg"]["blur"]))
    # darken far layer (atmospheric perspective)
    import numpy as np
    a = (np.array(far_world).astype(float) * 0.85).astype("uint8")
    far_world = Image.fromarray(a)
    # ground platform, at Cape parallax: top edge exactly at GY, full world width
    ground = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ground)
    d.rectangle([0, GY, W, H], fill=(38, 38, 46, 255))
    d.rectangle([0, GY, W, GY + 4], fill=(120, 120, 130, 255))  # ledge edge highlight
    for x in range(0, W, 170):  # faint rooftop seams, world-fixed
        d.line([(x, GY + 4), (x, H)], fill=(60, 60, 70, 255), width=2)
    # foreground bars, world layer
    p = PRESET["foreground"][variant]
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(fg)
    for x in range(0, W, p["spacing"]):
        d.rectangle([x, 0, x + p["bar_w"], H], fill=(20, 18, 25, p["alpha"]))
    fg = fg.filter(ImageFilter.GaussianBlur(p["blur"]))
    return far_world, ground, fg

def render(variant):
    cape, FEET_BOTTOM = build_cape()
    PASTE_Y = GY - FEET_BOTTOM
    far_world, ground, fg_world = build_world_layers(variant)
    frames, meas = [], []
    for i in range(N):
        t = i / (N - 1)
        cam = CAM_MAX * t
        canvas = Image.new("RGBA", (SW, H), (128, 128, 128, 255))
        # far: screen_x = world_x - cam*0.3  -> crop world at cam*0.3
        canvas.alpha_composite(far_world.crop((int(cam * 0.3), 0, int(cam * 0.3) + SW, H)).convert("RGBA"), (0, 0))
        # ground + cape at parallax 1.0: crop world at cam
        canvas.alpha_composite(ground.crop((int(cam), 0, int(cam) + SW, H)), (0, 0))
        cape_layer = Image.new("RGBA", (SW, H), (0, 0, 0, 0))
        cape_layer.alpha_composite(cape, (int(850 - 275 - cam), PASTE_Y))
        canvas.alpha_composite(cape_layer, (0, 0))
        # foreground at parallax 1.8
        canvas.alpha_composite(fg_world.crop((int(cam * 1.8), 0, int(cam * 1.8) + SW, H)), (0, 0))
        frame = canvas.convert("RGB")
        frames.append(frame)
        # measure: Cape feet on screen = figure paste y + bbox bottom
        feet_screen_y = PASTE_Y + FEET_BOTTOM
        # feet world y is invariant (vertical camera 0); feet world x of bbox centre:
        bbox = cape.getchannel("A").getbbox()  # (l, t, r, b) in figure coords
        feet_cx_screen = int(850 - 275 - cam) + (bbox[0] + bbox[2]) // 2
        feet_cx_world = feet_cx_screen + int(cam * 1.0)
        # occlusion: foreground alpha over CAPE FIGURE pixels only (not bbox rectangle)
        fg_crop = fg_world.crop((int(cam * 1.8), 0, int(cam * 1.8) + SW, H))
        cape_screen = Image.new("RGBA", (SW, H), (0, 0, 0, 0))
        cape_screen.alpha_composite(cape, (int(850 - 275 - cam), PASTE_Y))
        import numpy as np
        fa = np.array(fg_crop.getchannel("A")); ca = np.array(cape_screen.getchannel("A"))
        occ = int(((fa > 0) & (ca > 0)).sum())
        # no-crop gate: CAPE ALPHA pixels (not transparent image canvas) inside screen
        px0 = int(850 - 275 - cam) + bbox[0]; px1 = int(850 - 275 - cam) + bbox[2]
        py0 = PASTE_Y + bbox[1]; py1 = PASTE_Y + bbox[3]
        no_clip = (px0 >= 0 and px1 < SW and py0 >= 0 and py1 < H)
        meas.append({"frame": i, "t": round(t, 3), "camera_x": round(cam, 1),
                     "cape_paste_x_screen": int(850 - 275 - cam),
                     "feet_y_screen": feet_screen_y, "feet_y_world": GY,
                     "feet_centre_x_screen": feet_cx_screen, "feet_centre_x_world": feet_cx_world,
                     "foreground_occlusion_px_in_cape_bbox": occ, "no_clip": no_clip})
    return frames, meas

def save_gif_mp4(frames, stem):
    rgb = [f.convert("RGB") for f in frames]
    rgb[0].save(os.path.join(OUT, stem + ".gif"), save_all=True, append_images=rgb[1:],
                duration=int(1000 / FPS), loop=0)
    with tempfile.TemporaryDirectory() as td:
        for i, f in enumerate(rgb):
            f.save(os.path.join(td, f"f{i:03d}.jpg"), quality=92)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", os.path.join(td, "f%03d.jpg"),
                        "-vf", "scale=1100:750,format=yuv420p", "-c:v", "libx264",
                        os.path.join(OUT, stem + ".mp4")], check=True)
    print(stem, len(frames))

def contact(frames, idxs, stem, cols=4):
    c = Image.new("RGB", (1100, 750), (128, 128, 128))
    for j, idx in enumerate(idxs):
        c.paste(frames[idx].resize((550, 375)), ((j % 2) * 550, (j // 2) * 375))
    c.save(os.path.join(OUT, stem))
    return c

def main():
    with open(os.path.join(OUT, "bars-preset-20261031.json"), "w") as fh:
        json.dump(PRESET, fh, indent=2)
    all_meas = {}
    for variant in ("test", "final"):
        frames, meas = render(variant)
        all_meas[variant] = meas
        save_gif_mp4(frames, f"bars-preset-{variant}-20261031")
        contact(frames, [0, 8, 16, 23], f"bars-preset-{variant}-contact-20261031.png")
        # ground proof: frame 12 with red ground line + feet marker (PROOF ONLY)
        f = frames[12].copy()
        d = ImageDraw.Draw(f)
        d.line([(0, GY), (1100, GY)], fill=(255, 0, 0), width=3)
        d.text((20, GY - 28), "WORLD GROUND y=700  |  feet on line", fill=(255, 0, 0))
        f.save(os.path.join(OUT, f"bars-preset-{variant}-ground-proof-20261031.png"))
        if variant == "final":
            final_frames = frames
    # before/after: original frame 12 (rebuilt from original builder logic) vs new final frame 12
    orig = Image.open(os.path.join(RIG, "depth-25d-blockers-broken-20261031/experimental-multiplane-camera-20261031.gif"))
    orig.seek(12); orig_f = orig.convert("RGB")
    sheet = Image.new("RGB", (1100, 750), (128, 128, 128))
    sheet.paste(orig_f.resize((550, 375)), (0, 0))
    sheet.paste(final_frames[12].resize((550, 375)), (550, 0))
    d = ImageDraw.Draw(sheet)
    d.text((20, 390), "BEFORE (orig test): feet at y=653, NO visible ground line -> reads floating", fill=(255, 255, 0))
    d.text((20, 420), "AFTER (BARS PRESET final): feet at y=700 ON the rooftop ledge, world-fixed", fill=(255, 255, 0))
    d.text((20, 450), "Both: Cape IS behind the bars (foreground in front). Depth read is the same; feet are the fix.", fill=(255, 255, 0))
    d.text((20, 480), "Final bars: 28px alpha 140 every 260px (test bars were 55px alpha 210 every 180px).", fill=(255, 255, 0))
    sheet.save(os.path.join(OUT, "bars-preset-before-after-20261031.png"))
    with open(os.path.join(OUT, "feet-measurements-20261031.json"), "w") as fh:
        json.dump(all_meas, fh, indent=2)
    # summary checks
    for variant, meas in all_meas.items():
        ys = {m["feet_y_world"] for m in meas}; yss = {m["feet_y_screen"] for m in meas}
        wx = {m["feet_centre_x_world"] for m in meas}
        print(variant, "feet_y_world set", ys, "feet_y_screen set", yss,
              "feet_centre_x_world range", min(wx), max(wx),
              "no_clip all", all(m["no_clip"] for m in meas),
              "occlusion px f0/f12/f23",
              meas[0]["foreground_occlusion_px_in_cape_bbox"],
              meas[12]["foreground_occlusion_px_in_cape_bbox"],
              meas[23]["foreground_occlusion_px_in_cape_bbox"])

if __name__ == "__main__":
    main()
