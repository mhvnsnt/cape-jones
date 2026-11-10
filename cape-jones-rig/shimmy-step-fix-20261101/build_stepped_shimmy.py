"""Stepped shimmy, Mars 2026-11-01 00:42 CDT.
Old successor-shimmy: legs constant, only dx sway -30/0/+30, feet never lift.
New: same SHIM arms/head, but legs step in alternating pick-up/put-down pattern.
Foot1 = Leg_Front = our left. Foot2 = Leg_Back = our right.
Lift = knee bend only (whole lower piece rotates around the knee ball, ankle
intact, no foot cut/paste). Planted foot keeps base SHIM leg angles, so its
toe direction still matches its knee direction (knee-feet rule, per frame).
Lifted foot is NOT planted, so its toe is free to point down/back in the air.
"""
import sys, os, json, csv, subprocess
sys.path.insert(0, '/home/hatch/workspace/cape-jones-rig/rig-chains-20261031')
import build_chains as bc
from PIL import Image, ImageDraw

OUT = '/home/hatch/workspace/cape-jones-rig/shimmy-step-fix-20261101'
SHIM_ARMS = ((-130,130),(-60,60))
BASE_LEGS = ((-20,35),(30,-20))   # (leg_upper L,R), (leg_lower L,R)
LIFT_L = ((-20,35),(90,-20))      # Foot1 up: L lower 30 -> 90
LIFT_R = ((-20,35),(30,-70))      # Foot2 up: R lower -20 -> -70
def cfg(legs):
    return bc.C(SHIM_ARMS[0], SHIM_ARMS[1], legs[0], legs[1])
def K(name, legs, dx, hold, foot1, foot2):
    k = bc.K(name, cfg(legs), 10, (), 0, dx, hold, 'stepped shimmy')
    k['foot1']=foot1; k['foot2']=foot2
    return k

KEYS = [
    bc.APOSE,
    K('shimmy centre both down', BASE_LEGS, 0, 5, 'DOWN','DOWN'),
    K('step LEFT: Foot1 UP, Foot2 DOWN', LIFT_L, -15, 4, 'UP','DOWN'),
    K('step LEFT: Foot1 DOWN (stepped left), Foot2 DOWN', BASE_LEGS, -30, 4, 'DOWN','DOWN'),
    K('close LEFT: Foot2 UP, Foot1 DOWN', LIFT_R, -15, 4, 'DOWN','UP'),
    K('shimmy centre both down', BASE_LEGS, 0, 5, 'DOWN','DOWN'),
    K('step RIGHT: Foot2 UP, Foot1 DOWN', LIFT_R, 15, 4, 'DOWN','UP'),
    K('step RIGHT: Foot2 DOWN (stepped right), Foot1 DOWN', BASE_LEGS, 30, 4, 'DOWN','DOWN'),
    K('close RIGHT: Foot1 UP, Foot2 DOWN', LIFT_L, 15, 4, 'UP','DOWN'),
    K('shimmy centre both down', BASE_LEGS, 0, 5, 'DOWN','DOWN'),
]
frames, meta, masters = bc.build('shimmy-stepped', KEYS, n_inb=5, label='GROUNDED')
# meta does not carry foot states; rebuild key-frame map from holds/transitions is
# unreliable, so record the KEY list separately and gate on video frames below.
# Save in OUR folder, never touching rig-chains-20261031
sub = os.path.join(OUT,'frames'); os.makedirs(sub, exist_ok=True)
for i,f in enumerate(frames):
    f.save(os.path.join(sub, f'shimmy-stepped-{i:03d}.jpg'), quality=92)
