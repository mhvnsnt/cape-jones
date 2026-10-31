"""Visemes v2 — mask-first swap library.
Industry method (cited in VISEMES-V2-METHOD-20261031.md):
 - Toon Boom Harmony mouth chart (A-G + X) + drawing substitution:
   mouth shapes live on their own layer/symbol and are swapped per frame;
   the head underneath carries NO mouth that can show through.
 - Adobe Character Animator viseme set (14 shapes, Mouth group):
   inner-mouth mask is matched to the area between the lips; upper teeth
   do not move; each viseme is a complete drawing, not a paste-over.
Layer order per composite: head base -> SKIN MASK (gradient inpaint of the
mouth zone, covering old mouth line + cheek lines in that zone) -> new mouth
shape -> outline. The mask is sampled from the head's own skin per row, so
no flat-colour rectangle edge shows.
"""
from PIL import Image, ImageDraw
import json, os

SRC = os.path.expanduser('~/workspace/cape-jones-rig/sliced/Head_Front.png')
OUT = os.path.expanduser('~/workspace/cape-jones-rig/visemes-v2-20261031')
S = 4  # upscale factor for smooth lines
head0 = Image.open(SRC).convert('RGBA')
W0, H0 = head0.size
head = head0.resize((W0*S, H0*S), Image.LANCZOS)
W, H = head.size

# Mouth zone (fractions of head), measured from Head_Front:
# cheek lines at x~0.24 / 0.82, old mouth line at y~0.72, chin tick below 0.85
X0, X1 = int(0.235*W), int(0.825*W)
Y0, Y1 = int(0.595*H), int(0.815*H)
CX, CY = W//2, int(0.715*H)

def is_skin(px):
    r,g,b,a = px
    return a > 200 and r > 140 and r > g > b and r-b > 30

