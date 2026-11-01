#!/usr/bin/env python3
"""Rebuild sit-chair rig from Mars's saved Cape Jones Rig Drag layout, 2026-11-01 01:06 CST.
Mapping, plainly: IDENTITY, 1:1. App x,y = top-left of the piece on the 1400x1600
rig canvas, rotation about the piece centre. Proof: app starting pose pelvis
584,640 = attachment-fix pelvis top-left (693-109, 640); head 635,195 = attachment
head top-left (700-65, 195). No stage scale factor, no offset. So saved numbers
are used exactly as top-left + centre rotation. This is proportionally exact
AND, by that proof, pixel-coordinate exact to the app layout — the only
difference is piece render scale, stated below (3/4 pieces 1.3x, front
forearms/caps 0.95x, hands 1.3x), which is the same scale family as every
previous 3/4 build.
Fists: front lower pieces carry a fist as their bottom 25%. The fist is
treated as its own layer (split at 75% height, the builder wrist line) and
NOT drawn. Forearm-only portion is drawn. Separate open hands only.
"""
from PIL import Image, ImageDraw
import os, json, hashlib
import numpy as np
ROOT = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-rebuilt-saved-20261101")
SRC = os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101/pieces")
CUT = os.path.expanduser("~/workspace/cape-jones-rig/cut-limbs-v7c")
SLICED = os.path.expanduser("~/workspace/cape-jones-rig/sliced")
PREV = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-scale5-fist-remove-moves-20261101")
W, H = 1400, 1600
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
def load34(name, s=1.3):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA")
    return im.resize((int(im.width*s), int(im.height*s)), Image.LANCZOS)
def load_front_lower_no_fist(side):
    name = "Arm_Front_Lower.png" if side=="L" else "Arm_Back_Lower.png"
    im = Image.open(os.path.join(CUT, name)).convert("RGBA")
    im = im.resize((int(im.width*0.95), int(im.height*0.95)), Image.LANCZOS)
    cut = int(im.height*0.75)
    forearm = im.crop((0,0,im.width,cut))
    fist = im.crop((0,cut,im.width,im.height))
    forearm.save(f"{ROOT}/pieces/forearm_no_fist_{side}.png")
    fist.save(f"{ROOT}/pieces/fist_OMITTED_{side}.png")
    return forearm, fist, im.size
def load_cap(side):
    name = "Arm_Front_Cap.png" if side=="L" else "Arm_Back_Cap.png"
    im = Image.open(os.path.join(CUT, name)).convert("RGBA")
    return im.resize((int(im.width*0.95), int(im.height*0.95)), Image.LANCZOS)

# saved layout, top-left x,y, rotation deg, z, locked — verbatim from app
SAVED = [
 ("cape","cape_back.png",360,330,0,0,True),
 ("upperArmL","upper_arm_L_socket.png",490,390,5,1,True),
 ("thighR","thigh_bent_R.png",590,750,6,2,True),
 ("thighL","thigh_bent_L.png",400,710,2,3,True),
 ("pelvis","pelvis_belt.png",565,650,0,4,True),
 ("forearmL","FRONT_L",455,580,-15,4,True),
 ("kneeL","knee_ball_spare.png",380,885,0,4,False),
 ("elbowCapL","CAP_L",465,580,0,5,True),
 ("shinL","shin_boot_L.png",225,945,0,6,False),
 ("shinR","shin_boot_mid.png",395,985,-10,6,True),
 ("kneeR","knee_ball_spare.png",560,950,0,7,True),
 ("torso","torso.png",550,370,0,8,True),
 ("head","head_cowl.png",635,195,0,9,False),
 ("upperArmR","upper_arm_R.png",805,420,15,10,True),
 ("forearmR","FRONT_R",685,650,45,11,True),
 ("elbowCapR","CAP_R",775,610,0,12,False),
 ("handL","hand_spare_L.png",530,740,-46,13,True),
 ("handR","hand_spare_L.png",565,755,70,13,True),  # mirrored below
]
pieces = {}
for pid, src, x, y, rot, z, locked in SAVED:
    if src=="FRONT_L":
        fa, fist, fullsize = load_front_lower_no_fist("L"); pieces[pid]=(fa, x, y, rot, z, fullsize)
    elif src=="FRONT_R":
        fa, fist, fullsize = load_front_lower_no_fist("R"); pieces[pid]=(fa, x, y, rot, z, fullsize)
    elif src=="CAP_L": pieces[pid]=(load_cap("L"), x, y, rot, z, None)
    elif src=="CAP_R": pieces[pid]=(load_cap("R"), x, y, rot, z, None)
    else:
        if pid in ("handL","handR"):
            # HAND SCALE CORRECTION, Mars 2026-11-01 01:09 CST: final scale
            # 1.141875x native = 1.0875 scaledown x 1.05 model scale. No other scale.
            # Centred on the saved centres from the v1 rebuild: saved top-left
            # + half of the 1.3x hand (105x152) = handL (582,816), handR (617,831).
            # Stored as (image, centre_x, centre_y, rot, z, "CENTRE") so the draw
            # step places by centre, not by top-left.
            im0 = Image.open(os.path.join(SRC, src)).convert("RGBA")
            im = im0.resize((int(round(im0.width*1.141875)), int(round(im0.height*1.141875))), Image.LANCZOS)
            if pid=="handR": im = im.transpose(Image.FLIP_LEFT_RIGHT)
            cx, cy = (582,816) if pid=="handL" else (617,831)
            pieces[pid]=(im, cx, cy, rot, z, "CENTRE")
        else:
            im = load34(src)
            pieces[pid]=(im, x, y, rot, z, None)