small=[f.resize((550,375)) for f in frames]
small[0].save(os.path.join(OUT,'shimmy-stepped-20261101.gif'), save_all=True, append_images=small[1:], duration=42, loop=0)
with open(os.path.join(OUT,'frames.txt'),'w') as fh:
    for i in range(len(frames)): fh.write(f"file '{sub}/shimmy-stepped-{i:03d}.jpg'\n")
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-r','24','-i',
    os.path.join(OUT,'frames.txt'),'-vf','scale=1100:750','-c:v','libx264','-pix_fmt','yuv420p',
    os.path.join(OUT,'shimmy-stepped-20261101.mp4')], check=True)
with open(os.path.join(OUT,'shimmy-stepped-xsheet-20261101.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh, fieldnames=list(meta[0].keys())); w.writeheader(); w.writerows(meta)
# Contact: 10 tiles across the cycle, ground line at 652/750 scaled
idx=sorted(set([int(i*(len(frames)-1)/9) for i in range(10)]))
sheet=Image.new('RGB',(1100,470),(128,128,128)); d=ImageDraw.Draw(sheet)
labels=['centre','L UP','L DOWN left','R UP','centre','R UP','R DOWN right','L UP','centre','return']
for k,ix in enumerate(idx):
    tile=frames[ix].resize((220,150)); x,y=(k%5)*220,(k//5)*235
    sheet.paste(tile,(x,y)); d.line([(x,y+int(652*150/750)),(x+220,y+int(652*150/750))],fill=(255,0,0),width=2)
    d.text((x+4,y+152),f'f{ix:03d} {labels[k]}',fill=(255,255,255))
    d.text((x+4,y+168),meta[ix]['kind'][:28],fill=(255,255,0))
sheet.save(os.path.join(OUT,'shimmy-stepped-contact-20261101.png'))
# Step-pattern chart: Foot1 / Foot2 UP (yellow) vs DOWN (green) across the 10 keys
chart=Image.new('RGB',(1100,360),(255,255,255)); d=ImageDraw.Draw(chart)
d.text((10,10),'STEPPED SHIMMY — foot pattern (keys, in order)',fill=(0,0,0))
d.text((10,32),'Foot1 = Leg_Front = our left.  Foot2 = Leg_Back = our right.  GREEN = DOWN (planted)  YELLOW = UP (lifted)',fill=(0,0,0))
keylabels=['centre','L UP','L DOWN\nleft','R UP','centre','R UP','R DOWN\nright','L UP','centre']
states=[('DOWN','DOWN'),('UP','DOWN'),('DOWN','DOWN'),('DOWN','UP'),('DOWN','DOWN'),('DOWN','UP'),('DOWN','DOWN'),('UP','DOWN'),('DOWN','DOWN')]
for row,foot in enumerate(['Foot1','Foot2']):
    y=80+row*90; d.text((10,y+20),foot,fill=(0,0,0))
    for j,(s1,s2) in enumerate(states):
        s=s1 if row==0 else s2; x=90+j*110
        d.rectangle([x,y,x+100,y+50],fill=(0,180,0) if s=='DOWN' else (255,220,0),outline=(0,0,0))
        d.text((x+25,y+18),s,fill=(0,0,0))
        d.text((x+5,y+55),keylabels[j].split('\n')[0],fill=(0,0,0))
d.text((10,280),'Rule: NEVER both UP at once. At every key at least one foot is DOWN, planted, weight-bearing.',fill=(0,0,0))
d.text((10,302),'This is a simple pick-up / put-down shimmy, NOT a full walk cycle. It is the foundation for the walk cycle later.',fill=(0,0,0))
chart.save(os.path.join(OUT,'shimmy-step-pattern-chart-20261101.png'))
print('frames',len(frames),'seconds',round(len(frames)/24,2))
print('keys',[(k['name'],k.get('foot1'),k.get('foot2'),k['dx']) for k in KEYS])
json.dump({'frames':len(frames),'fps':24,'seconds':round(len(frames)/24,2),
 'keys':[{'name':k['name'],'foot1':k.get('foot1'),'foot2':k.get('foot2'),'dx':k['dx']} for k in KEYS]},
 open(os.path.join(OUT,'measurements-20261101.json'),'w'),indent=1)
