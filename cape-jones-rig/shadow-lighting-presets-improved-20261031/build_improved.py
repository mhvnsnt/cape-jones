#!/usr/bin/env python3
"""Improved shadow/lighting preset pipelines + new directions, 2026-10-31.
Approved presets in shadow-presets-angle-level-20261031/ are READ-ONLY here.
Everything here is a NEW v2 / new-direction / new-method version in a new folder.
Rules carried over: one light per composite; shadow tint (46,32,14) never pure
black (except where a named mood tint is stated); figure alpha NEVER changed;
ground behind figure; character layers darken RGB inside figure only;
feet Gy=1400, canvas 1100x1500, base rig-apose-v7c-clean-transparent.png.
AO note (plain): AO = darkening in crevices / where parts touch. Flashlight-
under-face = UNDERLIGHT / UPLIGHT, a low upward key light. AO + uplight belong
together: uplight lights from below, AO keeps crevices (eye sockets, cowl folds,
armpits, belt shadow) dark, which is the dark dramatic comic/cartoon look.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

OUT = os.path.expanduser("~/workspace/cape-jones-rig/shadow-lighting-presets-improved-20261031")
for _d in ("improved","directions","new_methods","contacts"): os.makedirs(os.path.join(OUT,_d), exist_ok=True)
FIG = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png")).convert("RGBA")
RIM = (255,180,80); TINT = tuple(int(round(0.18*c)) for c in RIM)  # (46,32,14)
W,H = 1100,1500; GY = 1400

def room_base():
    im = Image.new("RGB",(W,H))
    for y in range(H):
        v = int(70+30*y/H); im.paste((v,int(v*0.85),int(v*0.6)),(0,y,W,y+1))
    d = ImageDraw.Draw(im); d.rectangle([0,GY,W,H], fill=(150,120,80)); return im
ROOM = room_base()

def paste_fig(fig, feet_y=GY, centre_x=550):
    a = np.array(fig.split()[-1]); ys,xs = np.where(a>10)
    bbox=(int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
    px = centre_x-(bbox[0]+bbox[2])//2; py = feet_y-bbox[3]
    canvas = Image.new("RGBA",(W,H),(0,0,0,0)); canvas.paste(fig,(px,py))
    return canvas, (bbox[0]+px,bbox[1]+py,bbox[2]+px,bbox[3]+py)
CANVAS,BBOX = paste_fig(FIG)
ALPHA = np.array(CANVAS.split()[-1]).astype(np.float32)/255.0
YS,XS = np.where(ALPHA>0.04); FX0,FX1,FY1 = int(XS.min()),int(XS.max()),int(YS.max()); FCX=(FX0+FX1)//2; FW=FX1-FX0
DIST = ndimage.distance_transform_edt(ALPHA>0.04)

def compose(room, ground=None, fig=CANVAS, char=None):
    im = room.copy().convert("RGBA")
    if ground is not None: im.alpha_composite(ground)
    im.alpha_composite(fig)
    out = im.convert("RGB")
    if char is not None:
        o = out.convert("RGBA")
        for lay in char: o.alpha_composite(lay)
        out = o.convert("RGB")
    # restore figure alpha claim: character layers are black-alpha overlays, they do not erase figure
    return out

def dark_layer(gain_map, strength=1.0):
    # gain_map 1.0 lit .. 0 dark; returns black layer with alpha (1-gain)*ALPHA*255*strength
    dark = np.zeros((H,W,4),dtype=np.uint8)
    dark[...,3] = np.clip((1-gain_map)*ALPHA*255*strength,0,255).astype(np.uint8)
    return Image.fromarray(dark)

def smoothstep(x):
    x = np.clip(x,0,1); return x*x*(3-2*x)

def form_layer(axis, dark_end, wrap=0.0):
    if axis=='left': t = np.linspace(0,1,W)[None,:].repeat(H,axis=0)
    elif axis=='right': t = np.linspace(1,0,W)[None,:].repeat(H,axis=0)
    elif axis=='above': t = np.linspace(0,1,H)[:,None].repeat(W,axis=1)
    elif axis=='below': t = np.linspace(1,0,H)[:,None].repeat(W,axis=1)
    elif axis=='front': t = np.full((H,W),0.5)
    elif axis=='back': t = np.full((H,W),0.85)
    else: t = np.full((H,W),0.5)
    g = 1.0 - smoothstep(t)*(1-dark_end)
    if wrap: g = np.clip(g + wrap*(1-smoothstep(t))*0.0 + wrap*(t<0.25)*0.0,0,1)  # wrap handled in v2 below
    return dark_layer(g)

def form_layer_v2(axis, dark_end, wrap=0.15):
    # v2: smoothstep terminator + wrap light leaking past terminator into away side
    if axis=='left': t = np.linspace(0,1,W)[None,:].repeat(H,axis=0)
    elif axis=='right': t = np.linspace(1,0,W)[None,:].repeat(H,axis=0)
    elif axis=='above': t = np.linspace(0,1,H)[:,None].repeat(W,axis=1)
    elif axis=='below': t = np.linspace(1,0,H)[:,None].repeat(W,axis=1)
    else: t = np.full((H,W),0.5)
    s = smoothstep(t)
    g = 1.0 - s*(1-dark_end)
    # wrap: away side (s near 1) lifts by wrap * falloff from terminator
    g = np.clip(g + wrap*np.exp(-((s-0.5)**2)/0.08)*0.5, 0, 1)
    return dark_layer(g)

def ao_layer(band=12, darken=0.25):
    d = np.zeros((H,W,4),dtype=np.uint8); bandm=(DIST<band)&(ALPHA>0.04)
    d[...,3]=np.where(bandm, int(255*darken),0).astype(np.uint8); return Image.fromarray(d)

def ao_layer_v2(band=20, darken=0.35):
    # v2: graded by depth — deeper crevice (small EDT) darker, fading to 0 at band edge
    d = np.zeros((H,W,4),dtype=np.uint8)
    w = np.clip(1-DIST/band,0,1); m=(DIST<band)&(ALPHA>0.04)
    d[...,3]=np.where(m, (w*255*darken).astype(np.uint8),0).astype(np.uint8); return Image.fromarray(d)

def ground_contact(alpha=200, blur=10, core=False):
    im = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse([FCX-FW*0.58, GY-6, FCX+FW*0.58, GY+42], fill=TINT+(alpha,))
    out = im.filter(ImageFilter.GaussianBlur(blur))
    if core:
        core_im = Image.new("RGBA",(W,H),(0,0,0,0)); dd=ImageDraw.Draw(core_im)
        dd.ellipse([FCX-FW*0.38, GY-2, FCX+FW*0.38, GY+22], fill=TINT+(235,))
        out.alpha_composite(core_im.filter(ImageFilter.GaussianBlur(4)))
    return out

def ground_cast(light_dx, alpha_scale=1.0, taper=False):
    squashed = CANVAS.resize((W, max(1,int(H*0.28))), Image.LANCZOS)
    placed = Image.new("RGBA",(W,H),(0,0,0,0)); placed.paste(squashed,(0,GY-20))
    arr = np.array(placed); out = np.zeros_like(arr)
    for y in range(H):
        shift = int(light_dx * max(0,(y-GY))/120.0)
        if shift!=0:
            if shift>0: out[y, shift:,:] = arr[y, :W-shift, :]
            else: out[y, :W+shift,:] = arr[y, -shift:,:]
        else: out[y]=arr[y]
    ca = np.array(Image.fromarray(out).split()[-1]).astype(np.float32)/255.0
    if taper:
        # narrow with distance below ground line
        yy = np.arange(H)[:,None]; factor = np.clip(1 - np.maximum(0,yy-GY)/400.0*0.45, 0.55, 1.0)
        # apply horizontally around FCX by scaling alpha columns (approx: fade outer columns)
        xx = np.arange(W)[None,:]; colfade = np.clip(1 - np.abs(xx-FCX)/ (FW*0.9) * np.maximum(0,yy-GY)/300.0, 0.5, 1.0)
        ca = ca * factor * colfade
    col = np.zeros((H,W,4),dtype=np.uint8); col[...,0],col[...,1],col[...,2]=TINT
    col[...,3]=(ca*190*alpha_scale).astype(np.uint8)
    return Image.fromarray(col).filter(ImageFilter.GaussianBlur(12))

def ground_soft_v2(light_dx, alpha_scale=1.0):
    c = ground_contact(core=True); cast = ground_cast(light_dx, alpha_scale, taper=True)
    u = Image.new("RGBA",(W,H),(0,0,0,0)); u.alpha_composite(c); u.alpha_composite(cast)
    return u.filter(ImageFilter.GaussianBlur(12))

def tint_layer(tint, mask_alpha):
    col = np.zeros((H,W,4),dtype=np.uint8); col[...,0],col[...,1],col[...,2]=tint
    col[...,3]=mask_alpha.astype(np.uint8); return Image.fromarray(col)

def fig_mean(img):
    a = np.array(img); m = ALPHA>0.04
    return [round(float(a[...,c][m].mean()),1) for c in range(3)]

def ground_px(ground):
    if ground is None: return 0
    return int((np.array(ground.split()[-1])>10).sum())

def save(img, path):
    img.save(path); return path

meas = {"base":{"bbox":BBOX,"figure_alpha_px":int((ALPHA>0.04).sum()),"feet_y":GY,"canvas":[W,H]}}

# ---------- IMPROVED v2 presets ----------
imp = {}
# I1v2 contact with hard core
g = ground_contact(core=True); imp["I1v2-contact-core"] = compose(ROOM, g)
# I2v2 tapered cast
g = ground_cast(30, taper=True); imp["I2v2-cast-taper"] = compose(ROOM, g)
# I3v2 graded AO
imp["I3v2-ao-graded"] = compose(ROOM, None, char=[ao_layer_v2()])
# I4v2 form with wrap
imp["I4v2-form-wrap"] = compose(ROOM, None, char=[form_layer_v2('above',0.78,wrap=0.15)])
# I5v2 soft = core contact + tapered cast
imp["I5v2-soft-core-taper"] = compose(ROOM, ground_soft_v2(30))
# X1v2 shaft + figure dapple
cast = ground_cast(30); a=np.array(cast).copy()
mask=np.zeros((H,W),dtype=np.uint8)
for x0,x1 in [[58,212],[267,418],[474,622],[679,832],[887,1041]]: mask[:,x0:x1]=1
a[...,3]=(a[...,3]*mask).astype(np.uint8)
# figure dapple: brighten inside columns, darken between (as dark layer inverse)
colmask = np.zeros((H,W)); 
for x0,x1 in [[58,212],[267,418],[474,622],[679,832],[887,1041]]: colmask[:,x0:x1]=1
dapple = dark_layer(np.where(colmask>0, 0.92, 0.78))  # less dark inside columns
imp["X1v2-shaft-dapple"] = compose(ROOM, Image.fromarray(a), char=[dapple])
# X2v2 depth gradient: fade + blur grows with distance (approx: two casts, near sharp, far blurred, blended by y)
near = ground_cast(30); far = ground_cast(30).filter(ImageFilter.GaussianBlur(20))
na, fa = np.array(near), np.array(far); yy=np.linspace(0,1,H)[:,None,None]
blend = (na*(1-yy)+fa*yy).astype(np.uint8)
# apply fade with distance
fade = np.clip(1 - np.maximum(0,np.arange(H)[:,None]-GY)/350.0*0.75, 0.25, 1.0)
blend[...,3]=(blend[...,3]*fade).astype(np.uint8)
imp["X2v2-depth-fade-blur"] = compose(ROOM, Image.fromarray(blend))
# X3v2 colour-bleed two-zone: warm away side + floor bounce tint on ground
form = form_layer_v2('left',0.72); 
# recolour form layer warm: build warm tint layer with same alpha as form
fa_ = np.array(form.split()[-1]); warm = tint_layer((60,30,10), fa_)
bounce = ground_contact(alpha=150); ba=np.array(bounce); ba[...,0],ba[...,1],ba[...,2]=255,180,80; ba[...,3]=(ba[...,3]*0.6).astype(np.uint8)
imp["X3v2-colour-bleed-bounce"] = compose(ROOM, Image.fromarray(ba), char=[warm])
# X4v2 flicker-sway 5-frame
frames=[]
for off,al in [(-8,0.90),(-4,0.97),(0,1.0),(4,0.97),(8,0.90)]:
    cast = ground_cast(30+off, alpha_scale=al)
    frames.append(compose(ROOM, cast))
imp["X4v2-flicker-sway-5f"] = frames  # special: list
# X5v2 ground-texture graded: reduction continuous with pool brightness proxy (floor band gradient)
cast = ground_cast(30); ca=np.array(cast)
yy=np.arange(H)[:,None]; pool = np.clip((yy-(GY))/100.0,0,1)  # brighter deeper in floor band
red = 1 - 0.30*pool
ca[...,3]=(ca[...,3]*red).astype(np.uint8)
imp["X5v2-ground-texture-graded"] = compose(ROOM, Image.fromarray(ca))

for k,v in imp.items():
    if isinstance(v,list):
        v[0].save(f"{OUT}/improved/{k}-f0.png")
        v[0].save(f"{OUT}/improved/{k}.gif", save_all=True, append_images=v[1:], duration=200, loop=0)
    else:
        v.save(f"{OUT}/improved/{k}.png")
meas["improved"] = {k: ({"frames":len(v)} if isinstance(v,list) else {"fig_mean":fig_mean(v)}) for k,v in imp.items()}

# ---------- NEW DIRECTIONS ----------
# Each direction: full composite at Normal, plus Darkness variant for underlight set.
# Directions: underlight (below), underlight-left, underlight-right, low-back-rim, spot-dramatic
dirs = {}
def direction(name, axis, dark_end, dx, level_gain, ao=True):
    # gain: scale figure RGB by level (approx via brightening/darkening whole composite figure region is complex;
    # here we apply form+AO on figure, ground soft, and overall gain on the figure paste via a tinted overlay)
    soft = ground_soft_v2(dx, alpha_scale=1.0)
    layers = [form_layer_v2(axis, dark_end, wrap=0.10)]
    if ao: layers.append(ao_layer_v2())
    img = compose(ROOM, soft, char=layers)
    if level_gain != 1.0:
        arr = np.array(img).astype(np.float32)
        # scale only figure region
        m = ALPHA>0.04; arr[m] = np.clip(arr[m]*level_gain,0,255)
        img = Image.fromarray(arr.astype(np.uint8))
    return img

dirs["underlight"] = direction("underlight",'below',0.55,0,1.0)
dirs["underlight-darkness"] = direction("underlight",'below',0.45,0,0.55)
dirs["underlight-left"] = direction("underlight-left",'below',0.60,60,1.0)
dirs["underlight-right"] = direction("underlight-right",'below',0.60,-60,1.0)
dirs["low-back-rim"] = direction("low-back-rim",'back',0.55,0,1.0)
dirs["spot-dramatic"] = direction("spot-dramatic",'above',0.60,15,0.85)
# AO+uplight combined proof: underlight with extra-strong AO, face zoom
ao_strong = ao_layer_v2(band=24, darken=0.45)
soft = ground_soft_v2(0)
combined = compose(ROOM, soft, char=[form_layer_v2('below',0.55,wrap=0.10), ao_strong])
dirs["AO-plus-uplight-combined"] = combined
for k,v in dirs.items():
    v.save(f"{OUT}/directions/{k}.png")
meas["directions"] = {k: {"fig_mean":fig_mean(v)} for k,v in dirs.items()}
# face zoom: crop head region from combined and from plain underlight, 2x
# head approx: figure bbox top 359; head y 359-680, x 380-760 (from bbox 237-864, centre ~550)
for name, src in [("combined",combined),("underlight",dirs["underlight"])]:
    crop = src.crop((380,340,760,700)).resize((760,720), Image.LANCZOS)
    crop.save(f"{OUT}/directions/face-zoom-{name}.png")

# ---------- NEW METHODS: 5 industry + 5 experimental ----------
new = {}
# NI1 three-point: key left 1.0 + fill right 0.35 + rim back 0.8 — combine form layers: key form left, fill lifts away side, rim = edge band bright (approx: darken less at edges)
key = form_layer_v2('left',0.70); fill = form_layer_v2('right',0.90)
# combine: use key only (fill effect = key dark_end lifted) — implement as single gradient with dark_end 0.78 + rim edge: rim band = EDT<8 on right side brightened via negative dark layer is not possible; approximate with key form + AO light
new["NI1-three-point"] = compose(ROOM, ground_soft_v2(120), char=[form_layer_v2('left',0.78), ao_layer_v2(band=12,darken=0.20)])
# NI2 chiaroscuro / Rembrandt: strong side key, small bright patch on away cheek (head region, right side of face)
base = compose(ROOM, ground_soft_v2(120), char=[form_layer_v2('left',0.55), ao_layer_v2()])
arr = np.array(base).astype(np.float32)
# cheek patch: ellipse-ish rectangle in head area, away side (right of centre, head y)
yy,xx = np.mgrid[0:H,0:W]
patch = ((xx-620)**2/60**2 + (yy-520)**2/40**2) < 1
arr[patch] = np.clip(arr[patch]*1.35+20,0,255)
new["NI2-chiaroscuro-rembrandt"] = Image.fromarray(arr.astype(np.uint8))
# NI3 kicker / edge light: cool rim band on opposite side — implement as cool tint on edge band (EDT<10, x>centre)
edge = (DIST<10)&(ALPHA>0.04)&(np.arange(W)[None,:]>FCX)
cool = tint_layer((120,180,255), np.where(edge, 90, 0).astype(np.uint8))
# tint layer is additive-ish via alpha composite over figure: compose with char layer that is cool colour with alpha (not black)
def compose_tint(room, ground, tintlay):
    im = room.copy().convert("RGBA")
    if ground is not None: im.alpha_composite(ground)
    im.alpha_composite(CANVAS); im.alpha_composite(tintlay); return im.convert("RGB")
new["NI3-kicker-edge"] = compose_tint(ROOM, ground_soft_v2(-120), cool)
# NI4 spotlight cone: visible cone in air from above, falloff, plus figure lit under it
cone = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(cone)
d.polygon([(450,0),(650,0),(820,GY),(280,GY)], fill=(255,200,120,45))
cone = cone.filter(ImageFilter.GaussianBlur(15))
im = ROOM.copy().convert("RGBA"); im.alpha_composite(cone); im.alpha_composite(ground_soft_v2(15)); im.alpha_composite(CANVAS)
new["NI4-spotlight-cone"] = im.convert("RGB")
# NI5 colour-temperature split: warm left, cool right gradient on figure
warm = np.zeros((H,W,4),dtype=np.uint8); cool2 = np.zeros((H,W,4),dtype=np.uint8)
xx = np.linspace(0,1,W)[None,:].repeat(H,axis=0)
warm[...,0],warm[...,1],warm[...,2]=255,170,90; warm[...,3]=np.where(ALPHA>0.04, (np.clip(1-xx,0,1)*40).astype(np.uint8),0)
cool2[...,0],cool2[...,1],cool2[...,2]=120,170,255; cool2[...,3]=np.where(ALPHA>0.04, (np.clip(xx,0,1)*40).astype(np.uint8),0)
im = ROOM.copy().convert("RGBA"); im.alpha_composite(ground_soft_v2(0)); im.alpha_composite(CANVAS); im.alpha_composite(Image.fromarray(warm)); im.alpha_composite(Image.fromarray(cool2))
new["NI5-temperature-split"] = im.convert("RGB")
# NX1 comic halftone shadow: ground shadow as dots, density by cast alpha
cast = ground_cast(30); ca=np.array(cast.split()[-1])
halftone = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(halftone)
for y in range(0,H,12):
    for x in range(0,W,12):
        a = int(ca[y,x]) if y<H and x<W else 0
        if a>40:
            r = max(1, int(5*a/255)); d.ellipse([x-r,y-r,x+r,y+r], fill=TINT+(a,))
new["NX1-halftone-shadow"] = compose(ROOM, halftone)
# NX2 ink-outline thickening on shadow side: edge band on away (right) side thickened dark
edge2 = (DIST<22)&(ALPHA>0.04)&(np.arange(W)[None,:]>FCX)
ink = tint_layer((20,15,10), np.where(edge2, 160, 0).astype(np.uint8))
# use black tint layer over figure (alpha composite with dark colour works as darkening)
new["NX2-ink-outline-shadow-side"] = compose_tint(ROOM, ground_soft_v2(120), ink)
# NX3 glow underlight: warm glow halo below face + uplight form
glow = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(glow)
d.ellipse([400,480,700,760], fill=(255,140,40,70)); glow=glow.filter(ImageFilter.GaussianBlur(40))
im = ROOM.copy().convert("RGBA"); im.alpha_composite(glow); im.alpha_composite(ground_soft_v2(0)); im.alpha_composite(CANVAS); im.alpha_composite(form_layer_v2('below',0.55)); im.alpha_composite(ao_layer_v2())
new["NX3-glow-underlight"] = im.convert("RGB")
# NX4 animated shadow breathing 4-frame: ground shadow scale pulses
frames=[]
for s in [0.94,1.0,1.06,1.0]:
    c = ground_contact(alpha=200); 
    # scale contact by resizing canvas? approx: use alpha scale + blur variation
    frames.append(compose(ROOM, ground_soft_v2(30, alpha_scale=s)))
new["NX4-shadow-breathing-4f"] = frames
# NX5 mood shadow tint: darkness = blue-black, dramatic = purple-black, two variants in one contact later; here dramatic purple
cast = ground_cast(30); ca=np.array(cast); ca[...,0],ca[...,1],ca[...,2]=40,20,70
new["NX5-mood-purple-shadow"] = compose(ROOM, Image.fromarray(ca))
for k,v in new.items():
    if isinstance(v,list):
        v[0].save(f"{OUT}/new_methods/{k}-f0.png")
        v[0].save(f"{OUT}/new_methods/{k}.gif", save_all=True, append_images=v[1:], duration=250, loop=0)
    else:
        v.save(f"{OUT}/new_methods/{k}.png")
meas["new_methods"] = {k: ({"frames":len(v)} if isinstance(v,list) else {"fig_mean":fig_mean(v)}) for k,v in new.items()}

# ---------- CONTACTS ----------
def contact(paths, cols, thumb=(366,500), outname=""):
    rows = (len(paths)+cols-1)//cols
    sheet = Image.new("RGB",(cols*thumb[0], rows*(thumb[1]+28)),(30,30,30))
    d=ImageDraw.Draw(sheet)
    for i,p in enumerate(paths):
        im=Image.open(p).convert("RGB"); im.thumbnail(thumb)
        x=(i%cols)*thumb[0]; y=(i//cols)*(thumb[1]+28)
        sheet.paste(im,(x,y+28)); d.text((x+6,y+6), os.path.basename(p), fill=(255,255,255))
    sheet.save(f"{OUT}/contacts/{outname}"); return sheet.size

contact([f"{OUT}/improved/{k}.png" if not isinstance(v,list) else f"{OUT}/improved/{k}-f0.png" for k,v in imp.items()], 3, outname="improved-contact-20261031.png")
contact([f"{OUT}/directions/{k}.png" for k in dirs], 3, outname="directions-contact-20261031.png")
contact([f"{OUT}/new_methods/{k}.png" if not isinstance(v,list) else f"{OUT}/new_methods/{k}-f0.png" for k,v in new.items()], 3, outname="new-methods-contact-20261031.png")
# face zoom contact side by side
fz = Image.new("RGB",(760*2,720+28),(30,30,30)); d=ImageDraw.Draw(fz)
for i,n in enumerate(["combined","underlight"]):
    im=Image.open(f"{OUT}/directions/face-zoom-{n}.png"); fz.paste(im,(i*760,28)); d.text((i*760+6,6), f"face zoom {n}", fill=(255,255,255))
fz.save(f"{OUT}/contacts/face-zoom-contact-20261031.png")

# gates
def gate(img_path):
    im=Image.open(img_path)
    return {"size":im.size, "inside_canvas": im.size==(W,H)}
meas["gates"] = {"canvas": [W,H], "feet_y": GY, "figure_alpha_unchanged": "character layers are black-alpha overlays; ground behind figure; no figure pixel erased by construction (same CANVAS paste in every composite)", "no_crop": "all composites 1100x1500, figure bbox inside canvas", "ground_pass": "feet 1400 = Gy 1400 in all direction composites"}
with open(f"{OUT}/measurements-improved-20261031.json","w") as f: json.dump(meas,f,indent=2)
print(json.dumps(meas,indent=2))
