"""Cape Jones (own rig) + Charlie (own separate layer rig) interaction, 4.0s, 96f @24fps.
Charlie layers are schematic XFL re-renders, gaps carried over, NOT Animate renders.
Cape Jones is his own rig-apose v7c clean transparent, whole-plane moves only in this test.
No dialogue, no donor audio. Synthesized SFX only (footsteps + wave blips)."""
import os, math, wave, struct
from PIL import Image, ImageDraw, ImageFont
BASE=os.path.expanduser('~/workspace/cape-jones-rig')
OUT=os.path.join(BASE,'placeholder-interaction-charlie-20261101')
FR=os.path.join(OUT,'frames'); os.makedirs(FR, exist_ok=True)
W,H=1920,1080; GROUND=950; FPS=24; N=96
# --- load Charlie layers, trim to common bbox, scale ---
LDIR=os.path.join(OUT,'charlie_layers')
order=['Charlie_Back_Arm.png','Charlie_Legs.png','Charlie_Back_Hoodie.png','Charlie_Head.png','Charlie_Body.png','Charlie_direct.png','Charlie_Front_Arm.png']
layers={}
for fn in order:
    im=Image.open(os.path.join(LDIR,fn)).convert('RGBA'); layers[fn]=im
    print(fn, im.size, im.getbbox())
# common canvas 984x1735; charlie full height ~1656 (y40..1696). Scale to 640 tall.
CH_SCALE=640/1656
def scale_layer(im):
    nw=int(im.width*CH_SCALE); nh=int(im.height*CH_SCALE)
    return im.resize((nw,nh), Image.LANCZOS)
scaled={k:scale_layer(v) for k,v in layers.items()}
# pivots in scaled full-canvas coords (canvas scaled: 984*CH_SCALE x 1735*CH_SCALE)
CW=int(984*CH_SCALE); CH=int(1735*CH_SCALE)
def pivot(fn, fx, fy):
    # fx,fy = fraction of that layer's bbox centre-ish; use bbox
    bb=layers[fn].getbbox()
    return (int((bb[0]+fx*(bb[2]-bb[0]))*CH_SCALE), int((bb[1]+fy*(bb[3]-bb[1]))*CH_SCALE))
# head pivot: neck area ~ bottom centre of head bbox; front arm pivot: top of arm bbox
HEAD_PIV=pivot('Charlie_Head.png',0.5,0.95)
ARM_PIV=pivot('Charlie_Front_Arm.png',0.5,0.05)
print('charlie canvas',CW,CH,'head piv',HEAD_PIV,'arm piv',ARM_PIV)
# --- Cape Jones ---
cj=Image.open(os.path.join(BASE,'rig-apose-v7c-clean-transparent.png')).convert('RGBA')
cj_bb=cj.getbbox(); cj_h=cj_bb[3]-cj_bb[1]
CJ_SCALE=720/cj_h
cj_s=cj.resize((int(cj.width*CJ_SCALE),int(cj.height*CJ_SCALE)), Image.LANCZOS)
cj_bb2=cj_s.getbbox()
print('cj scaled',cj_s.size,'bbox',cj_bb2)
def lerp(a,b,t): return a+(b-a)*t
def ease(t): return t*t*(3-2*t)
def frame_params(f):
    # returns cj_x (left of CJ image), cj_bob, cj_rot, ch_head_rot, ch_arm_rot, ch_bob
    if f<24:  # walk in
        t=ease(f/23); x=lerp(-400, 430, t); bob=abs(math.sin(f*0.9))*6; return x,bob,0, 0,0, abs(math.sin(f*0.5))*3
    if f<48:  # stop + CJ waves (bob/lean), Charlie head turns, arm starts up
        t=(f-24)/23; return 430, math.sin(t*math.pi)*4, math.sin(t*math.pi)*2, -6*ease(t), -35*ease(t), 3
    if f<72:  # Charlie reacts: head nod, arm wave, body bounce; CJ nods
        t=(f-48)/23; wave=math.sin(t*math.pi*2)*20
        return 430, 3+math.sin(t*math.pi*2)*3, 2*math.sin(t*math.pi*2), -6+5*math.sin(t*math.pi*2), -25+wave, 4+abs(math.sin(t*math.pi*2))*5
    # settle
    t=(f-72)/23; return 430, 2*(1-t), 0, -6*(1-t), -25*(1-t), 3*(1-t)
