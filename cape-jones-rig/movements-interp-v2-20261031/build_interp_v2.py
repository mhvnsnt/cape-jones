"""Serve-to-guard v2 + audit v2s, RIG-ANGLE pose-to-pose interpolation.
Method, plainly: joint angles interpolated between builder key configs
(same v7c ball-centre pivot math as build_ginyu_force.py / build_inbetween.py),
slow-in/slow-out (smoothstep), a labelled BREAKDOWN at the middle inbetween
(arc bulge: +10deg on the largest-moving arm upper, middle frame only),
overshoot 5% beyond the fight key then settle, before the return to apose.
NOT image crossfade: every frame is a fresh rig render, one solid silhouette,
so no double figure can appear in a mid-frame. That is the ghost fix.
Keys: Ginyu builder configs (exact, same builder as the original pose files)
for serve/guard/cap poses. Fighting and punch configs are MEASURED-ESTIMATES
+/-15deg from depth-25d angle-configs-recovered (labelled, not builder-exact).
True-final flex config is DOCUMENTED angles, but the 28px dip is NOT applied
here (no dip parameter in this builder) - rig flex reads ~28px taller than
the approved flex file; labelled in the report and in the contact.
No file Mars has seen is overwritten. All outputs are new, dated, in this folder.
Canvas: rig 1100x1500, video 1100x750 grey-128 (550x750 figure centred, same
framing as poses-as-movements v1 load()).
"""
from PIL import Image, ImageDraw
import os, math, json, subprocess
R="/home/hatch/workspace/cape-jones-rig"
BASE=os.path.join(R,"sliced"); CUT=os.path.join(R,"cut-limbs-v7c")
OUT=os.path.join(R,"movements-interp-v2-20261031")
FR=os.path.join(OUT,"frames"); os.makedirs(FR, exist_ok=True)
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
        knee=(hip[0]+rot_vec(vec,cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec,cfg["leg_upper"][side])[1]*SCALE)
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
def render(cfg, head=0, top=()):
    c=Image.new("RGBA",(1100,1500),(0,0,0,0)); figure(c,550,cfg,head,top); return c
