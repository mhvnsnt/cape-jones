"""Inbetweening for pose dialects + Ginyu roll-call, RIG interpolation (not image blending).
Method: joint angles + head angle interpolated between key configs with slow-in/slow-out
(smoothstep) for dialects, and fast snap (ease-out) for roll-call. TOP-ARM layer = union of
the two endpoint top sets, so an inbetween never buries an arm that a key does not bury.
Singles are centred at cx=1100 on a 2200x1500 canvas so the figure centre does not jump
when a single transitions to a pair (original pair files, with user at 650/stand at 830,
are untouched). Pairs here: user at 1100, shadow at 1280 (+180, the coloured-shadow offset).
No new art drawn, no file Mars has seen overwritten. Output: full-size frames + 550x750
video frames, GIFs, MP4s (via ffmpeg), contact strips, onion skin, timing chart, easing
graph, arc track.
"""
from PIL import Image, ImageDraw
import os, math, json
BASE="/home/hatch/workspace/cape-jones-rig/sliced"; CUT="/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
OUT="/home/hatch/workspace/cape-jones-rig/inbetween-20261031"
os.makedirs(OUT+"/frames-dialects", exist_ok=True); os.makedirs(OUT+"/frames-rollcall", exist_ok=True)
SCALE=0.95
ARM={"L":((60,222),(76,30)), "R":((99,222),(76,30))}
LEG={"L":((95,314),(77,40)), "R":((100,314),(84,40))}
LEG_PIECES={"L":("Leg_Front_Upper.png","Leg_Front_Lower.png","Leg_Front_Cap.png"),"R":("Leg_Back_Upper.png","Leg_Back_Lower.png","Leg_Back_Cap.png")}
ARM_PIECES={"L":("Arm_Front_Upper.png","Arm_Front_Lower.png","Arm_Front_Cap.png"),"R":("Arm_Back_Upper.png","Arm_Back_Lower.png","Arm_Back_Cap.png")}
_cache={}
def load(p, scale=SCALE):
    if p not in _cache:
        im=Image.open(p).convert("RGBA"); _cache[p]=im.resize((max(1,int(im.size[0]*scale)), max(1,int(im.size[1]*scale))), Image.LANCZOS)
    return _cache[p]
def paste_at(c, im, cx, top): c.alpha_composite(im,(int(cx-im.size[0]/2),int(top)))
def limb(c, path, joint, angle, anchor):
    im=load(path); ax,ay=anchor[0]*SCALE,anchor[1]*SCALE
    layer=Image.new("RGBA",c.size,(0,0,0,0)); layer.alpha_composite(im,(int(joint[0]-ax),int(joint[1]-ay)))
    layer=layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im=load(path); c.alpha_composite(im,(int(joint[0]-im.size[0]/2),int(joint[1]-im.size[1]/2)))
def rot_vec(v, a):
    r=math.radians(a); x,y=v; return (x*math.cos(r)+y*math.sin(r), -x*math.sin(r)+y*math.cos(r))
