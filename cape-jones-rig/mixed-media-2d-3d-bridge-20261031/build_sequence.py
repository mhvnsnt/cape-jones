from PIL import Image, ImageDraw
import json, os, glob
BASE = "/home/hatch/workspace/cape-jones-rig/mixed-media-2d-3d-bridge-20261031"
D2 = "/home/hatch/workspace/cape-jones-rig/mouth-jaw-movement-20261031/frames_pahgo"
D3 = os.path.join(BASE, "frames_3d")
SEQ = os.path.join(BASE, "frames_seq")
os.makedirs(SEQ, exist_ok=True)
GREY = (128, 128, 128, 255)
def load(p):
    return Image.open(p).convert("RGBA")
def on_grey(im):
    bg = Image.new("RGBA", im.size, GREY)
    bg.alpha_composite(im)
    return bg.convert("RGB")
seq = []
# S00-S02 2D MBP, S03-S05 2D AH
for i in range(3): seq.append(("2D", load(f"{D2}/f00_MBP.png")))
for i in range(3): seq.append(("2D", load(f"{D2}/f09_AH.png")))
# S06-S13 3D
d3files = sorted(glob.glob(f"{D3}/*.png"))
for p in d3files: seq.append(("3D", load(p)))
# S14-S15 2D GK, S16-S17 2D REST
for i in range(2): seq.append(("2D", load(f"{D2}/f15_GK.png")))
for i in range(2): seq.append(("2D", load(f"{D2}/f27_REST.png")))
# Measure 3D jaw-tip: alpha bbox bottom per 3D frame
meas = []
for idx, (kind, im) in enumerate(seq):
    if kind == "3D":
        bbox = im.getchannel("A").getbbox()
        meas.append({"seq_frame": idx, "angle_deg": [0,12,24,32,32,24,12,0][idx-6],
                     "alpha_bbox": bbox, "jaw_tip_bottom_y": bbox[3] if bbox else None,
                     "alpha_px": sum(1 for v in im.getchannel("A").getdata() if v > 10)})
    else:
        meas.append({"seq_frame": idx, "kind": "2D"})
with open(os.path.join(BASE, "measurements-20261031.json"), "w") as f:
    json.dump({"sequence": "S00-S02 2D MBP, S03-S05 2D AH, S06-S13 3D jaw gag, S14-S15 2D GK, S16-S17 2D REST",
               "handoff_2d_to_3d": "S05 -> S06", "handoff_3d_to_2d": "S13 -> S14",
               "canvas": "476x688 all frames", "frames_3d": meas}, f, indent=2)
# Save seq frames (display grey) + GIF
frames = []
for i, (kind, im) in enumerate(seq):
    disp = on_grey(im)
    disp.save(os.path.join(SEQ, f"seq_{i:02d}_{kind}.png"))
    frames.append(disp)
frames[0].save(os.path.join(BASE, "jaw-gag-2d-3d-2d-20261031.gif"), save_all=True,
               append_images=frames[1:], duration=100, loop=0)
# Contact: 2D MBP, 2D AH, 3D 0deg, 3D 32deg peak, 3D 0deg back, 2D REST
tiles = [("2D MBP S00", seq[0][1]), ("2D AH S03", seq[3][1]),
         ("3D GAG 0deg S06", seq[6][1]), ("3D GAG 32deg S09 PEAK", seq[9][1]),
         ("3D GAG 0deg S13", seq[13][1]), ("2D REST S16", seq[16][1])]
W, H = 476, 688
contact = Image.new("RGB", (W*3, (H+30)*2), (20, 20, 20))
d = ImageDraw.Draw(contact)
for i, (label, im) in enumerate(tiles):
    x, y = (i % 3) * W, (i // 3) * (H+30)
    contact.paste(on_grey(im), (x, y))
    d.text((x+8, y+H+8), label, fill=(255, 255, 0))
contact.save(os.path.join(BASE, "jaw-gag-contact-20261031.png"))
print(json.dumps(meas, indent=2))
print("seq frames:", len(seq))
