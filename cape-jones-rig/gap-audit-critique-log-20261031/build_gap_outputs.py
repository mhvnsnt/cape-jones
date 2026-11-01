from PIL import Image, ImageDraw, ImageFont
import os, json
R="/home/hatch/workspace/cape-jones-rig"
O=os.path.join(R,"gap-audit-critique-log-20261031")
def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
def sil(path, size=(300,410)):
    im=Image.open(path).convert("RGBA")
    if im.mode=="RGBA" and path.endswith("transparent.png"):
        mask=im.split()[3]
    else:
        # grey-128 bg
        px=im.convert("RGB"); m=Image.new("L",im.size,0); d=ImageDraw.Draw(m)
        # vectorised-ish via point on luminance diff
        import numpy as np
        a=np.array(px).astype(int)
        diff=np.abs(a-np.array([128,128,128])).sum(axis=2)
        m=Image.fromarray((diff>60).astype('uint8')*255)
        mask=m
    out=Image.new("RGBA",size,(0,0,0,0))
    # crop to bbox of mask
    bbox=mask.getbbox()
    if bbox:
        crop=im.crop(bbox); mk=mask.crop(bbox)
        crop.thumbnail(size, Image.LANCZOS)
        # recolour to solid dark for silhouette: use mask resized to crop size
        mk2=mk.resize(crop.size, Image.LANCZOS)
        sil_im=Image.new("RGBA",crop.size,(20,20,30,255))
        out.paste(sil_im,(0,0),mk2)
    return out

