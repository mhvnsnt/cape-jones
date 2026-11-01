"""Default afterglow preset applied to running + flying.
Preset (approved 2026-10-31 17:49 CDT): soft rim = soft halo, ONE layer.
Cyan (0,200,255), dilate 6, blur 5, lag 6 past positions,
fade 0.50/0.40/0.30/0.20/0.12/0.06, hold decay 0.5^n per hold frame -> zero at rest.
Trail = soft bands of PREVIOUS positions only, behind plate, never over figure.
Current plate carries NO rim in these tests, so only the trail glows.
Plates: walk/flying clean frames are RGB on grey-128; grey-128 keyed to transparent.
Honest note: running test RETIMES the walk cycle as a run (faster step + bounce),
it is not a newly built run cycle. Flying test cycles the flying frames diagonally.
"""
from PIL import Image, ImageFilter
import numpy as np, os, json
BASE = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.expanduser("~/workspace/cape-jones-rig/afterglow-preset-20261031")
CYAN = (0, 200, 255)
TRAIL = [0.50, 0.40, 0.30, 0.20, 0.12, 0.06]
W, H = 640, 360
BG = (18, 18, 28, 255)

def load_plate(path):
    im = Image.open(path).convert("RGB")
    arr = np.array(im)
    # grey-128 key-out
    mask = ~((arr[:, :, 0] == 128) & (arr[:, :, 1] == 128) & (arr[:, :, 2] == 128))
    rgba = np.dstack([arr, (mask.astype(np.uint8) * 255)])
    im = Image.fromarray(rgba, "RGBA")
    w, h = im.size
    nw = int(w * 300 / h)
    return im.resize((nw, 300), Image.LANCZOS)

def soft_band(alpha_img, dilate=6, blur=5):
    d = alpha_img.filter(ImageFilter.MaxFilter(dilate * 2 + 1)).filter(ImageFilter.GaussianBlur(blur))
    band = np.clip(np.array(d, dtype=np.int16) - np.array(alpha_img, dtype=np.int16), 0, 255).astype(np.uint8)
    return Image.fromarray(band, "L")

def render(name, frame_paths, positions):
    plates = [load_plate(p) for p in frame_paths]
    nw = plates[0].size[0]
    frames = []
    for fi, (x, y) in enumerate(positions):
        canvas = Image.new("RGBA", (W, H), BG)
        decay = 1.0
        if fi >= 12:
            decay = 0.5 ** (fi - 11)
        for lag, f in enumerate(TRAIL, start=1):
            if fi - lag < 0:
                continue
            px, py = positions[fi - lag]
            band = soft_band(plates[(fi - lag) % len(plates)].split()[3])
            glow = Image.new("RGBA", (nw, 300), (CYAN[0], CYAN[1], CYAN[2], 0))
            glow.putalpha(band.point(lambda v, f=f, d=decay: int(v * f * d)))
            canvas.alpha_composite(glow, (px, py))
        canvas.alpha_composite(plates[fi % len(plates)], (x, y))
        frames.append(canvas.convert("RGB"))
    frames[0].save(f"{OUT}/{name}-20261031.gif", save_all=True, append_images=frames[1:], duration=90, loop=0)
    sheet = Image.new("RGB", (640 * 3 + 20, 360 + 40), (255, 255, 255))
    for i, idx in enumerate([5, 11, 17]):
        sheet.paste(frames[idx], (i * 650, 20))
    sheet.save(f"{OUT}/{name}-proof-contact-20261031.png")
    frames[-1].save(f"{OUT}/{name}-at-rest-20261031.png")
    print(name, len(frames), "plate", plates[0].size)

walk = [f"{BASE}/clips-v7c-clean-20261031/walk/walk-{n}-v7c-clean.png"
        for n in ["01-contact", "13-passing", "25-contact", "37-passing"]]
# running: 12 moving frames, 36px/frame, bounce 30/22, then 6 holds
run_pos = [(40 + i * 36, 30 if i % 2 == 0 else 22) for i in range(12)] + [(40 + 11 * 36, 30)] * 6
render("running-afterglow", walk, run_pos)

fly = [f"{BASE}/clips-v7c-clean-20261031/flying/flying-{n}-v7c-clean.png"
       for n in ["01-hover", "13-soar", "25-dive", "37-hover"]]
# flying: diagonal up-right, 28px x / -6px y per frame, then 6 holds
fly_pos = [(40 + i * 28, 90 - i * 6) for i in range(12)] + [(40 + 11 * 28, 90 - 11 * 6)] * 6
render("flying-afterglow", fly, fly_pos)
print("done")