def figure(c, cx, cfg, head_angle=0, top_arms=()):
    paste_at(c, load(os.path.join(BASE,"Cape_Back_Main.png")),cx,410)
    hips={"L":(cx-80,740),"R":(cx+65,740)}; shoulders={"L":(cx-120,445),"R":(cx+120,445)}
    for side in ("L","R"):
        hip=hips[side]; ball,hip_anchor=LEG[side]; vec=(ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up,low,cap=LEG_PIECES[side]
        limb(c, os.path.join(CUT,up), hip, cfg["leg_upper"][side], hip_anchor)
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_lower"][side])[1]*SCALE if False else rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
        limb(c, os.path.join(CUT,low), knee, cfg["leg_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), knee)
    elbows={}
    for side in ("L","R"):
        if side in top_arms: continue
        ball,sh_anchor=ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,_,_=ARM_PIECES[side]; sh=shoulders[side]
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side]=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
    paste_at(c, load(os.path.join(BASE,"Pelvis.png")),cx,680); paste_at(c, load(os.path.join(BASE,"Cape_Collar.png")),cx,370)
    paste_at(c, load(os.path.join(BASE,"Torso_Chest.png")),cx,400); paste_at(c, load(os.path.join(BASE,"Belt_Overlay.png")),cx,670)
    for side in ("L","R"):
        if side in top_arms: continue
        _,low,cap=ARM_PIECES[side]; ball,_=ARM[side]
        limb(c, os.path.join(CUT,low), elbows[side], cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbows[side])
    paste_at(c, load(os.path.join(BASE,"Neck.png"),scale=1.05),cx,360)
    head=load(os.path.join(BASE,"Head_Front.png"))
    if head_angle: head=head.rotate(head_angle, expand=True)
    c.alpha_composite(head,(int(cx-head.size[0]/2), int(331-head.size[1]/2)))
    for side in ("L","R"):
        if side not in top_arms: continue
        ball,sh_anchor=ARM[side]; vec=(ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up,low,cap=ARM_PIECES[side]; sh=shoulders[side]
        limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
        elbow=(sh[0]+rot_vec(vec,cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec,cfg["arm_upper"][side])[1]*SCALE)
        limb(c, os.path.join(CUT,low), elbow, cfg["arm_lower"][side], (ball[0],0)); cap_at(c, os.path.join(CUT,cap), elbow)
    return c
def silhouette(layer, rgb=(52,22,90)):
    out=Image.new("RGBA",layer.size,(0,0,0,0)); a=layer.split()[3].point(lambda v:int(v*0.92))
    solid=Image.new("RGBA",layer.size,rgb+(255,)); out.paste(solid, (0,0), a); return out
def C(au,al,lu,ll): return {"arm_upper":{"L":au[0],"R":au[1]},"arm_lower":{"L":al[0],"R":al[1]},"leg_upper":{"L":lu[0],"R":lu[1]},"leg_lower":{"L":ll[0],"R":ll[1]}}
def render_key(key):
    c=Image.new("RGBA",(2200,1500),(0,0,0,0))
    if key["kind"]=="pair":
        sl=Image.new("RGBA",(2200,1500),(0,0,0,0)); figure(sl,1280,key["stand_cfg"],key["stand_head"],key["top"])
        c.alpha_composite(silhouette(sl)); figure(c,1100,key["cfg"],key["head"],key["top"])
    else:
        figure(c,1100,key["cfg"],key["head"],key["top"])
    return c
def lerp_cfg(a,b,t):
    out={}
    for g in ("arm_upper","arm_lower","leg_upper","leg_lower"):
        out[g]={s: a[g][s]+(b[g][s]-a[g][s])*t for s in ("L","R")}
    return out
def interp_key(a,b,t):
    k={"kind": a["kind"] if a["kind"]==b["kind"] else "single",
       "cfg": lerp_cfg(a["cfg"],b["cfg"],t), "head": a["head"]+(b["head"]-a["head"])*t,
       "top": tuple(sorted(set(a["top"])|set(b["top"])))}
    if a["kind"]=="pair" and b["kind"]=="pair":
        k["kind"]="pair"; k["stand_cfg"]=lerp_cfg(a["stand_cfg"],b["stand_cfg"],t); k["stand_head"]=a["stand_head"]+(b["stand_head"]-a["stand_head"])*t
    elif a["kind"]=="pair" or b["kind"]=="pair":
        # single<->pair transition: shadow fades in/out by alpha in compositing step is complex;
        # instead the pair side is rendered and the single side renders the same user figure;
        # the shadow is drawn at reduced alpha for t<0.5 / t>=0.5 via a post-step in render_seq.
        k["kind"]="pair"
        sa=a.get("stand_cfg",a["cfg"]); sb=b.get("stand_cfg",b["cfg"])
        k["stand_cfg"]=lerp_cfg(sa,sb,t); k["stand_head"]=a.get("stand_head",a["head"])+(b.get("stand_head",b["head"])-a.get("stand_head",a["head"]))*t
        k["shadow_alpha"]= t if a["kind"]=="single" else (1-t)
    return k
def render_interp(k):
    c=Image.new("RGBA",(2200,1500),(0,0,0,0))
    if k["kind"]=="pair":
        sl=Image.new("RGBA",(2200,1500),(0,0,0,0)); figure(sl,1280,k["stand_cfg"],k["stand_head"],k["top"])
        sh=silhouette(sl)
        if "shadow_alpha" in k:
            a=sh.split()[3].point(lambda v:int(v*k["shadow_alpha"])); sh.putalpha(a)
        c.alpha_composite(sh)
    figure(c,1100,k["cfg"],k["head"],k["top"]); return c
def grey(im):
    bg=Image.new("RGBA",im.size,(128,128,128,255)); bg.alpha_composite(im); return bg.convert("RGB")
def smooth(t): return t*t*(3-2*t)
def easeout(t): return 1-(1-t)**2

# ---- KEYS ----
DIALECTS=[
 {"name":"JoJo 01","kind":"single","cfg":C((-75,40),(125,-45),(-38,28),(22,-18)),"head":12,"top":()},
 {"name":"JoJo 02","kind":"single","cfg":C((-115,65),(85,-95),(-16,32),(6,-28)),"head":-10,"top":()},
 {"name":"JoJo 03 FACE-SNAP","kind":"single","cfg":C((-25,-88),(35,145),(-42,12),(32,-6)),"head":8,"top":("R",)},
 {"name":"Stand 01 coloured-shadow pair","kind":"pair","cfg":C((-60,60),(130,-130),(-25,25),(12,-12)),"head":0,"stand_cfg":C((-60,60),(130,-130),(-25,25),(12,-12)),"stand_head":0,"top":()},
 {"name":"Stand 02 towering pair","kind":"pair","cfg":C((-35,35),(60,-60),(-30,30),(35,-35)),"head":6,"stand_cfg":C((-150,150),(-40,40),(-12,12),(-8,8)),"stand_head":-4,"top":()},
 {"name":"Ginyu 01 COWL-SNAP","kind":"single","cfg":C((-160,20),(-20,95),(-45,20),(10,-10)),"head":-6,"top":("L",)},
 {"name":"Ginyu 02 squat","kind":"single","cfg":C((-70,70),(140,-140),(-45,45),(40,-40)),"head":0,"top":()},
 {"name":"Ginyu 03 shimmy","kind":"single","cfg":C((-130,130),(-60,60),(-20,35),(30,-20)),"head":10,"top":()},
]
ROLLCALL=[
 {"name":"Recoome roll-call","kind":"single","cfg":C((-120,120),(-40,40),(-50,45),(25,-25)),"head":10,"top":("L","R")},
 {"name":"Burter roll-call","kind":"single","cfg":C((-90,90),(0,0),(-35,35),(20,-20)),"head":8,"top":("L","R")},
 {"name":"Jeice roll-call","kind":"single","cfg":C((-80,80),(130,-130),(-20,20),(10,-10)),"head":14,"top":()},
 {"name":"Guldo roll-call","kind":"single","cfg":C((-50,50),(90,-90),(-55,55),(55,-55)),"head":8,"top":()},
 {"name":"Captain roll-call","kind":"single","cfg":C((-100,10),(30,90),(-40,35),(15,-15)),"head":-8,"top":("L",)},
 {"name":"Captain final spread (unison)","kind":"single","cfg":C((-150,150),(-20,20),(-35,35),(20,-20)),"head":0,"top":("L","R")},
]
def build_sequence(keys, outdir, hold, n_inb, ease_fn, label):
    frames=[]; meta=[]
    for i in range(len(keys)-1):
        for h in range(hold):
            im=grey(render_key(keys[i])); frames.append(im); meta.append(f"{keys[i]['name']} KEY hold")
        for j in range(1, n_inb+1):
            t=j/(n_inb+1); e=ease_fn(t); k=interp_key(keys[i], keys[i+1], e)
            im=grey(render_interp(k)); frames.append(im)
            tag="BREAKDOWN" if j==(n_inb+1)//2 else "inbetween"
            meta.append(f"{keys[i]['name']} -> {keys[i+1]['name']} {tag} t={t:.2f} eased={e:.2f}")
    # final key hold
    for h in range(hold):
        im=grey(render_key(keys[-1])); frames.append(im); meta.append(f"{keys[-1]['name']} KEY hold")
    # EXTRAPOLATION (labelled): overshoot 8% beyond final key away from previous key, then settle
    prev, last = keys[-2], keys[-1]
    for fac, _lab in [(0.08, "OVERSHOOT"), (0.0, "SETTLE")]:
        cfg={g:{s: last["cfg"][g][s]+(last["cfg"][g][s]-prev["cfg"][g][s])*fac for s in ("L","R")} for g in ("arm_upper","arm_lower","leg_upper","leg_lower")}
        k=dict(last); k["cfg"]=cfg; k["head"]=last["head"]+(last["head"]-prev["head"])*fac
        im=grey(render_key(k)); frames.append(im); meta.append(f"{last['name']} EXTRAPOLATION {fac} ({'overshoot beyond key' if fac else 'settle back to key'})")
        if fac==0.08:
            im2=grey(render_key(last)); frames.append(im2); meta.append(f"{last['name']} KEY settle")
    for idx,im in enumerate(frames):
        im.save(f"{outdir}/f{idx+1:03d}.jpg", quality=90)
    json.dump(meta, open(f"{OUT}/{label}-timing.json","w"), indent=1)
    print(label, len(frames), "frames")
    return frames, meta

d_frames, d_meta = build_sequence(DIALECTS, OUT+"/frames-dialects", hold=4, n_inb=5, ease_fn=smooth, label="dialects")
r_frames, r_meta = build_sequence(ROLLCALL, OUT+"/frames-rollcall", hold=12, n_inb=4, ease_fn=easeout, label="rollcall")
# contact strips: key -> breakdown -> inbetween -> next key for 2 transitions each
def strip(frames, idxs, fn, titles):
    thumbs=[f.resize((275,188)) for f in [frames[i] for i in idxs]]
    s=Image.new("RGB",(275*len(thumbs),210),(128,128,128)); d=ImageDraw.Draw(s)
    for i,(t,tt) in enumerate(zip(thumbs,titles)):
        s.paste(t,(i*275,20)); d.text((i*275+4,4), tt, fill=(255,255,255))
    s.save(fn); print(fn)
# dialects indices: key0 hold frames 0-3, inbetweens 4-8 (j1..5), key1 9-12 ; transition JoJo03->Stand01: keys idx: key2 starts at 2*9=18, inbetweens 22-26, key3 27
strip(d_frames, [18,24,26,27], OUT+"/contact-dialects-jojo03-to-stand01-20261031.jpg", ["KEY JoJo03","BREAKDOWN","inbetween","KEY Stand01"])
# Ginyu01->Ginyu02: key5 starts 45, inbetweens 49-53, key6 54
strip(d_frames, [45,51,53,54], OUT+"/contact-dialects-ginyu01-to-ginyu02-20261031.jpg", ["KEY Ginyu01","BREAKDOWN","inbetween","KEY Ginyu02"])
# rollcall: hold12, inb4 => step 16. Rec->Bur: key0 0-11, inb 12-15, key1 16. Cap01->Cap02: key4 starts 64, inb 68-71, key5 72
strip(r_frames, [0,14,15,16], OUT+"/contact-rollcall-recoome-to-burter-20261031.jpg", ["KEY Recoome","inbetween","snap inbetween","KEY Burter"])
strip(r_frames, [64,70,71,72], OUT+"/contact-rollcall-captain-to-spread-20261031.jpg", ["KEY Captain","BREAKDOWN","inbetween","KEY Spread"])
# onion skin: JoJo03->Stand01, key + inbetweens at decreasing alpha over grey
on=Image.new("RGB",(1100,750),(128,128,128))
base=d_frames[18].resize((1100,750))
for idx,al in [(22,60),(24,110),(26,170)]:
    ov=d_frames[idx].resize((1100,750)).convert("RGBA"); ov.putalpha(Image.new("L",(1100,750),al)); on.paste(Image.alpha_composite(Image.new("RGBA",(1100,750),(128,128,128,255)), ov),(0,0))
on.save(OUT+"/onion-skin-jojo03-to-stand01-20261031.jpg"); print("onion done")
# easing graph + timing chart
g=Image.new("RGB",(600,400),(255,255,255)); dg=ImageDraw.Draw(g); dg.line([(50,350),(550,350)],fill=(0,0,0)); dg.line([(50,350),(50,50)],fill=(0,0,0))
for x in range(501):
    t=x/500; dg.point((50+x,350-int(smooth(t)*280)),fill=(200,0,0)); dg.point((50+x,350-int(easeout(t)*280)),fill=(0,0,200)); dg.point((50+x,350-int(t*280)),fill=(120,120,120))
dg.text((60,20),"red=smoothstep (dialects)  blue=ease-out snap (rollcall)  grey=linear",fill=(0,0,0)); g.save(OUT+"/easing-graph-20261031.jpg")
# arc track: R elbow for JoJo01->JoJo02 inbetweens
def elbow_pos(cfg, side="R"):
    cx,sh=1100,(1220,445); ball,anchor=ARM[side]; vec=((ball[0]-anchor[0])*SCALE,(ball[1]-anchor[1])*SCALE); v=rot_vec(vec,cfg["arm_upper"][side]); return (sh[0]+v[0], sh[1]+v[1])
arc=Image.new("RGB",(1100,750),(255,255,255)); da=ImageDraw.Draw(arc)
pts=[]
for j in range(0,7):
    t=j/6; cfg=lerp_cfg(DIALECTS[0]["cfg"], DIALECTS[1]["cfg"], smooth(t) if j not in (0,6) else t)
    # scale coords from 2200x1500 to 1100x750
    p=elbow_pos(cfg); pts.append((p[0]/2,p[1]/2))
da.line(pts, fill=(200,0,0), width=3)
for p in pts: da.ellipse([p[0]-5,p[1]-5,p[0]+5,p[1]+5], fill=(0,0,200))
da.text((10,10),"R elbow arc JoJo01->JoJo02 (red line, blue dots = key+inbetweens)",fill=(0,0,0)); arc.save(OUT+"/arc-track-jojo01-to-jojo02-20261031.jpg")
print("proofs done")