def sheet(title, subtitle, panels, path, W=1500):
    # panels: list of (img, caption)
    H=520
    img=Image.new("RGB",(W, 150+H* ((len(panels)+2)//3) ), (240,240,235))
    d=ImageDraw.Draw(img); d.text((30,20),title,fill=(0,0,0),font=font(34)); import textwrap as _tw
    for _i,_ln in enumerate(_tw.wrap(subtitle, width=95)): d.text((30,62+_i*24),_ln,fill=(60,60,60),font=font(20))
    cols=3; cw=W//cols
    for i,(p,cap) in enumerate(panels):
        x=(i%cols)*cw+20; y=140+(i//cols)*H
        p2=p.copy(); p2.thumbnail((cw-40,400), Image.LANCZOS)
        img.paste(p2,(x,y),p2 if p2.mode=="RGBA" else None)
        import textwrap as _tw2
        for _j,_ln in enumerate(_tw2.wrap(cap, width=30)): d.text((x,y+410+_j*22),_ln,fill=(0,0,0),font=font(18))
    img.save(path); print(path, img.size)

# 1 silhouette sheet
poses=[(os.path.join(R,"rig-apose-v7c-clean-transparent.png"),"APOSE — head/cape/torso distinct"),
       (os.path.join(R,"reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png"),"FIGHTING POSE — arm clear of torso"),
       (os.path.join(R,"reposes-v7c-clean/full-final-flex-v7c-clean-20261031.png"),"FULL FINAL FLEX — fists to head; wrist cleanup owed")]
panels=[]
for p,cap in poses:
    s=sil(p); thumb=s.copy(); thumb.thumbnail((110,150), Image.LANCZOS)
    canvas=Image.new("RGBA",(320,470),(255,255,255,255))
    canvas.paste(s,(10,10),s); canvas.paste(thumb,(190,10),thumb)
    panels.append((canvas,cap+" | thumb 110px"))
sheet("SILHOUETTE READABILITY — STAGING GATE (built now)",
      "Gate: action must read in silhouette at thumbnail size. If it does not, re-stage, do not add effects. Sheet labels only — pieces themselves are clean.",
      panels, os.path.join(O,"silhouette-readability-20261031.png"))

# 2 cape follow-through
cape_names=["cape-01-draped-20261031.png","cape-03-swinging-20261031.png","cape-04-billowing-20261031.png","cape-13-flying-spread-20261031.png"]
caps=["F0 body stops — cape draped","F+1 cape lags, still swinging","F+2 cape billows past body stop","F settle — cape settles AFTER body"]
panels=[]
for n,cap in zip(cape_names,caps):
    im=Image.open(os.path.join(R,"cape-styles-v2-20261031",n)).convert("RGBA")
    canvas=Image.new("RGBA",(320,470),(200,200,200,255)); im.thumbnail((300,440),Image.LANCZOS); canvas.paste(im,(10,10),im)
    panels.append((canvas,cap))
sheet("CAPE FOLLOW-THROUGH / OVERLAP — 1-2 FRAME LAG (built now)",
      "Principle 5: cape keeps moving after the body stops, settles after it, never with it. Warps of Cape_Back_Main only — not hand-painted masters.",
      panels, os.path.join(O,"cape-follow-through-20261031.png"))

# 3 punch exposure + smear draft
punch=Image.open(os.path.join(R,"clips-v7c-clean-20261031/punch/punch-09-impact-hold-v7c-clean.png")).convert("RGBA")
# smear draft: stretch punch horizontally with fading copies (labelled DRAFT)
smear=Image.new("RGBA",(500,500),(128,128,128,255))
for k,alpha in [(0,255),(30,120),(60,60)]:
    tmp=punch.copy(); tmp.thumbnail((420,420),Image.LANCZOS)
    smear.paste(tmp,(40-k,40),tmp)
panels=[]
for cap,im in [("WINDUP 6f — anticipation",punch),("SNAP 2f — fast in",punch),("IMPACT HOLD 12f — locked -110",punch),("RECOVER 6f — stretch",punch),("SMEAR DRAFT — PIL method only, not production",smear)]:
    canvas=Image.new("RGBA",(320,470),(255,255,255,255)); t=im.copy(); t.thumbnail((300,440),Image.LANCZOS); canvas.paste(t,(10,10),t if t.mode=="RGBA" else None)
    panels.append((canvas,cap))
sheet("PUNCH CJ-01 — EXPOSURE SHEET + SMEAR (built now, 1/30 shots checked)",
      "Timing: windup 6 / snap 2 / impact hold 12 / recover 6 @24fps. Arcs: fist path is an arc, never a straight line. Smear panel is a method draft only.",
      panels, os.path.join(O,"punch-cj01-exposure-smear-20261031.png"))

# 4 lip-sync timeline
vis=[("head-v2-05-oh-20261031.png","OH f1-2"),("head-v2-13-w-20261031.png","W f3-4"),("head-v2-06-oo-20261031.png","OO f5-6"),("head-v2-04-ah-20261031.png","AH f7-8"),("head-v2-07-mbp-20261031.png","M/B/P f9-10"),("head-v2-01-rest-20261031.png","REST f11-12")]
panels=[]
for n,cap in vis:
    im=Image.open(os.path.join(R,"visemes-v2-20261031",n)).convert("RGBA")
    canvas=Image.new("RGBA",(320,470),(255,255,255,255)); im.thumbnail((300,440),Image.LANCZOS); canvas.paste(im,(10,10),im)
    panels.append((canvas,cap))
sheet("LIP-SYNC TIMELINE — TEST PHRASE 'OH-WOO-AH-M' (built now)",
      "Visemes v2, mask-first method. 2 frames per viseme @24fps in this test strip; real dialogue timing comes from the recorded audio, not this strip.",
      panels, os.path.join(O,"lipsync-timeline-test-20261031.png"))

# 5 camera 180 diagram (drawn, no character art copied)
W,H=1500,600; img=Image.new("RGB",(W,H),(240,240,235)); d=ImageDraw.Draw(img)
d.text((30,20),"CAMERA 180-DEGREE RULE — PUNCH SHOT (built now)",fill=(0,0,0),font=font(34))
d.text((30,62),"Axis = line between Cape Jones and his opponent. Camera stays on ONE side of the axis for the whole punch sequence.",fill=(60,60,60),font=font(20))
d.line([(200,450),(1300,450)],fill=(200,0,0),width=4); d.text((700,460),"AXIS OF ACTION",fill=(200,0,0),font=font(20))
# characters as silhouettes
s=sil(os.path.join(R,"rig-apose-v7c-clean-transparent.png"),(180,240)); img.paste(s,(410,180),s); d.text((410,430),"CAPE JONES",fill=(0,0,0),font=font(18))
# opponent = plain grey block, deliberately NOT a Cape silhouette, NOT a character
d.rectangle([910,180,1090,420],fill=(160,160,160),outline=(0,0,0),width=3); d.text((910,430),"OPPONENT = GREY BLOCK ONLY",fill=(0,0,0),font=font(18)); d.text((910,455),"(placeholder, not a character)",fill=(0,0,0),font=font(16))
for cx,lab,col in [(300,"CAMERA A — OK", (0,140,0)),(750,"CAMERA B — SAME SIDE, OK",(0,140,0)),(1200,"CAMERA C — ACROSS AXIS, DO NOT CUT TO", (200,0,0))]:
    d.ellipse([cx-40,120,cx+40,200],outline=col,width=4); d.text((cx-110,210),lab,fill=col,font=font(16))
d.text((30,530),"Gate: if a cut crosses the axis, left/right flip and the punch reads backwards. Re-shoot the angle, do not flip the frame in post.",fill=(0,0,0),font=font(20))
img.save(os.path.join(O,"camera-180-rule-20261031.png")); print("camera done")
print("done")
