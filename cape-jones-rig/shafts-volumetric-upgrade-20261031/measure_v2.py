from PIL import Image
import numpy as np, json
D='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/'
shaft=np.array(Image.open(D+'shafts-only-cycles-v2-20261031.png').convert('RGB')).astype(float)
fig=np.array(Image.open('/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png').convert('RGBA')).astype(float)
# column profile: mean brightness over rows 250-450 (near top, below slats, above figure head top ~240? figure head at 240, so use rows 150-230 for shaft-only sky, and 500-700 for mid)
for y0,y1,label in [(150,230,'top'),(500,700,'mid'),(900,1100,'lower')]:
    prof = shaft[y0:y1].mean(axis=0).mean(axis=1)  # per x column, mean RGB
    # smooth with 15px window
    k=np.ones(15)/15; sm=np.convolve(prof,k,mode='same')
    print(label, "profile min", round(float(sm.min()),1), "max", round(float(sm.max()),1), "mean", round(float(sm.mean()),1))
    # peaks: columns above midpoint between min and max, runs >=30px
    thr=(sm.min()+sm.max())/2
    bright=sm>thr; runs=[]; s=None
    for i,v in enumerate(bright):
        if v and s is None: s=i
        if not v and s is not None: runs.append((s,i-1)); s=None
    if s is not None: runs.append((s,len(bright)-1))
    runs=[r for r in runs if r[1]-r[0]>=30]
    print(label, "threshold", round(float(thr),1), "runs", runs)
    # gap contrast: peak mean vs valley mean
    print(label, "peak_mean", round(float(sm[bright].mean()),1) if bright.any() else None, "valley_mean", round(float(sm[~bright].mean()),1) if (~bright).any() else None)
# shaft brightness vs background (dark world corners)
print("corner mean RGB", shaft[:100,:100].reshape(-1,3).mean(axis=0))
print("shaft centre mean RGB (x 480-620, y 300-500)", shaft[300:500,480:620].reshape(-1,3).mean(axis=0))
print("figure bbox", end=" ")
ys,xs=np.where(fig[...,3]>10); print(xs.min(),ys.min(),xs.max(),ys.max())
print("edge alpha max", int(np.concatenate([fig[0,:,3],fig[-1,:,3],fig[:,0,3],fig[:,-1,3]]).max()))
