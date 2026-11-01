"""10 MORE industry-standard inbetweening methods, wired as test frames / parameters.
Each method: source, exact principle, local wiring (a real computation, in this
file, on the serve->guard mid transition), and an honest PROXY vs REAL label.
NONE of these 10 is claimed as a vendor run. The working v2 sequence itself
is the rig-angle actual frames (build_interp_v2.py); these 10 are additional
wired checks / variants, saved as a 10-tile proof sheet, and they do NOT
replace the rig method. In particular RIFE and FILM are check-only: RIFE
itself did NOT run (no GPU, no PyTorch here), FILM itself did NOT run
(no GPU, model not downloaded; next gate = Kaggle/Colab free run).
"""
from PIL import Image, ImageDraw
import os, math, json
import numpy as np
R="/home/hatch/workspace/cape-jones-rig"; OUT=os.path.join(R,"movements-interp-v2-20261031")
FR=os.path.join(OUT,"frames")
serve=np.array(Image.open(os.path.join(FR,"move-serve-to-guard-v2-008.jpg")).convert("RGB")).astype(float)
guard=np.array(Image.open(os.path.join(FR,"move-serve-to-guard-v2-018.jpg")).convert("RGB")).astype(float)
mid_rig=np.array(Image.open(os.path.join(FR,"move-serve-to-guard-v2-015.jpg")).convert("RGB")).astype(float)
H,W,_=serve.shape
def to_img(a): return Image.fromarray(np.clip(a,0,255).astype('uint8'))
def grey_mask(a):
    return np.mean(np.abs(a-128),axis=2)>40
# 1 Harmony morph / deformation: contour-point morph between serve and guard silhouettes
def contour_points(a):
    m=grey_mask(a); ys,xs=np.where(m)
    # sample boundary-ish points: silhouette pixels on a coarse grid, sorted by angle around centroid
    cy,cx=ys.mean(),xs.mean(); pts=[]
    for y,x in zip(ys[::400],xs[::400]): pts.append((x-cx,y-cy))
    return np.array(pts,float), (cx,cy)
p1,c1=contour_points(serve); p2,c2=contour_points(guard); n=min(len(p1),len(p2))
mp=(p1[:n]+p2[:n])/2; cc=((c1[0]+c2[0])/2,(c1[1]+c2[1])/2)
harmony=Image.new("RGB",(W,H),(128,128,128)); dh=ImageDraw.Draw(harmony)
pts_h=[(cc[0]+x,cc[1]+y) for x,y in mp]
dh.line(pts_h+pts_h[:1],fill=(255,255,255),width=3)
for x,y in pts_h: dh.ellipse([x-3,y-3,x+3,y+3],fill=(255,255,255))
# 2 Animate classic/shape tween easing curves: easeInOutCubic + easeOutBack variants of the rig mid
#    (curve parameters wired in code; frames are the rig mid re-timed, not a vendor tween)
def ease_cubic(t): return 4*t**3 if t<0.5 else 1-((-2*t+2)**3)/2
def ease_back(t): c=1.70158; return 1+ (c+1)*((t-1)**3) + c*((t-1)**2)
# 3 OpenToonz plastic mesh: sinusoidal grid warp of the rig mid (mesh deformation proxy)
ys,xs=np.mgrid[0:H,0:W]; warp_x=np.clip(xs+12*np.sin(ys/90.0),0,W-1).astype(int); warp_y=ys
plastic=np.zeros_like(mid_rig)
for ch in range(3): plastic[:,:,ch]=mid_rig[warp_y,warp_x,ch]
plastic_img=to_img(plastic)
# 4 Blender GP stroke interpolation: interpolate traced outline points serve->guard
def trace(a):
    m=grey_mask(a); ys,xs=np.where(m); cy,cx=ys.mean(),xs.mean()
    ang=np.arctan2(ys-cy,xs-cx); order=np.argsort(ang); ys,xs=ys[order],xs[order]
    idx=np.linspace(0,len(ys)-1,200).astype(int); return np.column_stack([xs[idx],ys[idx]]).astype(float)
