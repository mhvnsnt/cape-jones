from PIL import Image
import os, json
SRC='/home/hatch/workspace/cape-jones-rig/sliced-68-unsliced-20261031/sheets/fla-packs/clean-F72A5'
CAPE='/home/hatch/workspace/cape-jones-rig/sliced-68-unsliced-20261031/sheets/fla-packs/clean-DGb2j/Row2_6.png'
OUT='/home/hatch/workspace/cape-jones-rig/threequarter-sitting-sheet-20261101'
def load(n, s):
    im=Image.open(os.path.join(SRC,n)).convert('RGBA')
    return im.resize((int(im.width*s), int(im.height*s)), Image.LANCZOS)
canvas=Image.new('RGBA',(1100,1500),(0,0,0,0))
# cape behind, scale 1.15
cape=Image.open(CAPE).convert('RGBA').resize((585,791), Image.LANCZOS)
canvas.alpha_composite(cape,(258,320))
# bent sitting legs first (under torso), scale 1.5
legL=load("Row3_4.png",1.3); legR=load("Row3_5.png",1.3)
canvas.alpha_composite(legL,(330,720))
canvas.alpha_composite(legR,(500,720))
# torso
torso=load('Row2_3.png',1.7)
canvas.alpha_composite(torso,(340,360))
# arms: Row2_1 left, Row2_4 right (as drawn, hands attached)
armL=load('Row2_1.png',1.7); armR=load('Row2_4.png',1.7)
canvas.alpha_composite(armL,(300,400))
canvas.alpha_composite(armR,(640,400))
# head
head=load('Row1_1.png',1.7)
canvas.alpha_composite(head,(460,150))
canvas.save(f'{OUT}/threequarter-sitting-rig-20261101.png')
# grey version for viewing
bg=Image.new('RGBA',canvas.size,(128,128,128,255)); bg.alpha_composite(canvas); bg.convert('RGB').save(f'{OUT}/threequarter-sitting-rig-20261101-on-grey.png')
print('bbox', canvas.getchannel('A').getbbox(), 'alpha', sum(1 for p in canvas.getchannel('A').getdata() if p>10))
