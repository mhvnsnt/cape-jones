"""Helper plates ONLY (not the composite): rim/bleed/shadow/spill masks from the arms-up plate alpha.
The final composite is built in the Blender compositor (blender_composite_l3.py) — PIL never composites the shot."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np, os
R = "/home/hatch/workspace/cape-jones-rig/godray-level3-20261031"
SRC = "/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png"
BASE = Image.open(SRC).convert("RGBA")
W, H = BASE.size
alpha = BASE.split()[3]
arr = np.array(alpha)
ys, xs = np.where(arr > 10)
xmin, xmax, ymin, ymax = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
cx = (xmin + xmax)//2
print("bbox", xmin, xmax, ymin, ymax)
def ring(inner_px, outer_px):
    d_out = alpha.filter(ImageFilter.MaxFilter(outer_px*2+1))
    d_in = alpha.filter(ImageFilter.MaxFilter(inner_px*2+1)) if inner_px>0 else Image.new("L",(W,H),0)
    return Image.fromarray(np.clip(np.array(d_out).astype(int)-np.array(d_in).astype(int),0,255).astype(np.uint8))
def save_mask(name, mask):
    # RGBA where A = mask, RGB = mask gray (so SeparateColor Alpha in Blender reads it)
    rgba = Image.merge("RGBA", (mask, mask, mask, mask))
    rgba.save(os.path.join(R, name)); print(name, "max", int(np.array(mask).max()))
inner = ring(0,2); outer = ring(2,5)
bleed = ring(0,8).filter(ImageFilter.GaussianBlur(5))
save_mask("mask-inner.png", inner)
save_mask("mask-outer.png", outer)
save_mask("mask-bleed.png", bleed)
# left/right split of rim (V5: gold front-left / cyan back-right), feathered at centre
for nm, m in (("inner",inner),("outer",outer)):
    a = np.array(m).astype(float)
    left = a.copy(); left[:, cx:] = 0
    right = a.copy(); right[:, :cx] = 0
    save_mask(f"mask-{nm}-left.png", Image.fromarray(left.astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)))
    save_mask(f"mask-{nm}-right.png", Image.fromarray(right.astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)))
# ground shadow (ellipse under feet) + cast shadow (silhouette offset right/down, blurred, dark)
g = Image.new("RGBA",(W,H),(0,0,0,0)); d = ImageDraw.Draw(g)
d.ellipse([cx-(xmax-xmin)//3, ymax-10, cx+(xmax-xmin)//3, ymax+60], fill=(0,0,0,130))
g = g.filter(ImageFilter.GaussianBlur(8)); g.save(os.path.join(R,"layer-ground-shadow.png")); print("ground shadow saved")
cast = Image.new("RGBA",(W,H),(0,0,0,0))
sil = Image.new("RGBA",(W,H),(0,0,0,0)); sil.paste((0,0,0,255),(0,0), alpha)
cast.alpha_composite(sil, dest=(60, 40))
cast = cast.filter(ImageFilter.GaussianBlur(10))
ca = np.array(cast); ca[:,:,3] = (ca[:,:,3]*0.45).astype(np.uint8)
Image.fromarray(ca).save(os.path.join(R,"layer-cast-shadow.png")); print("cast shadow saved")
# shaft spill ON the character only: vertical soft bands x plate alpha, cyan + gold versions
bands = np.zeros((H,W), dtype=float)
for bx in range(xmin, xmax, 180):
    bands[:, max(0,bx-50):bx+50] += 1.0
bands = np.clip(bands,0,1)
# blur bands via PIL
band_img = Image.fromarray((bands*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(25))
ba = np.array(band_img).astype(float)/255.0
pa = np.array(alpha).astype(float)/255.0
for nm, col in (("cyan",(0,200,255)),("gold",(255,180,80))):
    a = (ba*pa*0.14*255).astype(np.uint8)
    layer = np.zeros((H,W,4), dtype=np.uint8); layer[:,:,0]=col[0]; layer[:,:,1]=col[1]; layer[:,:,2]=col[2]; layer[:,:,3]=a
    Image.fromarray(layer,"RGBA").save(os.path.join(R,f"layer-spill-{nm}.png")); print("spill",nm)
# solid full-canvas colours for Blender SetAlpha rim layers
for nm, col in (("gold",(255,180,80)),("cyan",(0,200,255)),("goldbleed",(255,120,0)),("cyanbleed",(0,120,255))):
    Image.new("RGBA",(W,H),col+(255,)).save(os.path.join(R,f"solid-{nm}.png"))
print("masks done")