def clean_head(img):
    img = img.copy()
    px = img.load()
    # Per-row skin gradient, then smoothed over y to kill banding
    rows = []
    for y in range(Y0, Y1):
        def avg(xa, xb):
            vals = [px[x,y] for x in range(xa, xb) if is_skin(px[x,y])]
            if not vals: return None
            return tuple(sum(c[i] for c in vals)//len(vals) for i in range(3))
        rows.append((avg(X0, X0 + (X1-X0)//3), avg(X1 - (X1-X0)//3, X1)))
    # fill gaps + moving-average smooth (window 21 rows)
    def smooth(vals):
        out=[]
        for i in range(len(vals)):
            seg=[v for v in vals[max(0,i-10):i+11] if v is not None]
            out.append(tuple(sum(c[j] for c in seg)//len(seg) for j in range(3)) if seg else (226,166,130))
        return out
    lefts = smooth([r[0] for r in rows]); rights = smooth([r[1] for r in rows])
    # Elliptical feathered mask centred on the mouth: weight 1 at centre,
    # feathering to 0 at the ellipse edge — no hard rectangle edge.
    import math
    rx, ry = (X1-X0)/2, (Y1-Y0)/2
    for yi, y in enumerate(range(Y0, Y1)):
        for x in range(X0, X1):
            ex, ey = (x-CX)/rx, (y-CY)/ry
            d = math.sqrt(ex*ex + ey*ey)
            if d >= 1.0: continue
            w = 1.0 if d <= 0.75 else (1.0-d)/0.25  # feather ring
            w = w*w*(3-2*w)  # smoothstep
            t_ = (x-X0)/max(1,(X1-X0-1))
            grad = tuple(int(lefts[yi][i]*(1-t_)+rights[yi][i]*t_) for i in range(3))
            orig = px[x,y]
            px[x,y] = tuple(int(orig[i]*(1-w)+grad[i]*w) for i in range(3)) + (255,)
    return img

clean = clean_head(head)
clean.save(f'{OUT}/clean-head-base-20261031.png')

BLACK=(18,18,18); DARK=(35,12,16); WHITE=(252,252,252); TONGUE=(205,105,105); LIP=(150,80,80)

def ellipse(d, box, fill, outline=None, width=1):
    d.ellipse(box, fill=fill, outline=outline, width=width)
def rrect(d, box, rad, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)

def draw_mouth(name, d):
    """All shapes centred on (CX, CY) at 4x scale. Widths in px at 4x."""
    w = lambda v: v*S  # helper: values below are already 4x-scale px, kept explicit
    if name=='rest':
        d.line([(CX-48, CY),(CX+48, CY)], fill=BLACK, width=6)
        d.line([(CX-40, CY+10),(CX+40, CY+10)], fill=LIP, width=4)
    elif name=='ee':  # wide grin, teeth
        rrect(d, [CX-92, CY-26, CX+92, CY+30], 26, DARK, BLACK, 6)
        d.rectangle([CX-92, CY-26, CX+92, CY+2], fill=WHITE)
        d.line([(CX-92, CY+2),(CX+92, CY+2)], fill=BLACK, width=4)
    elif name=='eh':
        rrect(d, [CX-78, CY-30, CX+78, CY+38], 30, DARK, BLACK, 6)
        d.rectangle([CX-78, CY-30, CX+78, CY-2], fill=WHITE)
        ellipse(d, [CX-34, CY+8, CX+34, CY+34], TONGUE)
    elif name=='ah':  # tall open
        rrect(d, [CX-72, CY-62, CX+72, CY+62], 40, DARK, BLACK, 6)
        d.rectangle([CX-72, CY-62, CX+72, CY-28], fill=WHITE)
        ellipse(d, [CX-48, CY+6, CX+48, CY+56], TONGUE)
    elif name=='oh':  # tall oval
        ellipse(d, [CX-52, CY-64, CX+52, CY+64], DARK, BLACK, 6)
        ellipse(d, [CX-36, CY+18, CX+36, CY+58], TONGUE)
    elif name=='oo':  # TRUE circle
        ellipse(d, [CX-46, CY-46, CX+46, CY+46], DARK, BLACK, 6)
        ellipse(d, [CX-20, CY-20, CX+20, CY+20], (15,5,8))
    elif name=='mbp':  # pressed closed lips
        d.line([(CX-52, CY),(CX+52, CY)], fill=BLACK, width=8)
        ellipse(d, [CX-52, CY-10, CX+52, CY+10], (200,140,130))
        d.line([(CX-52, CY),(CX+52, CY)], fill=BLACK, width=5)
    elif name=='fv':  # teeth on lower lip
        rrect(d, [CX-80, CY-18, CX+80, CY+22], 14, DARK, BLACK, 6)
        d.rectangle([CX-80, CY-18, CX+80, CY+6], fill=WHITE)
        d.line([(CX-80, CY+6),(CX+80, CY+6)], fill=BLACK, width=4)
    elif name=='l':  # tongue tip up
        rrect(d, [CX-66, CY-32, CX+66, CY+36], 28, DARK, BLACK, 6)
        ellipse(d, [CX-28, CY-30, CX+28, CY+18], TONGUE)
        d.rectangle([CX-66, CY-32, CX+66, CY-8], fill=WHITE)
    elif name=='sz':  # teeth strip, narrow
        rrect(d, [CX-68, CY-16, CX+68, CY+16], 12, WHITE, BLACK, 6)
        d.line([(CX-68, CY),(CX+68, CY)], fill=BLACK, width=4)
    elif name=='th':  # tongue between teeth
        rrect(d, [CX-66, CY-20, CX+66, CY+20], 14, WHITE, BLACK, 6)
        ellipse(d, [CX-26, CY-4, CX+26, CY+30], TONGUE)
    elif name=='r':
        rrect(d, [CX-58, CY-38, CX+58, CY+38], 30, DARK, BLACK, 6)
        ellipse(d, [CX-38, CY+2, CX+38, CY+34], TONGUE)
    elif name=='w':  # TRUE circle, smaller + tighter than OO (pursed)
        ellipse(d, [CX-36, CY-36, CX+36, CY+36], DARK, BLACK, 7)
        ellipse(d, [CX-15, CY-15, CX+15, CY+15], (15,5,8))
    elif name=='gk':
        rrect(d, [CX-68, CY-44, CX+68, CY+44], 32, DARK, BLACK, 6)
        d.rectangle([CX-68, CY-44, CX+68, CY-14], fill=WHITE)
        ellipse(d, [CX-40, CY+4, CX+40, CY+40], TONGUE)
    else: raise ValueError(name)

VISEMES = [
    ('01','rest','rest / Neutral','X'),
    ('02','ee','EE','C'),
    ('03','eh','EH','C/D'),
    ('04','ah','AH','D'),
    ('05','oh','OH','E'),
    ('06','oo','OO','F'),
    ('07','mbp','M/B/P','A'),
    ('08','fv','F/V','G'),
    ('09','l','L','B'),
    ('10','sz','S/Z','G'),
    ('11','th','TH','B'),
    ('12','r','R','B'),
    ('13','w','W','F'),
    ('14','gk','G/K','B'),
]
manifest = {'method':'mask-first swap library','layer_order':['head base','skin mask (gradient inpaint, mouth zone)','mouth shape','outline'],
            'mouth_zone_fractions':{'x0':0.235,'x1':0.825,'y0':0.595,'y1':0.815,'centre':[0.5,0.715]},
            'head_source':'sliced/Head_Front.png','scale':S,'visemes':[]}
composites=[]
for num, key, label, chart in VISEMES:
    img = clean.copy()
    d = ImageDraw.Draw(img)
    draw_mouth(key, d)
    fn = f'{OUT}/head-v2-{num}-{key}-20261031.png'
    img.save(fn)
    # mouth-zone patch: the swap piece itself (skin patch + mouth)
    patch = img.crop((X0, Y0, X1, Y1))
    pfn = f'{OUT}/patch-v2-{num}-{key}-20261031.png'
    patch.save(pfn)
    composites.append((num, key, label, img))
    manifest['visemes'].append({'num':num,'key':key,'label':label,'toonboom_chart':chart,
        'head_file':os.path.basename(fn),'patch_file':os.path.basename(pfn),'patch_box_4x':[X0,Y0,X1,Y1]})

# Proof sheet: 14 heads + before/after for OO and W
from PIL import ImageFont
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
except Exception: font = ImageFont.load_default()
try: font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
except Exception: font2 = font
cell_w, cell_h = 340, 560
sheet = Image.new('RGB', (cell_w*4, cell_h*4 + 700), (128,128,128))
sd = ImageDraw.Draw(sheet)
sd.text((20,20), 'VISEMES v2 on Head_Front — mask-first swap library (mouth overlay, proof only)', fill=(0,0,0), font=font)
for i,(num,key,label,img) in enumerate(composites):
    r,c = divmod(i,4)
    x,y = c*cell_w, 70 + r*cell_h
    thumb = img.resize((300, int(300*img.height/img.width)), Image.LANCZOS)
    sheet.paste(thumb, (x+20, y), thumb)
    sd.text((x+20, y+thumb.height+10), f'{num}-{key}  {label}', fill=(0,0,0), font=font2)
# Before/after
by = 70 + cell_h*4 + 20
sd.text((20,by), 'BEFORE / AFTER — OO and W: old lines covered first in v2', fill=(0,0,0), font=font)
def v1_style(key):
    """Reconstruction of the v1 method: same shape pasted on the UNMASKED head."""
    img = head.copy(); d = ImageDraw.Draw(img); draw_mouth(key, d); return img
for j,key in enumerate(['oo','w']):
    y = by+50
    trio = [('ORIGINAL HEAD\n(old mouth + cheek lines)', head),
            (f'V1 METHOD: {key.upper()} pasted\non UNMASKED head', v1_style(key)),
            (f'V2: {key.upper()} on MASKED head\n(old lines covered first)', clean.copy())]
    # build v2 image for this key
    v2img = clean.copy(); dd = ImageDraw.Draw(v2img); draw_mouth(key, dd); trio[2] = (trio[2][0], v2img)
    for k,(lab,im) in enumerate(trio):
        x = k*cell_w + 20
        thumb = im.resize((300, int(300*im.height/im.width)), Image.LANCZOS)
        sheet.paste(thumb, (x, y + (j*560)), thumb)
        sd.text((x, y + (j*560) + thumb.height+10), lab, fill=(0,0,0), font=font2)
sheet.save(f'{OUT}/proof-visemes-v2-on-head-20261031.png')
with open(f'{OUT}/visemes-v2-manifest-20261031.json','w') as f: json.dump(manifest, f, indent=2)
print('done', len(composites), 'proof', sheet.size)
