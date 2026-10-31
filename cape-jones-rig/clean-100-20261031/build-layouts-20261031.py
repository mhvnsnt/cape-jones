from PIL import Image, ImageFilter, ImageDraw
import numpy as np, os

OUT = os.path.expanduser("~/workspace/cape-jones-rig/clean-100-20261031/layouts")
SRC = {
 "flying": "media-generation-bg-flying-painted-20261031-0-181dd433-b06d-41d2-adc0-f0f5c36dd955.jpg",
 "rooftop": "media-generation-bg-rooftop-painted-20261031-0-0855924d-a2fc-43cb-9d66-4229f31290c2.jpg",
 "alley": "media-generation-bg-alley-painted-20261031-0-c33c7256-e1cb-44dd-bc82-272326eeb87d.jpg",
 "desk": "media-generation-bg-desk-painted-20261031-0-fbb8591c-b500-47d6-95b8-57aab6d4828f.jpg",
}
W, H = 1168, 784

def to_bg(path, zoom=1.0):
    im = Image.open(os.path.join(OUT, path)).convert("RGB")
    if zoom != 1.0:
        w, h = im.size
        nw, nh = int(w * zoom), int(h * zoom)
        x, y = (w - nw) // 2, (h - nh) // 2
        im = im.crop((x, y, x + nw, y + nh))
    target = W / H
    w, h = im.size
    if w / h > target:
        nw = int(h * target); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / target); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    return im.resize((W, H), Image.LANCZOS)

bgs = {}
for k, src in SRC.items():
    bg = to_bg(src, zoom=0.92 if k == "desk" else 1.0)
    bg.save(os.path.join(OUT, f"bg-{k}-painted-20261031.jpg"), quality=92)
    bgs[k] = bg
    print(k, "bg saved", bg.size)

apose = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png")).convert("RGBA")
print("apose", apose.size, "alpha bbox", apose.getchannel("A").getbbox())

seated = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/reposes-v7c-clean/joint-seated-v7c-clean.png")).convert("RGB")
arr = np.asarray(seated).astype(np.float32)
dist = np.sqrt(((arr - np.array([128., 128., 128.])) ** 2).sum(axis=2))
alpha = np.clip((dist - 25) / (60 - 25), 0, 1) * 255
seated_rgba = seated.convert("RGBA")
seated_rgba.putalpha(Image.fromarray(alpha.astype(np.uint8)))
print("seated alpha bbox", seated_rgba.getchannel("A").getbbox())

def place(bg, plate, plate_h, bottom_y, center_x, shadow=False, shadow_w=260):
    pw, ph = plate.size
    s = plate_h / ph
    nw, nh = int(round(pw * s)), int(round(plate_h))
    resized = plate.resize((nw, nh), Image.LANCZOS)
    bbox = resized.getchannel("A").getbbox()
    print(f"  plate {plate_h}px -> visible bbox {bbox} h={bbox[3]-bbox[1]} w={bbox[2]-bbox[0]}")
    out = bg.copy()
    if shadow:
        sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(sh)
        d.ellipse([center_x - shadow_w // 2, bottom_y - 14, center_x + shadow_w // 2, bottom_y + 14], fill=(0, 0, 0, 70))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        out = Image.alpha_composite(out.convert("RGBA"), sh).convert("RGB")
    left = center_x - nw // 2
    top = bottom_y - bbox[3]
    out.paste(resized, (left, top), resized)
    return out

comp = place(bgs["flying"], apose, 520, 550, 584, shadow=False)
comp.save(os.path.join(OUT, "layout-pass-flying-painted-20261031.jpg"), quality=92)
comp = place(bgs["rooftop"], apose, 560, 750, 470, shadow=True, shadow_w=240)
comp.save(os.path.join(OUT, "layout-pass-rooftop-painted-20261031.jpg"), quality=92)
comp = place(bgs["alley"], apose, 560, 650, 584, shadow=True, shadow_w=240)
comp.save(os.path.join(OUT, "layout-pass-alley-painted-20261031.jpg"), quality=92)
comp = place(bgs["desk"], seated_rgba, 480, 685, 584, shadow=True, shadow_w=300)
comp.save(os.path.join(OUT, "layout-pass-desk-painted-20261031.jpg"), quality=92)
print("done")
