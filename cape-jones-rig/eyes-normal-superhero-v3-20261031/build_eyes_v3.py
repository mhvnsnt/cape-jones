"""Eyes v3: FLIP dark end (v2 dark was image-RIGHT x385-426; v3 dark is image-LEFT x38-79),
integrate brow into lid slant (remove floating brow bars above band), keep Cape Jones palette.
Reference method only: Batman-animated / Teen Titans Robin-mask white angular eyes -
large angular white, pupil-free, uniform mask band, thin bridge, pointed inner corner.
No DC art copied; shapes are original vector polygons fitted to Cape Jones head openings."""
from PIL import Image, ImageDraw
import os, glob, json
SRC='/home/hatch/workspace/cape-jones-rig/eyes-normal-superhero-v2-20261031'
DST='/home/hatch/workspace/cape-jones-rig/eyes-normal-superhero-v3-20261031'
BASE=(90,39,114,255); DARK=(52,22,66,255); BLACK=(10,5,15,255); WHITE=(250,250,248,255)
# lid slant per expression: degrees-like slope in px across eye width (inner side lower = angry)
LID={'01-neutral':(4,4),'02-determined-focused':(3,6),'03-angry-scowling':(2,10),
     '04-surprised-alarmed':(6,6),'05-concentrating':(3,8)}
manifest=[]
for src in sorted(glob.glob(SRC+'/eye-normal-*.png')):
    name=os.path.basename(src).replace('-20261031','').replace('eye-normal-','')
    key=name.split('-')[0]
    expr={'01':'neutral','02':'determined-focused','03':'angry-scowling','04':'surprised-alarmed','05':'concentrating'}[key]
    im=Image.open(src).convert('RGBA')
    w,h=im.size
    px=im.load()
    # 1) flip dark end: v2 dark -> base; base in left segment -> dark
    for y in range(h):
        for x in range(w):
            p=px[x,y]
            if p==DARK:
                px[x,y]=BASE
            elif p==BASE and 38<=x<=79 and 36<=y<=86:
                px[x,y]=DARK
            elif p==BLACK and y<36:
                px[x,y]=(0,0,0,0)  # floating brow bars removed; brow now lives in lid slant
    # 2) integrated lid: for each white eye cluster, redraw top lid as slanted black band
    pts=[(x,y) for y in range(h) for x in range(w) if px[x,y]==WHITE]
    xs=sorted(set(p[0] for p in pts)); clusters=[]; cur=[xs[0]]
    for x in xs[1:]:
        if x-cur[-1]<=3: cur.append(x)
        else: clusters.append(cur); cur=[x]
    clusters.append(cur)
    lid_lo, lid_hi = LID.get(f"{key}-{expr}", (4,4))
    for ci,c in enumerate(clusters):
        x0,x1=min(c),max(c)
        # left eye: inner corner is right side; right eye: inner corner is left side
        inner_right = (ci==0)
        for x in range(x0,x1+1):
            col=[y for xx,y in pts if xx==x]
            if not col: continue
            yt=min(col)
            t = (x-x0)/(x1-x0) if x1>x0 else 0
            # thickness grows toward inner corner
            thick = lid_lo + (lid_hi-lid_lo)*(t if inner_right else (1-t))
            for y in range(yt, min(yt+int(round(thick)), h)):
                if px[x,y]==WHITE: px[x,y]=BLACK
    out=f"{DST}/eye-normal-v3-{key}-{expr}-20261031.png"
    im.save(out)
    # verify dark segment
    dk=[x for y in range(h) for x in range(w) if im.getpixel((x,y))==DARK]
    manifest.append({'file':os.path.basename(out),'expression':expr,
        'dark_segment_x':[min(dk),max(dk)] if dk else None,
        'dark_segment_side':'image-LEFT (x38-79), Arm1 side as Mars sees it in the proof - FLIPPED from v2 image-RIGHT x385-426',
        'white_eye_clusters':[[min(c),max(c)] for c in clusters]})
    print(out, 'dark x', min(dk), max(dk))
json.dump(manifest, open(f'{DST}/eyes-v3-manifest-20261031.json','w'), indent=2)
# strips-alone sheet
from PIL import Image as I
strips=[I.open(f"{DST}/{m['file']}") for m in manifest]
sheet=I.new('RGBA',(480, 128*5+40*4),(128,128,128,255))
d=ImageDraw.Draw(sheet)
for i,s in enumerate(strips):
    y=i*(128+40); sheet.paste(s,(0,y),s); d.text((10,y+132), f"v3-{manifest[i]['file'][:30]}", fill=(0,0,0))
sheet.convert('RGB').save(f'{DST}/strips-alone-v3-20261031.png')
# proof on Head_Front: 3 cols x 2 rows, head 3x, strip 0.75x aligned on eye centres
head=I.open('/home/hatch/workspace/cape-jones-rig/sliced/Head_Front.png').convert('RGBA').resize((357,516), I.LANCZOS)
cell_w, cell_h = 480, 720
proof=I.new('RGBA',(cell_w*3, cell_h*2),(128,128,128,255))
d=ImageDraw.Draw(proof)
for i,m in enumerate(manifest):
    col,row=i%3,i//3; ox,oy=col*cell_w,row*cell_h
    proof.paste(head,(ox+60,oy+10),head)
    strip=I.open(f"{DST}/{m['file']}").resize((360,96), I.LANCZOS)
    proof.paste(strip,(ox+58,oy+10+179),strip)
    d.text((ox+10,oy+cell_h-30), f"v3-{m['expression']}", fill=(0,0,0))
proof.convert('RGB').save(f'{DST}/proof-normal-eyes-v3-on-head-20261031.png')
# before/after: v2 strip vs v3 strip for neutral, side by side with labels
v2=I.open(SRC+'/eye-normal-01-neutral-20261031.png'); v3=I.open(f"{DST}/{manifest[0]['file']}")
ba=I.new('RGBA',(960,200),(128,128,128,255)); d=ImageDraw.Draw(ba)
ba.paste(v2,(0,20),v2); ba.paste(v3,(480,20),v3)
d.text((10,160),'v2: dark RIGHT x385-426 (WRONG)',fill=(0,0,0))
d.text((490,160),'v3: dark LEFT x38-79 (FLIPPED, Arm1)',fill=(0,0,0))
ba.convert('RGB').save(f'{DST}/proof-before-after-v2-vs-v3-20261031.png')
print('done')
