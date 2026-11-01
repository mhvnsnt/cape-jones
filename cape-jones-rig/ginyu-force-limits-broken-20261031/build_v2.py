import os
src=open(os.path.expanduser("~/workspace/cape-jones-rig/ginyu-force-limits-broken-20261031/build_limits_broken.py")).read()
exec(src.split("# 1. KICK")[0])
# Kick reframed: figure centre 470 so the extended foot fits inside 1100px
c=Image.new("RGBA",(1100,1500),(0,0,0,0)); figure(c,470,C((-60,100),(80,-40),(-20,65),(10,60)),0,()); c.save(os.path.join(OUT,"bur-03-mach-kick-extended-20261031.png")); print("kick reframed cx=470")
# CAP twist stronger
save("cap-01-twist-segment-20261031.png", C((-100,10),(30,90),(-40,35),(15,-15)), -8, ("L",), chest_rot=-12, tilt=20)
# JEI-03X point variant: lower -160 puts the hand up-left, isolated (original JEI-03 lower 40
# bends the fist inward to the chest, so it does NOT point up-out as originally described)
save("jei-03x-point-variant-base-20261031.png", C((-110,20),(-160,100),(-35,25),(20,-20)), -12, ("L",))

def erase_white_circle(im, cx, cy, r):
    px=im.load()
    for y in range(max(0,int(cy-r)), min(im.size[1],int(cy+r))):
        for x in range(max(0,int(cx-r)), min(im.size[0],int(cx+r))):
            if (x-cx)**2+(y-cy)**2 <= r*r:
                R,G,B,A=px[x,y]
                if A>0 and R>180 and G>180 and B>180: px[x,y]=(0,0,0,0)
    return im
def hand_swap(pose_name, hand_file, centre, angle, erase_r, out_name):
    c=Image.open(os.path.join(OUT,pose_name)).convert("RGBA")
    c=erase_white_circle(c, centre[0], centre[1], erase_r)
    hand=load(os.path.join(BASE,hand_file), scale=1.0)
    if angle: hand=hand.rotate(angle, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(hand,(int(centre[0]-hand.size[0]/2), int(centre[1]-hand.size[1]/2)))
    c.save(os.path.join(OUT,out_name)); print(out_name, "hand centre", centre, "angle", angle)
hand_swap("jei-03x-point-variant-base-20261031.png", "Hand_4_Point.png", (157,134), 35, 55, "jei-03x-point-variant-20261031.png")
print("v2 done")
