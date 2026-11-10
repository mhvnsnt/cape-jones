"""Chest-masked split of the upper-eaten diff.
Torso mask = Torso_Chest.png (scale 0.95) pasted at cx=550, top=400, exactly
as snap_figure.figure() does. Collar mask likewise at top=370.
Diff pixels are counted inside torso mask, inside collar mask, and
inside neither (belt/pelvis/other). This separates 'bicep under CHEST'
(Mars's defect, arms in front) from 'shoulder under COLLAR' (present
even at apose, not the defect Mars named).
"""
import os, json, importlib.util
import numpy as np
from PIL import Image
RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "coming-forward-walk-layer-fix-20261031")
spec = importlib.util.spec_from_file_location("snap", os.path.join(RIG, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)
def mask_of(name, top):
    im = snap.load(os.path.join(snap.BASE, name))
    m = np.zeros((1500, 1100), dtype=bool)
    x0 = int(550 - im.size[0]/2); y0 = int(top)
    a = np.array(im.split()[3]) > 10
    m[y0:y0+im.size[1], x0:x0+im.size[0]] = a
    return m
TORSO = mask_of("Torso_Chest.png", 400)
COLLAR = mask_of("Cape_Collar.png", 370)
print("torso alpha px", int(TORSO.sum()), "collar alpha px", int(COLLAR.sum()), "overlap", int((TORSO & COLLAR).sum()), flush=True)
def smooth(t): return t*t*(3-2*t)
def interp(a,b,t):
    return {k:{s:a[k][s]+(b[k][s]-a[k][s])*smooth(t) for s in ("L","R")} for k in a}
CONTACT_L = {"arm_upper": {"L": 20, "R": -20}, "arm_lower": {"L": -30, "R": 30}, "leg_upper": {"L": -28, "R": 22}, "leg_lower": {"L": 5, "R": 15}}
PASSING = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": -10, "R": 10}, "leg_upper": {"L": 0, "R": 5}, "leg_lower": {"L": 15, "R": 5}}
CONTACT_R = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": 30, "R": -30}, "leg_upper": {"L": 22, "R": -28}, "leg_lower": {"L": 15, "R": 5}}
keys=[(CONTACT_L,),(PASSING,),(CONTACT_R,),(PASSING,),(CONTACT_L,)]
cfgs=[]
for ki in range(4):
    ca, cb = keys[ki][0], keys[ki+1][0]
    for i in range(10):
        cfgs.append(interp(ca,cb,i/10))
for _ in range(4): cfgs.append(CONTACT_L)
def diffmask(a,b):
    aa=np.array(a).astype(int); bb=np.array(b).astype(int)
    return (np.abs(aa-bb).max(axis=2)>10)
rows=[]
for i,cfg in enumerate(cfgs):
    normal=snap.figure(550,cfg)
    for side in ("L","R"):
        d=diffmask(normal, snap.figure(550,cfg,snap={side:"chest"}))
        rows.append({"frame":i,"side":side,
            "diff_total":int(d.sum()),"diff_torso_only":int((d & TORSO & ~COLLAR).sum()),
            "diff_collar_only":int((d & COLLAR & ~TORSO).sum()),"diff_both":int((d & TORSO & COLLAR).sum()),
            "diff_other":int((d & ~TORSO & ~COLLAR).sum())})
    print(i, rows[-2], rows[-1], flush=True)
with open(os.path.join(OUT,"chest_masked_measurements.json"),"w") as f: json.dump(rows,f,indent=2)
print("DONE")