canvas = Image.new("RGBA",(W,H),(0,0,0,0))
# draw in z order; stable by saved order for equal z
ordered = sorted(SAVED, key=lambda t: t[5])
for pid, src, x, y, rot, z, locked in ordered:
    im, px, py, prot, pz, fullsize = pieces[pid]
    if fullsize == "CENTRE":
        # x,y here are the centre coordinates
        layer = Image.new("RGBA",(W,H),(0,0,0,0))
        layer.alpha_composite(im,(x-im.width//2, y-im.height//2))
        layer = layer.rotate(rot, center=(x,y), expand=False, resample=Image.BICUBIC)
        canvas.alpha_composite(layer)
    elif fullsize is not None:
        # full-piece layer: forearm portion at top-left, rotate about FULL piece centre
        layer = Image.new("RGBA",(W,H),(0,0,0,0))
        layer.alpha_composite(im,(x,y))
        cx, cy = x+fullsize[0]//2, y+fullsize[1]//2
        layer = layer.rotate(rot, center=(cx,cy), expand=False, resample=Image.BICUBIC)
        canvas.alpha_composite(layer)
    else:
        layer = Image.new("RGBA",(W,H),(0,0,0,0))
        layer.alpha_composite(im,(x,y))
        cx, cy = x+im.width//2, y+im.height//2
        layer = layer.rotate(rot, center=(cx,cy), expand=False, resample=Image.BICUBIC)
        canvas.alpha_composite(layer)

canvas.save(f"{ROOT}/poses/sit-chair-rebuilt-saved-20261101.png")
grey = Image.new("RGBA", canvas.size, (126,126,126,255)); grey.alpha_composite(canvas)
grey.convert("RGB").save(f"{ROOT}/poses/sit-chair-rebuilt-saved-20261101-on-grey.png")

a = np.array(canvas)[:,:,3]; ys, xs = np.where(a>10)
bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
def bottom_band(x0,x1):
    sub=a[:,x0:x1]; yy,_=np.where(sub>10); return int(yy.max()) if len(yy) else None
def alpha_bottom_in_box(x0,y0,x1,y1):
    sub=a[y0:y1,x0:x1]; yy,xx=np.where(sub>10); return (int(yy.max())+y0) if len(yy) else None
gates={
 "mapping":"IDENTITY 1:1, app x,y = top-left on 1400x1600 canvas, rotation about piece centre. Proof: starting pelvis 584,640 and head 635,195 match attachment-fix top-lefts exactly.",
 "bbox":bbox, "alpha_px":int((a>10).sum()),
 "inside_canvas": bool(xs.min()>=0 and ys.min()>=0 and xs.max()<W and ys.max()<H),
 "alpha_bottom_overall": int(ys.max()),
 "alpha_bottom_left_band_0_700": bottom_band(0,700),
 "alpha_bottom_right_band_700_1400": bottom_band(700,1400),
 "feet_note":"Feet are at the measured alpha bottom of this saved pose, NOT at 1475: saved shin top-lefts (225,945 / 395,985) place the boots higher than the previous 1475-ground builds. No figure shift was applied to fake 1475, because the task was exact saved numbers.",
 "hands":2, "fists_drawn":0,
 "hand_scale_final":"1.141875x native (1.0875 scaledown x 1.05 model scale), both hands, Mars 2026-11-01 01:09 CST",
 "hand_centres":{"handL":[582,816],"handR":[617,831]},
 "hand_sizes_px":{"handL":[93,134],"handR":[93,134]},
 "pieces": [{"id":pid,"x":x,"y":y,"rotation":rot,"z":z,"locked":locked} for pid,_,x,y,rot,z,locked in SAVED],
}
json.dump({"gates":gates}, open(f"{ROOT}/gates-20261101.json","w"), indent=2)
json.dump({"prev_untouched":{"scale5_pose":md5(f"{PREV}/poses/sit-chair-scale5-fist-removed-20261101.png")},
           "front_rig_untouched":{"sliced/Torso_Chest.png":md5(os.path.join(SLICED,"Torso_Chest.png"))}},
          open(f"{ROOT}/untouched-check-20261101.json","w"), indent=2)
print("bbox",bbox,"overall_bottom",int(ys.max()),"left_band",bottom_band(0,700),"right_band",bottom_band(700,1400))

# contacts
old_im = Image.open(f"{PREV}/poses/sit-chair-scale5-fist-removed-20261101-on-grey.png").convert("RGB")
new_im = grey.convert("RGB")
for im in (old_im,new_im): im.thumbnail((700,800))
contact = Image.new("RGB",(2*710,840),(30,30,30)); d=ImageDraw.Draw(contact)
d.text((10,10),"OLD scale5 pose (model 1.05x, pelvis 673)",fill="white")
d.text((720,10),"NEW rebuilt from saved app positions (identity)",fill="white")
contact.paste(old_im,(5,40)); contact.paste(new_im,(715,40))
contact.save(f"{ROOT}/contacts/old-vs-new-rebuilt-saved-20261101.png")
# hand zooms
full=grey.convert("RGB")
def zoom(box,out,label):
    c=full.crop(box); c=c.resize((c.width*2,c.height*2), Image.NEAREST)
    sheet=Image.new("RGB",(c.width,c.height+30),(30,30,30)); ImageDraw.Draw(sheet).text((10,8),label,fill="white"); sheet.paste(c,(0,30)); sheet.save(out)
# hand areas approx from saved top-lefts + sizes
zoom((450,650,750,950), f"{ROOT}/contacts/hand1-new-zoom-20261101.png","Hand1 LEFT, separate open, no fist underneath")
zoom((450,650,800,950), f"{ROOT}/contacts/hand2-new-zoom-20261101.png","Hand2 RIGHT mirrored, separate open, no fist underneath")
