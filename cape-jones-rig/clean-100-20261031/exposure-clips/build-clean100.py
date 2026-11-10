"""Clean-100 build, 2026-10-31. Labels=False only. No base art recoloured.
Rig builder: rig-v7c-clean100.py (v7c anchors/scale/piece order, output path + OutFixed selectable).
Sources:
 - 17 files already clean in clips-v7c-clean-20261031/ -> copied pixel-identical to new dated names.
 - fighting + flex-07 (same pose, verified 0-diff labelled) -> rig re-render, labels=False, OutFixed lowers
   (arms up + in front, |lower|=160 >= 120, fighting pose condition).
 - punch-arm2 variants + punch-impact-locked (locked = -110 variant, verified 0-diff labelled)
   -> rig re-render, labels=False, ORIGINAL lowers (punch is not the fighting pose; -110/-70/-90 are
   below the 120 threshold and -110 is the Mars-locked punch frame; 160-current = punch-09).
 - wave 1/2/3 -> NEW rig renders, labels=False, original lowers (arm up BEHIND head, not in front of
   torso, so the fighting-pose OutFixed condition does not apply). R arm upper=lower -120/-150/-180,
   L arm apose -20/-20, legs apose -10/10, 10/-10.
Exposure sheets: same panel layouts as the v6 sheets, assembled from the clean frames above, no labels.
"""
import sys, os, shutil, json, hashlib
import importlib.util
_spec = importlib.util.spec_from_file_location("rigv7c", os.path.join(os.path.dirname(os.path.abspath(__file__)), "rig-v7c-clean100.py"))
_rig = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_rig)
build = _rig.build
from PIL import Image, ImageDraw
import numpy as np
ROOT="/home/hatch/workspace/cape-jones-rig"
OUT=os.path.dirname(os.path.abspath(__file__))
CLEAN=f"{ROOT}/clips-v7c-clean-20261031"
manifest=[]
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:12]
def redcount(p):
    a=np.array(Image.open(p).convert("RGB")).astype(int)
    return int(((a[:,:,0]>200)&(a[:,:,1]<80)&(a[:,:,2]<80)).sum())
def copy_clean(src_rel, dst_rel):
    s=os.path.join(ROOT,src_rel); d=os.path.join(OUT,dst_rel); shutil.copyfile(s,d)
    manifest.append({"file":dst_rel,"source":src_rel,"method":"copy of existing v7c clean render (labels=False), new dated filename only","red_px":redcount(d),"sha12":sha(d)})
    return d
def render(dst_rel, cfg, outfixed=False, arms_whole=False, note=""):
    d=os.path.join(OUT,dst_rel); build(d,cfg,labels=False,outfixed=outfixed,arms_whole=arms_whole)
    manifest.append({"file":dst_rel,"source":"joint_locked_rig_v7c (rig-v7c-clean100.py), labels=False"+note,"method":"rig re-render, labels=False"+(" + OutFixed lowers" if outfixed else " + original lowers"),"red_px":redcount(d),"sha12":sha(d),"cfg":cfg})
    return d
# --- 17 already-clean files, new dated names ---
for cat, names in {
 "walk":["walk-01-contact","walk-13-passing","walk-25-contact","walk-37-passing"],
 "dance":["dance-01-a","dance-13-b","dance-25-a"],
 "flying":["flying-01-hover","flying-13-soar","flying-25-dive","flying-37-hover"],
 "jump":["jump-01-crouch","jump-07-takeoff","jump-13-tuck","jump-25-land"],
 "punch":["punch-09-impact-hold"],
}.items():
    for n in names:
        copy_clean(f"clips-v7c-clean-20261031/{cat}/{n}-v7c-clean.png", f"clips/{cat}/{n}-v7c-clean100-20261031.png")
# --- fighting / flex-07: same pose, OutFixed ---
fight={"arm_upper":{"L":-20,"R":20},"arm_lower":{"L":160,"R":-160},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":10,"R":-10}}
fight_clean=render("clips/flex/fighting-pose-forward-bicep-curl-v7c-clean100-20261031.png", fight, outfixed=True, note=" (fighting pose, arms up+in front)")
render("clips/flex/flex-07-flex-hold-v7c-clean100-20261031.png", fight, outfixed=True, note=" (SUPERSEDED name for the same fighting pose; pixels identical to fighting file)")
# --- punch variants + locked ---
punch_base={"arm_upper":{"L":-90,"R":20},"arm_lower":{"L":-90,"R":160},"leg_upper":{"L":-15,"R":15},"leg_lower":{"L":15,"R":-15}}
variants=[("punch-impact-a2l-160-current",160),("punch-impact-a2l-minus110-across-up",-110),("punch-impact-a2l-minus70-across-down",-70),("punch-impact-a2l-minus90-across",-90)]
for name,val in variants:
    cfg=dict(punch_base); cfg["arm_lower"]={"L":-90,"R":val}
    render(f"clips/punch-arm2-variants/{name}-v7c-clean100-20261031.png", cfg, note=" (punch impact, original lowers)")
cfg110=dict(punch_base); cfg110["arm_lower"]={"L":-90,"R":-110}
render("clips/punch/punch-impact-locked-v7c-clean100-20261031.png", cfg110, note=" (locked punch = -110 variant)")
# --- wave, new ---
wave_files=[]
for i,ang in enumerate((-120,-150,-180),start=1):
    cfg={"arm_upper":{"L":-20,"R":ang},"arm_lower":{"L":-20,"R":ang},"leg_upper":{"L":-10,"R":10},"leg_lower":{"L":10,"R":-10}}
    wave_files.append(render(f"wave/wave-{i}-v7c-clean100-20261031.png", cfg, note=" (wave, R arm up behind head)"))
# --- exposure sheets ---
def crop_char(im):
    a=np.array(im.convert("RGB")).astype(int)
    m=np.any(a!=np.array([128,128,128]),axis=2)
    ys,xs=np.where(m); x0,x1,y0,y1=int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max())
    return im.crop((max(0,x0-10),max(0,y0-10),min(im.size[0],x1+11),min(im.size[1],y1+11)))
