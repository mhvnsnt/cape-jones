"""Per-frame, per-side measurement of the walk layering defect.
Method: render the same rig pose twice with snap_figure.figure():
  normal = no snap (upper BEFORE torso/collar, lower AFTER torso)
  chestL / chestR = that side's whole chain AFTER torso, BEFORE head
Diff(normal, chestX) = pixels of side X's upper arm that were hidden
under torso/collar in the normal pass = 'eaten bicep' pixels.
Lower arm is after torso in BOTH passes, so it cannot contribute to
the diff; the diff isolates the upper arm. This is a flat-PNG
after-the-fact proof, used alongside (not instead of) the angle gate
check_pose_snap.py, which runs BEFORE rendering.
"""
import os, sys, json, math, importlib.util
import numpy as np
from PIL import Image
RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "coming-forward-walk-layer-fix-20261031")
spec = importlib.util.spec_from_file_location("snap", os.path.join(RIG, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)

def smooth(t): return t*t*(3-2*t)
def interp(a,b,t):
    return {k:{s:a[k][s]+(b[k][s]-a[k][s])*smooth(t) for s in ("L","R")} for k in a}
CONTACT_L = {"arm_upper": {"L": 20, "R": -20}, "arm_lower": {"L": -30, "R": 30},
             "leg_upper": {"L": -28, "R": 22}, "leg_lower": {"L": 5, "R": 15}}
PASSING = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": -10, "R": 10},
           "leg_upper": {"L": 0, "R": 5}, "leg_lower": {"L": 15, "R": 5}}
CONTACT_R = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": 30, "R": -30},
             "leg_upper": {"L": 22, "R": -28}, "leg_lower": {"L": 15, "R": 5}}
keys=[(CONTACT_L,0.70,"CONTACT-L"),(PASSING,0.95,"PASSING"),(CONTACT_R,1.20,"CONTACT-R"),(PASSING,1.40,"PASSING"),(CONTACT_L,1.60,"CONTACT-L")]
cfgs=[]; phases=[]
SEG=10
for ki in range(len(keys)-1):
    ca,sa,la=keys[ki]; cb,sb,lb=keys[ki+1]
    for i in range(SEG):
        t=i/SEG; cfgs.append((interp(ca,cb,t), sa+(sb-sa)*smooth(t))); phases.append(la if i==0 else "INBETWEEN")
for _ in range(4): cfgs.append((CONTACT_L,1.60)); phases.append("CONTACT-L-HOLD")

def diff_px(a,b):
    aa=np.array(a).astype(int); bb=np.array(b).astype(int)
    return int((np.abs(aa-bb).max(axis=2)>10).sum())

rows=[]
for i,(cfg,s) in enumerate(cfgs):
    normal=snap.figure(550,cfg)
    dl=diff_px(normal, snap.figure(550,cfg,snap={"L":"chest"}))
    dr=diff_px(normal, snap.figure(550,cfg,snap={"R":"chest"}))
    rows.append({"frame":i,"scale":round(s,4),"phase":phases[i],
                 "arm_upper_L":cfg["arm_upper"]["L"],"arm_upper_R":cfg["arm_upper"]["R"],
                 "arm_lower_L":cfg["arm_lower"]["L"],"arm_lower_R":cfg["arm_lower"]["R"],
                 "upper_eaten_L_px":dl,"upper_eaten_R_px":dr})
    print(i, phases[i], "L eaten",dl,"R eaten",dr, flush=True)
with open(os.path.join(OUT,"upper_eaten_measurements.json"),"w") as f: json.dump(rows,f,indent=2)
print("DONE", len(rows), "L total", sum(r["upper_eaten_L_px"] for r in rows), "R total", sum(r["upper_eaten_R_px"] for r in rows))
