"""Cut back rig pieces from the TRUE hand-drawn back sheet (not a mirror, not a redraw).
Source (read-only): sliced-clean-20261031/B-model/model-sheet-back-set2/Row1_1.png (1086x1004)
Method: region-box crops + colour mask. Dark mask = cape (max channel < 80).
Non-dark mask = suit/gauntlet/cowl (removes cape intrusion into limb boxes).
Arm boxes are tight to the arm band (y235-275) because at y245-255 the arm+cape
run is continuous; the discriminating row is y260 (upper 310-367, forearm 169-260,
gap 261-309 = elbow split). Knee pads are LINE ART on the thigh in this sheet,
not separable solids, so knees are pivots on thigh/shin pieces, NOT separate pieces.
No pixels recoloured, no mirror, no front piece reused.
"""
from PIL import Image
import json
ROOT="/home/hatch/workspace/cape-jones-rig"
SRC=f"{ROOT}/sliced-clean-20261031/B-model/model-sheet-back-set2/Row1_1.png"
OUT="/home/hatch/workspace/cape-jones-rig/back-art-back-rig-view-field-20261101/pieces"
im=Image.open(SRC).convert("RGBA")
def crop(box, mask=None):
    piece=im.crop(box)
    # fringe kill: alpha <128 -> transparent (true-master twist v6 method)
    _px=piece.load()
    for _y in range(piece.size[1]):
        for _x in range(piece.size[0]):
            if _px[_x,_y][3]<128:
                _px[_x,_y]=(0,0,0,0)
    if mask:
        px=piece.load()
        for y in range(piece.size[1]):
            for x in range(piece.size[0]):
                r,g,b,a=px[x,y]
                if a>10 and not mask(r,g,b):
                    px[x,y]=(0,0,0,0)
    return piece
def dark(r,g,b): return max(r,g,b)<80
def nondark(r,g,b): return max(r,g,b)>=80
BOXES={
 "back_head_cowl":      ((490,0,595,150), None),
 "back_cape":           ((260,145,830,1004), dark),
 "back_belt_pelvis":    ((400,465,685,650), nondark),
 "back_upper_arm_L":    ((290,170,380,280), nondark),
 "back_forearm_hand_L": ((50,170,290,280), nondark),
 "back_upper_arm_R":    ((705,170,800,280), nondark),
 "back_forearm_hand_R": ((800,170,1035,280), nondark),
 "back_thigh_L":        ((405,620,550,850), nondark),
 "back_thigh_R":        ((540,620,680,850), nondark),
 "back_shin_boot_L":    ((400,820,505,1004), nondark),
 "back_shin_boot_R":    ((590,820,690,1004), nondark),
}
stats={}
for name,(box,mask) in BOXES.items():
    p=crop(box,mask); p.save(f"{OUT}/{name}.png")
    a=p.getchannel("A"); bb=a.getbbox()
    n=sum(1 for v in a.getdata() if v>10)
    stats[name]={"source_box":list(box),"size":list(p.size),"alpha_bbox_in_piece":list(bb) if bb else None,"alpha_px":n}
    print(name, p.size, "alpha_bbox", bb, "px", n)
json.dump(stats, open("/home/hatch/workspace/cape-jones-rig/back-art-back-rig-view-field-20261101/piece-stats-20261101.json","w"), indent=1)
print("pieces:", len(stats), "total_alpha_px:", sum(s["alpha_px"] for s in stats.values()))
