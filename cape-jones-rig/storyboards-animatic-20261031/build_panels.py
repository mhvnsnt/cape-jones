"""Drawn storyboard panels 30/30 + index + animatic frames.
Panel 1920x1440: picture 1920x1200 + caption 240. Base art never recoloured:
poses pasted as-is; annotations are a separate overlay layer (yellow arrows/
badge), captions are text below the picture, never over base art.
No-crop: picture canvas auto-fits the full pose (pose trimmed only to its own
alpha bbox + margin); room panels use 3.0x lock: standing displayed height
1140px (950px at 2.5x -> 1140px at 3.0x, same linear lock definition)."""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os, json
RIG="/home/hatch/workspace/cape-jones-rig"; D=os.path.join(RIG,"storyboards-animatic-20261031")
POSES=os.path.join(D,"poses"); PANELS=os.path.join(D,"panels"); os.makedirs(PANELS, exist_ok=True)
def font(sz, bold=True):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try: return ImageFont.truetype(p, sz)
    except Exception: return ImageFont.load_default()
FB=font(54); F=font(34); FS=font(28)
PW,PH=1920,1200; W,H=1920,1440
def cover(im, w, h):
    im=im.convert("RGB"); r=max(w/im.size[0], h/im.size[1]); im=im.resize((int(im.size[0]*r+0.5), int(im.size[1]*r+0.5)), Image.LANCZOS)
    x=(im.size[0]-w)//2; y=(im.size[1]-h)//2; return im.crop((x,y,x+w,y+h))
def standin(label):
    im=Image.new("RGB",(PW,PH),(42,42,48)); d=ImageDraw.Draw(im)
    d.text((60,1100), label, fill=(200,200,210), font=FS)
    d.text((60,1140), "STAND-IN PLATE — final painted background owed", fill=(160,160,170), font=FS)
    return im
def neutral(label="NEUTRAL / ANY (stand-in)"):
    return standin(label)
