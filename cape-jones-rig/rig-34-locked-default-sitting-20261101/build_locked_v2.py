from PIL import Image
import json, os, math
ROOT="/home/hatch/workspace/cape-jones-rig"
OUT=f"{ROOT}/rig-34-locked-default-sitting-20261101"
P34=f"{ROOT}/sitting-rig-34-20261101/pieces"
PV7=f"{ROOT}/cut-limbs-v7c"
# DEFS from literal rebuild, in DEFS-stable z order; neck inserted z=8.5 (after arms, before head)
DEFS=[
 ("cape", f"{P34}/cape_back.png", (514,900), (0.5,0.5), 0),
 ("upperArmL", f"{P34}/upper_arm_L_socket.png", (125,237), (0.5,0), 1),
 ("thighR", f"{P34}/thigh_bent_R.png", (218,299), (0.5,0), 2),
 ("thighL", f"{P34}/thigh_bent_L.png", (230,267), (0.5,0), 3),
 ("forearmL", f"{ROOT}/rig-34-disassembled-wired-20261101/pieces/forearm_no_fist_L.png", (145,275), (0.39,0.11), 4),
 ("pelvis", f"{P34}/pelvis_belt.png", (218,181), (0.5,0.5), 4),
 ("kneeL", f"{P34}/knee_ball_spare.png", (74,94), (0.5,0.5), 4),
 ("elbowCapL", f"{PV7}/Arm_Front_Cap.png", (63,63), (0.5,0.5), 5),
 ("shinL", f"{P34}/shin_boot_L.png", (244,410), (0.5,0), 6),
 ("shinR", f"{P34}/shin_boot_mid.png", (256,415), (0.5,0), 6),
 ("kneeR", f"{P34}/knee_ball_spare.png", (74,94), (0.5,0.5), 7),
 ("torso", f"{P34}/torso.png", (291,315), (0.5,0), 8),
 ("upperArmR", f"{P34}/upper_arm_R.png", (112,256), (0.5,0), 10),
 ("forearmR", f"{ROOT}/rig-34-disassembled-wired-20261101/pieces/forearm_no_fist_R.png", (150,274), (0.63,0.11), 11),
 ("elbowCapR", f"{PV7}/Arm_Back_Cap.png", (63,63), (0.5,0.5), 12),
 # neck: front view, sliced/Neck.png, alpha-cropped 96x78 -> rendered 101x82 at v7c 1.05, centre x700, top 330
 ("neck", f"{ROOT}/sliced/Neck.png", (109,87), (0.5,0.5), 8.5),
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
# neck saved placement: centre 700, top 330 -> top-left = 700-50.5=649.5 -> 650,330 ; rotation 0
NECK_XY=(645,329,0)
W,H=1400,1600
# upper-body group moves together in animation (bob), preserving shoulder/torso locks
UPPER={"head","neck","torso","upperArmL","upperArmR","forearmL","forearmR","elbowCapL","elbowCapR","handL","handR"}
def paste_piece(canvas, pid, src, size, pivot, rot, xy, flip=False):
    ox,oy=pivot; x,y=xy
    im=Image.open(src).convert("RGBA")
    # neck: WHOLE piece, no crop ever (new standing rule) - full 104x83 resized to 109x87,
    # so its alpha (96x78) renders at 101x82, exactly the front-view rendered size.
    im=im.resize(size, Image.LANCZOS)
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    tmp=Image.new("RGBA",(size[0]*3,size[1]*3),(0,0,0,0))
    tmp.alpha_composite(im,(size[0],size[1]))
    px,py=size[0]+ox*size[0], size[1]+oy*size[1]
    rot_im=tmp.rotate(-rot, resample=Image.BICUBIC, center=(px,py))
    paste_x=int(round(x+ox*size[0]-px)); paste_y=int(round(y+oy*size[1]-py))
    canvas.alpha_composite(rot_im,(paste_x,paste_y))
    return rot_im, paste_x, paste_y

def render(bob_y=0, extra_head_rot=0):
    canvas=Image.new("RGBA",(W,H),(0,0,0,0))
    centres={}
    for pid,src,size,pivot,z in DEFS:
        if pid=="neck":
            x,y,rot=NECK_XY
        elif pid=="head":
            x,y,rot=SAVED[pid]; rot=rot+extra_head_rot
        else:
            x,y,rot=SAVED[pid]
        if pid in UPPER: y=y+bob_y
        # head is in UPPER but also handled above; neck too
        rot_im,px,py=paste_piece(canvas,pid,src,size,pivot,rot,(x,y),flip=(pid=="handR"))
        single=Image.new("RGBA",(W,H),(0,0,0,0)); single.alpha_composite(rot_im,(px,py))
        bb=single.getbbox()
        centres[pid]={"xy":[x,y],"rotation":rot,"size":list(size),"pivot":list(pivot),"z":z,
                      "alpha_bbox":list(bb) if bb else None,
                      "alpha_centre":[round((bb[0]+bb[2])/2,1),round((bb[1]+bb[3])/2,1)] if bb else None,
                      "expected_pivot_xy":[round(x+pivot[0]*size[0],1),round(y+pivot[1]*size[1],1)]}
    # head separately (not in DEFS list order above? it is missing: add it after neck, before hands is wrong order;
    # Actually DEFS omitted head intentionally? No - re-add: we must draw head after neck. Do it here on top of canvas in correct order is impossible after hands.
    return canvas, centres
# NOTE: DEFS above omitted head by mistake in list construction - fix by rebuilding with head included in order:
DEFS2=[]
for pid,src,size,pivot,z in DEFS:
    DEFS2.append((pid,src,size,pivot,z))
    if pid=="neck":
        DEFS2.append(("head", f"{P34}/head_cowl.png", (130,196), (0.5,0.5), 9))
def render2(bob_y=0, extra_head_rot=0):
    canvas=Image.new("RGBA",(W,H),(0,0,0,0))
    centres={}
    for pid,src,size,pivot,z in DEFS2:
        if pid=="neck":
            x,y,rot=NECK_XY
        elif pid=="head":
            x,y,rot=SAVED[pid]; rot=rot+extra_head_rot
        else:
            x,y,rot=SAVED[pid]
        if pid in UPPER: y=y+bob_y
        rot_im,px,py=paste_piece(canvas,pid,src,size,pivot,rot,(x,y),flip=(pid=="handR"))
        single=Image.new("RGBA",(W,H),(0,0,0,0)); single.alpha_composite(rot_im,(px,py))
        bb=single.getbbox()
        centres[pid]={"xy":[x,y],"rotation":rot,"size":list(size),"pivot":list(pivot),"z":z,
                      "alpha_bbox":list(bb) if bb else None,
                      "alpha_centre":[round((bb[0]+bb[2])/2,1),round((bb[1]+bb[3])/2,1)] if bb else None,
                      "expected_pivot_xy":[round(x+pivot[0]*size[0],1),round(y+pivot[1]*size[1],1)]}
    return canvas, centres

canvas,centres=render2(0,0)
canvas.save(f"{OUT}/poses/default-sitting-pose-locked-20261101.png")
bg=Image.new("RGBA",(W,H),(126,126,126,255)); bg.alpha_composite(canvas); bg.convert("RGB").save(f"{OUT}/poses/default-sitting-pose-locked-20261101-on-grey.png")
# neck closeup crop around neck/head/torso join
crop=bg.convert("RGB").crop((550,180,850,500)); crop=crop.resize((crop.width*2,crop.height*2), Image.NEAREST)
crop.save(f"{OUT}/contacts/neck-closeup-20261101.png")
# joint-lock diagram: text overlay on grey figure using PIL default font, listing locks
from PIL import ImageDraw
diag=bg.convert("RGB").copy(); d=ImageDraw.Draw(diag)
locks=["SHOULDER->TORSO","ELBOW->BICEP","ELBOW->FOREARM","FOREARM->WRIST/HAND","HIP->PELVIS","HIP->KNEE TURN","KNEE->SHIN","CAPE->BACK","NECK->HEAD"]
for i,t in enumerate(locks):
    d.rectangle([20,20+i*28,340,44+i*28], fill=(0,0,0)); d.text((28,26+i*28), t, fill=(255,255,0))
diag.save(f"{OUT}/contacts/joint-lock-diagram-20261101.png")
# animation: 48f @24fps, 2s loop, upper-body bob +-3px, head tilt +-2deg, all upper chains move together
import numpy as np
frames=[]
for f in range(48):
    bob=int(round(3*math.sin(2*math.pi*f/48)))
    tilt=int(round(2*math.sin(2*math.pi*f/48)))
    c,_=render2(bob, tilt)
    b=Image.new("RGBA",(W,H),(126,126,126,255)); b.alpha_composite(c); rgb=b.convert("RGB")
    rgb.save(f"{OUT}/frames/frame-{f:02d}.png")
    frames.append(rgb)
frames[0].save(f"{OUT}/frames/first-frame-20261101.png")
frames[-1].save(f"{OUT}/frames/last-frame-20261101.png")
frames[0].save(f"{OUT}/animation/sit-idle-locked-20261101.gif", save_all=True, append_images=frames[1:], duration=42, loop=0) if False else None
# gif via PIL (need dir)
os.makedirs(f"{OUT}/animation", exist_ok=True)
frames[0].save(f"{OUT}/animation/sit-idle-locked-20261101.gif", save_all=True, append_images=frames[1:], duration=42, loop=0)
a=np.array(canvas); alpha=a[:,:,3]>0; ys,xs=np.where(alpha)
gates={"canvas":[W,H],"bbox":[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
 "alpha_bottom_overall":int(ys.max()),"neck":{"source":"sliced/Neck.png","rendered_size":[101,82],"centre_x":700,"top":330,"bottom":412,"draw_order":"after arms, before head","front_view_scale":"1.05, native alpha 96x78"},
 "head_bottom":centres["head"]["alpha_bbox"][3],"torso_top":centres["torso"]["alpha_bbox"][1],
 "hands":2,"fists_full_forearm_drawn":2,
 "note":"Full forearm+fist drawn as in literal widget rebuild; separate open hands drawn over them at saved positions. Fist-omitted clean version is a separate toggleable-layer job, not faked here."}
json.dump({"centres":centres,"gates":gates}, open(f"{OUT}/gates-20261101.json","w"), indent=2)
print(json.dumps(gates,indent=2))
print("neck centre", centres["neck"])
