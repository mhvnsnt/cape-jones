"""Build cj-dance-proof-3d-v4-sheet.png from verified stills."""
from PIL import Image, ImageDraw, ImageFont
import os

B = "/home/hatch/workspace/_cj_v4_build"
OUT = "/home/hatch/workspace/your_files/cape-jones-dance-proof/cj-dance-proof-3d-v4-sheet.png"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    FONTS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception:
    FONT = ImageFont.load_default(); FONTS = FONT

def load(p):
    return Image.open(os.path.join(B, p)).convert("RGB")

def panel(img, w, label):
    # fit into w x (w*9/16) box, center-cropping overflow -> clean grid
    th = int(w * 9 / 16)
    r = max(w / img.width, th / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1))
    x = (img.width - w) // 2; y = (img.height - th) // 2
    img = img.crop((x, y, x + w, y + th))
    bar = Image.new("RGB", (w, 34), (20, 20, 28))
    d = ImageDraw.Draw(bar)
    d.text((8, 5), label, font=FONTS, fill=(255, 255, 120))
    out = Image.new("RGB", (w, th + 34), (0, 0, 0))
    out.paste(bar, (0, 0)); out.paste(img, (0, 34))
    return out

def crop(img, box, w, label):
    c = img.crop(box)
    return panel(c, w, label)

W3 = 620
rows = []
# row 1: loop phases (front)
r1 = [panel(load("stills/s_f9.png"), W3, "loop f9 - arms down, fingers open"),
      panel(load("stills/s_f33.png"), W3, "loop f33 - bounce, arm raised"),
      panel(load("check/zoom_f49.png"), W3, "loop f49 - deep squat, arms out")]
# row 2: world cycle sections
r2 = [panel(load("check/v4_magenta417.png"), W3, "section 2 - LED magenta (hflip)"),
      panel(load("check/v4_cyan801.png"), W3, "section 3 - LED cyan"),
      panel(load("check/v4_night1185.png"), W3, "section 4 - night (hflip)")]
# row 3: zooms
f33 = load("stills/s_f33.png"); f57 = load("stills/s_f57.png")
z1 = crop(f33, (270, 110, 560, 320), W3, "ZOOM shoulder+elbow: arm leaves T-pose, elbow bent")
z2 = crop(f33, (285, 125, 485, 305), W3, "ZOOM hand: fingers spread, wrist turned")
z3 = panel(load("stills/s_back33.png"), W3, "back: cape ONE solid piece, no holes/slits")
rows = [r1, r2, [z1, z2, z3],
        [crop(load("check/zoom_f49.png"), (330, 300, 620, 540), W3, "ZOOM hem + between legs: one piece"),
         panel(load("stills/s_back57.png"), W3, "back f57: cape sweeps as one sheet"),
         panel(load("stills/s_f81.png"), W3, "loop f81 - late loop phase")]]
H = sum(max(p.height for p in r) for r in rows) + 70
sheet = Image.new("RGB", (W3 * 3 + 8, H), (12, 12, 16))
d = ImageDraw.Draw(sheet)
d.text((10, 8), "CAPE JONES 3D DANCE v4 - Rigify auto-IK rig + CMU 15_04 mocap loop (no hand-keyed motion)", font=FONT, fill=(255, 255, 255))
d.text((10, 40), "v3 stiffness fix: elbows/knees/spine/neck/head/fingers measured in README - cape one solid piece in every zoom", font=FONTS, fill=(180, 220, 255))
y = 70
for r in rows:
    x = 0
    rh = max(p.height for p in r)
    for p in r:
        sheet.paste(p, (x, y)); x += p.width + 4
    y += rh + 4
sheet.save(OUT)
print("SHEET", OUT, sheet.size, os.path.getsize(OUT))
