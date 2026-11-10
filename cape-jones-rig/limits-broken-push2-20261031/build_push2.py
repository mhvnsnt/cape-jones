from PIL import Image, ImageDraw, ImageFont
import numpy as np, json, os
from scipy import ndimage
BASE="/home/hatch/workspace/cape-jones-rig"
OUT=f"{BASE}/limits-broken-push2-20261031/proofs"
os.makedirs(OUT, exist_ok=True)
ap=Image.open(f"{BASE}/rig-apose-v7c-clean-transparent.png").convert("RGBA")
W,H=ap.size
alpha=np.array(ap)[:,:,3]
ys,xs=np.where(alpha>10)
bbox=(int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
print("bbox",bbox)

def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()

# --- P1 G1 side v2: squish 0.45 + profile head ---
squished=ap.resize((int(W*0.45),H), Image.LANCZOS)
# centre it
canvas=Image.new("RGBA",(W,H),(128,128,128,255))
ox=(W-squished.width)//2
canvas.alpha_composite(squished,(ox,0))
# clear front-head area in squished coords: original head approx x 430-670? use bbox centre
# squished head region: centre x=550, width ~120, y 253-430
arr=np.array(canvas)
arr[253:435, 470:635, 3]=0
canvas=Image.fromarray(arr)
prof=Image.open(f"{BASE}/sliced/Head_Profile.png").convert("RGBA")
prof2=prof.resize((120,200), Image.LANCZOS)
canvas.alpha_composite(prof2,(490,253))
canvas.convert("RGB").save(f"{OUT}/P1-G1-side-v2-profile-head-20261031.png")
pa=np.array(canvas.convert("RGBA"))[:,:,3]
print("P1 saved, profile pasted 120x200 at (490,253)")

# --- P2 G2 silhouette-distance + per-limb side weight ---
mask=(alpha>10)
dist=ndimage.distance_transform_edt(mask)
dist_n=dist/(dist.max() if dist.max() else 1)
arr=np.array(ap).astype(float)
# side weight: left of centre brighter, right darker, modulated by dist (interior stronger)
cx=(bbox[0]+bbox[2])/2
xx=np.arange(W)[None,:]
side=np.tile(np.clip((cx-xx)/ (bbox[2]-bbox[0]) *2, -1, 1), (H,1))  # + left, - right
factor=np.ones((H,W))
factor[mask]=1.0 + 0.18*side[mask]* (0.5+0.5*dist_n[mask])  # left up, right down
for c in range(3):
    arr[:,:,c]=np.clip(arr[:,:,c]*factor,0,255)
out2=Image.fromarray(arr.astype(np.uint8))
out2.save(f"{OUT}/P2-G2-distance-normal-sideweight-20261031.png")
# measure left vs right mean R inside alpha
left=mask.copy(); left[:,int(cx):]=False
right=mask.copy(); right[:,:int(cx)]=False
lm=float(np.array(out2)[:,:,0][left].mean()); rm=float(np.array(out2)[:,:,0][right].mean())
print(f"P2 left {lm:.1f} right {rm:.1f} delta {lm-rm:.1f} (L02 delta +31.9, control -0.8)")

# --- P3 G3 shafts BEHIND figure ---
bg=Image.new("RGBA",(W,H),(20,20,40,255))
d=ImageDraw.Draw(bg)
# sharp shafts from top centre fan
for x0,x1 in [(300,340),(500,560),(700,760),(850,900)]:
    d.polygon([(x0,0),(x1,0),(x1+120,H),(x0+60,H)], fill=(180,220,255,255))
# paste figure on top
bg.alpha_composite(ap)
bg.convert("RGB").save(f"{OUT}/P3-G3-shafts-behind-figure-20261031.png")
# measure: row y=200 above figure? figure starts y253, so row 200 is shafts only; row 800 across figure: shaft colour visible only outside alpha
row=np.array(bg.convert("RGB"))[800]
# count shaft-blue pixels outside alpha vs inside alpha at y=800
shaft_blue = (np.array(bg.convert("RGB"))[:,:,2]>200) & (np.array(bg.convert("RGB"))[:,:,0]>150)
inside = shaft_blue & mask
outside = shaft_blue & (~mask)
print(f"P3 shaft-blue px total {int(shaft_blue.sum())} inside-figure-alpha {int(inside.sum())} outside {int(outside.sum())} -- inside should be figure pixels, check by colour: figure suit is white, so blue-tinted shaft over figure would be distinct; visual check required")

# --- P4 G5 Arm1 piece-only ---
piece=Image.open(f"{BASE}/cut-limbs-v7c/Arm_Front_Upper.png").convert("RGBA")
rot=piece.rotate(18.2, resample=Image.BICUBIC, expand=False, center=(piece.width//2, 20))  # -18.2 correction direction labelled
sheet=Image.new("RGBA",(900,420),(128,128,128,255))
sheet.alpha_composite(piece,(40,40)); sheet.alpha_composite(rot,(480,40))
dd=ImageDraw.Draw(sheet); f=font(22)
dd.text((40,10),"ORIGINAL Arm_Front_Upper",fill=(255,255,255),font=f)
dd.text((480,10),"ROTATED -18.2 deg (piece only)",fill=(255,255,255),font=f)
dd.text((40,380),"NOT a v7c-builder frame. Builder frame still owed.",fill=(255,255,0),font=f)
sheet.convert("RGB").save(f"{OUT}/P4-G5-arm1-piece-rotation-20261031.png")
print("P4 piece",piece.size,"rot bbox alpha",int((np.array(rot)[:,:,3]>10).sum()))

# --- P5 G7 gold split on real apose frame ---
g=ap.copy()
gd=ImageDraw.Draw(g)
# gold test patch across seam x=600, on figure area y 700-900, opaque hard seam
for x in range(500,700):
    for y in range(700,900):
        pass
# efficient numpy
ga=np.array(g)
patch_mask=np.zeros((H,W),bool); patch_mask[700:900,500:700]=True
# only where figure alpha OR patch area? Use patch as test strip over frame (labelled test)
ga[patch_mask]=[255,180,80,255]
# hard seam 2px at x=600: opaque black? No - seam line is boundary, keep gold both sides, seam marker 2px dark for visibility in proof only, measurement excludes seam
ga[700:900,599:601]=[0,0,0,255]
g2=Image.fromarray(ga)
g2.save(f"{OUT}/P5-G7-gold-split-apose-20261031.png")
left_patch=ga[700:900,500:599][:,:3]; right_patch=ga[700:900,601:700][:,:3]
print("P5 gold left median", [float(np.median(left_patch[:,:,c])) for c in range(3)], "right", [float(np.median(right_patch[:,:,c])) for c in range(3)], "input (255,180,80)")

# --- P6 G4 real gate measurements ---
rgb=np.array(ap.convert("RGB")).astype(int)
red_label = (rgb[:,:,0]>200)&(rgb[:,:,1]<80)&(rgb[:,:,2]<80)&(alpha>10)
stats={
 "source":"rig-apose-v7c-clean-transparent.png (1100x1500)",
 "alpha_bbox":bbox, "alpha_px":int((alpha>10).sum()),
 "figure_w":bbox[2]-bbox[0], "figure_h":bbox[3]-bbox[1],
 "centre_x":(bbox[0]+bbox[2])//2, "red_label_px":int(red_label.sum()),
 "g4_methods_total":20,
 "g4_methods_with_real_measurement_here":6,
 "g4_real_methods":["alpha_bbox","alpha_px","figure_w_h","centre_x","red_label_px","apose_size"],
 "g4_methods_still_schema_or_placeholder":14,
 "note":"Cowl collar-edge, arm angle, fist offset, knee/foot angle need piece-separated renders, not a flat apose PNG. Those 14 remain NOT measured here."
}
json.dump(stats, open(f"{OUT}/P6-G4-real-gate-measurements-20261031.json","w"), indent=2)
print(stats)
