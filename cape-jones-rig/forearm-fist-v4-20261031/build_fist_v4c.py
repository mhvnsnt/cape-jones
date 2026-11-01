"""V4b: true front-facing punching fist, merged-silhouette method.
Body + knuckles drawn as ONE white silhouette, outline = dilated silhouette
behind it (no individual knuckle rings, no floating circles). Thumb = separate
capsule crossing the front (its outline is the digit separation, correct).
Knuckles TOP facing camera, NO palm. Wrist cuff bottom, standalone.
"""
from PIL import Image, ImageDraw

SS = 4
W, H = 300*SS, 320*SS
WHITE = (255,255,255,255); BLACK = (0,0,0,255)

# --- silhouette layer (white shapes, no outlines yet) ---
sil = Image.new("RGBA", (W, H), (0,0,0,0))
d = ImageDraw.Draw(sil)
# fist mass: rounded rect, wide at top, slightly narrower at wrist
d.polygon([(72*SS, 82*SS), (228*SS, 82*SS), (240*SS, 150*SS), (228*SS, 248*SS), (196*SS, 258*SS), (104*SS, 258*SS), (72*SS, 248*SS), (60*SS, 150*SS)], fill=WHITE)
for _cx,_cy in [(72,82),(228,82),(228,248),(72,248)]:
    d.ellipse([(_cx-28)*SS,(_cy-28)*SS,(_cx+28)*SS,(_cy+28)*SS], fill=WHITE)
# knuckle bumps: overlapping ellipses across the top edge, merged into mass
for (cx, cy, rx, ry) in [(95,72,34,30),(140,66,36,32),(186,68,35,31),(224,76,28,26)]:
    d.ellipse([(cx-rx)*SS,(cy-ry)*SS,(cx+rx)*SS,(cy+ry)*SS], fill=WHITE)
# slight wrist taper: white rect narrowing below mass (covered by cuff later)
d.rounded_rectangle([86*SS, 230*SS, 214*SS, 272*SS], radius=20*SS, fill=WHITE)

# outline by dilation: paste silhouette in black offset in a ring, then white on top
out_img = Image.new("RGBA", (W, H), (0,0,0,0))
for dx in range(-5*SS, 5*SS+1, 2*SS):
    for dy in range(-5*SS, 5*SS+1, 2*SS):
        if dx*dx+dy*dy <= (5*SS)**2 + 2:
            blk = Image.new("RGBA", (W, H), (0,0,0,0))
            # black version of silhouette: use alpha as mask
            blk.paste((0,0,0,255), (dx, dy), sil.split()[3])
            out_img = Image.alpha_composite(out_img, blk)
out_img = Image.alpha_composite(out_img, sil)
d = ImageDraw.Draw(out_img)

# shading: soft grey on right side + under knuckles, clipped to silhouette
shade = Image.new("RGBA", (W, H), (0,0,0,0))
ds = ImageDraw.Draw(shade)
ds.polygon([(190*SS,80*SS),(242*SS,80*SS),(242*SS,252*SS),(185*SS,252*SS)], fill=(188,196,208,110))
ds.ellipse([(120*SS,190*SS),(250*SS,260*SS)], fill=(188,196,208,70))
out_img = Image.alpha_composite(out_img, shade)
# re-apply silhouette alpha clip (shade already inside? shade may spill outside
# silhouette on the right edge -- clip it)
alpha = sil.split()[3]
# composite shade only where silhouette exists: rebuild
base = Image.new("RGBA", (W, H), (0,0,0,0))
for dx in range(-5*SS, 5*SS+1, 2*SS):
    for dy in range(-5*SS, 5*SS+1, 2*SS):
        if dx*dx+dy*dy <= (5*SS)**2 + 2:
            blk = Image.new("RGBA", (W, H), (0,0,0,0))
            blk.paste((0,0,0,255), (dx, dy), alpha)
            base = Image.alpha_composite(base, blk)
base = Image.alpha_composite(base, sil)
# shade clipped
shade_clipped = Image.new("RGBA", (W, H), (0,0,0,0))
shade_clipped.paste(shade, (0,0), alpha)
out_img = Image.alpha_composite(base, shade_clipped)
d = ImageDraw.Draw(out_img)

# knuckle seams: SHORT vertical creases only, between knuckles, upper third
for x in (118, 163, 206):
    d.line([(x*SS, 90*SS), (x*SS, 110*SS)], fill=(105,112,124,255), width=2*SS)
# knuckle face highlights: small light arcs (not rings)
# no separate highlight arcs: knuckle faces stay clean white, shading carries form
# finger-curl hint: one shallow curved line, low, not a full arc across the face
d.arc([92*SS, 132*SS, 208*SS, 196*SS], start=15, end=165, fill=(70,74,82,255), width=3*SS)

