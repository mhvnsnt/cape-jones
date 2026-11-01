# Composite: shaft-only Cycles render (background) + Cape arms-up plate IN FRONT.
# Shaft masking method: shafts are multiplied by (1 - figure_alpha) before pasting,
# so no shaft pixel exists underneath the figure silhouette. Then figure is pasted
# at its native 1100x1500 position, no resize, no crop window. Canvas = figure canvas.
# Gate: figure alpha at canvas edge must be 0 (no clipping), and shaft-over-figure
# in the final (where figure alpha==255) must be exactly the figure's own colour.
from PIL import Image, ImageDraw, ImageFont
import numpy as np, json, os
D = '/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/'
shaft = Image.open(D+'shafts-only-cycles-20261031.png').convert('RGB')
fig = Image.open('/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png').convert('RGBA')
assert shaft.size == fig.size, (shaft.size, fig.size)
s = np.array(shaft).astype(float)
f = np.array(fig).astype(float)
fa = f[...,3:4]/255.0
# masked shafts: remove shafts under the figure silhouette
masked = s * (1-fa)
comp = masked*(1-fa) + f[...,:3]*fa
comp_img = Image.fromarray(np.clip(comp,0,255).astype(np.uint8))
comp_img.save(D+'composite-shafts-behind-20261031.png')
fig.save(D+'figure-only-plate-20261031.png')
Image.fromarray(np.clip(masked,0,255).astype(np.uint8)).save(D+'shafts-masked-behind-figure-20261031.png')
# measurements
# shaft separation: take a horizontal cut at y=600 (above head, no figure) across shaft render
cut = np.array(shaft)[600,:,0].astype(float)  # use R channel (warm shafts are bright in R)
# find columns: bright >120 vs dark <60, count runs
bright = cut > 120
runs=[]; inrun=False; start=0
for i,v in enumerate(bright):
    if v and not inrun: start=i; inrun=True
    if not v and inrun: runs.append((start,i-1)); inrun=False
if inrun: runs.append((start,len(bright)-1))
shaft_runs=[r for r in runs if r[1]-r[0]>=20]
# brightness
bg = np.array(shaft)
shaft_px = bg[400:900,:,:].reshape(-1,3)
bright_px = shaft_px[np.max(shaft_px,axis=1)>150]
# no-crop gate
edge_alpha = np.concatenate([f[0,:,3], f[-1,:,3], f[:,0,3], f[:,-1,3]])
ys,xs = np.where(f[...,3]>10)
# shaft-over-figure in final: where fig alpha==255, final must equal fig RGB
opaque = f[...,3]==255
diff = np.abs(comp[...,:3]-f[...,:3])[opaque]
meas = {
 "canvas": list(fig.size),
 "figure_alpha_bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
 "edge_alpha_max": int(edge_alpha.max()),
 "no_crop_gate": "PASS" if int(edge_alpha.max())==0 else "FAIL",
 "shaft_runs_at_y600": shaft_runs,
 "shaft_columns_count": len(shaft_runs),
 "shaft_bright_pixel_fraction_rows400_900": float(len(bright_px)/len(shaft_px)),
 "shaft_mean_bright_RGB": [round(float(x),1) for x in np.mean(bright_px,axis=0)] if len(bright_px) else None,
 "shaft_over_opaque_figure_max_diff": float(diff.max()),
 "shaft_over_figure_gate": "PASS" if float(diff.max())==0 else "FAIL",
 "note": "shaft-over-figure is 0 by construction: shafts masked by (1-figure_alpha) and figure pasted on top at full opacity where alpha==255",
}
json.dump(meas, open(D+'measurements-20261031.json','w'), indent=2)
print(json.dumps(meas, indent=2))
