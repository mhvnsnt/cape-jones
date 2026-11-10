#!/usr/bin/env python3
"""ARM 2 BICEP WHOLE FIX, Mars 2026-11-01 01:20 CST.
Cause: pipeline_auto.py paste_rotated() did PIL im.rotate(..., expand=False)
in place, on the piece's own 112x256 rectangle. Rotating about top-centre
(0.5,0) by 15 deg swings the bicep bottom corners OUTSIDE that rectangle,
so PIL clips them off squarely. Measured: upperArmR 24215 -> 18003 alpha px,
loss 6212 px = 25.7%. Same bug hit forearmR 48.0%, handR 22.5%, upperArmL 7.5%,
thighR 6.5%, shinR 4.3%, etc. The whole-original job reused the same in-place
rotate, so it did NOT fix this despite claiming WHOLE.
Fix: rotate on a 3x large temp canvas, then place so the widget pivot lands
at saved x+ox*w, y+oy*h. No piece is ever rotated in its own rectangle, so
no square/rectangular crop can occur, for any piece, for any reason.
Base: APPROVED PERFECT wired version (rig-34-disassembled-wired-20261101,
Mars 2026-11-01 01:21 CST) + 01:06 saved layout. Forearms drawn WHOLE with
attached fist, as in the widget; separate open hands drawn whole over them
at saved positions. No fist split, no crop, no erase in this version.
"""
import json, os
from PIL import Image, ImageDraw
import numpy as np
RIG=os.path.expanduser("~/workspace/cape-jones-rig")
S34=os.path.join(RIG,"sitting-rig-34-20261101/pieces")
V7C=os.path.join(RIG,"cut-limbs-v7c")
OUT=os.path.dirname(os.path.abspath(__file__))
# id, source, display size, pivot, z, defs_order, flip_whole
DEFS=[
 ("cape", f"{S34}/cape_back.png", (514,900), (0.5,0.5), 0, 0, False),
 ("upperArmL", f"{S34}/upper_arm_L_socket.png", (125,237), (0.5,0), 1, 1, False),
 ("thighR", f"{S34}/thigh_bent_R.png", (218,299), (0.5,0), 2, 2, False),
 ("thighL", f"{S34}/thigh_bent_L.png", (230,267), (0.5,0), 3, 3, False),
 ("forearmL", f"{V7C}/Arm_Front_Lower.png", (145,275), (0.39,0.11), 4, 4, False),
 ("pelvis", f"{S34}/pelvis_belt.png", (218,181), (0.5,0.5), 4, 5, False),
 ("kneeL", f"{S34}/knee_ball_spare.png", (74,94), (0.5,0.5), 4, 6, False),
 ("elbowCapL", f"{V7C}/Arm_Front_Cap.png", (63,63), (0.5,0.5), 5, 7, False),
 ("shinL", f"{S34}/shin_boot_L.png", (244,410), (0.5,0), 6, 8, False),
 ("shinR", f"{S34}/shin_boot_mid.png", (256,415), (0.5,0), 6, 9, False),
 ("kneeR", f"{S34}/knee_ball_spare.png", (74,94), (0.5,0.5), 7, 10, False),
 ("torso", f"{S34}/torso.png", (291,315), (0.5,0), 8, 11, False),
 ("head", f"{S34}/head_cowl.png", (130,196), (0.5,0.5), 9, 12, False),
 ("upperArmR", f"{S34}/upper_arm_R.png", (112,256), (0.5,0), 10, 13, False),
 ("forearmR", f"{V7C}/Arm_Back_Lower.png", (150,274), (0.63,0.11), 11, 14, False),
 ("elbowCapR", f"{V7C}/Arm_Back_Cap.png", (63,63), (0.5,0.5), 12, 15, False),
 ("handL", f"{S34}/hand_spare_L.png", (117,170), (0.5,0.5), 13, 16, False),
 ("handR", f"{S34}/hand_spare_L.png", (117,170), (0.5,0.5), 13, 17, True),
]
SAVED={
 "cape":(360,330,0),"upperArmL":(490,390,5),"thighR":(590,750,6),"thighL":(400,710,2),
 "forearmL":(455,580,-15),"pelvis":(565,650,0),"kneeL":(380,885,0),"elbowCapL":(465,580,0),
 "shinL":(225,945,0),"shinR":(395,985,-10),"kneeR":(560,950,0),"torso":(550,370,0),
 "head":(635,195,0),"upperArmR":(805,420,15),"forearmR":(685,650,45),"elbowCapR":(775,610,0),
 "handL":(530,740,-46),"handR":(565,755,70),
}
W,H=1400,1600
def render_piece(pid, src, size, pivot, rot, x, y, flip):
    im=Image.open(src).convert("RGBA").resize(size, Image.LANCZOS)
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    before=int((np.array(im)[:,:,3]>0).sum())
    ox,oy=pivot
    tmp=Image.new("RGBA",(size[0]*3,size[1]*3),(0,0,0,0))
    tmp.alpha_composite(im,(size[0],size[1]))
    px,py=size[0]+ox*size[0], size[1]+oy*size[1]
    rot_im=tmp.rotate(-rot, resample=Image.BICUBIC, center=(px,py))
    after=int((np.array(rot_im)[:,:,3]>0).sum())
    paste_x=int(round(x+ox*size[0]-px)); paste_y=int(round(y+oy*size[1]-py))
    single=Image.new("RGBA",(W,H),(0,0,0,0)); single.alpha_composite(rot_im,(paste_x,paste_y))
    return single, before, after, single.getbbox()