def sheet(outname, title, subtitle, panels):
    PW,PH,GAP,HEAD,CAP=380,540,20,70,30
    W=len(panels)*PW+(len(panels)+1)*GAP; H=HEAD+PH+CAP
    s=Image.new("RGB",(W,H),(10,10,10)); d=ImageDraw.Draw(s)
    d.text((20,12),title,fill=(255,255,255)); d.text((20,38),subtitle,fill=(255,200,80))
    for i,(path,cap) in enumerate(panels):
        x=GAP+i*(PW+GAP); s.paste((128,128,128),(x,HEAD,x+PW,HEAD+PH))
        ch=crop_char(Image.open(path)); ch.thumbnail((PW-20,PH-20), Image.LANCZOS)
        s.paste(ch,(x+(PW-ch.size[0])//2, HEAD+(PH-ch.size[1])//2))
        d.text((x,HEAD+PH+6),cap,fill=(255,255,255))
    p=os.path.join(OUT,"exposure-sheets",outname); s.save(p)
    manifest.append({"file":f"exposure-sheets/{outname}","source":"clean frames listed in panels","method":"exposure sheet assembly from clean frames, no labels, no recolour","red_px":redcount(p),"sha12":sha(p),"panels":[c for _,c in panels]})
    return p
C=lambda rel: os.path.join(OUT,rel)
sheet("exposure-walk-variant-v7c-clean100-20261031.png","EXPOSURE SHEET - WALK CYCLE VARIANT (CLEAN, v7c)",
 "Walk, v7c rig clean, 4 drawings, loops. Variant = passing pose included, not just contacts.",
 [(C("clips/walk/walk-01-contact-v7c-clean100-20261031.png"),"F1 contact LEG1 fwd - hold 12"),
  (C("clips/walk/walk-13-passing-v7c-clean100-20261031.png"),"F13 passing - hold 12"),
  (C("clips/walk/walk-25-contact-v7c-clean100-20261031.png"),"F25 contact LEG2 fwd - hold 12"),
  (C("clips/walk/walk-37-passing-v7c-clean100-20261031.png"),"F37 passing - hold 12, loop to F1")])
sheet("exposure-dance-v7c-clean100-20261031.png","EXPOSURE SHEET - DANCE (CLEAN, v7c)",
 "Dance, v7c rig clean, 3 drawings, loops a-b-a.",
 [(C("clips/dance/dance-01-a-v7c-clean100-20261031.png"),"F1 dance-a - hold 12"),
  (C("clips/dance/dance-13-b-v7c-clean100-20261031.png"),"F13 dance-b - hold 12"),
  (C("clips/dance/dance-25-a-v7c-clean100-20261031.png"),"F25 dance-a repeat - hold 12")])
sheet("exposure-power-pose-v7c-clean100-20261031.png","EXPOSURE SHEET - POWER POSE (CLEAN, v7c)",
 "Power pose = fighting pose, gauntlet-out-fixed (approved). NOT the true flex.",
 [(fight_clean,"F7 fighting pose - POWER POSE - gauntlet-out-fixed"),
  (C("clips/punch/punch-09-impact-hold-v7c-clean100-20261031.png"),"F9 punch impact hold - hold 12")])
sheet("exposure-landing-v7c-clean100-20261031.png","EXPOSURE SHEET - LANDING (CLEAN, v7c)",
 "Jump / landing, v7c rig clean. Landing drawing is F25.",
 [(C("clips/jump/jump-01-crouch-v7c-clean100-20261031.png"),"F1 crouch - hold 6"),
  (C("clips/jump/jump-07-takeoff-v7c-clean100-20261031.png"),"F7 takeoff - hold 2"),
  (C("clips/jump/jump-13-tuck-v7c-clean100-20261031.png"),"F13 tuck - hold 12"),
  (C("clips/jump/jump-25-land-v7c-clean100-20261031.png"),"F25 LAND - hold 6 (landing drawing)")])
sheet("exposure-wave-v7c-clean100-20261031.png","EXPOSURE SHEET - WAVE (CLEAN, v7c, NEW)",
 "Wave, NEW, built from v7c rig clean, labels=False. 3 drawings cycle 1-2-3-2.",
 [(wave_files[0],"Wave 1 - arm up, elbow -120"),
  (wave_files[1],"Wave 2 - arm up, elbow -150"),
  (wave_files[2],"Wave 3 - arm up, elbow -180")])
json.dump({"batch":"clean-100-20261031 exposure-clips","labels":"False only","files":manifest}, open(os.path.join(OUT,"MANIFEST-clean100-20261031.json"),"w"), indent=1)
print(f"manifest files: {len(manifest)}")
for m in manifest: print(m["file"], "red=",m["red_px"], m["sha12"])