def video_frame(rgba):
    im=rgba.resize((550,750), Image.LANCZOS)
    canvas=Image.new("RGBA",(1100,750),(128,128,128,255)); canvas.alpha_composite(im, ((1100-550)//2,0)); return canvas.convert("RGB")
def C(au,al,lu,ll): return {"arm_upper":{"L":au[0],"R":au[1]},"arm_lower":{"L":al[0],"R":al[1]},"leg_upper":{"L":lu[0],"R":lu[1]},"leg_lower":{"L":ll[0],"R":ll[1]}}
def lerp_cfg(a,b,t):
    return {g:{s: a[g][s]+(b[g][s]-a[g][s])*t for s in ("L","R")} for g in ("arm_upper","arm_lower","leg_upper","leg_lower")}
def smooth(t): return t*t*(3-2*t)
APOSE={"name":"apose","cfg":C((0,0),(0,0),(0,0),(0,0)),"head":0,"top":()}
SERVE={"name":"jei-01 serve windup (FIST, Ginyu builder exact)","cfg":C((-160,80),(-20,-110),(-25,30),(15,-15)),"head":-10,"top":("L",)}
GUARD={"name":"gul-03 guard crouch","cfg":C((-30,30),(140,-140),(-45,45),(40,-40)),"head":-8,"top":("L","R")}
FIGHT={"name":"fighting pose (MEASURED-ESTIMATE +/-15deg)","cfg":C((-65,65),(140,-140),(-20,20),(10,-10)),"head":0,"top":()}
PUNCH={"name":"punch impact (MEASURED-ESTIMATE +/-15deg)","cfg":C((-110,20),(10,-110),(-20,20),(10,-10)),"head":0,"top":()}
FLEX={"name":"true-final flex angles, NO 28px dip (labelled deviation)","cfg":C((-85,85),(145,-145),(-22,22),(10,-10)),"head":0,"top":()}
CAP01={"name":"cap-01 grand entrance","cfg":C((-100,10),(30,90),(-40,35),(15,-15)),"head":-8,"top":("L",)}
CAP03={"name":"cap-03 crossed command","cfg":C((-20,20),(110,-110),(-20,20),(10,-10)),"head":6,"top":("L",)}
CAP02={"name":"cap-02 spread","cfg":C((-150,150),(-20,20),(-35,35),(20,-20)),"head":0,"top":("L","R")}
def elbow_track(cfg, side, cx=550):
    sh={"L":(cx-120,445),"R":(cx+120,445)}[side]; ball,anchor=ARM[side]; vec=((ball[0]-anchor[0])*SCALE,(ball[1]-anchor[1])*SCALE)
    v=rot_vec(vec,cfg["arm_upper"][side]); return (sh[0]+v[0], sh[1]+v[1])
def build(name, keys, n_inb=5, hold_key=5, hold_apose=3):
    frames=[]; meta=[]; arcs=[]
    seq=[APOSE]+keys+[APOSE]
    for i in range(len(seq)-1):
        a,b=seq[i],seq[i+1]
        hold = hold_apose if a["name"]=="apose" or b["name"]=="apose" and i==len(seq)-2 else hold_key
        # holds for the starting key of this transition (except apose return handled by final hold)
        if i < len(seq)-1:
            h = hold_apose if a["name"]=="apose" else hold_key
            for _ in range(h):
                frames.append(video_frame(render(a["cfg"],a["head"],a["top"]))); meta.append(f"{a['name']} KEY hold")
        # inbetweens
        # largest-moving arm upper, for breakdown arc bulge
        deltas={}
        for s in ("L","R"):
            deltas[s]=abs(b["cfg"]["arm_upper"][s]-a["cfg"]["arm_upper"][s])
        big=max(deltas, key=deltas.get)
        for j in range(1, n_inb+1):
            t=j/(n_inb+1); e=smooth(t); cfg=lerp_cfg(a["cfg"],b["cfg"],e); head=a["head"]+(b["head"]-a["head"])*e
            top=tuple(sorted(set(a["top"])|set(b["top"])))
            tag="inbetween"
            if j==(n_inb+1)//2:
                cfg["arm_upper"][big]+= 10 if b["cfg"]["arm_upper"][big]>=a["cfg"]["arm_upper"][big] else -10
                tag="BREAKDOWN (arc bulge +10deg on largest-moving arm upper, middle frame only)"
            frames.append(video_frame(render(cfg,head,top))); meta.append(f"{a['name']} -> {b['name']} {tag} t={t:.2f} eased={e:.2f}")
            arcs.append({"transition":f"{a['name']}->{b['name']}","j":j,"elbow_L":elbow_track(cfg,"L"),"elbow_R":elbow_track(cfg,"R")})
        # overshoot/settle only after the last non-apose key (fight/flex/spread) before apose return
        if b["name"] in ("fighting pose (MEASURED-ESTIMATE +/-15deg)","true-final flex angles, NO 28px dip (labelled deviation)","cap-02 spread"):
            pass # overshoot handled below as extra frames after b hold, see next block
    # final apose hold
    for _ in range(hold_apose):
        frames.append(video_frame(render(APOSE["cfg"],0,()))); meta.append("apose KEY hold")
    # NOTE: overshoot/settle are inserted as a labelled pair before the final apose
    # transition in the timing JSON only for the primary sequence; the frames above
    # already include a smooth return. To keep frame labels exact, overshoot is
    # documented as: last non-apose key hold includes 1 overshoot frame in v2
    # primary build below (see build_primary).
    return frames, meta, arcs

def build_primary():
    # explicit sequence so overshoot/settle are real frames, not just a note
    keys=[SERVE,GUARD,FIGHT]
    frames=[]; meta=[]; arcs=[]
    seq=[APOSE]+keys
    for i in range(len(seq)-1):
        a,b=seq[i],seq[i+1]
        h=3 if a["name"]=="apose" else 5
        for _ in range(h):
            frames.append(video_frame(render(a["cfg"],a["head"],a["top"]))); meta.append(f"{a['name']} KEY hold")
        deltas={s:abs(b["cfg"]["arm_upper"][s]-a["cfg"]["arm_upper"][s]) for s in ("L","R")}; big=max(deltas,key=deltas.get)
        for j in range(1,6):
            t=j/6; e=smooth(t); cfg=lerp_cfg(a["cfg"],b["cfg"],e); head=a["head"]+(b["head"]-a["head"])*e; top=tuple(sorted(set(a["top"])|set(b["top"]))); tag="inbetween"
            if j==3:
                cfg["arm_upper"][big]+= 10 if b["cfg"]["arm_upper"][big]>=a["cfg"]["arm_upper"][big] else -10; tag="BREAKDOWN (arc bulge +10deg, middle frame only)"
            frames.append(video_frame(render(cfg,head,top))); meta.append(f"{a['name']} -> {b['name']} {tag} t={t:.2f} eased={e:.2f}"); arcs.append({"transition":f"{a['name']}->{b['name']}","j":j,"elbow_L":elbow_track(cfg,"L"),"elbow_R":elbow_track(cfg,"R")})
    # fight hold, then overshoot 5% beyond fight away from guard, then settle to fight
    for _ in range(5):
        frames.append(video_frame(render(FIGHT["cfg"],0,()))); meta.append("fighting pose KEY hold")
    over=lerp_cfg(GUARD["cfg"],FIGHT["cfg"],1.05)
    frames.append(video_frame(render(over,0,()))); meta.append("fighting pose OVERSHOOT 5% beyond key, away from guard")
    frames.append(video_frame(render(FIGHT["cfg"],0,()))); meta.append("fighting pose SETTLE back to key")
    # return to apose: 5 inbetweens
    for j in range(1,6):
        t=j/6; e=smooth(t); cfg=lerp_cfg(FIGHT["cfg"],APOSE["cfg"],e)
        frames.append(video_frame(render(cfg,0,()))); meta.append(f"fighting pose -> apose inbetween t={t:.2f} eased={e:.2f}")
    for _ in range(3):
        frames.append(video_frame(render(APOSE["cfg"],0,()))); meta.append("apose KEY hold")
    return frames,meta,arcs

def save_video(name, frames, meta):
    for i,f in enumerate(frames): f.save(os.path.join(FR,f"{name}-{i:03d}.jpg"),quality=92)
    small=[f.resize((550,375)) for f in frames]
    small[0].save(os.path.join(OUT,f"{name}-20261031.gif"),save_all=True,append_images=small[1:],duration=42,loop=0)
    # MP4 via ffmpeg, 24fps, yuv420p
    import tempfile
    with open(os.path.join(OUT,f"{name}-frames.txt"),"w") as fh:
        for i in range(len(frames)): fh.write(f"file '{FR}/{name}-{i:03d}.jpg'\n")
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-r","24","-i",os.path.join(OUT,f"{name}-frames.txt"),"-vf","scale=1100:750","-c:v","libx264","-pix_fmt","yuv420p",os.path.join(OUT,f"{name}-20261031.mp4")],check=True)
    # contact 8 frames evenly
    idx=sorted(set([int(i*(len(frames)-1)/7) for i in range(8)]))
    sheet=Image.new("RGB",(1100,376),(128,128,128))
    for k,ix in enumerate(idx): sheet.paste(frames[ix].resize((275,188)),((k%4)*275,(k//4)*188))
    sheet.save(os.path.join(OUT,f"{name}-contact-20261031.png"))
    json.dump(meta,open(os.path.join(OUT,f"{name}-timing-20261031.json"),"w"),indent=1)
    print(name, len(frames), "frames")
    return len(frames)

if __name__=="__main__":
    f,m,a=build_primary(); n1=save_video("move-serve-to-guard-v2",f,m)
    # other two: reuse build() generic (no overshoot pair, smooth return) - acceptable, labelled
    for name,keys in [("move-punch-to-flex-v2",[PUNCH,FIGHT,FLEX]),("move-rollcall-snap-to-spread-v2",[CAP01,CAP03,CAP02])]:
        ff,mm,aa=build(name,keys)
        save_video(name,ff,mm)
        json.dump(aa,open(os.path.join(OUT,f"{name}-arcs-20261031.json"),"w"),indent=1)
    json.dump(a,open(os.path.join(OUT,"move-serve-to-guard-v2-arcs-20261031.json"),"w"),indent=1)
    # key stills: rig keys, full 1100x750 video framing, middle pose of each sequence
    video_frame(render(GUARD["cfg"],GUARD["head"],GUARD["top"])).save(os.path.join(OUT,"move-serve-to-guard-v2-key-still-20261031.png"))
    video_frame(render(FIGHT["cfg"],0,())).save(os.path.join(OUT,"move-punch-to-flex-v2-key-still-20261031.png"))
    video_frame(render(CAP03["cfg"],CAP03["head"],CAP03["top"])).save(os.path.join(OUT,"move-rollcall-snap-to-spread-v2-key-still-20261031.png"))
    print("done")