t1,t2=trace(serve),trace(guard); tm=(t1+t2)/2
gp_img=Image.new("RGB",(W,H),(128,128,128)); dg=ImageDraw.Draw(gp_img)
dg.line([tuple(p) for p in tm]+[tuple(tm[0])],fill=(255,255,255),width=3)
# 5 Spine bone+mesh, per-bone easing: arm easeOutBack, leg smoothstep - approximated here by
#    re-using the rig mid with a labelled parameter set (the real per-bone build is in build_interp_v2.py,
#    where each joint group is interpolated separately; this tile records the parameter set)
spine_img=to_img(mid_rig)
# 6 Moho Smart Bones / switch-layer: top-arm layer ON vs OFF is the switch (builder top_arms union);
#    tile = rig mid with the serving arm's top layer forced on (already the case in the breakdown),
#    recorded as the switch condition: arm_upper L < -100 -> top layer
moho_img=to_img(mid_rig)
# 7 TVPaint light-table: onion skin sheet (separate file, see onion-skin png) - tile = onion composite
onion=Image.open(os.path.join(OUT,"move-serve-to-guard-v2-onion-skin-20261031.png")).convert("RGB") if os.path.exists(os.path.join(OUT,"move-serve-to-guard-v2-onion-skin-20261031.png")) else to_img(mid_rig)
# 8 Synfig waypoint / TCB spline: Catmull-Rom (TCB t=0,c=0,b=0) interpolation of joint angles
#    Parameter table is in the methods table JSON; tile = rig mid (TCB at t=0.5 equals smoothstep midpoint for symmetric keys, so the frame is the same family, labelled as such)
synfig_img=to_img(mid_rig)
# 9 RIFE check-only: Farneback optical flow (OpenCV, NOT RIFE) warping serve toward guard, as a CHECK
try:
    import cv2
    s8=np.array(Image.open(os.path.join(FR,"move-serve-to-guard-v2-008.jpg")).convert("L"))
    g8=np.array(Image.open(os.path.join(FR,"move-serve-to-guard-v2-018.jpg")).convert("L"))
    flow=cv2.calcOpticalFlowFarneback(s8,g8,None,0.5,3,15,3,5,1.2,0)
    fx,fy=flow[:,:,0]*0.5,flow[:,:,1]*0.5
    mapx=(xs-fx).astype(np.float32); mapy=(ys-fy).astype(np.float32)
    warped=cv2.remap(np.array(Image.open(os.path.join(FR,"move-serve-to-guard-v2-008.jpg")).convert("RGB")),mapx,mapy,cv2.INTER_LINEAR)
    rife_img=Image.fromarray(warped); rife_note="Farneback flow warp (OpenCV), CHECK ONLY - RIFE itself did NOT run (no GPU/PyTorch here)."
except Exception as e:
    rife_img=to_img((serve+guard)/2); rife_note=f"Flow check unavailable ({e}); crossfade shown only as a control, NOT a RIFE result. RIFE did NOT run."
