from PIL import Image, ImageDraw, ImageFont
import os
R='/home/hatch/workspace/cape-jones-rig'; OUT=os.path.join(R,'art-owed-cj15-cj18-20261031')
def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except Exception: pass
    return ImageFont.load_default()
def label(img, text, sub=""):
    d=ImageDraw.Draw(img); d.rectangle([0,0,img.size[0],64],fill=(0,0,0))
    d.text((12,8),text,fill=(255,255,0),font=font(26))
    if sub: d.text((12,36),sub,fill=(255,255,255),font=font(18))
    return img
def thumb(im,w):
    return im.resize((w,int(im.size[1]*w/im.size[0])),Image.LANCZOS)
# ---- CJ-15 before/after ----
orig=Image.open(os.path.join(R,'shots-endtoend-20261031/finals/CJ-15-flying-forward-foreshortened-endtoend-20261031.png')).convert('RGB')
new=Image.open(os.path.join(OUT,'CJ-15-flying-forward-foreshortened-rerender-20261031.png')).convert('RGB')
piece=Image.open(os.path.join(OUT,'cj15-foreshortened-forearm-piece-on-grey-20261031.png')).convert('RGB')
o_t,n_t=thumb(orig,940),thumb(new,940)
join_new=new.crop((1030,320,1300,620)); join_new=join_new.resize((540,600),Image.NEAREST)
join_orig=orig.crop((1030,320,1300,620)); join_orig=join_orig.resize((540,600),Image.NEAREST)
piece_t=thumb(piece,540)
W=1900; H=64+o_t.size[1]+64+600+40
sheet=Image.new('RGB',(W,H),(20,20,20)); d=ImageDraw.Draw(sheet)
label(sheet,"CJ-15 BEFORE (left, flying-37 hover stand-in)  vs  AFTER (right, REAL foreshortened forearm)  — approval 0/1")
sheet.paste(o_t,(10,74)); sheet.paste(n_t,(950,74))
d.text((10,74+o_t.size[1]+10),"BEFORE: hover plate, both forearms hanging at sides",fill=(255,255,255),font=font(20))
d.text((950,74+o_t.size[1]+10),"AFTER: viewer-right forearm = foreshortened piece",fill=(255,255,255),font=font(20))
y=74+o_t.size[1]+64
for x,im,txt in [(10,join_orig,"BEFORE join (3x crop)"),(560,join_new,"AFTER join (3x crop)"),(1110,piece_t,"NEW PIECE (on grey)")]:
    sheet.paste(im,(x,y)); d.text((x,y+600+6),txt,fill=(255,255,0),font=font(20))
sheet.save(os.path.join(OUT,'contact-cj15-before-after-20261031.png'))
print('cj15 contact',sheet.size)
# ---- CJ-18 seam options ----
opts=[]
for key,txt in [('A-keep-seam','A — KEEP SEAM (as-is)'),('B-blend-seam','B — BLEND SEAM (softened)'),('C-half-blend-seam','C — HALF-BLEND (middle)')]:
    im=Image.open(os.path.join(OUT,f'CJ-18-true-flex-double-bicep-{key}-20261031.png')).convert('RGB')
    opts.append((key,txt,im))
    for side,box in [('left',(650,180,880,330)),('right',(1030,180,1270,330))]:
        c=im.crop(box); c=c.resize((c.size[0]*2,c.size[1]*2),Image.NEAREST)
        c.save(os.path.join(OUT,f'cj18-seam-crop-{key}-{side}-20261031.png'))
W2=1900; row_h=64+340
H2=64+row_h*3+40
sheet2=Image.new('RGB',(W2,H2),(20,20,20)); d2=ImageDraw.Draw(sheet2)
d2.rectangle([0,0,W2,64],fill=(0,0,0)); d2.text((12,8),"CJ-18 SEAM OPTIONS — NO DECISION MADE — Mars picks A, B, or C",fill=(255,255,0),font=font(26))
d2.text((12,36),"Same shot spec, grade, rim, aura for all three. Only the two forearm/upper-arm join bands differ. Approval 0/1 for seam options.",fill=(255,255,255),font=font(18))
for i,(key,txt,im) in enumerate(opts):
    y=64+i*row_h+10
    t=thumb(im,620); sheet2.paste(t,(10,y))
    lc=Image.open(os.path.join(OUT,f'cj18-seam-crop-{key}-left-20261031.png')); rc=Image.open(os.path.join(OUT,f'cj18-seam-crop-{key}-right-20261031.png'))
    sheet2.paste(lc,(650,y)); sheet2.paste(rc,(1130,y))
    d2.text((10,y+t.size[1]+4),txt,fill=(255,255,0),font=font(20))
    d2.text((650,y+lc.size[1]+4),"left-arm seam crop (2x)",fill=(255,255,255),font=font(18))
    d2.text((1130,y+rc.size[1]+4),"right-arm seam crop (2x)",fill=(255,255,255),font=font(18))
sheet2.save(os.path.join(OUT,'contact-cj18-seam-options-20261031.png'))
print('cj18 contact',sheet2.size)
