import json, os
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
W='/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031'
LIB=f'{W}/library'; os.makedirs(f'{W}/proofs', exist_ok=True)
head=Image.open('/home/hatch/workspace/cape-jones-rig/sliced/Head_Front.png').convert('RGBA')
print('head', head.size)
man=json.load(open(f'{LIB}/manifest.json'))
# openings at 1x: left x25-44, right x73-92, y72-80 (from v4). Proof at 4x.
S=4
proofs=[]
for e in man:
    canvas=head.resize((head.size[0]*S, head.size[1]*S), Image.NEAREST)
    eyes=[Image.open(f"{LIB}/{e['id']}-eye{j}.png") for j in range(e['eyes'])]
    openings=[(25,44),(73,92)] if e['eyes']>=2 else [(25,44)]
    oh=8*S  # opening height at 4x
    for mk,(ox0,ox1) in zip(eyes, openings):
        s=oh/mk.size[1]; nm=mk.resize((max(1,int(mk.size[0]*s)), oh), Image.LANCZOS)
        cx=((ox0+ox1)/2)*S; cy=76*S
        canvas.paste(nm,(int(cx-nm.size[0]/2), int(cy-nm.size[1]/2)), nm)
    canvas.save(f"{W}/proofs/{e['id']}-inmask.png")
    proofs.append(e['id'])
print('proofs', len(proofs))
# contact sheet of strips: 4 cols
from PIL import Image as I
strips=[f"{LIB}/{e['id']}-strip.png" for e in man]
cols=4; cellw=480; cellh=128+22; rows=(len(strips)+cols-1)//cols
S2=I.new('RGB',(cols*cellw, rows*cellh),(128,128,128)); d=ImageDraw.Draw(S2)
for i,p in enumerate(strips):
    im=I.open(p).convert('RGBA'); x=(i%cols)*cellw; y=(i//cols)*cellh
    S2.paste(im,(x,y),im); d.text((x+6,y+130), man[i]['id'], fill=(255,255,0))
S2.save(f'{W}/library-contact-sheet.png'); print('contact', S2.size)
# CAPE: black outer from RBN03 back render (11_)
im=np.array(Image.open(f'{W}/render/11_RBN03_CAMS_DCTTAS.png').convert('RGBA'))
rgb=im[:,:,:3].astype(int); al=im[:,:,3]
black=(rgb[:,:,0]<30)&(rgb[:,:,1]<30)&(rgb[:,:,2]<30)&(al>200)
lab,n=ndimage.label(black)
best=None
for i in range(1,n+1):
    yy,xx=np.where(lab==i)
    if len(yy)>5000:
        # prefer component in lower 2/3 and central
        if yy.mean()>400: 
            if best is None or len(yy)>best[0]: best=(len(yy), int(xx.min()),int(xx.max()),int(yy.min()),int(yy.max()), lab==i)
print('cape black comp:', best[:5] if best else None)
if best:
    m=best[5]; out=np.zeros_like(im); out[m]=im[m]
    yy,xx=np.where(m)
    Image.fromarray(out[int(yy.min()):int(yy.max())+1, int(xx.min()):int(xx.max())+1]).save(f'{W}/library/robin-cape-black-outer.png')
    print('cape saved')
# YELLOW lining from Robin 2.ai render: yellow pixels (255,225,82 approx)
im2=np.array(Image.open(f'{W}/render/01_Robin_2.png').convert('RGBA'))
rgb2=im2[:,:,:3].astype(int); al2=im2[:,:,3]
yel=(rgb2[:,:,0]>200)&(rgb2[:,:,1]>170)&(rgb2[:,:,2]<130)&(al2>200)
ys,xs=np.where(yel)
print('yellow lining px', len(ys), 'x', xs.min(), xs.max(), 'y', ys.min(), ys.max())
if len(ys):
    sample=tuple(int(v) for v in rgb2[int(np.median(ys)), int(np.median(xs))])
    print('yellow median RGB', sample)
    lab2,n2=ndimage.label(yel)
    # largest yellow comp = cape lining
    sizes=[(int((lab2==i).sum()), i) for i in range(1,n2+1)]
    sizes.sort(reverse=True); print('largest yellow comps', sizes[:3])
    m2=(lab2==sizes[0][1]); out2=np.zeros_like(im2); out2[m2]=im2[m2]
    yy,xx=np.where(m2)
    Image.fromarray(out2[int(yy.min()):int(yy.max())+1, int(xx.min()):int(xx.max())+1]).save(f'{W}/library/robin-cape-yellow-lining.png')
    print('lining saved')
# PSD duplicate check
for psd,jpg in [('44_ROBIN.Day.psd','02_ROBIN_Day.jpg'),('43_ROBIN.Night.psd','03_ROBIN_Night.jpg')]:
    a=Image.open(f'{W}/raw/{psd}').convert('RGB'); b=Image.open(f'{W}/raw/{jpg}').convert('RGB')
    a.thumbnail((400,400)); b.thumbnail((400,400))
    d=np.abs(np.array(a).astype(int)-np.array(b).astype(int)).mean()
    print('PSD-vs-JPG', psd, 'mean abs diff', round(float(d),2), a.size, b.size)
# place.jpg eyes quick check
pl=Image.open(f'{W}/raw/04_Robin_place.jpg').convert('RGBA')
a=np.array(pl); rgb=a[:,:,:3].astype(int); al=a[:,:,3]
white=(rgb[:,:,0]>235)&(rgb[:,:,1]>235)&(rgb[:,:,2]>235)&(al>200)
lab,n=ndimage.label(white)
print('place.jpg size', pl.size, 'white comps>=40:', sum(1 for i in range(1,n+1) if (lab==i).sum()>=40))
for i in range(1,n+1):
    yy,xx=np.where(lab==i)
    if len(yy)>=40: print('  place comp', len(yy), int(xx.min()),int(xx.max()),int(yy.min()),int(yy.max()))
