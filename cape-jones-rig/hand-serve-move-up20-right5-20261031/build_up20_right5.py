"""Serve hand move up20 + right5, 2026-10-31, Mars order 22:15 CDT.
Move, stated plainly, from the current move-up-left palm/ball centre (304, 501):
up 20 -> y 481, right 5 -> x 309, new palm/ball centre (309, 481).
Total from the original ball centre (314, 530): dx -5, dy -49.
Rebuilt from the original serve logic (base jei-01-base-for-swap, fist erased
dot>0/dist<=160 from F, Hand_3_Open mirrored Arm1, angle 164.8, scale 1.0),
NOT by smearing the previous composite. Paste centre shifts by the same
(+5, -20) as the ball centre. Ball centre = paste centre + (11.0, -18.3).
No existing file overwritten; outputs only in this folder.
"""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/wrist-attach-fix-20261031")
from check_wrist_attach import HANDS, rot_vec, angle_for_direction

RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(RIG, "hand-serve-move-up20-right5-20261031")
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
SLICED = os.path.join(RIG, "sliced")

def hand_image(scale, mirror):
    im = Image.open(os.path.join(SLICED, "Hand_3_Open.png")).convert("RGBA")
    im = im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if mirror else im

def paste_hand(plate, centre, angle, scale, mirror):
    im = hand_image(scale, mirror)
    rot = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    plate.alpha_composite(rot, (int(centre[0]-rot.size[0]/2), int(centre[1]-rot.size[1]/2)))
    return rot

