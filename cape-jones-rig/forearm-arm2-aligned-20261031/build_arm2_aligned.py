"""Rebuild Arm2 foreshortened forearm from ORIGINAL v7c Arm_Back_Lower, straight axis.
Foreshortening done correctly: shorten ONLY the shaft between elbow and cuff.
Cuff and fist (closest to camera) stay at full size, all segments centred on one axis.
No flip, no rotation, no shear warp.
Segments (original y): cap+shaft 0-90, cuff 90-178, fist 178-284 (wrist constriction ~178).
Stack on 249x215 canvas, axis X=175:
  shaft: 96x35 at y0, cuff: 96x80 at y35, wrist cap centre (175,115) behind fist,
  fist: 110x135 at y97 (18px overlap over wrist).
"""
from PIL import Image, ImageDraw
import os
BASE = os.path.expanduser('~/workspace/cape-jones-rig/')
SRC = BASE + 'cut-limbs-v7c/Arm_Back_Lower.png'
OUT = BASE + 'forearm-arm2-aligned-20261031/forearm-v3-arm2-back-aligned-20261031.png'
AXIS_X = 175
src = Image.open(SRC).convert('RGBA')
shaft = src.crop((0, 0, src.width, 90)).resize((96, 35), Image.LANCZOS)
cuff  = src.crop((0, 90, src.width, 178)).resize((96, 80), Image.LANCZOS)
fist  = src.crop((55, 178, 152, 284)).resize((110, 135), Image.LANCZOS)
canvas = Image.new('RGBA', (249, 215), (0, 0, 0, 0))
canvas.alpha_composite(shaft, (AXIS_X-48-19, 0))  # art-centre correction: original crop has ~32px transparent left margin
canvas.alpha_composite(cuff, (AXIS_X-48-19, 35))  # same art-centre correction
d = ImageDraw.Draw(canvas)
r = 28
d.ellipse([AXIS_X-r, 115-r, AXIS_X+r, 115+r], fill=(255,255,255,255), outline=(0,0,0,255), width=3)
canvas.alpha_composite(fist, (AXIS_X-55, 97))
canvas.save(OUT)
import numpy as np
a = np.array(canvas)[:,:,3] > 10
ys, xs = np.where(a)
print(f"saved {OUT} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} opaque={a.sum()}")