# --- thumb: capsule crossing the FRONT, right side -> centre (standalone) ---
# draw thumb on its own layer, then paste with outline
thumb_layer = Image.new("RGBA", (W, H), (0,0,0,0))
dt = ImageDraw.Draw(thumb_layer)
# capsule as thick line with round ends (PIL line caps are not round by default,
# so add circles at ends)
x0,y0,x1,y1 = 242*SS, 186*SS, 148*SS, 214*SS
dt.line([(x0,y0),(x1,y1)], fill=WHITE, width=52*SS)
dt.ellipse([x0-26*SS, y0-26*SS, x0+26*SS, y0+26*SS], fill=WHITE)
dt.ellipse([x1-26*SS, y1-26*SS, x1+26*SS, y1+26*SS], fill=WHITE)
# thumb outline: dilate thumb alpha in black, then thumb white on top
ta = thumb_layer.split()[3]
thumb_out = Image.new("RGBA", (W, H), (0,0,0,0))
for dx in range(-4*SS, 4*SS+1, 2*SS):
    for dy in range(-4*SS, 4*SS+1, 2*SS):
        if dx*dx+dy*dy <= (4*SS)**2 + 2:
            blk = Image.new("RGBA", (W, H), (0,0,0,0))
            blk.paste((0,0,0,255), (dx, dy), ta)
            thumb_out = Image.alpha_composite(thumb_out, blk)
thumb_out = Image.alpha_composite(thumb_out, thumb_layer)
out_img = Image.alpha_composite(out_img, thumb_out)
d = ImageDraw.Draw(out_img)
# thumb tip crease (short, near the right end = thumb tip)
d.arc([(150*SS, 192*SS), (180*SS, 224*SS)], start=90, end=270, fill=(105,112,124,255), width=2*SS)

# --- wrist / gauntlet cuff (separate piece, own outline, narrower than fist) ---
cuff = Image.new("RGBA", (W, H), (0,0,0,0))
dc = ImageDraw.Draw(cuff)
dc.rounded_rectangle([88*SS, 252*SS, 212*SS, 302*SS], radius=12*SS, fill=WHITE)
ca = cuff.split()[3]
cuff_out = Image.new("RGBA", (W, H), (0,0,0,0))
for dx in range(-4*SS, 4*SS+1, 2*SS):
    for dy in range(-4*SS, 4*SS+1, 2*SS):
        if dx*dx+dy*dy <= (4*SS)**2 + 2:
            blk = Image.new("RGBA", (W, H), (0,0,0,0))
            blk.paste((0,0,0,255), (dx, dy), ca)
            cuff_out = Image.alpha_composite(cuff_out, blk)
cuff_out = Image.alpha_composite(cuff_out, cuff)
out_img = Image.alpha_composite(out_img, cuff_out)
d = ImageDraw.Draw(out_img)
d.line([(88*SS, 276*SS), (212*SS, 276*SS)], fill=BLACK, width=3*SS)

out = out_img.resize((300, 320), Image.LANCZOS)
out.save("/home/hatch/workspace/cape-jones-rig/forearm-fist-v4-20261031/fist-front-facing-punch-v4-20261031.png")
print("fist saved", out.size)

# ---- seated forearm, fist scaled to forearm width ----
base_p = "/home/hatch/workspace/cape-jones-rig/forearm-fist-v3-20261031/forearm-v3-arm2-standard-clean-20261031.png"
base = Image.open(base_p).convert("RGBA")
canvas = Image.new("RGBA", (300, 360), (0,0,0,0))
crop = base.crop((0, 0, base.size[0], 108))
# centre the forearm crop: its alpha centre is ~x175 in 249-wide file
canvas.paste(crop, (25, 0), crop)
# NO separate cap disc: the forearm's own wrist ball is the v7c cap, behind the fist.
# Seating the fist over it leaves only its side arcs peeking -- no second dome.
cx, cy = 25+175, 102
# seated fist: rotate 180 (knuckles -> strike edge, thumb -> LEFT for Arm2),
# scaled to ~165 wide to match a ~110-wide wrist/forearm
seated = out.rotate(180).resize((165, 176), Image.LANCZOS)
canvas.paste(seated, (cx-82, cy-48), seated)
canvas.save("/home/hatch/workspace/cape-jones-rig/forearm-fist-v4-20261031/forearm-v4-arm2-front-punch-fist-20261031.png")
print("seated saved", canvas.size)

# proof
proof = Image.new("RGB", (980, 430), (128,128,128))
d0 = "/home/hatch/workspace/cape-jones-rig/forearm-fist-v4-20261031/"
for i, f in enumerate(["fist-palm-facing-v3-relabeled-20261031.png",
                        "fist-front-facing-punch-v4-20261031.png",
                        "forearm-v4-arm2-front-punch-fist-20261031.png"]):
    im = Image.open(d0+f).convert("RGBA"); im.thumbnail((300,410))
    proof.paste(im, (10+i*325, 10), im)
proof.save(d0+"proof-v3-palm-vs-v4-front-punch-20261031.png")
print("proof saved")