def compose(f):
    cj_x,cj_bob,cj_rot,ch_head,ch_arm,ch_bob=frame_params(f)
    # background: simple test stage, labelled as such (not a painted BG)
    img=Image.new('RGB',(W,H),(216,216,210))
    dr=ImageDraw.Draw(img)
    for y in range(H):
        g=int(216- (y/H)*18); dr.line([(0,y),(W,y)], fill=(g,g,g-6))
    dr.rectangle([0,GROUND,W,H], fill=(150,140,125))
    dr.line([(0,GROUND),(W,GROUND)], fill=(60,50,40), width=3)
    # Charlie at right: centre x ~1380. Charlie canvas scaled, feet at bottom of canvas (y1696*scale ~655)
    ch_left=1380-CW//2; ch_top=GROUND-CH+ch_bob  # canvas bottom ~ feet? canvas bottom is 1735*scale=670, feet at 1696*scale=655, so bottom is ~15 below feet; acceptable, feet near ground
    ch_top=int(ch_top)+15  # feet (canvas y1696) land on ground line, not 15px above it
    # paste layers back-to-front, with head/arm rotations about pivots on full-canvas images
    for fn in order:
        lay=scaled[fn]
        if fn=='Charlie_Head.png' and ch_head!=0:
            lay=lay.rotate(-ch_head, resample=Image.BICUBIC, center=(HEAD_PIV[0],HEAD_PIV[1]))
        if fn=='Charlie_Front_Arm.png' and ch_arm!=0:
            lay=lay.rotate(-ch_arm, resample=Image.BICUBIC, center=(ARM_PIV[0],ARM_PIV[1]))
        img.paste(lay,(ch_left,ch_top),lay)
    # Cape Jones: rotate whole plane slightly about feet centre, then paste
    cj_img=cj_s
    if cj_rot!=0:
        cj_img=cj_s.rotate(-cj_rot, resample=Image.BICUBIC, center=(cj_s.width//2, int(cj_bb2[3])))
    cj_top=int(GROUND-cj_s.height+ (cj_s.height-cj_bb2[3]) + cj_bob)  # align bbox bottom to ground: top = ground - (bbox bottom offset)
    # bbox bottom offset: image height - (height - bb bottom)?? simpler: paste so that bbox bottom lands on ground+bob: top = GROUND - cj_bb2[3] + cj_bob
    cj_top=int(GROUND - cj_bb2[3] + cj_bob)
    img.paste(cj_img,(int(cj_x),cj_top),cj_img)
    # labels
    dr=ImageDraw.Draw(img)
    dr.rectangle([0,0,W,36], fill=(0,0,0))
    dr.text((12,8), "TEST ONLY - CHARLIE = ACTUAL DONOR CHARACTER PLACEHOLDER - DO NOT SHIP AS-IS - RESKIN PENDING", fill=(255,220,80))
    dr.text((12,H-30), "Cape Jones (own rig, left) + Charlie (own separate XFL layer rig, right) - no dialogue, no donor audio", fill=(40,40,40))
    return img
for f in range(N):
    compose(f).save(os.path.join(FR,f'frame_{f+1:03d}.png'))
print('frames done',N)
# contact sheet: f1, f24, f36, f60, f72, f96
sel=[1,24,36,60,72,96]
sheet=Image.new('RGB',(1920,1080),(20,20,20)); dr=ImageDraw.Draw(sheet)
for i,fn in enumerate(sel):
    im=Image.open(os.path.join(FR,f'frame_{fn:03d}.png')).resize((640,360))
    x=(i%3)*640; y=(i//3)*540
    sheet.paste(im,(x,y)); dr.text((x+10,y+10), f'frame {fn}', fill=(255,255,0))
sheet.save(os.path.join(OUT,'contact-sheet-charlie-interaction-20261101.png'))
print('contact done')
# SFX wav: footsteps during walk-in (f0-23), soft blips at wave (f24, f48), settle blip (f72). 4s, 22050Hz
sr=22050; dur=4.0; data=[0]*int(sr*dur)
def tone(t0,t1,freq,amp=0.25):
    for i in range(int(t0*sr), int(t1*sr)):
        if i < len(data): data[i]+=int(amp*32767*math.sin(2*math.pi*freq*(i/sr-t0))*(1-(i/sr-t0)/(t1-t0)))
for k in range(6): tone(0.1+k*0.16, 0.1+k*0.16+0.08, 90, 0.30)  # footsteps
tone(1.0,1.3,660,0.12); tone(1.3,1.6,880,0.12)  # wave blips
tone(2.0,2.4,520,0.10); tone(3.0,3.3,440,0.10)
with wave.open(os.path.join(OUT,'interaction-sfx-20261101.wav'),'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(b''.join(struct.pack('<h', max(-32767,min(32767,v))) for v in data))
print('sfx done')
