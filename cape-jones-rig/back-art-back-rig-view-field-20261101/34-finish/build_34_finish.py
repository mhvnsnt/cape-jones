"""3/4 SITTING RIG - FINISH, from the LOCKED DEFAULT SITTING POSE.
Base: rig-34-disassembled-wired-20261101 (APPROVED PERFECT 2026-11-01 01:21 CST)
  + rig-34-locked-default-sitting-20261101 v2 (fists OFF, whole pieces only).
Method: rebuild FROM THE WIRED MANIFEST ALONE (same rotation method as
  build_wired.py: rotate -rotation about piece centre, place so centre lands
  on pivot_xy), then add the neck. This is a rig rebuild, not a copy of a flat PNG.
Neck: sliced/Neck.png (front rig, READ ONLY, md5 94025a6c683d6b7d6b2bc73267b2e725),
  whole file, NO crop, resized 104x83 -> 109x87 so its alpha renders 101 wide,
  exactly the front-view rendered size. Drawn AFTER arms, BEFORE head (z 8.5),
  attached to head as in the front view: alpha centre x ~700, bridging head
  bottom 391 and torso top 370.
Fists: OFF (toggleable layers, visible=false), hands 2, thumbs opposite.
Joint locks are TOGETHER, NOT frozen in space: chains move together; the
  manifest records parent/child pivots, and no piece is frozen at an absolute
  position outside its chain. Knee/shin gap is MEASURED below, not hidden.
RIG-00 front rig untouched. No repo push.
"""
from PIL import Image
import json, os, hashlib
ROOT="/home/hatch/workspace/cape-jones-rig"
WIRED=f"{ROOT}/rig-34-disassembled-wired-20261101"
OUT="/home/hatch/workspace/cape-jones-rig/back-art-back-rig-view-field-20261101/34-finish"
W,H=1400,1600
man=json.load(open(f"{WIRED}/MANIFEST-20261101.json"))
pieces=sorted([p for p in man["pieces"] if p["visible"]], key=lambda p:(p["z"], p["defs_order"]))
def render_piece(p):
    im=Image.open(os.path.join(WIRED, p["file"])).convert("RGBA")
    im=im.resize(tuple(p["display_size"]), Image.LANCZOS)
    if p.get("flip"):
        im=im.transpose(Image.FLIP_LEFT_RIGHT)
    px,py=p["pivot_xy"]; ox,oy=p["pivot"]
    ccx,ccy=im.width*ox, im.height*oy
    tmp=Image.new("RGBA",(im.width*3,im.height*3),(0,0,0,0))
    tmp.alpha_composite(im,(im.width,im.height))
    rot=tmp.rotate(-p["rotation"], resample=Image.BICUBIC, center=(im.width+ccx, im.height+ccy))
    layer=Image.new("RGBA",(W,H),(0,0,0,0))
    layer.alpha_composite(rot,(int(round(px-(im.width+ccx))), int(round(py-(im.height+ccy)))))
    return layer
canvas=Image.new("RGBA",(W,H),(0,0,0,0))
layers={}
for p in pieces:
    lay=render_piece(p)
    layers[p["id"]]=lay
    if p["id"]=="torso":
        # neck goes after arms (upperArmR/forearmR/elbowCapR are z10-12, after torso)
        pass
    canvas.alpha_composite(lay)
# Neck insertion must be AFTER arms, BEFORE head: rebuild in correct order instead.
canvas=Image.new("RGBA",(W,H),(0,0,0,0))
neck_src=Image.open(f"{ROOT}/sliced/Neck.png").convert("RGBA")
md5=hashlib.md5(open(f"{ROOT}/sliced/Neck.png","rb").read()).hexdigest()
neck=neck_src.resize((109,87), Image.LANCZOS)
neck_layer=Image.new("RGBA",(W,H),(0,0,0,0))
neck_layer.alpha_composite(neck,(646,329))  # alpha centre lands ~700,371 (measured below)
for p in pieces:
    if p["id"]=="head":
        canvas.alpha_composite(neck_layer)
    canvas.alpha_composite(layers[p["id"]])
