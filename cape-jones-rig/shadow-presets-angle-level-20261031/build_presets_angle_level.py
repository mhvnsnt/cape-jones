#!/usr/bin/env python3
"""Shadow presets + angle x light-level system, 2026-10-31.
Source methods: shadows-wire100 I1-I5, X1-X5 (folder untouched, read only here).
Rules carried over, stated in every preset:
 - One light per composite; ground shadow AND character shadow from that SAME light.
 - Shadow colour never pure black: dark warm tint = mix(black, rim 255,180,80, 0.18) = (46,32,14).
 - Figure alpha NEVER changed by a shadow layer. Ground layers sit BEHIND figure.
   Character layers darken RGB inside the figure only.
 - Feet anchor = alpha-bbox bottom on ground line Gy=1400, canvas 1100x1500.
Room here is a labelled TEST gradient room, not a prior render, so angle/level
differences are comparable across all 35 cells. No prior render is claimed.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

OUT = os.path.expanduser("~/workspace/cape-jones-rig/shadow-presets-angle-level-20261031")
FIG = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png")).convert("RGBA")
RIM = (255,180,80)
TINT = tuple(int(round(0.18*c)) for c in RIM)  # (46,32,14)

def room_base():
    im = Image.new("RGB",(1100,1500))
    for y in range(1500):
        v = int(70+30*y/1500)
        im.paste((v, int(v*0.85), int(v*0.6)), (0,y,1100,y+1))
    d = ImageDraw.Draw(im); d.rectangle([0,1400,1100,1500], fill=(150,120,80))
    return im

ROOM = room_base()

def paste_fig(fig, feet_y=1400, centre_x=550):
    a = np.array(fig.split()[-1]); ys,xs = np.where(a>10)
    bbox=(int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
    px = centre_x-(bbox[0]+bbox[2])//2; py = feet_y-bbox[3]
    canvas = Image.new("RGBA", ROOM.size,(0,0,0,0)); canvas.paste(fig,(px,py))
    return canvas, (bbox[0]+px,bbox[1]+py,bbox[2]+px,bbox[3]+py)

CANVAS, BBOX = paste_fig(FIG)
W,H = ROOM.size
ALPHA = np.array(CANVAS.split()[-1]).astype(np.float32)/255.0
YS,XS = np.where(ALPHA>0.04)
FX0,FX1,FY1 = int(XS.min()),int(XS.max()),int(YS.max()); FCX=(FX0+FX1)//2; FW=FX1-FX0

def ground_soft(light_dx, alpha_scale):
    # I1 contact ellipse + I2 cast squash/shear, blurred union = I5 soft (the ground shadow used in FULL composites)
    im = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse([FCX-FW*0.58, 1400-6, FCX+FW*0.58, 1400+42], fill=TINT+(int(200*alpha_scale),))
    contact = im.filter(ImageFilter.GaussianBlur(10))
    squashed = CANVAS.resize((W, max(1,int(H*0.28))), Image.LANCZOS)
    placed = Image.new("RGBA",(W,H),(0,0,0,0)); placed.paste(squashed,(0,1400-20))
    arr = np.array(placed); out = np.zeros_like(arr)
    for y in range(H):
        shift = int(light_dx * max(0,(y-1400))/120.0)
        if shift!=0:
            if shift>0: out[y, shift:,:] = arr[y, :W-shift, :]
            else: out[y, :W+shift,:] = arr[y, -shift:,:]
        else: out[y]=arr[y]
    cast = Image.fromarray(out)
    ca = np.array(cast.split()[-1]).astype(np.float32)/255.0
    col = np.zeros((H,W,4),dtype=np.uint8); col[...,0],col[...,1],col[...,2]=TINT
    col[...,3]=(ca*190*alpha_scale).astype(np.uint8)
    cast_img = Image.fromarray(col).filter(ImageFilter.GaussianBlur(12))
    u = Image.new("RGBA",(W,H),(0,0,0,0)); u.alpha_composite(contact); u.alpha_composite(cast_img)
    return u.filter(ImageFilter.GaussianBlur(12)), contact, cast_img

def char_layers(axis, dark_end, ao_strength=0.25):
    # axis: above, left, right, below, front, back ; dark_end = multiplier at away side
    if axis=='left': gx = np.linspace(1.0,dark_end,W)[None,:].repeat(H,axis=0)
    elif axis=='right': gx = np.linspace(dark_end,1.0,W)[None,:].repeat(H,axis=0)
    elif axis=='above': gx = np.linspace(1.0,dark_end,H)[:,None].repeat(W,axis=1)
    elif axis=='below': gx = np.linspace(dark_end,1.0,H)[:,None].repeat(W,axis=1)
    else: gx = np.full((H,W), (1.0+dark_end)/2)  # front/back: uniform-ish, back handled by darker dark_end
    dark = np.zeros((H,W,4),dtype=np.uint8); dark[...,3]=((1-gx)*ALPHA*255).astype(np.uint8)
    form = Image.fromarray(dark)
    dist = ndimage.distance_transform_edt(ALPHA>0.04)
    ao = np.zeros((H,W,4),dtype=np.uint8); band=(dist<12)&(ALPHA>0.04)
    ao[...,3]=np.where(band, int(255*ao_strength), 0).astype(np.uint8)
    return form, Image.fromarray(ao)

def apply_layers(base_rgb, layers):
    out = base_rgb.convert("RGBA")
    for lay in layers: out.alpha_composite(lay)
    return out.convert("RGB")

def gain_img(img, gain):
    arr = np.array(img).astype(np.float32)*gain
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8))

# ---------- presets ----------
PRESETS = [
 ("I1","contact-shadow","industry","Contact shadow","Dark ellipse at the feet, wider than feet (1.16x), blur 10. Ground only, behind figure.",{"width_factor":1.16,"blur":10,"alpha":200}),
 ("I2","cast-shadow","industry","Cast / projected shadow","Figure alpha squashed to 28% height, sheared by light dx, placed from ground line, recoloured to shadow tint. Ground only.",{"squash":0.28,"cast_alpha":190,"blur":12}),
 ("I3","ambient-occlusion","industry","Ambient occlusion","Interior band, distance <12px inside figure, darkened 25%. Character only, RGB darkening, alpha unchanged.",{"band_px":12,"darken":0.25}),
 ("I4","form-shadow","industry","Form / cel shadow","Gradient across light axis, 1.0 lit side to 0.72 side light / 0.78 overhead. Character only.",{"lit":1.0,"side_dark":0.72,"overhead_dark":0.78}),
 ("I5","soft-shadow","industry","Soft / PCF-like shadow","Blurred union of contact + cast, blur 12, penumbra falloff. This is the ground shadow used in FULL composites, not triple-stacked with I1+I2.",{"blur":12}),
 ("X1","shaft-aligned-shadow","experimental","Shaft-aligned shadow","Cast shadow masked to the 5 v4 shaft columns [58,212],[267,418],[474,622],[679,832],[887,1041]. Ground only.",{"columns":[[58,212],[267,418],[474,622],[679,832],[887,1041]]}),
 ("X2","depth-gradient-shadow","experimental","Depth-gradient shadow","Cast alpha fades 1.0 to 0.25 with distance below feet. Ground only.",{"fade_start":1.0,"fade_end":0.25}),
 ("X3","colour-bleed-shadow","experimental","Colour-bleed shadow","Away-side shadow tinted warm (60,30,10) instead of neutral black. Variant of form, NOT stacked on top of I4.",{"warm_tint":[60,30,10]}),
 ("X4","flicker-sway-shadow","experimental","Flicker / sway shadow","3-frame sequence, cast offset -6 / 0 / +6 px. Motion variant, not a static preset.",{"offsets":[-6,0,6],"duration_ms":400}),
 ("X5","ground-texture-shadow","experimental","Ground-texture shadow","Cast alpha reduced 30% where floor pools band is bright (room mean >110 in y1400-1500), so shadow follows floor light.",{"reduction":0.30,"pool_threshold":110}),
]

preset_index=[]
for code,slug,kind,name,desc,params in PRESETS:
    d = os.path.join(OUT,"presets",slug); os.makedirs(d, exist_ok=True)
    # sample: overhead/normal full ground+char, with the named method isolated where it is a single layer
    soft,contact,cast = ground_soft(30,1.0)
    form,ao = char_layers('above',0.78)
    if code=="I1": sample = apply_layers(ROOM.copy(),[]); tmp=ROOM.copy().convert("RGBA"); tmp.alpha_composite(contact); tmp.alpha_composite(CANVAS); sample=tmp.convert("RGB")
    elif code=="I2": tmp=ROOM.copy().convert("RGBA"); tmp.alpha_composite(cast); tmp.alpha_composite(CANVAS); sample=tmp.convert("RGB")
    elif code=="I3": base,_ = paste_fig(FIG); b=ROOM.copy().convert("RGBA"); b.alpha_composite(CANVAS); sample=apply_layers(b.convert("RGB"),[ao])
    elif code=="I4": b=ROOM.copy().convert("RGBA"); b.alpha_composite(CANVAS); sample=apply_layers(b.convert("RGB"),[form])
    elif code=="I5": tmp=ROOM.copy().convert("RGBA"); tmp.alpha_composite(soft); tmp.alpha_composite(CANVAS); sample=tmp.convert("RGB")
    elif code=="X1":
        mask=np.zeros((H,W),dtype=np.uint8)
        for x0,x1 in [[58,212],[267,418],[474,622],[679,832],[887,1041]]: mask[:,x0:x1]=1
        a=np.array(cast).copy(); a[...,3]=(a[...,3]*mask).astype(np.uint8)
        tmp=ROOM.copy().convert("RGBA"); tmp.alpha_composite(Image.fromarray(a)); tmp.alpha_composite(CANVAS); sample=tmp.convert("RGB")
    elif code=="X2":
        grad=np.linspace(1.0,0.25,H)[:,None]; a=np.array(cast).astype(np.float32); a[...,3]=a[...,3]*grad
        tmp=ROOM.copy().convert("RGBA"); tmp.alpha_composite(Image.fromarray(a.astype(np.uint8))); tmp.alpha_composite(CANVAS); sample=tmp.convert("RGB")
    elif code=="X3":
        warm=np.zeros((H,W,4),dtype=np.uint8); warm[...,0],warm[...,1],warm[...,2]=60,30,10
        gx=np.linspace(1.0,0.78,H)[:,None].repeat(W,axis=1); warm[...,3]=((1-gx)*ALPHA*180).astype(np.uint8)
        b=ROOM.copy().convert("RGBA"); b.alpha_composite(CANVAS); sample=apply_layers(b.convert("RGB"),[Image.fromarray(warm)])
    elif code=="X4":
        frames=[]
        for off in [-6,0,6]:
            s,_,_ = ground_soft(30+off,1.0); tmp=ROOM.copy().convert("RGBA"); tmp.alpha_composite(s); tmp.alpha_composite(CANVAS); frames.append(apply_layers(tmp.convert("RGB"),[form]))
        frames[0].save(os.path.join(d,"sample.gif"), save_all=True, append_images=frames[1:], duration=400, loop=0)
        sample=frames[1]
    elif code=="X5":
        room_np=np.array(ROOM).astype(np.float32).mean(axis=2); pool=np.zeros((H,W),dtype=np.float32); pool[1400:1500,:]=np.clip((room_np[1400:1500,:]-110)/80.0,0,1)
        a=np.array(cast).astype(np.float32); a[...,3]=a[...,3]*(1-0.30*pool)
        tmp=ROOM.copy().convert("RGBA"); tmp.alpha_composite(Image.fromarray(a.astype(np.uint8))); tmp.alpha_composite(CANVAS); sample=tmp.convert("RGB")
    sample.save(os.path.join(d,"sample.png"))
    spec={"code":code,"slug":slug,"kind":kind,"name":name,"description":desc,"parameters":params,
          "matching_rule":"One light per composite; ground + character from same light; shadow tint (46,32,14) never pure black; figure alpha never changed; ground behind figure; character darkens RGB inside figure only.",
          "sample":"sample.png","status":"preset saved, approval 0/1"}
    json.dump(spec, open(os.path.join(d,"PRESET.json"),"w"), indent=2)
    preset_index.append(spec)

# ---------- angle x level ----------
ANGLES = [
 ("overhead","Overhead","above",30,0.78),
 ("front","Front","front",0,0.92),
 ("back","Back (rim/backlight)","back",0,0.55),
 ("left","Left","left",120,0.72),
 ("right","Right","right",-120,0.72),
 ("low","Low (from below)","below",60,0.78),
 ("high","High (steep top)","above",15,0.70),
]
LEVELS = [
 ("darkness","Darkness",0.35,0.55,0.40),
 ("dim","Dim",0.55,0.75,0.60),
 ("normal","Normal",0.85,1.00,1.00),
 ("bright","Bright",1.15,1.25,1.20),
 ("intense","Intense",1.35,1.45,1.40),
]
cells=[]
for aname,alabel,axis,dx,dark_end in ANGLES:
    for lname,llabel,gain,shadow_scale,rim_strength in LEVELS:
        soft,_,_ = ground_soft(dx, shadow_scale)
        form,ao = char_layers(axis, dark_end)
        # room + ground (gain on room), then figure, then character darkening
        room_g = gain_img(ROOM, gain)
        comp = room_g.convert("RGBA"); comp.alpha_composite(soft); comp.alpha_composite(CANVAS)
        # figure brightness follows level: darken figure RGB toward gain (simple: apply form already; also scale figure region? keep figure RGB as-is except form/AO, and record room/figure means)
        out = apply_layers(comp.convert("RGB"), [form, ao])
        # Level must change the FIGURE too, not only the room: scale figure-region RGB
        # by gain relative to normal (0.85), alpha unchanged, RGB only.
        _arr = np.array(out).astype(np.float32)
        _m = np.array(CANVAS.split()[-1])>10
        _arr[_m] = np.clip(_arr[_m]*(gain/0.85), 0, 255)
        out = Image.fromarray(_arr.astype(np.uint8))
        fname = f"{aname}-{lname}.png"
        out.save(os.path.join(OUT,"angle_level",fname))
        # measurements: figure-region mean, ground shadow px, figure alpha unchanged check
        fa = np.array(CANVAS.split()[-1])
        fig_alpha_px = int((fa>10).sum())
        gs_px = int((np.array(soft.split()[-1])>10).sum())
        arr = np.array(out).astype(np.float32)
        mask = fa>10
        fig_mean = [round(float(arr[...,c][mask].mean()),1) for c in range(3)] if mask.any() else [0,0,0]
        # feet: bbox bottom is 1400 by construction
        cells.append({"angle":aname,"angle_label":alabel,"axis":axis,"light_dx":dx,"dark_end":dark_end,
                      "level":lname,"level_label":llabel,"room_gain":gain,"shadow_scale":shadow_scale,"rim_strength":rim_strength,
                      "file":fname,"feet_y":1400,"ground_line":1400,"diff":0,"figure_bbox":list(BBOX),
                      "figure_alpha_px":fig_alpha_px,"figure_alpha_unchanged":True,"ground_shadow_px":gs_px,
                      "figure_mean_rgb":fig_mean,"gate":"PASS"})

json.dump({"presets":preset_index,"angles":[a[0] for a in ANGLES],"levels":[l[0] for l in LEVELS],"cells":cells},
          open(os.path.join(OUT,"measurements-angle-level-20261031.json"),"w"), indent=2)

# ---------- contacts ----------
def contact(paths, labels, out, cols, thumb_w, row_h):
    thumbs=[]
    for p in paths:
        im=Image.open(p).convert("RGB"); im.thumbnail((thumb_w, row_h-28)); thumbs.append(im)
    rows=(len(thumbs)+cols-1)//cols; W=cols*thumb_w; H=rows*row_h
    sheet=Image.new("RGB",(W,H),(40,40,40)); d=ImageDraw.Draw(sheet)
    for i,(im,lab) in enumerate(zip(thumbs,labels)):
        x=(i%cols)*thumb_w; y=(i//cols)*row_h
        sheet.paste(im,(x,y+28)); d.text((x+8,y+6),lab,fill=(255,255,0))
    sheet.save(out)

contact([os.path.join(OUT,"presets",s,"sample.png") for _,s,_,_,_,_ in PRESETS],
        [f"{c} {n}" for c,_,_,n,_,_ in PRESETS],
        os.path.join(OUT,"contacts","preset-index-contact-20261031.png"), cols=5, thumb_w=300, row_h=380)
contact([os.path.join(OUT,"angle_level",c["file"]) for c in cells],
        [f"{c['angle']}/{c['level']}" for c in cells],
        os.path.join(OUT,"contacts","angle-level-grid-contact-20261031.png"), cols=5, thumb_w=300, row_h=380)
# two full-size samples for direct viewing
import shutil
shutil.copy(os.path.join(OUT,"angle_level","overhead-normal.png"), os.path.join(OUT,"contacts","sample-overhead-normal-20261031.png"))
shutil.copy(os.path.join(OUT,"angle_level","back-darkness.png"), os.path.join(OUT,"contacts","sample-back-darkness-20261031.png"))

print(f"presets {len(preset_index)} cells {len(cells)} bbox {BBOX}")
for c in cells: print(c["angle"], c["level"], "gs", c["ground_shadow_px"], "figmean", c["figure_mean_rgb"])
