"""Poses as movements, on video. METHOD, stated plainly:
Keys are EXISTING rig poses (v7c / wire-100 cowl-snap / Ginyu / dialect files).
Inbetweens are IMAGE interpolation (eased alpha crossfade between consecutive
key images, plus whole-image translation for jump height / shimmy sway) at 24fps.
This is NOT rig-angle inbetweening: the keys pass knee-feet + face/cowl snap
because they are the original files (layer order preserved inside each image);
a mid-blend frame is a blend of two passing keys, and can ghost slightly at
50% blend — that is the honest limit of this method, and it is labelled here.
No new art drawn, no file Mars has seen overwritten, all outputs new dated files.
Canvas: 1100x750 video frames (1100x1500 poses downscaled 0.5, grey-128 bg).
"""
from PIL import Image
import os, json, math
R = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(R, "poses-as-movements-20261031")
FR = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
W,H = 1100,750
def load(path, dy=0, dx=0, rot=0):
    im = Image.open(path).convert("RGBA")
    # downscale 1100x1500 -> 550x750, then centre on 1100x750 grey canvas
    im = im.resize((550,750), Image.LANCZOS)
    if rot: im = im.rotate(rot, expand=False, center=(275,375))
    canvas = Image.new("RGBA",(W,H),(128,128,128,255))
    canvas.alpha_composite(im, ((W-550)//2+dx, dy))
    return canvas.convert("RGB")
def smooth(t): return t*t*(3-2*t)
def easeout(t): return 1-(1-t)**2
def seq(frames_list):
    """frames_list: list of (image, hold_count) or ('blend', imgA, imgB, n, ease) expanded by caller"""
    return frames_list
def build(name, keys):
    """keys: list of dicts {img, hold, blend_n, ease} ; blend_n = inbetweens after this key toward next"""
    frames=[]
    for i,k in enumerate(keys):
        frames += [k["img"]]*k.get("hold",4)
        if i < len(keys)-1:
            nxt = keys[i+1]["img"]; n = k.get("blend_n",3); ease = k.get("ease", smooth)
            for j in range(1, n+1):
                t = ease(j/(n+1))
                frames.append(Image.blend(k["img"], nxt, t))
    # save video frames
    for i,f in enumerate(frames):
        f.save(os.path.join(FR, f"{name}-{i:03d}.jpg"), quality=90)
    # GIF 550x375
    small=[f.resize((550,375)) for f in frames]
    small[0].save(os.path.join(OUT, f"{name}-20261031.gif"), save_all=True, append_images=small[1:], duration=42, loop=0)
    # contact: sample up to 8 frames evenly
    import math as m
    idx = sorted(set([int(i*(len(frames)-1)/7) for i in range(8)])) if len(frames)>=8 else list(range(len(frames)))
    sheet = Image.new("RGB",(1100, 750), (128,128,128))
    # 4x2 grid of 275x375? use 550x375 scaled to 275x188 -> grid 4 cols x 2 rows = 1100x376, pad
    sheet = Image.new("RGB",(1100,376),(128,128,128))
    for k,ix in enumerate(idx):
        th = frames[ix].resize((275,188))
        sheet.paste(th, ((k%4)*275, (k//4)*188))
    sheet.save(os.path.join(OUT, f"{name}-contact-20261031.png"))
    return len(frames)

P = lambda *a: os.path.join(R, *a)
APOSE = P("reposes-v7c-clean/joint-apose-v7c-clean.png")
CROUCH = P("clips-v7c/jump/jump-01-crouch-v7c.png")
TAKEOFF = P("clips-v7c/jump/jump-07-takeoff-v7c.png")
TUCK = P("clips-v7c/jump/jump-13-tuck-v7c.png")
LAND = P("clips-v7c/jump/jump-25-land-v7c.png")
JUMPAPEX = P("face-cowl-snap-wire100-20261031/v7c-jump-arms-up-COWL-SNAP-20261031.png")
SHIMMY = P("face-cowl-snap-wire100-20261031/ginyu-03-dance-shimmy-hips-out-COWL-SNAP-20261031.png")
FIGHT = P("reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png")
PUNCH = P("clips-v7c/punch/punch-09-impact-hold-v7c.png")
FLEX = P("reposes-v7c-clean/true-final-flex-relaxed-clean-20261031.png")
results={}
# A: jump — crouch, takeoff, apex (raised 100px), tuck, land, neutral
results["jump-cowl-snap-movement"] = build("jump-cowl-snap-movement", [
 {"img":load(APOSE), "hold":4, "blend_n":3},
 {"img":load(CROUCH), "hold":4, "blend_n":3},
 {"img":load(TAKEOFF, dy=-40), "hold":3, "blend_n":3},
 {"img":load(JUMPAPEX, dy=-100), "hold":6, "blend_n":3},
 {"img":load(TUCK, dy=-60), "hold":3, "blend_n":3},
 {"img":load(LAND), "hold":4, "blend_n":3},
 {"img":load(APOSE), "hold":4},
])
# B: shimmy loop, 2 cycles — sway dx/rot, cowl-snap pose only (layer order preserved)
shimmy_frames=[]
sway=[(0,0),(-40,-3),(0,0),(40,3),(0,0),(-40,-3),(0,0),(40,3),(0,0)]
for dx,rot in sway:
    shimmy_frames.append(load(SHIMMY, dx=dx, rot=rot))
# build manually: hold 2 + blend 2 between each sway step, twice through the list
frames=[]
for cyc in range(2):
    for i,im in enumerate(shimmy_frames):
        frames += [im]*2
        if not (cyc==1 and i==len(shimmy_frames)-1):
            nxt = shimmy_frames[(i+1)%len(shimmy_frames)]
            for j in range(1,3):
                frames.append(Image.blend(im, nxt, smooth(j/3)))
for i,f in enumerate(frames): f.save(os.path.join(FR, f"shimmy-cowl-snap-movement-{i:03d}.jpg"), quality=90)
small=[f.resize((550,375)) for f in frames]
small[0].save(os.path.join(OUT,"shimmy-cowl-snap-movement-20261031.gif"), save_all=True, append_images=small[1:], duration=42, loop=0)
sheet=Image.new("RGB",(1100,376),(128,128,128))
idx=sorted(set([int(i*(len(frames)-1)/7) for i in range(8)]))
for k,ix in enumerate(idx): sheet.paste(frames[ix].resize((275,188)), ((k%4)*275,(k//4)*188))
sheet.save(os.path.join(OUT,"shimmy-cowl-snap-movement-contact-20261031.png"))
results["shimmy-cowl-snap-movement"]=len(frames)
# C: Ginyu Force movement — roll-call order, announce hold, snap, hold
force_keys=[
 ("rec-01", P("ginyu-force-poses-20261031/rec-01-power-showboat-wide-20261031.png")),
 ("bur-01", P("ginyu-force-poses-20261031/bur-01-speed-lean-dash-20261031.png")),
 ("jei-01", P("ginyu-force-poses-20261031/jei-01-crusher-serve-windup-20261031.png")),
 ("gul-01", P("ginyu-force-poses-20261031/gul-01-low-crouch-compact-20261031.png")),
 ("cap-01", P("ginyu-force-poses-20261031/cap-01-grand-entrance-rollcall-20261031.png")),
 ("cap-02-spread", P("ginyu-force-poses-20261031/cap-02-body-change-spread-20261031.png")),
]
results["ginyu-force-movement"] = build("ginyu-force-movement", [
 {"img":load(APOSE), "hold":4, "blend_n":2, "ease":easeout},
]+[{"img":load(p), "hold":6, "blend_n":4, "ease":easeout} for _,p in force_keys[:-1]]+
 [{"img":load(force_keys[-1][1]), "hold":8}])
# D: pose dialects as movements — neutral -> pose -> neutral, 8 poses
dialects=[
 ("jojo-01", P("pose-dialects-20261031/jojo-01-contrapposto-s-curve-20261031.png")),
 ("jojo-02", P("pose-dialects-20261031/jojo-02-fashion-twist-point-20261031.png")),
 ("jojo-03-face-snap", P("pose-dialects-fix-face-cowl-20261031/jojo-03-menacing-lean-hand-face-FACE-SNAP-20261031.png")),
 ("stand-01", P("pose-dialects-20261031/stand-01-mirrored-pair-20261031.png")),
 ("stand-02", P("pose-dialects-20261031/stand-02-towering-behind-20261031.png")),
 ("ginyu-01-cowl-snap", P("pose-dialects-fix-face-cowl-20261031/ginyu-01-rollcall-chest-out-COWL-SNAP-20261031.png")),
 ("ginyu-02", P("pose-dialects-20261031/ginyu-02-squat-elbows-out-goofy-20261031.png")),
 ("ginyu-03-cowl-snap", P("face-cowl-snap-wire100-20261031/ginyu-03-dance-shimmy-hips-out-COWL-SNAP-20261031.png")),
]
keys=[{"img":load(APOSE), "hold":3, "blend_n":3}]
for _,p in dialects:
    keys.append({"img":load(p), "hold":4, "blend_n":3})
    keys.append({"img":load(APOSE), "hold":3, "blend_n":3})
keys[-1]={"img":load(APOSE), "hold":4}
results["pose-dialects-movements"] = build("pose-dialects-movements", keys)
# E: 4 NEW movement-poses (new sequences, key still = mid-transition frame)
new_moves={
 "move-punch-to-flex": [PUNCH, FIGHT, FLEX],
 "move-jump-to-shimmy": [LAND, SHIMMY, SHIMMY],
 "move-serve-to-guard": [P("ginyu-force-poses-20261031/jei-01-crusher-serve-windup-20261031.png"), P("ginyu-force-poses-20261031/gul-03-guard-crouch-startled-20261031.png"), FIGHT],
 "move-rollcall-snap-to-spread": [P("ginyu-force-poses-20261031/cap-01-grand-entrance-rollcall-20261031.png"), P("ginyu-force-poses-20261031/cap-03-crossed-command-20261031.png"), P("ginyu-force-poses-20261031/cap-02-body-change-spread-20261031.png")],
}
for name, paths in new_moves.items():
    ks=[{"img":load(APOSE), "hold":3, "blend_n":3}]
    for p in paths: ks.append({"img":load(p), "hold":5, "blend_n":3})
    ks.append({"img":load(APOSE), "hold":3})
    results[name]=build(name, ks)
    # key still = middle pose of the sequence
    load(paths[1]).save(os.path.join(OUT, f"{name}-key-still-20261031.png"))
print(json.dumps(results, indent=2))
with open(os.path.join(OUT,"MOVEMENTS-META-20261031.json"),"w") as f: json.dump({"fps":24,"method":"IMAGE interpolation (eased crossfade + whole-image translation), NOT rig-angle inbetweening; keys are original rig files, layer order preserved inside each key image; mid-blend frames can ghost slightly","videos":results},f,indent=2)