BG={
 "street": ("standin","STREET (stand-in)"), "town": ("standin","TOWN (stand-in)"),
 "alley": ("painted","clean-100-20261031/layouts/bg-alley-painted-20261031.jpg"),
 "flying": ("painted","clean-100-20261031/layouts/bg-flying-painted-20261031.jpg"),
 "rooftop": ("painted","clean-100-20261031/layouts/bg-rooftop-painted-20261031.jpg"),
 "desk": ("painted","clean-100-20261031/layouts/bg-desk-painted-20261031.jpg"),
 "skyline": ("standin","SKYLINE / SKY (stand-in)"), "stage": ("standin","STAGE / STREET (stand-in)"),
 "room": ("standin","LOUNGE ROOM (stand-in — final lounge plate owed)"), "any": ("standin","ANY (stand-in)"),
}
# shot: slug, pose file (None=CJ26 composite), bg key, action, camera framing, duration, audio, lighting/LUT, special
SHOTS=[
 ("CJ-01","punch-windup","CJ-01-punch-windup-pose-20261031.png","street","Punch windup — arm pulled back, fist cocked","Full figure, eye level",6,"CJ-A01","Level 2 / golden-hour",""),
 ("CJ-02","punch-extend-snap","CJ-02-punch-extend-snap-pose-20261031-v2.png","street","Punch extend — SNAP, arm straight out","Full figure, eye level",2,"CJ-A02","Level 2 / golden-hour","v2 wide canvas: fist unclipped"),
 ("CJ-03","punch-impact-locked","CJ-03-punch-impact-locked-pose-20261031-v2.png","street","Punch impact — HOLD, locked frame","Full figure, eye level",12,"CJ-A03","Level 2 / golden-hour + FX passes","Locked impact frame (Mars 15:33); shot itself pending Mars look"),
 ("CJ-04","punch-recover","CJ-04-punch-recover-pose-20261031.png","street","Punch recover — back to ready, base palette restored","Full figure, eye level",6,"CJ-A04","Level 2 / golden-hour (base)","Return-to-base beat"),
 ("CJ-05","punch-across-down-placement","CJ-05-punch-across-down-pose-20261031-v2.png","street","Arm2 across-down placement — forearm down across belly, fist low centre","Full figure, eye level",12,"CJ-A05","Level 2 / daylight","Scene placement, NOT the impact frame"),
 ("CJ-06","walk-street-contact","CJ-06-walk-street-contact-pose-20261031.png","street","Walk contact — leg1 forward","Full figure, eye level",12,"CJ-A06","Level 2 / daylight",""),
 ("CJ-07","walk-town-passing","CJ-07-walk-town-passing-pose-20261031.png","town","Walk passing — legs together mid-stride","Full figure, eye level",12,"CJ-A07","Level 2 / golden-hour",""),
 ("CJ-08","walk-alley-night","CJ-08-walk-alley-night-pose-20261031.png","alley","Walk cycle, alley at night","Full figure, eye level",12,"CJ-A08","Level 2 / night-city","Cool key only"),
 ("CJ-09","dance-a","CJ-09-dance-a-pose-20261031.png","stage","Dance A — first half of loop","Full figure, eye level",12,"CJ-A09","Level 2 / magenta-normal",""),
 ("CJ-10","dance-b","CJ-10-dance-b-pose-20261031.png","stage","Dance B — second half of loop","Full figure, eye level",12,"CJ-A10","Level 2 / pink-normal",""),
 ("CJ-11","dance-combined-finale","CJ-11-dance-combined-finale-pose-20261031.png","stage","Dance combined finale — BOTH arms up","Full figure, eye level",12,"CJ-A11","Level 3 / violet-magenta-normal","Combined A+B finale pose (storyboard)"),
 ("CJ-12","flying-hover","CJ-12-flying-hover-pose-20261031.png","flying","Flying hover — held in air","Full figure, eye level",12,"CJ-A12","Level 3 / golden-hour","Airborne — feet off floor line"),
 ("CJ-13","flying-soar","CJ-13-flying-soar-pose-20261031-v2.png","flying","Flying soar — arms out wide","Full figure, eye level",12,"CJ-A13","Level 3 / desert-sun","v2 wide canvas: both fists unclipped"),
 ("CJ-14","flying-dive","CJ-14-flying-dive-pose-20261031.png","flying","Flying dive — arms up, diving","Full figure, eye level",12,"CJ-A14","Level 3 / warm-sunset","Airborne"),
 ("CJ-15","flying-forward-foreshortened","CJ-15-flying-forward-foreshortened-pose-20261031-v3.png","flying","Flying FORWARD at camera — near arm enlarged 1.7x","Full figure, eye level",12,"CJ-A15","Level 2 / cyan-blue-normal","STORYBOARD indication only — final foreshortened forearm piece still owed per spec"),
 ("CJ-16","flex-anticipation-before-tighten","CJ-16-flex-anticipation-pose-20261031.png","any","Flex anticipation — before the tighten","Full figure, eye level",12,"CJ-A16","Level 2 / orange-normal","Anticipation frame, NOT final flex"),
 ("CJ-17","arms-up-reference","CJ-17-arms-up-reference-pose-20261031.png","any","Arms-up reference — arms up-out (NOT a flex)","Full figure, eye level",12,"CJ-A17","Level 2 / yellow-normal","Reference pose family for CJ-20"),
 ("CJ-18","true-flex-double-bicep","CJ-18-true-flex-double-bicep-pose-20261031.png","any","True flex — double bicep, fists in","Full figure, eye level",12,"CJ-A18","Level 2 / red-orange-normal","STORYBOARD pose — final flex shot still spec-only per shot spec"),
 ("CJ-19","fighting-pose-forward-bicep-curl","CJ-19-fighting-curl-pose-20261031.png","any","Fighting pose — forward bicep curl","Full figure, eye level",12,"CJ-A19","Level 3 dual-light / golden-hour","Dual-light: both sources named in spec"),
 ("CJ-20","fighting-stance-arms-up-high","CJ-20-fighting-stance-arms-up-high-pose-20261031.png","any","Fighting stance — arms up HIGH, legs wide","Full figure, eye level",12,"CJ-A20","Level 2 / fire","Uses CJ-17 arms-up family"),
 ("CJ-21","jump-crouch-takeoff","CJ-21-jump-crouch-takeoff-pose-20261031.png","rooftop","Jump crouch / takeoff","Full figure, eye level",6,"CJ-A21","Level 2 / teal-normal",""),
 ("CJ-22","jump-tuck-landing","CJ-22-jump-tuck-landing-pose-20261031.png","rooftop","Jump tuck / landing","Full figure, eye level",12,"CJ-A22","Level 3 / golden-hour","Airborne tuck"),
 ("CJ-23","lounge-seated-room","CJ-23-lounge-seated-room-pose-20261031.png","room","Lounge seated in room (3.0x room scale)","Full figure, eye level",12,"CJ-A23","Level 2 / warm-interior","ROOM 3.0x: seated at standing-equivalent scale"),
 ("CJ-24","desk-seated","CJ-24-desk-seated-pose-20261031.png","desk","Desk seated","Full figure, eye level",12,"CJ-A24","Level 2 / warm-lamp","Desk plate is painted; final painted desk owed per spec"),
 ("CJ-25","room-standing-device-gag","CJ-25-room-standing-device-pose-20261031.png","room","Room standing — device gag (device: see prop sheet)","Full figure, eye level",12,"CJ-A25","Level 2 / warm-interior","ROOM 3.0x standing (1140px tall in panel)"),
 ("CJ-26","dialogue-neutral-unsure",None,"room","Dialogue — neutral / unsure [line: Mars to fill post-episode]","Full figure, eye level",12,"CJ-A26","Level 2 / natural-window-light","Existing dialogue composite (gap-close-tv); dialogue text post-episode per Space Ghost workflow"),
 ("CJ-27","dialogue-shout-angry","CJ-27-dialogue-shout-angry-pose-20261031-v2.png","room","Dialogue — SHOUT, angry [line: Mars to fill post-episode]","Full figure, eye level",12,"CJ-A27","Level 2 / red-alert","ROOM 3.0x standing; angry eyes + shout mouth overlay (pieces only)"),
 ("CJ-28","rooftop-sunset","CJ-28-rooftop-sunset-pose-20261031.png","rooftop","Rooftop at sunset","Full figure, eye level",12,"CJ-A28","Level 3 / sunset-rooftop",""),
 ("CJ-29","rooftop-night-city","CJ-29-rooftop-night-city-pose-20261031.png","rooftop","Rooftop at night, city behind","Full figure, eye level",12,"CJ-A29","Level 3 / night-city","Cool family only"),
 ("CJ-30","alley-neon-dual-light","CJ-30-alley-neon-dual-light-pose-20261031.png","alley","Alley neon — dual light","Full figure, eye level",12,"CJ-A30","Level 3 dual-light / neon-alley-pink-cyan","Dual-light: both sources named in spec"),
]
def arrow(d, x, y, dx, dy):
    d.line((x,y,x+dx,y+dy), fill=(255,220,0), width=10)
    d.polygon([(x+dx,y+dy),(x+dx-dx*0.25-dy*0.18,y+dy-dy*0.25+dx*0.18),(x+dx-dx*0.25+dy*0.18,y+dy-dy*0.25-dx*0.18)], fill=(255,220,0))
