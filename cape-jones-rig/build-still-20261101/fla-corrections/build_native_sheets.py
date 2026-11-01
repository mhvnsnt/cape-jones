#!/usr/bin/env python3
"""Native 1:1 sheets for the 44 remaining batch-60 pieces (sheets 2,4,5,6,7,8).
Pieces are pasted at NATIVE pixel size (no scaling) on grey, with labels.
Read-only on sources; outputs go to this folder only.
"""
import json, os
from PIL import Image, ImageDraw
ROOT='/home/hatch/workspace/cape-jones-rig'
OUT=os.path.dirname(os.path.abspath(__file__))
props=json.load(open(ROOT+'/fla-piece-labelling-top5-20261031/batch-60-20261031/proposals.json'))['proposals']
order={p['piece_id']:i for i,p in enumerate(props)}
# remaining = contact sheets 2,4,5,6,7,8 = items 09-16,25-60 in proposal order
remaining=[p for i,p in enumerate(props) if (i//8+1) not in (1,3)]
print('remaining', len(remaining))
groups={}
for p in remaining:
    idx=order[p['piece_id']]
    sheet=idx//8+1
    groups.setdefault(sheet,[]).append(p)
for sheet, ps in sorted(groups.items()):
    # lay out in 2 rows x 4 cols at native size; cell = max piece size in group + label space
    imgs=[]
    for p in ps:
        src=os.path.join(ROOT,'sliced-clean-20261031/D-xray-angle-ref',p['piece_id'])
        im=Image.open(src).convert('RGBA')
        imgs.append((p,im))
    cell_w=max(im.size[0] for _,im in imgs)+20
    cell_h=max(im.size[1] for _,im in imgs)+60
    cols=4; rows=(len(imgs)+cols-1)//cols
    W=cell_w*cols; H=cell_h*rows
    sheet_im=Image.new('RGBA',(W,H),(128,128,128,255))
    d=ImageDraw.Draw(sheet_im)
    d.text((10,5),f'NATIVE 1:1 — batch-60 contact sheet {sheet} — agent-eye draft, NOT Mars-verified',fill=(255,255,255))
    for k,(p,im) in enumerate(imgs):
        cx=(k%cols)*cell_w+10; cy=(k//cols)*cell_h+30
        sheet_im.alpha_composite(im,(cx,cy))
        d.text((cx,cy+im.size[1]+4),f"{p['piece_id']}\nprop: {p['canonical']}",fill=(255,255,255))
    fn=os.path.join(OUT,f'native-1to1-batch60-sheet{sheet}-20261101.png')
    sheet_im.convert('RGB').save(fn)
    print(sheet, len(imgs), sheet_im.size, fn)
