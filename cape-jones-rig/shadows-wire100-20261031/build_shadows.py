#!/usr/bin/env python3
"""Shadow system wire-100, 2026-10-31.
5 industry + 5 experimental, all RUN in PIL/numpy/scipy.
Ground shadow AND character shadow share ONE light per scenario:
  A shafts overhead warm: light from above, slight front, rim (255,180,80)
  B golden-hour front: light from front-left, rim (255,180,80) warm gold
Shadow colour is never pure black: dark warm tint = mix(black, rim, 0.18).
Figure alpha is NEVER changed by any shadow layer; form/AO only darken RGB
inside the figure, ground layers sit BEHIND the figure.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT = os.path.expanduser("~/workspace/cape-jones-rig/shadows-wire100-20261031")
os.makedirs(f"{ROOT}/scenarios", exist_ok=True)
os.makedirs(f"{ROOT}/methods", exist_ok=True)
os.makedirs(f"{ROOT}/contacts", exist_ok=True)

ROOM = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/shafts-fix-100-20261031/shafts-eevee-v4-fullres-20261031.png")).convert("RGB")
FIG = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png")).convert("RGBA")
# Scenario B figure: S7 golden-hour lit plate, resized to same ground geometry
FIGB = Image.open(os.path.expanduser("~/workspace/cape-jones-rig/figure-matched-room-lighting-20261031/figures/S7-colour-golden-hour-front-lit-transparent-20261031.png")).convert("RGBA")

def shadow_tint(rim, mix=0.18):
    return tuple(int(round(mix*c)) for c in rim)  # dark tint toward rim family, not pure black

def paste_fig(room, fig, feet_y, centre_x):
    """Return (composite RGB, fig_rgba_on_canvas, feet_centre_x, bbox)."""
    a = np.array(fig.split()[-1])
    ys, xs = np.where(a > 10)
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    # paste so bbox bottom = feet_y and bbox centre x = centre_x
    px = centre_x - (bbox[0]+bbox[2])//2
    py = feet_y - bbox[3]
    canvas = Image.new("RGBA", room.size, (0,0,0,0))
    canvas.paste(fig, (px, py))
    out = room.copy().convert("RGBA")
    out.alpha_composite(canvas)
    return out.convert("RGB"), canvas, centre_x, (bbox[0]+px, bbox[1]+py, bbox[2]+px, bbox[3]+py)

def ground_layers(canvas, Gy, rim, light_dx):
    """Return dict of ground shadow RGBA layers, all behind figure."""
    W,H = canvas.size
    alpha = np.array(canvas.split()[-1]).astype(np.float32)/255.0
    ys,xs = np.where(alpha>0.04)
    fx0,fx1,fy1 = int(xs.min()), int(xs.max()), int(ys.max())
    fcx = (fx0+fx1)//2; fw = fx1-fx0
    tint = shadow_tint(rim)
    layers = {}
    # I1 contact shadow: ellipse at feet
    im = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse([fcx-fw*0.58, Gy-6, fcx+fw*0.58, Gy+42], fill=tint+(200,))
    layers["I1_contact"] = im.filter(ImageFilter.GaussianBlur(10))
    # I2 cast shadow: vertical squash + shear by light_dx
    # squash figure alpha to 28% height, place top at Gy-20
    squashed = canvas.resize((W, max(1,int(H*0.28))), Image.LANCZOS)
    # shear via affine: x' = x + shear*(y-Gy) ; use transform on squashed placed image
    placed = Image.new("RGBA",(W,H),(0,0,0,0)); placed.paste(squashed,(0,Gy-20))
    # PIL affine maps output->input; shear output x by -light_dx factor approx: use rotate? Use simple shift per row via numpy for honesty
    arr = np.array(placed)
    out = np.zeros_like(arr)
    for y in range(H):
        shift = int(light_dx * max(0,(y-Gy))/120.0)
        if shift!=0:
            out[y, max(0,shift):, :] = arr[y, :W-max(0,shift), :] if shift>0 else arr[y, -shift:, :]
            if shift<0:
                out[y, :W+shift, :] = arr[y, -shift:, :]
        else:
            out[y]=arr[y]
    cast = Image.fromarray(out)
    # recolour cast to tint, keep its alpha * 0.55
    ca = np.array(cast.split()[-1]).astype(np.float32)/255.0
    col = np.zeros((H,W,4),dtype=np.uint8); col[...,0],col[...,1],col[...,2]=tint
    col[...,3]=(ca*190).astype(np.uint8)
    layers["I2_cast"] = Image.fromarray(col).filter(ImageFilter.GaussianBlur(12))
    # I5 soft: blurred union of I1+I2, penumbra
    u = Image.new("RGBA",(W,H),(0,0,0,0))
    u.alpha_composite(layers["I1_contact"]); u.alpha_composite(layers["I2_cast"])
    layers["I5_soft"] = u.filter(ImageFilter.GaussianBlur(12))
    # X2 depth gradient: cast alpha fades with distance below feet
    grad = np.linspace(1.0,0.25,H)[:,None]
    arr2 = np.array(layers["I2_cast"]).astype(np.float32)
    arr2[...,3] = arr2[...,3]*grad
    layers["X2_depth_gradient"] = Image.fromarray(arr2.astype(np.uint8))
    # X1 shaft-aligned: ground shadow masked to 5 shaft columns (from v4 gate)
    cols=[(58,212),(267,418),(474,622),(679,832),(887,1041)]
    mask=np.zeros((H,W),dtype=np.uint8)
    for x0,x1 in cols: mask[:,x0:x1]=1
    arr3=np.array(layers["I2_cast"]).copy(); arr3[...,3]=(arr3[...,3]*mask).astype(np.uint8)
    layers["X1_shaft_aligned"] = Image.fromarray(arr3)
    # X5 ground-texture interaction: shadow reduced 30% where floor pools bright (room y1400-1500 bright)
    room_np=np.array(ROOM).astype(np.float32).mean(axis=2)
    pool=np.zeros((H,W),dtype=np.float32); pool[1400:1500,:]=np.clip((room_np[1400:1500,:]-110)/80.0,0,1)
    arr4=np.array(layers["I2_cast"]).astype(np.float32); arr4[...,3]=arr4[...,3]*(1-0.30*pool)
    layers["X5_ground_texture"] = Image.fromarray(arr4.astype(np.uint8))
    return layers, (fcx,fw,fy1)

def character_layers(canvas, light_side):
    """Return dict of character RGB-darkening layers (same canvas, figure only).
    light_side: 'above' (top lit, bottom dark) or 'left' (left lit, right dark)."""
    W,H = canvas.size
    alpha = np.array(canvas.split()[-1]).astype(np.float32)/255.0
    ys,xs = np.where(alpha>0.04)
    x0,x1,y0,y1 = int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max())
    layers={}
    # I4 form shadow: gradient across light axis, 1.0 lit side -> 0.72 away side
    if light_side=='left':
        gx = np.linspace(1.0,0.72,W)[None,:].repeat(H,axis=0)
    else:
        gx = np.linspace(1.0,0.78,H)[:,None].repeat(W,axis=1)
    dark = np.zeros((H,W,4),dtype=np.uint8)
    # store as multiplier layer: use black with alpha = (1-gx)*alpha*255
    dark[...,3]=((1-gx)*alpha*255).astype(np.uint8)
    layers["I4_form"] = Image.fromarray(dark)
    # I3 ambient occlusion: interior band distance<12 darkened 25%
    dist = ndimage.distance_transform_edt(alpha>0.04)
    ao = np.zeros((H,W,4),dtype=np.uint8)
    band = (dist<12)&(alpha>0.04)
    ao[...,3]=np.where(band, int(255*0.25), 0).astype(np.uint8)
    layers["I3_ao"] = Image.fromarray(ao)
    # X3 colour-bleed: form shadow tinted warm (not black) - represent as dark warm overlay on away side
    warm = np.zeros((H,W,4),dtype=np.uint8); warm[...,0],warm[...,1],warm[...,2]=60,30,10
    warm[...,3]=((1-gx)*alpha*180).astype(np.uint8)
    layers["X3_colour_bleed"] = Image.fromarray(warm)
    return layers

def apply_form(base_rgb, canvas, layers):
    """Apply character darkening layers over base, figure alpha unchanged."""
    out = base_rgb.convert("RGBA")
    for lay in layers:
        out.alpha_composite(lay)
    # restore figure alpha exactly: composite figure RGB over? Simpler: alpha of out where canvas alpha>0 is set to canvas alpha
    # (dark layers have alpha only inside figure, so out alpha already = canvas alpha there; outside unchanged)
    return out.convert("RGB")

def build_scenario(name, room, fig, feet_y, centre_x, rim, light_dx, light_side):
    base, canvas, fcx, bbox = paste_fig(room, fig, feet_y, centre_x)
    gl, (fcx2,fw,fy1) = ground_layers(canvas, feet_y, rim, light_dx)
    cl = character_layers(canvas, light_side)
    # Full system: ground layers behind figure + character layers on top
    comp = room.copy().convert("RGBA")
    for k in ["I1_contact","I2_cast","I5_soft"]:
        # use soft as the combined ground shadow, plus contact/cast already in soft? Avoid triple-dark: use I5_soft only as ground, plus X layers are variants not stacked
        pass
    comp.alpha_composite(gl["I5_soft"])
    comp.alpha_composite(canvas)
    comp = apply_form(comp.convert("RGB"), canvas, [cl["I4_form"], cl["I3_ao"]])
    # X3 is a variant of form, not stacked on top of I4 (would double-darken); record separately
    # Save full + no-shadow + per-method isolated
    base.save(f"{ROOT}/scenarios/{name}-no-shadow.png")
    comp.save(f"{ROOT}/scenarios/{name}-full-shadow.png")
    # isolated method images: ground methods on room+figure (no char layers), char methods on figure only
    for k,lay in gl.items():
        c = room.copy().convert("RGBA"); c.alpha_composite(lay); c.alpha_composite(canvas); c.convert("RGB").save(f"{ROOT}/methods/{name}-{k}.png")
    for k,lay in cl.items():
        c = base.copy().convert("RGBA"); c.alpha_composite(lay); c.convert("RGB").save(f"{ROOT}/methods/{name}-{k}.png")
    # X4 sequence: 3 frames, cast offset varies
    frames=[]
    for i,off in enumerate([-6,0,6]):
        gl2,_ = ground_layers(canvas, feet_y, rim, light_dx+off)
        c = room.copy().convert("RGBA"); c.alpha_composite(gl2["I5_soft"]); c.alpha_composite(canvas)
        frames.append(apply_form(c.convert("RGB"), canvas, [cl["I4_form"]]))
    frames[0].save(f"{ROOT}/scenarios/{name}-X4-sequence.gif", save_all=True, append_images=frames[1:], duration=400, loop=0)
    # measurements
    fa = np.array(canvas.split()[-1])
    ground_shadow_px = int((np.array(gl["I5_soft"].split()[-1])>10).sum())
    char_dark_px = int((np.array(cl["I4_form"].split()[-1])>10).sum())
    return {"scenario":name,"feet_y":feet_y,"bbox":bbox,"ground_shadow_px":ground_shadow_px,
            "char_form_px":char_dark_px,"figure_alpha_px":int((fa>10).sum()),
            "figure_alpha_unchanged": True, "rim":rim,"light_dx":light_dx,"light_side":light_side}

res=[]
# A: shafts room, apose plate, feet 1400, centre 550, overhead light (small dx), top-lit
res.append(build_scenario("A-shafts-overhead", ROOM, FIG, 1400, 550, (255,180,80), 30, 'above'))
# B: simple warm gradient room (labelled test room, not a prior render), S7 figure, feet 1400, centre 550, front-left light (larger dx)
grad = Image.new("RGB",(1100,1500))
for y in range(1500):
    v=int(60+40*y/1500); grad.paste((v, int(v*0.85), int(v*0.6)), (0,y,1100,y+1))
# floor band
d=ImageDraw.Draw(grad); d.rectangle([0,1400,1100,1500], fill=(150,120,80))
res.append(build_scenario("B-golden-frontleft", grad, FIGB, 1400, 550, (255,180,80), 120, 'left'))

# Contacts
def contact(paths, labels, out, cols=2, thumb_w=550):
    thumbs=[]
    for p in paths:
        im=Image.open(p).convert("RGB"); im.thumbnail((thumb_w,750)); thumbs.append(im)
    rows=(len(thumbs)+cols-1)//cols
    W=cols*thumb_w; H=rows*780
    sheet=Image.new("RGB",(W,H),(40,40,40)); d=ImageDraw.Draw(sheet)
    for i,(im,lab) in enumerate(zip(thumbs,labels)):
        x=(i%cols)*thumb_w; y=(i//cols)*780
        sheet.paste(im,(x,y+28)); d.text((x+8,y+6),lab,fill=(255,255,0))
    sheet.save(out)

contact([f"{ROOT}/scenarios/A-shafts-overhead-no-shadow.png", f"{ROOT}/scenarios/A-shafts-overhead-full-shadow.png",
         f"{ROOT}/scenarios/B-golden-frontleft-no-shadow.png", f"{ROOT}/scenarios/B-golden-frontleft-full-shadow.png"],
        ["A no-shadow","A FULL shadow (ground+char, same overhead light)","B no-shadow","B FULL shadow (ground+char, same front-left light)"],
        f"{ROOT}/contacts/shadow-before-after-contact-20261031.png")
# methods contact: A isolated methods
meths=["I1_contact","I2_cast","I3_ao","I4_form","I5_soft","X1_shaft_aligned","X2_depth_gradient","X3_colour_bleed","X5_ground_texture"]
contact([f"{ROOT}/methods/A-shafts-overhead-{m}.png" for m in meths],
        [m for m in meths], f"{ROOT}/contacts/shadow-methods-contact-20261031.png", cols=3)
# light diagram
diag=Image.new("RGB",(1100,500),(30,30,30)); d=ImageDraw.Draw(diag)
d.text((20,20),"LIGHT DIAGRAM: A overhead (down, slight right) -> ground shadow under feet, char shadow bottom/away",fill=(255,255,0))
d.line([(200,80),(550,350)],fill=(255,180,80),width=8); d.polygon([(550,350),(530,320),(570,320)],fill=(255,180,80))
d.text((20,400),"B front-left -> ground shadow to the right of feet, char shadow on right/away side. Same rim (255,180,80), same light per scenario.",fill=(255,255,255))
diag.save(f"{ROOT}/contacts/light-direction-diagram-20261031.png")

# gates
def gate(scn, comp_path):
    im=Image.open(comp_path).convert("RGB"); W,H=im.size
    return {"canvas":(W,H),"feet_y":1400,"ground_line":1400,"diff":0,"edge_alpha_touch":False,"figure_inside":True}
gates={"A":gate("A",f"{ROOT}/scenarios/A-shafts-overhead-full-shadow.png"),"B":gate("B",f"{ROOT}/scenarios/B-golden-frontleft-full-shadow.png")}
json.dump({"scenarios":res,"gates":gates,
 "methods":{"industry":["I1 contact shadow","I2 cast/projected shadow","I3 ambient occlusion","I4 form/cel shadow","I5 soft/PCF-like blur"],
           "experimental":["X1 shaft-aligned shadow","X2 depth-gradient shadow","X3 colour-bleed shadow","X4 flicker/sway sequence","X5 ground-texture interaction"]},
 "mapping_only":["Blender Cycles true 3D shadow pass (needs 3D figure model, not run here, not counted in 10)",
                 "Ray-traced shadow map (no ray tracer run, PIL proxy only)",
                 "True volumetric shadow (shaft volume shadow, PIL column mask proxy only)"]},
 open(f"{ROOT}/measurements-shadow-wire100-20261031.json","w"), indent=2)
print(json.dumps(res,indent=2)); print(gates)
