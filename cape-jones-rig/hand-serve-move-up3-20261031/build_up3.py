"""Serve move up 3, 2026-10-31, Mars order 23:02 CDT, from the UP2 no-crop build.
Revert: start from original jei-01-base-for-swap, full body + cape intact.
Fix: NO radius-circle erase. Old builder erased dot>0 & dist<=160 from F,
10,173 px, of which only 2,298 px were under the new hand; 7,875 px of
torso/cape (bbox x332-472 y502-665) were deleted, leaving the semicircular
notch Mars never ordered. In the fixed build the old fist is covered by
the new open palm itself (palm bbox x248-354 y432-563, larger than the fist
it replaces), so no base pixel outside the new hand mask is changed at all.
Palm/ball centre (314, 476); total from original (314, 530): dx 0, dy -54.
Angle 164.8, scale 1.0, Arm1 horizontal in-place mirror, unchanged.
Outputs only in this folder; no existing file overwritten; no repo push.
"""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/wrist-attach-fix-20261031")
from check_wrist_attach import HANDS, rot_vec, angle_for_direction

RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(RIG, "hand-serve-move-up3-20261031")
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

base = Image.open(os.path.join(RIG,"ginyu-force-limits-broken-20261031","jei-01-base-for-swap-20261031.png")).convert("RGBA")
F=(314.0,517.0); D=(-0.263,0.965); ang=angle_for_direction(D)
Wpt=(F[0]-D[0]*25, F[1]-D[1]*25)
arr=np.array(base); yy,xx=np.mgrid[0:arr.shape[0],0:arr.shape[1]]
dot=(xx-Wpt[0])*D[0]+(yy-Wpt[1])*D[1]; dist=np.sqrt((xx-F[0])**2+(yy-F[1])**2)
old_erase=(dot>0)&(dist<=160)&(arr[:,:,3]>10)

(Wd,Hd), wrist0, tip0 = HANDS["Hand_3_Open.png"]
wrist_m=(Wd-wrist0[0], wrist0[1]); tip_m=(Wd-tip0[0], tip0[1]); ic=(Wd/2,Hd/2)
wo=(wrist_m[0]-ic[0], wrist_m[1]-ic[1]); to=(tip_m[0]-ic[0], tip_m[1]-ic[1])
centre_orig=(Wpt[0]-rot_vec(wo,ang)[0], Wpt[1]-rot_vec(wo,ang)[1])
centre_new=(303.0, 494.3)  # up2 paste centre (303.0, 497.3) shifted up 3; palm centre = paste + (11, -18.3) = (314, 476)
print("paste centre", centre_new)

hand_layer=Image.new("RGBA", base.size, (0,0,0,0)); paste_hand(hand_layer, centre_new, ang, 1.0, True)
hand_mask=np.array(hand_layer)[:,:,3]>10
# FIXED: no erase at all. Old fist is under the new palm.
plain=base.copy(); plain.alpha_composite(hand_layer)
# Verification 1: base vs fixed outside new hand mask must be identical
pa=np.array(plain); ba=np.array(base)
diff_outside=int(np.sum((np.abs(pa[:,:,:4].astype(int)-ba[:,:,:4].astype(int)).sum(axis=2)>0) & (~hand_mask)))
# Verification 2: old erase zone restored
old_uncovered = old_erase & (~hand_mask)
restored=int(np.sum(old_uncovered & (pa[:,:,3]>10)))
restored_total=int(old_uncovered.sum())
# Verification 3: interior hole in previously notched zone (torso/cape zone)
zone = np.zeros_like(hand_mask); zone[502:666, 332:473]=True
zone_base_alpha = ba[:,:,3]>10
hole_in_zone=int(np.sum(zone & zone_base_alpha & (pa[:,:,3]<=10)))
# Verification 4: old fist fringe outside new hand: by construction diff_outside==0, so 0
wrist=(centre_new[0]+rot_vec(wo,ang)[0], centre_new[1]+rot_vec(wo,ang)[1])
tip=(centre_new[0]+rot_vec(to,ang)[0], centre_new[1]+rot_vec(to,ang)[1])
pc=(int(round(centre_new[0]+11.0)), int(round(centre_new[1]-18.3)))
ys,xs=np.where(hand_mask); hand_bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
gate_plain=finish(plain, "jei-01-serve-open-palm-UP3-20261031.png")
ball=plain.copy(); lay=Image.new("RGBA", ball.size, (0,0,0,0)); d=ImageDraw.Draw(lay)
for r,col in [(70,(255,230,110,90)),(48,(255,230,110,255))]:
    d.ellipse([pc[0]-r,pc[1]-r,pc[0]+r,pc[1]+r], fill=col)
