"""Afterglow from SOFT RIM only. Soft rim = soft halo, ONE layer (v3: cyan (0,200,255), dilate 6, blur 5, factor 0.60).
Motion-only: trail = soft bands of PREVIOUS positions only, fading. Current plate carries NO rim.
At rest (hold frames) the trail decays to zero -> no afterglow visible."""
from PIL import Image, ImageFilter, ImageOps
import numpy as np, os
OUT = os.path.expanduser("~/workspace/cape-jones-rig/afterglow-20261031")
plate = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png")).convert("RGBA")
# scale to 300px tall
w,h = plate.size; nw = int(w*300/h); plate = plate.resize((nw,300), Image.LANCZOS)
W,H = 640,360
BG = (18,18,28,255)
CYAN = (0,200,255)
def soft_band(alpha_img, dilate=6, blur=5):
    d = alpha_img.filter(ImageFilter.MaxFilter(dilate*2+1)).filter(ImageFilter.GaussianBlur(blur))
    band = np.array(d, dtype=np.int16) - np.array(alpha_img, dtype=np.int16)
    band = np.clip(band, 0, 255).astype(np.uint8)
    return Image.fromarray(band, "L")
# motion: x 60 -> 60+11*24=324, y centre-ish (figure top at 30)
xs = [60 + i*24 for i in range(12)]
positions = xs + [xs[-1]]*6   # 6 hold frames at rest, trail fades to zero
TRAIL = [0.50, 0.40, 0.30, 0.20, 0.12, 0.06]  # 1 frame ago .. 6 frames ago
frames = []
for fi, x in enumerate(positions):
    canvas = Image.new("RGBA",(W,H),BG)
    # trails first (behind plate)
    for lag, f in enumerate(TRAIL, start=1):
        if fi-lag < 0: continue
        px = positions[fi-lag]
        if px == x:  # at rest, same position = no new trail; past trail still drawn but decays via hold logic below
            pass
        a = plate.split()[3]
        band = soft_band(a)
        glow = Image.new("RGBA",(nw,300),(CYAN[0],CYAN[1],CYAN[2],0))
        glow.putalpha(band.point(lambda v: int(v*f)))
        canvas.alpha_composite(glow,(px,30))
    # hold-frame decay: on hold frames, trail factors shrink by 0.5 per hold frame is NOT applied above;
    # instead: redraw correctly -- simpler: if holding, scale all trail alphas by (0.5 ** hold_index)
    if fi >= 12:
        # rebuild canvas with decayed trails
        canvas = Image.new("RGBA",(W,H),BG)
        decay = 0.5 ** (fi-11)   # hold1:0.5, hold2:0.25 ... hold6: ~0.016 -> visually zero
        for lag, f in enumerate(TRAIL, start=1):
            if fi-lag < 0: continue
            px = positions[fi-lag]
            a = plate.split()[3]
            band = soft_band(a)
            glow = Image.new("RGBA",(nw,300),(CYAN[0],CYAN[1],CYAN[2],0))
            glow.putalpha(band.point(lambda v: int(v*f*decay)))
            canvas.alpha_composite(glow,(px,30))
    canvas.alpha_composite(plate,(x,30))
    frames.append(canvas.convert("RGB"))
frames[0].save(f"{OUT}/afterglow-soft-rim-motion-20261031.gif", save_all=True, append_images=frames[1:], duration=90, loop=0)
frames[-1].save(f"{OUT}/afterglow-at-rest-final-frame-20261031.png")
# contact sheet: moving frame 6, moving frame 12, final rest frame
sheet = Image.new("RGB",(640*3+20,360+40),(255,255,255))
for i,idx in enumerate([5,11,17]):
    sheet.paste(frames[idx],(i*650,20))
sheet.save(f"{OUT}/afterglow-proof-contact-20261031.png")
print("frames",len(frames),"plate",plate.size)
print("trail factors",TRAIL,"hold decay 0.5^n per hold frame; final frame trail max =", 0.50*(0.5**6))
