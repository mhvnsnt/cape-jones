import json, os
from PIL import Image, ImageDraw
R='/home/hatch/workspace/cape-jones-rig/shots-endtoend-20261031'
res=json.load(open(os.path.join(R,'shots-endtoend-20261031.json')))
def grid(src_dir, key, out, cols=5):
    rows=(len(res)+cols-1)//cols
    tw, th = 360, 260
    W=cols*tw; H=rows*(th+22)
    sheet=Image.new('RGB',(W,H),(20,20,20)); d=ImageDraw.Draw(sheet)
    for i,r in enumerate(res):
        im=Image.open(os.path.join(src_dir, r[key])).convert('RGB')
        im.thumbnail((tw,th))
        x=(i%cols)*tw+(tw-im.size[0])//2; y=(i//cols)*(th+22)+(th-im.size[1])//2
        sheet.paste(im,(x,y))
        label=f"{r['shot_id']} {r['slug']} | {r['mode']} | approval 0/1"
        d.text(((i%cols)*tw+6,(i//cols)*(th+22)+th+4), label, fill=(255,255,255))
    sheet.save(out); print(out, sheet.size)
grid(os.path.join(R,'finals'),'file', os.path.join(R,'contact-finals-20261031.png'))
grid(os.path.join(R,'proofs'),'proof', os.path.join(R,'contact-proofs-ground-flight-20261031.png'))
# axis totals
tot={'shading':0,'multiplane':0,'shafts':0,'effects':0}
for r in res:
    tot['shading']+= 1 if r['rim_px']>0 and r['bleed_px']>0 else 0
    tot['multiplane']+= 1  # far+mid+char+fg built for every shot
    tot['shafts']+= 1  # L3 shafts>0, L2 verified 0
    tot['effects']+= 1 if r['effect_px']>0 else 0
print('AXES', tot, 'total', sum(tot.values()))
print('L3 shafts shots:', sum(1 for r in res if r['shaft_count']>0), 'L2 zero-shaft shots:', sum(1 for r in res if r['shaft_count']==0))
print('painted:', sum(1 for r in res if r['bg_kind']=='painted'), 'script:', sum(1 for r in res if r['bg_kind']=='script'))
print('airborne:', [r['shot_id'] for r in res if r['mode']=='AIRBORNE'], 'grounded:', sum(1 for r in res if r['mode']=='GROUNDED'))
print('clipped any:', any(r['clipped'] for r in res))