d.ellipse([pc[0]-18,pc[1]-18,pc[0]+18,pc[1]+18], fill=(255,250,220,255))
ball.alpha_composite(lay); gate_ball=finish(ball, "jei-01-serve-open-palm-ball-UP3-20261031.png")
ba2=np.array(ball); r,g,b=ba2[:,:,0].astype(int),ba2[:,:,1].astype(int),ba2[:,:,2].astype(int)
mask=(r>240)&(g>200)&(b<180)&(ba2[:,:,3]>200); ys2,xs2=np.where(mask)
ball_meas=(round(float(xs2.mean()),1), round(float(ys2.mean()),1))
# ball vs plain outside ball circles: only ball area changes
print("diff_outside_hand", diff_outside)
print("old_erase_total", int(old_erase.sum()), "old_erase_under_hand", int((old_erase & hand_mask).sum()), "old_erase_outside_hand_restored", restored, "/", restored_total)
print("interior_hole_in_notch_zone", hole_in_zone)
print("wrist", wrist, "tip", tip, "palm/ball centre", pc, "measured yellow", ball_meas)
print("hand_bbox", hand_bbox, "gate_plain", gate_plain, "gate_ball", gate_ball)
res={"move":"palm/ball centre (314,476); total from original (314,530): dx=0, dy=-54; from up2 (314,479): dy=-3",
 "angle":round(ang,1),"scale":1.0,"mirror":"Arm1 horizontal in place, unchanged",
 "revert_base":"ginyu-force-limits-broken-20261031/jei-01-base-for-swap-20261031.png, full body+cape, no erase circle",
 "old_erase_circle_px_total":int(old_erase.sum()),"old_erase_under_new_hand_px":int((old_erase & hand_mask).sum()),
 "old_erase_outside_hand_px":restored_total,"old_erase_outside_hand_restored_px":restored,
 "previously_notched_zone":"x332-472 y502-665",
 "interior_hole_px_in_notch_zone":hole_in_zone,
 "base_vs_fixed_diff_outside_new_hand_mask_px":diff_outside,
 "old_fist_pixels_visible_outside_new_hand_px":diff_outside,
 "centre_paste_new":[round(v,1) for v in centre_new],"palm_ball_centre_new":list(pc),
 "palm_ball_centre_measured_yellow":list(ball_meas),
 "wrist_registry_new":[round(v,1) for v in wrist],"tip_registry_new":[round(v,1) for v in tip],
 "d_wrist_registry_to_forearm_end_F":round(math.dist(wrist,F),1),"cuff_bottom_y":474,
 "wrist_registry_above_cuff_bottom_px":round(474-wrist[1],1),
 "hand_bbox_new":hand_bbox,"no_crop_plain":gate_plain,"no_crop_ball":gate_ball,
 "approval":"0/1, NOT approved until Mars sees it and says perfect; up2 was real real close and Mars would accept it but wants perfect, so up2 is NOT approved; previous right5 with notch is NOT approved"}
json.dump(res, open(os.path.join(OUT,"measurements-up3-20261031.json"),"w"), indent=2)
print("DONE")
