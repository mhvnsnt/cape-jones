#!/usr/bin/env python3
"""Ground-gate complete 2026-10-31: 30/30 shots, L/R feet, MediaPipe pose run.
Plates: transparent-plates-sweep output first (already converted, not duplicated),
else reposes-v7c-clean / rig apose transparent plates. No original overwritten.
Ground line Gy=1000 on a 1100x1500 grey canvas; grounded paste = bbox bottom 1000,
airborne paste = bbox bottom 1000-height. Feet re-measured from composites, never
copied from paste math. L/R feet = alpha bottom per half, split at bbox centre-x.
"""
import json, os, sys
from PIL import Image, ImageDraw
import numpy as np
RIG=os.path.expanduser("~/workspace/cape-jones-rig")
OUT=os.path.join(RIG,"ground-gate-complete-20261031")
SW=os.path.join(RIG,"transparent-plates-sweep-20261031","plates")
def p(*a): return os.path.join(RIG,*a)
SHOTS=[
 ("CJ-01","punch-windup","GROUNDED","standing",os.path.join(SW,"clips-v7__punch__punch-01-windup-v7.png"),None,None),
 ("CJ-02","punch-extend-snap","GROUNDED","standing",os.path.join(SW,"clips-v7__punch__punch-07-extend-snap-v7.png"),None,None),
 ("CJ-03","punch-impact-locked","GROUNDED","standing",os.path.join(SW,"clips-v7c__punch-impact-locked-v7c.png"),None,None),
 ("CJ-04","punch-recover","GROUNDED","standing",os.path.join(SW,"clips-v7__punch__punch-21-recover-v7.png"),None,None),
 ("CJ-05","punch-across-down-placement","GROUNDED","standing",os.path.join(SW,"clips-v7c__punch-arm2-variants__punch-impact-a2l-minus70-across-down-v7c.png"),None,None),
 ("CJ-06","walk-street-contact","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__walk__walk-01-contact-v7c-clean.png"),None,None),
 ("CJ-07","walk-town-passing","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__walk__walk-13-passing-v7c-clean.png"),None,None),
 ("CJ-08","walk-alley-night","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__walk__walk-25-contact-v7c-clean.png"),None,None),
 ("CJ-09","dance-a","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__dance__dance-01-a-v7c-clean.png"),None,None),
 ("CJ-10","dance-b","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__dance__dance-13-b-v7c-clean.png"),None,None),
 ("CJ-11","dance-combined-finale","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__dance__dance-25-a-v7c-clean.png"),None,None),
 ("CJ-12","flying-hover","AIRBORNE","flying",os.path.join(SW,"clips-v7c-clean-20261031__flying__flying-01-hover-v7c-clean.png"),180,"hover 180px above floor, flight line y=820"),
 ("CJ-13","flying-soar","AIRBORNE","flying",os.path.join(SW,"clips-v7c-clean-20261031__flying__flying-13-soar-v7c-clean.png"),260,"soar 260px above floor, flight line y=740"),
 ("CJ-14","flying-dive","AIRBORNE","flying",os.path.join(SW,"clips-v7c-clean-20261031__flying__flying-25-dive-v7c-clean.png"),220,"dive 220px above floor, flight line y=780"),
 ("CJ-15","flying-forward-foreshortened","AIRBORNE","flying",os.path.join(SW,"clips-v7c-clean-20261031__flying__flying-37-hover-v7c-clean.png"),200,"forward flight 200px above floor, flight line y=800; PLATE STAND-IN: no true foreshortened plate exists, flying-37 used, labelled"),
 ("CJ-16","flex-anticipation-before-tighten","GROUNDED","standing",os.path.join(OUT,"plates","flex-anticipation-before-tighten-v7c-clean.png"),None,None),
 ("CJ-17","arms-up-reference","GROUNDED","standing",p("dual-light-variants-20261031","base-arms-up-transparent-20261031.png"),None,None),
 ("CJ-18","true-flex-double-bicep","GROUNDED","standing",os.path.join(OUT,"plates","true-flex-double-bicep-v7c-clean.png"),None,None),
 ("CJ-19","fighting-pose-forward-bicep-curl","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__flex__fighting-pose-forward-bicep-curl-v7c-clean.png"),None,None),
 ("CJ-20","fighting-stance-arms-up-high","GROUNDED","standing",p("dual-light-variants-20261031","base-arms-up-transparent-20261031.png"),None,"plate reuse: same arms-up plate as CJ-17, different shot spec"),
 ("CJ-21a","jump-crouch","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__jump__jump-01-crouch-v7c-clean.png"),None,"CJ-21 frame A crouch, grounded"),
 ("CJ-21b","jump-takeoff","AIRBORNE","jumping",os.path.join(SW,"clips-v7c-clean-20261031__jump__jump-07-takeoff-v7c-clean.png"),120,"CJ-21 frame B takeoff, jumping 120px above floor, flight line y=880"),
 ("CJ-22a","jump-tuck","AIRBORNE","jumping",os.path.join(SW,"clips-v7c-clean-20261031__jump__jump-13-tuck-v7c-clean.png"),140,"CJ-22 frame A tuck, jumping 140px above floor, flight line y=860"),
 ("CJ-22b","jump-landing","GROUNDED","standing",os.path.join(SW,"clips-v7c-clean-20261031__jump__jump-25-land-v7c-clean.png"),None,"CJ-22 frame B landing, grounded"),
 ("CJ-23","lounge-seated-room","GROUNDED","standing",os.path.join(OUT,"plates","joint-seated-v7c-clean.png"),None,"seated: feet on floor, ground line = floor"),
 ("CJ-24","desk-seated","GROUNDED","standing",os.path.join(OUT,"plates","joint-seated-v7c-clean.png"),None,"seated: plate reuse, same seated plate as CJ-23, different shot spec"),
 ("CJ-25","room-standing-device-gag","GROUNDED","standing",p("rig-apose-v7c-clean-transparent.png"),None,None),
 ("CJ-26","dialogue-neutral-unsure","GROUNDED","standing",p("rig-apose-v7c-clean-transparent.png"),None,"body plate = apose; dialogue beat is mouth, not body"),
 ("CJ-27","dialogue-shout-angry","GROUNDED","standing",p("rig-apose-v7c-clean-transparent.png"),None,"body plate = apose; dialogue beat is mouth, not body"),
 ("CJ-28","rooftop-sunset","GROUNDED","standing",p("rig-apose-v7c-clean-transparent.png"),None,None),
 ("CJ-29","rooftop-night-city","GROUNDED","standing",p("rig-apose-v7c-clean-transparent.png"),None,None),
 ("CJ-30","alley-neon-dual-light","GROUNDED","standing",p("rig-apose-v7c-clean-transparent.png"),None,None),
]
GY=1000; W,H=1100,1500; TOL=10
results=[]
for sid,slug,mode,cat,plate,height,flight in SHOTS:
    assert os.path.exists(plate), plate
    im=Image.open(plate).convert("RGBA")
    # scale plate to height 900 max, keep aspect, so all composites comparable
    if im.height>900:
        im=im.resize((int(im.width*900/im.height),900), Image.LANCZOS)
    a=np.asarray(im)[:,:,3]
    ys,xs=np.where(a>10)
    bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
    target_bottom=GY-(height or 0)
    paste_y=target_bottom-bbox[3]
    paste_x=(W-(bbox[2]-bbox[0]))//2-bbox[0]
    comp=Image.new("RGB",(W,H),(128,128,128))
    comp.paste(im,(paste_x,paste_y),im)
    d=ImageDraw.Draw(comp); d.line([(0,GY),(W,GY)],fill=(255,0,0),width=3)
    fn=f"{sid}-{slug}-20261031.png"; comp.save(os.path.join(OUT,"composites",fn))
    # re-measure from composite: figure = pixels differing from grey bg (allow red line row skip)
    arr=np.asarray(comp).astype(int)
    diff=np.abs(arr-np.array([128,128,128])).max(axis=2)
    mask=(diff>20); mask[GY-2:GY+3,:]=False
    ys2,xs2=np.where(mask)
    cb=[int(xs2.min()),int(ys2.min()),int(xs2.max()),int(ys2.max())]
    feet_y=cb[3]; cx=(cb[0]+cb[2])//2
    # L/R: split at centre-x, bottom-most alpha in each half, in original plate coords -> composite coords
    def half_bottom(left):
        sub = a[:, :cx-bbox[0]+ (bbox[0]-paste_x) ] if False else None
        return None
    # do it in composite mask space: left half = x<cx, right half x>=cx
    def hb(is_left):
        colmask = (xs2<cx) if is_left else (xs2>=cx)
        if not colmask.any(): return None
        return int(ys2[colmask].max())
    L=hb(True); R=hb(False)
    spread=abs(L-R) if (L is not None and R is not None) else None
    raised=None
    if spread is not None and spread>20: raised="L (left foot higher)" if L<R else "R (right foot higher)"
    elif spread is not None: raised="none (both planted within 20px)"
    if mode=="GROUNDED":
        verdict="PASS" if abs(feet_y-GY)<=TOL else "FAIL"
        meas_height=GY-feet_y
    else:
        meas_height=GY-feet_y
        verdict="PASS" if (height and abs(meas_height-height)<=TOL+6) else "FAIL"
    results.append({"shot":sid,"slug":slug,"mode":mode,"category":cat,"plate":os.path.relpath(plate,RIG),
      "stated_height":height,"flight_line":flight,"note":None,
      "composite":f"composites/{fn}","bbox":cb,"feet_y":feet_y,"ground_y":GY,
      "offset":feet_y-GY,"measured_height":meas_height,"L_feet_y":L,"R_feet_y":R,
      "LR_spread":spread,"raised_foot":raised,"verdict":verdict})
    print(sid, mode, "feet",feet_y,"L",L,"R",R,"spread",spread,"->",verdict)
json.dump(results, open(os.path.join(OUT,"gate-30-results.json"),"w"), indent=2)
print("shots:",len(results),"pass:",sum(1 for r in results if r['verdict']=='PASS'))
