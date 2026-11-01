"""Back rig builder (RIG-07, view=back). One skeleton/system, back drawing set.
Source pieces: pieces/ cut from model-sheet-back-set2 (see cut_back_pieces.py).
Canvas 1400x1600, scale 1.28, offset (5,170). Ground (feet bottom) = 1455.
Layer order (back view, cape in front of torso, behind arms/legs surface):
  cape < belt_pelvis < thighs < shins < upper_arms < forearm_hands < head_cowl
  (no separate torso piece: cape IS the torso covering from the back, as drawn;
   belt_pelvis is drawn over the cape, as drawn.)
Joint locks (together, not in space): shoulder->upper_arm->elbow->forearm_hand
  (hand fused into forearm piece, as drawn), hip->thigh->knee(pivot)->shin_boot.
  Knee pad is line art on the thigh piece; knee joint = pivot point, not a piece.
Poses: back-stand (T-pose as drawn, reassembly gate) and back-arms-down (FK proof:
  upper arms rotated about shoulder pivots, forearms follow elbows).
No front piece mirrored, no front piece reused. Front Neck.png is NOT used here:
  from the back the neck is hidden by cowl + cape collar, as drawn.
"""
from PIL import Image
import json, math, os
BASE="/home/hatch/workspace/cape-jones-rig/back-art-back-rig-view-field-20261101"
P=f"{BASE}/pieces"
OUT=f"{BASE}/poses"
SCALE=1.28; OX=5; OY=170; CANVAS=(1400,1600)
def S(x,y): return (x*SCALE+OX, y*SCALE+OY)
def load(name):
    im=Image.open(f"{P}/{name}") if name.endswith(".png") else Image.open(f"{P}/{name}.png").convert("RGBA")
    return im.resize((round(im.size[0]*SCALE), round(im.size[1]*SCALE)), Image.LANCZOS)
# piece placement: (piece, source_box_origin, anchor_in_piece_scaled)
# anchor = joint point in piece coords (pre-scale, source pixels)
PIECES={
 "back_cape":           ("back_cape.png",(260,145),(285,0)),
 "back_belt_pelvis":    ("back_belt_pelvis.png",(400,465),(142,0)),
 "back_thigh_L":        ("back_thigh_L.png",(405,620),(72,0)),
 "back_thigh_R":        ("back_thigh_R.png",(540,620),(70,0)),
 "back_shin_boot_L":    ("back_shin_boot_L.png",(400,820),(52,0)),
 "back_shin_boot_R":    ("back_shin_boot_R.png",(590,820),(50,0)),
 "back_upper_arm_L":    ("back_upper_arm_L.png",(290,170),(90,67)),
 "back_forearm_hand_L": ("back_forearm_hand_L.png",(50,170),(240,67)),
 "back_upper_arm_R":    ("back_upper_arm_R.png",(705,170),(0,67)),
 "back_forearm_hand_R": ("back_forearm_hand_R.png",(800,170),(0,67)),
 "back_head_cowl":      ("back_head_cowl.png",(490,0),(52,150)),
}
ORDER=["back_cape","back_belt_pelvis","back_thigh_L","back_thigh_R","back_shin_boot_L",
       "back_shin_boot_R","back_upper_arm_L","back_upper_arm_R","back_forearm_hand_L",
       "back_forearm_hand_R","back_head_cowl"]