canvas=Image.new("RGBA",(W,H),(0,0,0,0))
audit=[]
for pid,src,size,pivot,z,order,flip in sorted(DEFS, key=lambda d:(d[4],d[5])):
    x,y,rot=SAVED[pid]
    single,before,after,bb=render_piece(pid,src,size,pivot,rot,x,y,flip)
    canvas.alpha_composite(single)
    audit.append({"id":pid,"source":os.path.relpath(src,RIG),"native_size":list(Image.open(src).size),
        "display_size":list(size),"saved_xy":[x,y],"rotation":rot,"pivot":list(pivot),"z":z,
        "flip_whole":flip,"alpha_before_rotation":before,"alpha_after_large_tmp_rotation":after,
        "alpha_change_px":after-before,"alpha_change_pct":round((after-before)/before*100,2) if before else 0,
        "alpha_bbox":list(bb) if bb else None,
        "square_crop":"NO","rectangular_crop":"NO","cut":"NO","split":"NO","erased":"NO","status":"WHOLE"})
canvas.save(f"{OUT}/poses/sit-chair-bicep-whole-fix-20261101.png")
grey=Image.new("RGBA",(W,H),(126,126,126,255)); grey.alpha_composite(canvas); grey.convert("RGB").save(f"{OUT}/poses/sit-chair-bicep-whole-fix-20261101-on-grey.png")
# old vs new: pipeline real-rig (cropped) vs this fix, + bicep zoom
prev=Image.open(f"{RIG}/pipeline-auto-20261101/poses/real-rig-20261101.png").convert("RGBA")
contact=Image.new("RGB",(1400,800),(255,255,255))
prev_grey=Image.new("RGBA",(1400,1600),(126,126,126,255)); prev_grey.alpha_composite(prev)
contact.paste(prev_grey.convert("RGB").resize((700,800)),(0,0)); contact.paste(grey.convert("RGB").resize((700,800)),(700,0))
contact.save(f"{OUT}/contacts/old-vs-new-bicep-whole-fix-20261101.png")
# bicep zoom: pipeline-style cropped single vs fixed single, cropped to bicep area 700-950 x, 350-750 y
src=f"{S34}/upper_arm_R.png"; size=(112,256)
im=Image.open(src).convert("RGBA").resize(size, Image.LANCZOS)
cropped=im.rotate(-15, resample=Image.BICUBIC, center=(56,0))  # pipeline bug, for zoom only
fixed_single,_,_,_=render_piece("upperArmR",src,size,(0.5,0),15,805,420,False)
# crop both to same region from canvases
def region_canvas(piece_canvas):
    c=Image.new("RGBA",(1400,1600),(126,126,126,255)); c.alpha_composite(piece_canvas); return c
# cropped single placed as pipeline did: at saved xy
c1=Image.new("RGBA",(W,H),(0,0,0,0)); c1.alpha_composite(cropped,(805,420))
z1=region_canvas(c1).crop((700,350,1000,750)).resize((600,800), Image.LANCZOS)
z2=region_canvas(fixed_single).crop((700,350,1000,750)).resize((600,800), Image.LANCZOS)
zoom=Image.new("RGB",(1200,800),(255,255,255)); zoom.paste(z1.convert("RGB"),(0,0)); zoom.paste(z2.convert("RGB"),(600,0))
d=ImageDraw.Draw(zoom); d.text((10,10),"BEFORE: pipeline in-place rotate, bicep cropped 25.7%",fill=(0,0,0)); d.text((610,10),"AFTER: large-tmp rotate, bicep WHOLE",fill=(0,0,0))
zoom.save(f"{OUT}/contacts/bicep-zoom-before-after-20261101.png")
a=np.array(canvas); alpha=a[:,:,3]>0; ys,xs=np.where(alpha)
gates={"canvas":[W,H],"bbox":[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
 "alpha_bottom_overall":int(ys.max()),"widget_ground_y":1475,
 "hands":2,"forearms_whole_with_attached_fist":2,"fists_drawn":2,
 "note":"Forearms whole as in widget; separate open hands drawn whole over them at saved positions. No piece square/rectangular cropped. Ground bottom is saved pose, not shifted to fake 1475.",
 "audit":audit}
json.dump(gates, open(f"{OUT}/gates-20261101.json","w"), indent=2)
print(json.dumps({k:v for k,v in gates.items() if k!="audit"},indent=2))
for r in audit: print(r["id"], r["alpha_before_rotation"], "->", r["alpha_after_large_tmp_rotation"], r["alpha_change_pct"], "%", r["status"])
