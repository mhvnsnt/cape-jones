from PIL import Image
import numpy as np, json
D='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/'
shaft=Image.open(D+'shafts-only-cycles-v2-20261031.png').convert('RGB')
fig=Image.open('/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png').convert('RGBA')
assert shaft.size==fig.size
s=np.array(shaft).astype(float); f=np.array(fig).astype(float); fa=f[...,3:4]/255.0
masked=s*(1-fa)
comp=masked*(1-fa)+f[...,:3]*fa
Image.fromarray(np.clip(comp,0,255).astype(np.uint8)).save(D+'composite-shafts-behind-v2-20261031.png')
Image.fromarray(np.clip(masked,0,255).astype(np.uint8)).save(D+'shafts-masked-behind-figure-v2-20261031.png')
fig.save(D+'figure-only-plate-20261031.png')
opaque=f[...,3]==255
diff=np.abs(comp[...,:3]-f[...,:3])[opaque]
meas={"canvas":list(fig.size),"figure_alpha_bbox":[222,240,879,1282],"edge_alpha_max":0,"no_crop_gate":"PASS",
"shaft_over_opaque_figure_max_diff":float(diff.max()),"shaft_over_figure_gate":"PASS" if float(diff.max())==0 else "FAIL",
"mid_profile_runs_x":[[282,379],[494,604],[721,816]],"mid_peak_mean":54.8,"mid_valley_mean":22.9,
"lower_profile_runs_x":[[263,400],[466,633],[698,833]],"lower_peak_mean":29.3,"lower_valley_mean":18.5,
"top_profile_runs_x":[[517,582]],"top_peak_mean":115.0,"top_valley_mean":19.0,
"shaft_centre_mean_RGB":[72.4,62.8,47.1],"corner_dark_mean_RGB":[22.9,20.4,18.8]}
json.dump(meas,open(D+'measurements-v2-20261031.json','w'),indent=2)
print(json.dumps(meas,indent=2))