def place(canvas, name, xy=None, pivot=None, clockwise_deg=0, anchor=None):
    """Paste piece at source origin xy (or rotate about pivot). anchor: point in
    piece (scaled px) that must land on pivot after rotation."""
    fname, origin, _ = PIECES[name]
    piece=load(fname)
    if pivot is None:
        x,y=S(*origin) if xy is None else xy
        canvas.alpha_composite(piece,(round(x),round(y)))
        return {"xy":[round(x),round(y)],"size":list(piece.size)}
    layer=Image.new("RGBA",CANVAS,(0,0,0,0))
    ax,ay=anchor
    layer.alpha_composite(piece,(round(pivot[0]-ax),round(pivot[1]-ay)))
    # PIL rotate: positive = counter-clockwise visually = negative clockwise
    layer=layer.rotate(-clockwise_deg, center=pivot, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    return {"pivot":[round(pivot[0]),round(pivot[1])],"clockwise_deg":clockwise_deg}
def rot_vec(vx,vy,deg_cw):
    a=math.radians(deg_cw); c,s=math.cos(a),math.sin(a)
    return (vx*c - vy*s, vx*s + vy*c)  # y-down coords, positive deg = clockwise visually
def build(pose):
    canvas=Image.new("RGBA",CANVAS,(0,0,0,0))
    info={}
    # static pieces first in ORDER, arms handled by pose branch
    static=[n for n in ORDER if "arm" not in n and "forearm" not in n]
    for n in static:
        info[n]=place(canvas,n)
    # shoulders in rig coords (source shoulder points)
    shL=S(375,228); shR=S(710,228)
    if pose=="back-stand":
        for n in ["back_upper_arm_L","back_upper_arm_R","back_forearm_hand_L","back_forearm_hand_R"]:
            info[n]=place(canvas,n)
        info["shoulder_L"]=shL; info["shoulder_R"]=shR
    elif pose=="back-arms-down":
        # upper L: shoulder anchor = right end centre of piece (80,21); outer = left end (0,21)
        # rotate so (-1,0) -> (0,1): clockwise -90 in y-down math? verified by gate below.
        # We rotate by +90 clockwise visually: vector (-1,0) -> (0,-1) is UP, so use -90.
        for side,sh,upper,fore,inner_x in [("L",shL,"back_upper_arm_L","back_forearm_hand_L",90),
                                            ("R",shR,"back_upper_arm_R","back_forearm_hand_R",0)]:
            deg=-90  # clockwise_deg param: -90 = 90 counter-clockwise visually = down for L? checked by gate
            # For R, vector (+1,0) -> down (0,1) needs +90 clockwise. So per-side sign:
            deg = -90 if side=="L" else 90
            up=load(PIECES[upper][0]); up_w=up.size[0]
            anchor=(inner_x*SCALE, 67*SCALE)
            info[upper]=place(canvas,upper,pivot=sh,clockwise_deg=deg,anchor=anchor)
            # elbow = shoulder + rotated (outer-inner) vector
            outer_local=((0-inner_x)*SCALE,0) if side=="L" else ((95-inner_x)*SCALE,0)
            # outer_local for L: (0-80)*SCALE; for R piece width 80, outer at x=80: (80-0)*SCALE
            ev=rot_vec(*outer_local,deg)
            elbow=(sh[0]+ev[0], sh[1]+ev[1])
            fanchor=(240*SCALE,67*SCALE) if side=="L" else (0*SCALE,67*SCALE)
            info[fore]=place(canvas,fore,pivot=elbow,clockwise_deg=deg,anchor=fanchor)
            info[f"shoulder_{side}"]=sh; info[f"elbow_{side}"]=elbow
    else:
        raise ValueError(pose)
    a=canvas.getchannel("A"); bb=a.getbbox()
    info["bbox"]=list(bb) if bb else None
    info["alpha_px"]=sum(1 for v in a.getdata() if v>10)
    info["inside_canvas"]=bb is not None and bb[0]>=0 and bb[1]>=0 and bb[2]<=1400 and bb[3]<=1600
    canvas.save(f"{OUT}/{pose}-20261101.png")
    canvas2=Image.new("RGBA",CANVAS,(128,128,128,255)); canvas2.alpha_composite(canvas)
    canvas2.save(f"{OUT}/{pose}-20261101-on-grey.png")
    return info
gates={}
for pose in ["back-stand","back-arms-down"]:
    gates[pose]=build(pose)
    print(pose, gates[pose]["bbox"], "alpha", gates[pose]["alpha_px"], "inside", gates[pose]["inside_canvas"])
    if pose=="back-arms-down":
        print("  elbows", gates[pose].get("elbow_L"), gates[pose].get("elbow_R"))
# reassembly gate: stand vs source plate scaled to same geometry
src=Image.open("/home/hatch/workspace/cape-jones-rig/sliced-clean-20261031/B-model/model-sheet-back-set2/Row1_1.png").convert("RGBA")
src_s=src.resize((round(1086*SCALE),round(1004*SCALE)), Image.LANCZOS)
plate=Image.new("RGBA",CANVAS,(0,0,0,0)); plate.alpha_composite(src_s,(round(OX),round(OY)))
stand=Image.open(f"{OUT}/back-stand-20261101.png")
import numpy as np
pa=np.array(plate.getchannel("A"))>10; sa=np.array(stand.getchannel("A"))>10
gates["reassembly"]={"source_alpha_px":int(pa.sum()),"stand_alpha_px":int(sa.sum()),
  "only_source":int((pa&~sa).sum()),"only_stand":int((sa&~pa).sum()),
  "note":"only_source = sheet pixels not covered by any cut piece (cape highlights masked out of cape piece + arm-band slice edges); only_stand = piece pixels outside sheet (cut-through edges + overlaps)."}
print(gates["reassembly"])
json.dump(gates, open(f"{BASE}/gates-20261101.json","w"), indent=1)
