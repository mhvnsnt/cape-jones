from PIL import Image
import json, os
ROOT="/home/hatch/workspace/cape-jones-rig"
OUT=f"{ROOT}/rig-34-literal-widget-rebuild-20261101"
P34=f"{ROOT}/sitting-rig-34-20261101/pieces"
PV7=f"{ROOT}/cut-limbs-v7c"
# id, source, display size (widget DEFS), pivot ox,oy, z, defs_order
DEFS=[
 ("cape", f"{P34}/cape_back.png", (514,900), (0.5,0.5), 0),
 ("upperArmL", f"{P34}/upper_arm_L_socket.png", (125,237), (0.5,0), 1),
 ("thighR", f"{P34}/thigh_bent_R.png", (218,299), (0.5,0), 2),
 ("thighL", f"{P34}/thigh_bent_L.png", (230,267), (0.5,0), 3),
 ("forearmL", f"{PV7}/Arm_Front_Lower.png", (145,275), (0.39,0.11), 4),
 ("pelvis", f"{P34}/pelvis_belt.png", (218,181), (0.5,0.5), 4),
 ("kneeL", f"{P34}/knee_ball_spare.png", (74,94), (0.5,0.5), 4),
 ("elbowCapL", f"{PV7}/Arm_Front_Cap.png", (63,63), (0.5,0.5), 5),
 ("shinL", f"{P34}/shin_boot_L.png", (244,410), (0.5,0), 6),
 ("shinR", f"{P34}/shin_boot_mid.png", (256,415), (0.5,0), 6),
 ("kneeR", f"{P34}/knee_ball_spare.png", (74,94), (0.5,0.5), 7),
 ("torso", f"{P34}/torso.png", (291,315), (0.5,0), 8),
 ("head", f"{P34}/head_cowl.png", (130,196), (0.5,0.5), 9),
 ("upperArmR", f"{P34}/upper_arm_R.png", (112,256), (0.5,0), 10),
 ("forearmR", f"{PV7}/Arm_Back_Lower.png", (150,274), (0.63,0.11), 11),
 ("elbowCapR", f"{PV7}/Arm_Back_Cap.png", (63,63), (0.5,0.5), 12),
 ("handL", f"{P34}/hand_spare_L.png", (117,170), (0.5,0.5), 13),
 ("handR", f"{P34}/hand_spare_L.png", (117,170), (0.5,0.5), 13),
]
SAVED={
 "cape":(360,330,0),"upperArmL":(490,390,5),"thighR":(590,750,6),"thighL":(400,710,2),
 "forearmL":(455,580,-15),"pelvis":(565,650,0),"kneeL":(380,885,0),"elbowCapL":(465,580,0),
 "shinL":(225,945,0),"shinR":(395,985,-10),"kneeR":(560,950,0),"torso":(550,370,0),
 "head":(635,195,0),"upperArmR":(805,420,15),"forearmR":(685,650,45),"elbowCapR":(775,610,0),
 "handL":(530,740,-46),"handR":(565,755,70),
}
W,H=1400,1600
canvas=Image.new("RGBA",(W,H),(0,0,0,0))
centres={}
for idx,(pid,src,size,(ox,oy),z) in enumerate(DEFS):
    x,y,rot=SAVED[pid]
    im=Image.open(src).convert("RGBA").resize(size, Image.LANCZOS)
    if pid=="handR":
        im=im.transpose(Image.FLIP_LEFT_RIGHT)
    # rotate about pivot: paste on large temp, rotate, then place so pivot lands at saved x+ox*w, y+oy*h
    # PIL rotate: positive = CCW, widget/CSS positive = CW, so rotate by -rot
    tmp=Image.new("RGBA",(size[0]*3,size[1]*3),(0,0,0,0))
    tmp.alpha_composite(im,(size[0],size[1]))
    # pivot in tmp coords
    px,py=size[0]+ox*size[0], size[1]+oy*size[1]
    rot_im=tmp.rotate(-rot, resample=Image.BICUBIC, center=(px,py))
    # pivot point after rotation stays same in tmp coords
    paste_x=int(round(x+ox*size[0]-px)); paste_y=int(round(y+oy*size[1]-py))
    canvas.alpha_composite(rot_im,(paste_x,paste_y))
    # alpha bbox centre of this piece alone (re-render single)
    single=Image.new("RGBA",(W,H),(0,0,0,0)); single.alpha_composite(rot_im,(paste_x,paste_y))
    bb=single.getbbox()
    centres[pid]={"saved_xy":[x,y],"rotation":rot,"size":list(size),"pivot":[ox,oy],"z":z,
                  "alpha_bbox":list(bb) if bb else None,
                  "alpha_centre":[round((bb[0]+bb[2])/2,1),round((bb[1]+bb[3])/2,1)] if bb else None,
                  "expected_pivot_xy":[round(x+ox*size[0],1),round(y+oy*size[1],1)]}
canvas.save(f"{OUT}/poses/sit-chair-literal-widget-20261101.png")
bg=Image.new("RGBA",(W,H),(126,126,126,255)); bg.alpha_composite(canvas); bg.convert("RGB").save(f"{OUT}/poses/sit-chair-literal-widget-20261101-on-grey.png")
# side-by-side: previous rebuild vs literal
prev=Image.open(f"{ROOT}/rig-34-rebuilt-saved-20261101/poses/sit-chair-rebuilt-saved-20261101-on-grey.png").convert("RGB")
cur=bg.convert("RGB")
contact=Image.new("RGB",(1400,800),(255,255,255))
contact.paste(prev.resize((700,800)),(0,0)); contact.paste(cur.resize((700,800)),(700,0))
contact.save(f"{OUT}/contacts/side-by-side-previous-vs-literal-20261101.png")
# gates
import numpy as np
a=np.array(canvas); alpha=a[:,:,3]>0
ys,xs=np.where(alpha)
bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
left=np.where(alpha[:,:700])[0]; right=np.where(alpha[:,700:])[0]
gates={"canvas":[W,H],"bbox":bbox,"alpha_bottom_overall":int(ys.max()),
 "alpha_bottom_left_band_0_700":int(left.max()) if len(left) else None,
 "alpha_bottom_right_band_700_1400":int(right.max()) if len(right) else None,
 "widget_ground_y":1475,"hands":2,"fists_drawn_full_forearm":2,
 "note":"Full forearm+fist drawn as in widget; separate open hands drawn over them at saved positions. Fist peek is therefore possible where hand shape is narrower than fist; see zooms/table, not hidden."}
json.dump({"centres":centres,"gates":gates}, open(f"{OUT}/gates-20261101.json","w"), indent=2)
print(json.dumps(gates,indent=2)); print(centres)
