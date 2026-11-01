import json, os
from PIL import Image, ImageDraw
BASE = os.path.dirname(os.path.abspath(__file__))
V4 = '/home/hatch/workspace/cape-jones-rig/shafts-fix-100-20261031'
shafts = Image.open(os.path.join(V4,'shafts-eevee-v4-fullres-20261031.png')).convert('RGB')
before = Image.open(os.path.join(V4,'composite-shafts-v4-figure-20261031.png')).convert('RGB')
after = Image.open(os.path.join(BASE,'composite-shafts-v4-GROUNDED-20261031.png')).convert('RGB')
glare = Image.open(os.path.join(V4,'methods','I4-glare-v4.png')).convert('RGB')
rows = json.load(open(os.path.join(BASE,'gate-grounded-20261031.json')))['per_shot']

def tile(images, labels, cols, tw, th, bg=(40,40,40)):
    rws = (len(images)+cols-1)//cols
    out = Image.new('RGB',(cols*tw, rws*(th+28)), bg)
    d = ImageDraw.Draw(out)
    for i,(im,lab) in enumerate(zip(images,labels)):
        r,c = divmod(i,cols); x,y = c*tw, r*(th+28)
        out.paste(im.resize((tw,th)),(x,y)); d.text((x+6,y+th+6),lab,fill=(255,255,0))
    return out

# before/after main + feet zoom
zoom_before = before.crop((200,1200,900,1500)).resize((700,300))
zoom_after = after.crop((200,1200,900,1500)).resize((700,300))
ba = Image.new('RGB',(1400, 2*1500//2 + 2*300 + 84),(40,40,40))
# simpler: stack full before/after at half scale + zooms
ba = Image.new('RGB',(1100, 1500+300+84),(40,40,40))
d = ImageDraw.Draw(ba)
ba.paste(before.resize((550,750)),(0,0)); d.text((6,756),'BEFORE floating, feet y1282, 118px above Gy1400',fill=(255,255,0))
ba.paste(after.resize((550,750)),(550,0)); d.text((556,756),'AFTER GROUNDED, feet y1400 = Gy, margin bottom 99',fill=(255,255,0))
ba.paste(zoom_before,(0,784)); d.text((6,1084),'ZOOM BEFORE feet x200-900 y1200-1500',fill=(255,255,0))
ba.paste(zoom_after,(0,1112)); d.text((6,1412),'ZOOM AFTER feet planted on pools band y1400-1500',fill=(255,255,0))
# right column note area
d.text((560,784),'Ground line Gy=1400',fill=(255,255,255))
d.text((560,810),'= top of in-scene pools band',fill=(255,255,255))
d.text((560,836),'Shift dy +118, no scale,',fill=(255,255,255))
d.text((560,862),'no recolour, shafts behind',fill=(255,255,255))
d.text((560,888),'figure, occlusion 0.0',fill=(255,255,255))
ba.save(os.path.join(BASE,'grounded-before-after-contact-20261031.png'))

# grounded final contact, same layout as original
samples = [Image.open(os.path.join(BASE,'per-shot-grounded',r['file'])).convert('RGB') for r in rows[:4]]
labs = [r['shot_id']+' GROUNDED shafts' for r in rows[:4]]
tile([shafts, after, glare]+samples, ['V4 Eevee shafts only','V4 Eevee + figure GROUNDED','V4 Glare']+labs, 3, 360, 490).save(os.path.join(BASE,'final-contact-GROUNDED-20261031.png'))

# grounded per-shot grid
imgs = [Image.open(os.path.join(BASE,'per-shot-grounded',r['file'])).convert('RGB') for r in rows]
labs = [f"{r['shot_id']} {'G' if r['mode']=='GROUNDED' else 'AIR'}" for r in rows]
tile(imgs, labs, 5, 300, 408).save(os.path.join(BASE,'per-shot-contact-GROUNDED-20261031.png'))
print('contacts done')
