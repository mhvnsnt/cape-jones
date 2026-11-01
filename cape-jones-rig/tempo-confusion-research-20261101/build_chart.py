from PIL import Image, ImageDraw
W,H=1600,900
im=Image.new("RGB",(W,H),(20,20,28)); d=ImageDraw.Draw(im)
d.text((40,20),"BEAT GRID  @24fps  —  107 BPM (picture now)  vs  152 BPM (song)",fill=(255,255,255))
d.text((40,50),"1 beat at 107 = 13.46 frames (0.561s)   |   1 beat at 152 = 9.47 frames (0.395s)   |   1 bar (4 beats): 107 = 53.8f, 152 = 37.9f",fill=(180,220,255))
# two rows, 16 beats each
for row,(bpm,color,label) in enumerate([(107,(255,200,80),"107 BPM"),(152,(80,220,255),"152 BPM")]):
    y=140+row*280
    d.text((40,y-30),f"{label} — beat = {60/bpm*24:.2f} frames",fill=color)
    x0=40; scale=90  # px per beat approx: use frames*? just spacing 90px/beat
    for b in range(17):
        x=x0+b*90
        d.line([(x,y),(x,y+180)],fill=color,width=2 if b%4==0 else 1)
        d.text((x+2,y+185),f"{b}",fill=color)
        if b%4==0: d.text((x+2,y-55),f"bar {b//4}",fill=(200,200,200))
    d.text((40,y+220),"Bar lines = every 4 beats. At 152 the beats come ~30% faster, so a move timed to 1 beat shrinks from ~13-14f to ~9-10f.",fill=(200,200,200))
d.text((40,760),"Rule: hit points lock to TIME (seconds/frames), not to bars. Change tempo -> bars move, hit points do not. That is the whole confusion, in one line.",fill=(255,255,120))
d.text((40,800),"Stretch demo: 152 mix atempo 0.70395 -> 17.94s, exactly the native 107 mix length (17.94s). DEMO only, must be heard first.",fill=(200,200,200))
im.save("/home/hatch/workspace/cape-jones-rig/tempo-confusion-research-20261101/beat-grid-chart-20261101.png")
print("ok")
