from PIL import Image, ImageDraw, ImageFont
import os
R=os.path.expanduser("~/workspace/cape-jones-rig/")
OUT=R+"shows-qc-room-jump-20261101/contacts/"
def font(s):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p,s)
            except: pass
    return ImageFont.load_default()
def thumb(path,w,h):
    im=Image.open(path).convert("RGB"); im.thumbnail((w,h)); c=Image.new("RGB",(w,h),(20,20,20)); c.paste(im,((w-im.width)//2,(h-im.height)//2)); return c
def label(img, lines, y0=10):
    d=ImageDraw.Draw(img)
    for i,t in enumerate(lines):
        d.text((20,y0+i*34),t,fill=(255,255,255),font=font(28))
    return img

# --- QC contact ---
W,H=1920,1500
img=Image.new("RGB",(W,H),(15,15,15)); d=ImageDraw.Draw(img)
d.text((20,10),"QC - WHAT IT MEANS: the checker could not verify these 3, it did NOT find a wrong colour",fill=(255,220,0),font=font(30))
shots=[("CJ-05 punch across-down","shots-endtoend-20261031/finals/CJ-05-punch-across-down-placement-endtoend-20261031.png"),
("CJ-06 walk street contact","shots-endtoend-20261031/finals/CJ-06-walk-street-contact-endtoend-20261031.png"),
("CJ-26 dialogue neutral unsure","shots-endtoend-20261031/finals/CJ-26-dialogue-neutral-unsure-endtoend-20261031.png")]
for i,(t,p) in enumerate(shots):
    x=20+i*633
    img.paste(thumb(R+p,613,500),(x,60))
    d.text((x,575),t,fill=(255,255,255),font=font(26))
    d.text((x,610),"Spec key hue = None, rim hue = None",fill=(255,180,180),font=font(24))
    d.text((x,645),"Rim rule has NO black/white/grey case",fill=(255,180,180),font=font(24))
    d.text((x,680),"Dual-light applies to NONE of these",fill=(255,180,180),font=font(24))
# rim swatches
y=760
d.text((20,y),"CJ-26 RIM PAPERWORK FIX - the two numbers, blown up:",fill=(255,220,0),font=font(30))
for i,(col,lab) in enumerate([((255,255,255),"Field says 255,255,255  (pure white)"),((240,240,240),"Notes say 240,240,240  (15 darker, ~6%)")]):
    x=20+i*700
    d.rectangle([x,y+50,x+300,y+250],fill=col,outline=(255,255,0),width=3)
    d.text((x+320,y+80),lab,fill=(255,255,255),font=font(26))
    d.text((x+320,y+120),"To the eye: almost identical." if i==0 else "Fix = pick ONE number, use it everywhere.",fill=(200,200,200),font=font(24))
y=1070
d.text((20,y),"YOUR THREE CHOICES:",fill=(255,220,0),font=font(30))
for i,t in enumerate(["R1 PASS ALL 3 -> 30/30. New rule: black/white/grey shots pass.",
"R2 PASS CJ-05 + CJ-06, HOLD CJ-26 -> 29/30. CJ-26 waits for its rim fix.",
"R3 FAIL STANDS -> 27/30. Nothing changes, 3 stay failed."]):
    d.text((20,y+45+i*40),t,fill=(255,255,255),font=font(26))
d.text((20,1230),"R1 does NOT make CJ-26 canon or final. CJ-26 stays DEMO-ONLY / SPEC-ONLY.",fill=(255,180,0),font=font(26))
d.text((20,1270),"Plain words: FAIL here = 'cannot check', NOT 'colour is wrong'.",fill=(255,255,255),font=font(26))
img.save(OUT+"show-qc-r1-r2-r3-20261101.png")

# --- Room scale contact ---
img=Image.new("RGB",(W,1500),(15,15,15)); d=ImageDraw.Draw(img)
d.text((20,10),"ROOM SCALE GENERAL - what 'confirm generally' actually changes",fill=(255,220,0),font=font(30))
# Panel A: CJ-25 room standing
img.paste(thumb(R+"shots-endtoend-20261031/finals/CJ-25-room-standing-device-gag-endtoend-20261031.png",613,500),(20,60))
d.text((20,575),"A. IN THE ROOM, 3.0x - ALREADY LOCKED",fill=(255,255,255),font=font(26))
d.text((20,610),"CJ-25 room standing, 3.0x. Seated 2.8x",fill=(200,200,200),font=font(24))
d.text((20,645),"is locked separately. This does not change.",fill=(200,200,200),font=font(24))
# Panel B: CJ-01 spec
img.paste(thumb(R+"shots-endtoend-20261031/finals/CJ-01-punch-windup-endtoend-20261031.png",613,500),(653,60))
d.text((653,575),"B. ROOM-ONLY (NOW) - other shots keep",fill=(255,255,255),font=font(26))
d.text((653,610),"their own spec scale, ~0.35 on rig canvas.",fill=(200,200,200),font=font(24))
d.text((653,645),"CJ-01 street punch, as built. 25/30 shots",fill=(200,200,200),font=font(24))
d.text((653,680),"are NOT-ROOM like this.",fill=(200,200,200),font=font(24))
# Panel C: illustration enlarged CJ-01
src=Image.open(R+"shots-endtoend-20261031/finals/CJ-01-punch-windup-endtoend-20261031.png").convert("RGB")
big=src.resize((613*2,500*2)); crop=big.crop((400,300,400+613,300+500))
img.paste(crop,(1286,60))
d.text((1286,575),"C. GENERAL (IF YOU CONFIRM) - ILLUSTRATION",fill=(255,180,0),font=font(26))
d.text((1286,610),"Same CJ-01 blown up toward 3.0x: figure",fill=(200,200,200),font=font(24))
d.text((1286,645),"bursts the frame, ground line breaks.",fill=(200,200,200),font=font(24))
d.text((1286,680),"Not a real render - a warning picture.",fill=(255,180,0),font=font(24))
y=760
d.text((20,y),"So the pick is:",fill=(255,220,0),font=font(30))
for i,t in enumerate(["CONFIRM GENERALLY = 3.0x becomes the rule for EVERY shot, not just room shots.",
"KEEP ROOM-ONLY = 3.0x stays in the room only, other shots keep spec scale (today's rule).",
"Canonical room you sent (2026-11-01) does NOT change this pick: standing height in the",
"new perspective room must be re-derived from chair height, not pasted at old 1140px."]):
    d.text((20,y+45+i*40),t,fill=(255,255,255),font=font(26))
d.text((20,980),"Room shots at 3.0x: CJ-25, CJ-26, CJ-27. Seated in canonical room: CJ-23, CJ-24 (2.8x).",fill=(200,200,200),font=font(24))
img.save(OUT+"show-room-scale-general-20261101.png")

# --- Jump to shimmy ---
img=Image.new("RGB",(W,1500),(15,15,15)); d=ImageDraw.Draw(img)
d.text((20,10),"JUMP-TO-SHIMMY - the one missing link, successors 8/9",fill=(255,220,0),font=font(30))
img.paste(thumb(R+"rig-chains-20261031/chain-jump-contact-20261031.png",613,400),(20,60))
d.text((20,475),"1. JUMP chain - built, 62 frames, AIRBORNE",fill=(255,255,255),font=font(26))
d.text((20,510),"Ends on a LAND key.",fill=(200,200,200),font=font(24))
# gap panel
d.rectangle([653,60,1286,460],outline=(255,220,0),width=4)
d.text((673,100),"2. THE GAP - ???",fill=(255,220,0),font=font(30))
d.text((673,150),"V1 land key is a RENDERED",fill=(255,255,255),font=font(26))
d.text((673,190),"clip frame. It has NO builder",fill=(255,255,255),font=font(26))
d.text((673,230),"config, so it cannot be rebuilt",fill=(255,255,255),font=font(26))
d.text((673,270),"exactly. A re-key CHANGES",fill=(255,255,255),font=font(26))
d.text((673,310),"the sequence - it is a NEW",fill=(255,255,255),font=font(26))
d.text((673,350),"land pose, not a copy.",fill=(255,255,255),font=font(26))
img.paste(thumb(R+"rig-chains-20261031/chain-dance-contact-20261031.png",613,400),(1286,60))
d.text((1286,475),"3. SHIMMY / DANCE chain - built, 93 frames",fill=(255,255,255),font=font(26))
d.text((1286,510),"Shimmy starts here. Jump must land INTO it.",fill=(200,200,200),font=font(24))
y=580
d.text((20,y),"YOUR TWO CHOICES:",fill=(255,220,0),font=font(30))
for i,t in enumerate(["RE-KEY: you state the new key sequence (crouch -> land -> shimmy start).",
"  A new land pose is built from the rig. Successors become 9/9.",
"DROP IT: successors stay 8/9. Jump and shimmy stay separate chains,",
"  no fake link is built. Nothing else is lost - the other 8 successors stand."]):
    d.text((20,y+45+i*40),t,fill=(255,255,255),font=font(26))
d.text((20,820),"Plain words: we cannot glue jump to shimmy without a new land pose,",
fill=(255,255,255),font=font(26))
d.text((20,860),"because the old land pose exists only as a finished picture, not as rig keys.",
fill=(255,255,255),font=font(26))
img.save(OUT+"show-jump-to-shimmy-20261101.png")
print("done")