manifest=[]
for sid, slug, posefile, bgkey, action, camera, dur, audio, light, special in SHOTS:
    kind, bgval = BG[bgkey]
    if kind=="painted": pic=cover(Image.open(os.path.join(RIG,bgval)), PW, PH)
    else: pic=standin(bgval)
    pic=pic.convert("RGB")
    if sid=="CJ-26":
        comp=Image.open(os.path.join(RIG,"gap-close-tv-20261031/dialogue-shot-cj26-neutral-ah-20261031.png")).convert("RGB")
        comp.thumbnail((PW,PH), Image.LANCZOS)
        base=Image.new("RGB",(PW,PH),(20,20,24)); base.paste(comp,((PW-comp.size[0])//2,(PH-comp.size[1])//2)); pic=base
        char_h=None; bg_status="EXISTING COMPOSITE (gap-close-tv)"
    else:
        pose=Image.open(os.path.join(POSES,posefile)).convert("RGBA")
        room = bgkey=="room"
        if room:
            # 3.0x: standing displayed height 1140; scale factor from standing rig reference 1059
            scale=1140/1059.0; disp_h=int(pose.size[1]*scale); disp_w=int(pose.size[0]*scale)
            pose_r=pose.resize((disp_w,disp_h), Image.LANCZOS)
            x=(PW-disp_w)//2; y=1170-disp_h
        elif sid in ("CJ-12","CJ-14","CJ-22"):
            disp_h=950; disp_w=int(pose.size[0]*disp_h/pose.size[1]); pose_r=pose.resize((disp_w,disp_h), Image.LANCZOS)
            x=(PW-disp_w)//2; y=(PH-disp_h)//2-40
        else:
            disp_h=1000; disp_w=int(pose.size[0]*disp_h/pose.size[1]); pose_r=pose.resize((disp_w,disp_h), Image.LANCZOS)
            x=(PW-disp_w)//2; y=1125-disp_h
        # clamp: never crop pose — if wider than picture, shrink to fit width
        if disp_w>PW-40:
            disp_w=PW-40; disp_h=int(pose.size[1]*disp_w/pose.size[0]); pose_r=pose.resize((disp_w,disp_h), Image.LANCZOS)
            x=20; y=1125-disp_h if sid not in ("CJ-12","CJ-14","CJ-22") else (PH-disp_h)//2-40
        pic.paste(pose_r,(x,y),pose_r); char_h=disp_h
        bg_status="PAINTED PLATE" if kind=="painted" else "STAND-IN PLATE"
    d=ImageDraw.Draw(pic)
    # badge + annotation (overlay layer only)
    d.rectangle((30,30,330,110), fill=(0,0,0)); d.text((50,48), sid, fill=(255,220,0), font=FB)
    if sid in ("CJ-02","CJ-03"): arrow(d, 420, 420, -260, 0)
    if sid in ("CJ-12","CJ-13","CJ-14","CJ-15"):
        for yy in (500,620,740): d.line((150,yy,420,yy), fill=(255,220,0), width=8)
    if sid=="CJ-15": d.text((60,1120), ">> TOWARD CAMERA", fill=(255,220,0), font=F)
    if sid=="CJ-27": d.text((1450,200), "SHOUT!", fill=(255,220,0), font=FB)
    panel=Image.new("RGB",(W,H),(17,17,20)); panel.paste(pic,(0,0))
    d2=ImageDraw.Draw(panel)
    d2.text((40,1225), f"{sid} — {slug}", fill=(255,220,0), font=F)
    y=1290
    for line in textwrap.wrap(f"{action}  |  {camera}  |  {dur}f @24fps  |  Audio {audio}  |  {light}", width=105)[:2]:
        d2.text((40,y), line, fill=(255,255,255), font=FS); y+=34
    note=f"STORYBOARD — NOT FINAL SHOT  |  BG: {bg_status}" + (f"  |  {special}" if special else "")
    for line in textwrap.wrap(note, width=105)[:2]:
        d2.text((40,y), line, fill=(180,180,190), font=FS); y+=34
    name=f"panel-{sid}-{slug}-20261031.png"; panel.save(os.path.join(PANELS,name))
    manifest.append({"shot":sid,"slug":slug,"panel":name,"pose":posefile,"bg":bgkey,"bg_status":bg_status,"duration_frames":dur,"audio":audio,"lighting":light,"char_display_height":char_h,"special":special})
    print(name, panel.size, "char_h", char_h, bg_status)
json.dump(manifest, open(os.path.join(D,"panels-manifest-20261031.json"),"w"), indent=1)
print("panels", len(manifest))