a=canvas.getchannel("A"); bb=a.getbbox()
na=neck_layer.getchannel("A"); nbb=na.getbbox()
canvas.save(f"{OUT}/default-sitting-finished-20261101.png")
bg=Image.new("RGBA",(W,H),(128,128,128,255)); bg.alpha_composite(canvas)
bg.save(f"{OUT}/default-sitting-finished-20261101-on-grey.png")
# per-piece final alpha bboxes
pb={}
for pid,lay in layers.items():
    b=lay.getchannel("A").getbbox(); pb[pid]=list(b) if b else None
pb["neck"]=list(nbb) if nbb else None
# knee/shin gap measurement (both legs, from final layers)
import numpy as np
def gap(leg):
    k=layers[f"knee{leg}"]; s=layers[f"shin{leg}"]
    ka=np.array(k.getchannel("A"))>10; sa=np.array(s.getchannel("A"))>10
    overlap=int((ka&sa).sum())
    kb=k.getchannel("A").getbbox(); sb=s.getchannel("A").getbbox()
    kcx=(kb[0]+kb[2])/2; kcy=(kb[1]+kb[3])/2
    # shin pivot_xy from manifest (top-centre of shin piece)
    sp=[p for p in man["pieces"] if p["id"]==f"shin{leg}"][0]["pivot_xy"]
    kp=[p for p in man["pieces"] if p["id"]==f"knee{leg}"][0]["pivot_xy"]
    import math
    dist=math.hypot(sp[0]-kp[0], sp[1]-kp[1])
    return {"knee_bbox":list(kb),"shin_bbox":list(sb),"knee_pivot_xy":kp,"shin_pivot_xy":sp,
            "pivot_centre_distance_px":round(dist,1),
            "horizontal_pivot_offset_px":round(sp[0]-kp[0],1),
            "vertical_pivot_offset_px":round(sp[1]-kp[1],1),
            "alpha_overlap_px":overlap,
            "knee_bottom_minus_shin_top_px":round(kb[3]-sb[1],1)}
gates={"canvas":[W,H],"bbox":list(bb) if bb else None,
       "alpha_px":sum(1 for v in a.getdata() if v>10),
       "inside_canvas":bool(bb and bb[0]>=0 and bb[1]>=0 and bb[2]<=W and bb[3]<=H),
       "pieces_drawn":len(pieces),"pieces_total_manifest":man["piece_count"],
       "fists_drawn":0,"hands_drawn":2,
       "neck":{"source":"sliced/Neck.png","md5":md5,"resized_to":[109,87],
               "alpha_bbox":list(nbb) if nbb else None,
               "alpha_width_px":(nbb[2]-nbb[0]) if nbb else None,
               "alpha_height_px":(nbb[3]-nbb[1]) if nbb else None,
               "draw_order":"after arms, before head (z 8.5)","piece_crop":"NONE - whole file"},
       "piece_bboxes":pb,
       "knee_shin_L":gap("L"),"knee_shin_R":gap("R")}
# compare with locked v2 pose
locked=Image.open(f"{ROOT}/rig-34-locked-default-sitting-20261101/poses/default-sitting-pose-locked-20261101.png").convert("RGBA")
la=np.array(locked.getchannel("A"))>10; ca=np.array(canvas.getchannel("A"))>10
gates["vs_locked_v2"]={"locked_bbox":list(locked.getchannel("A").getbbox()),
  "finished_bbox":list(bb) if bb else None,
  "alpha_only_locked":int((la&~ca).sum()),"alpha_only_finished":int((ca&~la).sum())}
print(json.dumps(gates,indent=1))
json.dump(gates, open(f"{OUT}/gates-20261101.json","w"), indent=1)
