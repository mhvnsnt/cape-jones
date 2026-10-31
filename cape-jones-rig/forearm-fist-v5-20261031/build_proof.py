from PIL import Image, ImageDraw
D='/home/hatch/workspace/cape-jones-rig/forearm-fist-v5-20261031/'
src=Image.open('/home/hatch/workspace/user/files/1000179204_34_scne.jpg').convert('RGBA')
left=Image.open(D+'fist-left-v5-20261031.png')
right=Image.open(D+'fist-right-v5-20261031.png')
arm2=Image.open(D+'forearm-v5-arm2-front-punch-fist-20261031.png')
arm1=Image.open(D+'forearm-v5-arm1-front-punch-fist-20261031.png')
W,H=1600,620
sheet=Image.new('RGB',(W,H),(128,128,128))
dr=ImageDraw.Draw(sheet)
def paste(img, x, y, maxw, maxh):
    im=img.copy(); im.thumbnail((maxw,maxh), Image.LANCZOS)
    sheet.paste(im,(x,y),im)
    return im.size
dr.text((20,10),'SOURCE (Mars upload, beige bg)',fill=(0,0,0))
paste(src,20,40,380,260)
dr.text((440,10),'CUT-OUT LEFT (transparent, near-white)',fill=(0,0,0))
paste(left,440,40,300,270)
dr.text((780,10),'CUT-OUT RIGHT (transparent, near-white)',fill=(0,0,0))
paste(right,780,40,300,270)
dr.text((1120,10),'SEATED Arm2 (left fist, rotated)',fill=(0,0,0))
paste(arm2,1120,40,320,300)
dr.text((20,360),'SEATED Arm1 (right fist, rotated)',fill=(0,0,0))
paste(arm1,20,390,320,300)
dr.text((380,390),'Knuckles at strike edge (bottom) in seated versions; knuckles at top in standalone cut-outs.',fill=(0,0,0))
dr.text((380,420),'Method: pulled from Mars upload + cut out + fitted. NOT generated, NOT hand-drawn vector.',fill=(0,0,0))
dr.text((380,450),'No beige halo. No WWE logo, no wrestler, no branding shipped. SmackDown search superseded by upload.',fill=(0,0,0))
sheet.save(D+'proof-v5-source-cutouts-seated-20261031.png')
print(sheet.size)
