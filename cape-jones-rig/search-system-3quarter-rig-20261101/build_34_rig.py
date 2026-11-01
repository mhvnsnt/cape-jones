#!/usr/bin/env python3
"""Assemble 3/4 sitting rig from Mars upload pieces. RIG-00 untouched — this is a NEW rig."""
from PIL import Image
import os
OUT='/home/hatch/workspace/cape-jones-rig/search-system-3quarter-rig-20261101'
P=f'{OUT}/pieces'
def load(name, s):
    im=Image.open(os.path.join(P,name)).convert('RGBA')
    return im.resize((int(im.width*s),int(im.height*s)), Image.LANCZOS)
canvas=Image.new('RGBA',(1100,1500),(0,0,0,0))
# cape behind
cape=load('piece-13-743x723.png',1.25); canvas.alpha_composite(cape,(480,260))
# thighs (as drawn, angled = sitting) under torso
thighL=load('piece-15-311x785.png',1.45); canvas.alpha_composite(thighL,(270,700))
thighR=load('piece-18-508x833.png',1.45); canvas.alpha_composite(thighR,(500,700))
# shins + feet vertical, feet planted
shinL=load('piece-21-190x1028.png',1.35); canvas.alpha_composite(shinL,(285,975))
shinR=load('piece-23-350x1096.png',1.35); canvas.alpha_composite(shinR,(510,975))
# pelvis/belt over thigh tops
pelvis=load('piece-12-498x677.png',1.55); canvas.alpha_composite(pelvis,(360,640))
# torso
torso=load('piece-03-500x406.png',1.65); canvas.alpha_composite(torso,(360,290))
# upper arms
uaL=load('piece-02-352x382.png',1.55); canvas.alpha_composite(uaL,(300,330))
uaR=load('piece-04-776x439.png',1.55); canvas.alpha_composite(uaR,(660,330))
# forearms + hands down to knees
faL=load('piece-06-116x534.png',1.55); canvas.alpha_composite(faL,(290,560))
faR=load('piece-11-714x671.png',1.55); canvas.alpha_composite(faR,(650,560))
# head
head=load('piece-01-559x241.png',1.65); canvas.alpha_composite(head,(445,95))
canvas.save(f'{OUT}/threequarter-sitting-rig-20261101.png')
bg=Image.new('RGBA',canvas.size,(128,128,128,255)); bg.alpha_composite(canvas); bg.convert('RGB').save(f'{OUT}/threequarter-sitting-rig-20261101-on-grey.png')
print('bbox',canvas.getchannel('A').getbbox(),'alpha',sum(1 for p in canvas.getchannel('A').getdata() if p>10))
# contact of cut pieces
import glob
files=sorted(glob.glob(f'{P}/*.png'))
tiles=[]
for f in files:
    im=Image.open(f).convert('RGBA'); im.thumbnail((220,220)); tiles.append((os.path.basename(f),im))
cols=5; rows=(len(tiles)+cols-1)//cols
from PIL import ImageDraw
sheet=Image.new('RGB',(cols*230,rows*250),(255,255,255)); d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(tiles):
    x=(i%cols)*230; y=(i//cols)*250
    sheet.paste(im,(x,y+20),im); d.text((x+5,y+2),name[:30],fill=(0,0,0))
sheet.save(f'{OUT}/contacts/cut-pieces-contact-20261101.png'); print('pieces contact',len(tiles))
