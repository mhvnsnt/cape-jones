"""Ghost measurement v1 (image crossfade) vs v2 (rig-angle actual frames).
Silhouette = pixel mean-abs distance from grey-128 background > 40.
Edge = silhouette pixel with a 4-neighbour non-silhouette pixel.
Double-edge ratio = edge_count(mid) / mean(edge_count(keyA), edge_count(keyB)).
A ratio ~2 means two figures' edges are superimposed (ghost); ~1 means one figure.
Wash = pixels in A-xor-B silhouette where the mid pixel sits halfway between
that key's pixel and grey (mean-abs diff to grey 20..120 AND diff to key >20):
exactly what a 50% crossfade produces in a non-overlap region. A rig frame
has solid figure or grey there, not a halfway wash, except anti-aliased edges.
v1 frames: poses-as-movements-20261031/frames/move-serve-to-guard-*.jpg
v1 serve->guard blend frames are 011,012,013; mid = 012 (t=0.5).
v2 frames: movements-interp-v2-20261031/frames/move-serve-to-guard-v2-*.jpg
v2 serve->guard inbetweens are 013..017; mid/breakdown = 015 (t=0.5).
Keys for both: original serve/guard files, framed exactly as v1 load()
(1100x1500 -> 550x750, centred on 1100x750 grey-128).
"""
from PIL import Image
import numpy as np, os, json
R="/home/hatch/workspace/cape-jones-rig"
def load_v1key(path):
    im=Image.open(path).convert("RGBA").resize((550,750), Image.LANCZOS)
    c=Image.new("RGBA",(1100,750),(128,128,128,255)); c.alpha_composite(im,((1100-550)//2,0)); return c.convert("RGB")
def sil(arr):
    return np.mean(np.abs(arr.astype(int)-128),axis=2)>40
def edge_count(s):
    e=np.zeros_like(s); e[1:-1,1:-1]= s[1:-1,1:-1] & (~s[:-2,1:-1] | ~s[2:,1:-1] | ~s[1:-1,:-2] | ~s[1:-1,2:])
    return int(e.sum())
def wash(a,b,mid):
    sa,sb,sm=sil(a),sil(b),sil(mid); xor=sa ^ sb
    # in xor region, the covering key is the one whose silhouette covers it
    key=np.where(sa[:,:,None],a,b)
    d_grey=np.mean(np.abs(mid.astype(int)-128),axis=2); d_key=np.mean(np.abs(mid.astype(int)-key.astype(int)),axis=2)
    return int((xor & (d_grey>20) & (d_grey<120) & (d_key>20)).sum()), int(xor.sum())
def iou(sa,sb): return float((sa&sb).sum()/max(1,(sa|sb).sum()))
def arr(p): return np.array(Image.open(p).convert("RGB"))
serve=load_v1key(os.path.join(R,"ginyu-force-poses-20261031/jei-01-crusher-serve-windup-20261031.png"))
guard=load_v1key(os.path.join(R,"ginyu-force-poses-20261031/gul-03-guard-crouch-startled-20261031.png"))
fight_orig=load_v1key(os.path.join(R,"reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png"))
A=np.array(serve); B=np.array(guard); sa,sb=sil(A),sil(B)
v1mid=arr(os.path.join(R,"poses-as-movements-20261031/frames/move-serve-to-guard-012.jpg"))
v2mid=arr(os.path.join(R,"movements-interp-v2-20261031/frames/move-serve-to-guard-v2-015.jpg"))
v2serve=arr(os.path.join(R,"movements-interp-v2-20261031/frames/move-serve-to-guard-v2-008.jpg"))
v2guard=arr(os.path.join(R,"movements-interp-v2-20261031/frames/move-serve-to-guard-v2-018.jpg"))
v2fight=arr(os.path.join(R,"movements-interp-v2-20261031/frames/move-serve-to-guard-v2-028.jpg"))
def report(name,mid):
    sm=sil(mid); ec=edge_count(sm); ratio=ec/max(1,(edge_count(sa)+edge_count(sb))/2); w,x=wash(A,B,mid)
    print(f"{name}: silhouette={int(sm.sum())} edge={ec} double_edge_ratio={ratio:.2f} wash_px={w} xor_px={x} wash_pct={100*w/max(1,x):.1f}%")
    return {"silhouette":int(sm.sum()),"edge":ec,"double_edge_ratio":round(ratio,2),"wash_px":w,"xor_px":x,"wash_pct":round(100*w/max(1,x),1)}
out={}
print("keys: serve edge",edge_count(sa),"guard edge",edge_count(sb))
out["v1_mid_serve_guard"]=report("v1 mid (crossfade t=0.5)",v1mid)
out["v2_mid_serve_guard_breakdown"]=report("v2 mid (rig breakdown t=0.5)",v2mid)
out["rig_key_vs_original"]={
 "serve_iou":round(iou(sa,sil(v2serve)),3),
 "guard_iou":round(iou(sb,sil(v2guard)),3),
 "fight_iou_vs_approved_file":round(iou(sil(np.array(fight_orig)),sil(v2fight)),3),
}
print(out["rig_key_vs_original"])
json.dump(out,open(os.path.join(R,"movements-interp-v2-20261031/ghost-measurement-20261031.json"),"w"),indent=1)