def no_crop_gate(im):
    a = np.array(im.getchannel("A")); ys, xs = np.where(a > 10)
    touch = bool(ys.min()==0 or ys.max()==im.size[1]-1 or xs.min()==0 or xs.max()==im.size[0]-1)
    return {"pass": not touch, "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]}

def finish(plate, name):
    plate.save(os.path.join(OUT, "frames", name.replace(".png","-transparent.png")))
    bg = Image.new("RGBA", plate.size, (128,128,128,255)); bg.alpha_composite(plate)
    bg.convert("RGB").save(os.path.join(OUT, name))
    return no_crop_gate(plate)

def column_gaps(hand_mask, cuff_y=474):
    gaps = {}
    for x in (290,300,310,320,330,340,350):
        ys = np.where(hand_mask[:,x])[0]
        gaps[f"x{x}"] = int(ys.min()-cuff_y-1) if len(ys) else None
    return gaps

base = Image.open(os.path.join(RIG,"ginyu-force-limits-broken-20261031","jei-01-base-for-swap-20261031.png")).convert("RGBA")
F=(314.0,517.0); D=(-0.263,0.965); ang=angle_for_direction(D)
Wpt=(F[0]-D[0]*25, F[1]-D[1]*25)
arr=np.array(base); yy,xx=np.mgrid[0:arr.shape[0],0:arr.shape[1]]
dot=(xx-Wpt[0])*D[0]+(yy-Wpt[1])*D[1]; dist=np.sqrt((xx-F[0])**2+(yy-F[1])**2)
erase_mask=(dot>0)&(dist<=160)&(arr[:,:,3]>10)
arr[erase_mask]=(0,0,0,0); erased=Image.fromarray(arr,"RGBA")

(Wd,Hd), wrist0, tip0 = HANDS["Hand_3_Open.png"]
wrist_m=(Wd-wrist0[0], wrist0[1]); tip_m=(Wd-tip0[0], tip0[1]); ic=(Wd/2,Hd/2)
wo=(wrist_m[0]-ic[0], wrist_m[1]-ic[1]); to=(tip_m[0]-ic[0], tip_m[1]-ic[1])
centre_orig=(Wpt[0]-rot_vec(wo,ang)[0], Wpt[1]-rot_vec(wo,ang)[1])
centre_moveup=(centre_orig[0], centre_orig[1]-19)
centre_moveupleft=(centre_moveup[0]-10, centre_moveup[1]-10)
centre_new=(centre_moveupleft[0]+5, centre_moveupleft[1]-20)

def build(centre):
    hand_layer=Image.new("RGBA", base.size, (0,0,0,0)); paste_hand(hand_layer, centre, ang, 1.0, True)
    hand_mask=np.array(hand_layer)[:,:,3]>10
    final=erased.copy(); final.alpha_composite(hand_layer)
    fa=np.array(final)
    remaining=int(np.sum(erase_mask & (~hand_mask) & (fa[:,:,3]>10)))
    wrist=(centre[0]+rot_vec(wo,ang)[0], centre[1]+rot_vec(wo,ang)[1])
    tip=(centre[0]+rot_vec(to,ang)[0], centre[1]+rot_vec(to,ang)[1])
    ball_centre=(int(round(centre[0]+11.0)), int(round(centre[1]-18.3)))
    return final, hand_layer, hand_mask, remaining, wrist, tip, ball_centre

plain, hl, hm, rem, wrist, tip, pc = build(centre_new)
plain_prev, hl_prev, hm_prev, _, wrist_prev, tip_prev, pc_prev = build(centre_moveupleft)
gaps_new=column_gaps(hm); gaps_prev=column_gaps(hm_prev)
gate_plain=finish(plain, "jei-01-serve-open-palm-UP20RIGHT5-20261031.png")
ball=plain.copy(); lay=Image.new("RGBA", ball.size, (0,0,0,0)); d=ImageDraw.Draw(lay)
for r,col in [(70,(255,230,110,90)),(48,(255,230,110,255))]:
    d.ellipse([pc[0]-r,pc[1]-r,pc[0]+r,pc[1]+r], fill=col)
d.ellipse([pc[0]-18,pc[1]-18,pc[0]+18,pc[1]+18], fill=(255,250,220,255))
ball.alpha_composite(lay); gate_ball=finish(ball, "jei-01-serve-open-palm-ball-UP20RIGHT5-20261031.png")
ba=np.array(ball); r,g,b=ba[:,:,0].astype(int),ba[:,:,1].astype(int),ba[:,:,2].astype(int)
mask=(r>240)&(g>200)&(b<180)&(ba[:,:,3]>200); ys,xs=np.where(mask)
ball_meas=(round(float(xs.mean()),1), round(float(ys.mean()),1))
diff=int(np.sum((np.abs(np.array(plain)[:,:,:3].astype(int)-np.array(plain_prev)[:,:,:3].astype(int)).sum(axis=2)>30) & (np.array(plain)[:,:,3]>10) & (np.arange(1100)[None,:]>=380)))
ys,xs=np.where(hm); hand_bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
ys,xs=np.where(hm_prev); hand_bbox_prev=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
# alpha continuity x290-340 in final composite, max transparent run per column (same check as before)
def max_runs(im):
    a=np.array(im)[:,:,3]>10; out={}
    for x in (290,300,310,320,330,340):
        col=a[:,x]; run=mx=0
        for v in col:
            run=run+1 if not v else 0; mx=max(mx,run)
        out[f"x{x}"]=int(mx)
    return out
runs_new=max_runs(plain); runs_prev=max_runs(plain_prev)
print("centre_paste_moveupleft",centre_moveupleft); print("centre_paste_new",centre_new)
print("palm/ball centre prev",pc_prev,"new",pc,"measured yellow",ball_meas)
print("wrist registry prev",wrist_prev,"new",wrist,"tip new",tip,"d_wrist_to_F",math.dist(wrist,F))
print("gaps prev",gaps_prev); print("gaps new",gaps_new)
print("hand bbox prev",hand_bbox_prev,"new",hand_bbox,"remaining fist",rem,"torso/cape diff x>=380",diff)
print("alpha runs prev",runs_prev,"new",runs_new)
print("nocrop plain",gate_plain); print("nocrop ball",gate_ball)
res={"move":"dx=+5, dy=-20 from move-up-left version; palm/ball centre (304,501) -> (309,481); total from original (314,530): dx=-5, dy=-49",
 "angle":round(ang,1),"scale":1.0,"mirror":"Arm1 horizontal in place, unchanged","forced_changes":"none to angle/scale/mirror; paste centre shifted (+5,-20) only",
 "centre_paste_moveupleft":[round(v,1) for v in centre_moveupleft],"centre_paste_new":[round(v,1) for v in centre_new],
 "palm_ball_centre_prev":list(pc_prev),"palm_ball_centre_new":list(pc),"palm_ball_centre_measured_yellow":list(ball_meas),
 "wrist_registry_prev":[round(v,1) for v in wrist_prev],"wrist_registry_new":[round(v,1) for v in wrist],"tip_registry_new":[round(v,1) for v in tip],
 "d_wrist_registry_to_forearm_end_F":round(math.dist(wrist,F),1),"cuff_bottom_y":474,
 "wrist_registry_above_cuff_bottom_px":round(474-wrist[1],1),
 "column_gaps_prev":gaps_prev,"column_gaps_new":gaps_new,
 "hand_bbox_prev":hand_bbox_prev,"hand_bbox_new":hand_bbox,"fist_pixels_remaining_outside_hand":rem,
 "torso_cape_diff_x_ge_380_new_vs_moveupleft":diff,
 "alpha_transparent_runs_prev":runs_prev,"alpha_transparent_runs_new":runs_new,
 "no_crop_plain":gate_plain,"no_crop_ball":gate_ball,
 "approval":"0/1, NOT approved until Mars sees it"}
json.dump(res, open(os.path.join(OUT,"measurements-up20-right5-20261031.json"),"w"), indent=2)
print("DONE")