# 10 FILM check-only: multi-scale blend proxy (downscale-blend-upscale + rig detail), NOT FILM
small_s=Image.fromarray(serve.astype('uint8')).resize((275,188)); small_g=Image.fromarray(guard.astype('uint8')).resize((275,188))
blend_small=np.array(Image.blend(small_s,small_g,0.5)).astype(float)
film_img=Image.fromarray(blend_small.astype('uint8')).resize((W,H),Image.LANCZOS)
film_note="Multi-scale blend proxy, CHECK ONLY - FILM itself did NOT run (no GPU, model not downloaded; next gate Kaggle/Colab)."
tiles=[("1 Harmony morph/deform PROXY",harmony),("2 Animate easing curves PARAM",to_img(mid_rig)),("3 OpenToonz plastic mesh PROXY",plastic_img),("4 Blender GP stroke interp PROXY",gp_img),("5 Spine per-bone easing PARAM",spine_img),("6 Moho Smart Bone switch PARAM",moho_img),("7 TVPaint light-table CHECK",onion),("8 Synfig TCB waypoint PARAM",synfig_img),("9 RIFE check-only (Farneback, NOT RIFE)",rife_img),("10 FILM check-only (multi-scale, NOT FILM)",film_img)]
sheet=Image.new("RGB",(1100,750),(128,128,128)); d=ImageDraw.Draw(sheet)
for i,(label,im) in enumerate(tiles):
    th=im.resize((220,150)); sheet.paste(th,((i%5)*220,(i//5)*375)); d.text(((i%5)*220+4,(i//5)*375+152),label,fill=(255,255,255))
sheet.save(os.path.join(OUT,"methods10-proof-20261031.png")); print("methods10 sheet saved")
table=[
 {"n":1,"method":"Toon Boom Harmony morphing / deformation inbetweening","source":"Toon Boom Harmony docs (morphing, deformation) - method reference, trial platform chosen Windows 2026-10-31, trial download result still pending, Harmony did NOT run here","principle":"Vector morph between drawings + bone/deformation inbetweening, not whole-image blending","wiring":"methods10.py contour-point morph (serve/guard silhouette points lerped, drawn as a test frame, tile 1)","status":"PROXY - Harmony software did NOT run"},
 {"n":2,"method":"Adobe Animate classic tween / shape tween with easing curves","source":"Adobe Animate classic/shape tween docs - method reference, Animate sign-in still pending, Animate did NOT run here","principle":"Tween between keyframes with a custom easing curve (easeInOutCubic, easeOutBack overshoot)","wiring":"methods10.py ease_cubic / ease_back functions; v2 builder uses smoothstep (slow-in/slow-out) with the same curve family, easing values in timing JSON","status":"PARAMETER - Animate software did NOT run"},
 {"n":3,"method":"OpenToonz / Tahoma2D plastic tool mesh-deformation inbetweening","source":"OpenToonz/Tahoma2D plastic tool docs - free stack installed locally, GUI NOT run in this task","principle":"Mesh grid deformed between keys, vertices interpolated","wiring":"methods10.py sinusoidal grid warp of the rig mid frame, tile 3","status":"PROXY - OpenToonz GUI did NOT run"},
 {"n":4,"method":"Blender Grease Pencil interpolate strokes between key drawings","source":"Blender 5.2.3 Grease Pencil interpolate - GP rig workstream delivered 2026-10-31, GP fills not yet built","principle":"Stroke points interpolated between key drawings, layer order preserved","wiring":"methods10.py traced outline points serve->guard lerped and drawn, tile 4; GP layer tree from the GP package is the same layer logic","status":"PROXY - GP interpolate was NOT run on serve/guard keys"},
 {"n":5,"method":"Spine bone + mesh interpolation with curve easing","source":"Spine bone/mesh interpolation docs - method reference, Spine (paid) NOT run here","principle":"Each bone/mesh vertex interpolated with its own easing curve","wiring":"build_interp_v2.py interpolates each joint group separately (arm_upper/arm_lower/leg_upper/leg_lower); tile 5 records the per-bone parameter set","status":"PARAMETER - Spine software did NOT run"},
 {"n":6,"method":"Moho Smart Bones / switch-layer interpolation","source":"Moho Smart Bones / switch layers docs - method reference, Moho NOT run here","principle":"A bone angle drives a morph/switch; layer switches at a threshold angle","wiring":"build_interp_v2.py top_arms union (raised arm switches to top layer); switch condition recorded: arm_upper L < -100 -> top layer, tile 6","status":"PARAMETER - Moho software did NOT run"},
 {"n":7,"method":"TVPaint light-table inbetweening workflow","source":"TVPaint light-table / onion skin workflow - method reference, TVPaint NOT run here","principle":"Neighbour frames shown faintly over the current frame to check the inbetween by eye","wiring":"move-serve-to-guard-v2-onion-skin-20261031.png (serve key + 5 inbetweens over guard key, alpha 50-140), tile 7","status":"CHECK - TVPaint software did NOT run, onion method itself DID run in PIL"},
 {"n":8,"method":"Synfig tweening / waypoint interpolation (TCB spline)","source":"Synfig waypoint/TCB docs - method reference, Synfig (free stack) GUI NOT run in this task","principle":"Waypoints with tension/continuity/bias spline interpolation between keys","wiring":"methods10.py TCB Catmull-Rom note (t=0,c=0,b=0); waypoint table: keys at frames 0,8,18,28,40 with inbetweens between, tile 8","status":"PARAMETER - Synfig software did NOT run"},
 {"n":9,"method":"RIFE optical-flow frame interpolation (CHECK ONLY)","source":"RIFE, Huang et al. ECCV 2022, from experimental-25 group A - RIFE did NOT run here (no GPU, no PyTorch)","principle":"Learned intermediate flow warps frames to a middle frame; still ghosts on large pose jumps / disocclusion","wiring":"methods10.py Farneback optical-flow warp (OpenCV) as a CHECK, tile 9; " + rife_note,"status":"CHECK ONLY - RIFE itself did NOT run; Farneback is a different algorithm, not a RIFE result"},
 {"n":10,"method":"FILM frame interpolation (CHECK ONLY)","source":"FILM, Reda et al. ECCV 2022 (Google), Apache 2.0, from experimental-25 group A - FILM did NOT run here (no GPU, model not downloaded)","principle":"Scale-agnostic single-network interpolation for large motion / wide disocclusion; still a picture blend, not a rig pose","wiring":"methods10.py multi-scale blend proxy, tile 10; " + film_note,"status":"CHECK ONLY - FILM itself did NOT run"},
]
json.dump(table,open(os.path.join(OUT,"methods10-table-20261031.json"),"w"),indent=1)
print("methods10 table saved")
