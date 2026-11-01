"""Chart cycle GIF + movement phrase GIF + DEMO audio-driven timing (placeholder, not Mars dialogue).
Audio demo: synthesised syllable bursts with UNEVEN timing; onsets detected from RMS per frame;
GIF frames follow DETECTED onsets, not a fixed grid. Dialogue-driven Rhubarb pass = POST-EPISODE."""
from PIL import Image, ImageDraw
import numpy as np, os, json, wave, struct, math
RIG='/home/hatch/workspace/cape-jones-rig'; OUT=f'{RIG}/lipsync-production-20261031'
BASE=Image.open(f'{RIG}/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')
TARGET=(231.5,504.5)
import json as js
meas={m['key']:m for m in js.load(open(f'{OUT}/chart-measurements-20261031.json'))}
ORDER=['rest','ee','eh','ah','oh','oo','mbp','fv','l','sz','th','r','w','gk']
def alpha_bbox(im):
    a=np.array(im); ys,xs=np.where(a[:,:,3]>0)
    return (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),int(len(xs)))
def jaw_shift(head, drop):
    drop=int(round(drop))
    if drop==0: return head.copy()
    a=np.array(head); H=a.shape[0]; out=np.zeros_like(a); out[:560]=a[:560]; out[560+drop:]=a[560:H-drop]
    sm=out[560+drop,:,3]>0
    for y in range(560,560+drop):
        row=a[559].copy(); row[~sm]=0; out[y]=row
    return Image.fromarray(out)
def fit_frame(key, w=None, jaw=None):
    m=meas[key]; patch=Image.open(f'{OUT}/mouths/{m["patch"]}').convert('RGBA')
    fw=m['fitted_width'] if w is None else w; jd=m['jaw_drop'] if jaw is None else jaw
    bb=alpha_bbox(patch); pw=bb[2]-bb[0]+1; sc=fw/pw
    rs=patch.resize((max(1,int(round(patch.width*sc))), max(1,int(round(patch.height*sc)))), Image.LANCZOS)
    bb2=alpha_bbox(rs); cx=(bb2[0]+bb2[2])/2; cy=(bb2[1]+bb2[3])/2
    head=jaw_shift(BASE, jd); head.alpha_composite(rs,(int(round(TARGET[0]-cx)), int(round(TARGET[1]+jd/4-cy))))
    return head
def smooth(t): return t*t*(3-2*t)
# ---- 1. chart cycle: 14 keys x 6f @24fps ----
frames=[]; timeline=[]
os.makedirs(f'{OUT}/frames_chart', exist_ok=True)
for ki,key in enumerate(ORDER):
    for f in range(6):
        fr=fit_frame(key); frames.append(fr); timeline.append(dict(frame=len(frames)-1, viseme=key, source='chart-cycle'))
        fr.save(f'{OUT}/frames_chart/chart-f{len(frames)-1:02d}-{key}.png')
frames[0].save(f'{OUT}/chart-cycle-20261031.gif', save_all=True, append_images=frames[1:], duration=1000//24, loop=0)
print('chart cycle', len(frames), 'frames', flush=True)
# ---- 2. movement phrase with smoothstep: OH W FV L SZ TH AH MBP, 6f/key, 3f transitions ----
KEYS=['oh','w','fv','l','sz','th','ah','mbp']
frames2=[]; tl2=[]
os.makedirs(f'{OUT}/frames_phrase', exist_ok=True)
for ki,key in enumerate(KEYS):
    nxt=KEYS[(ki+1)%len(KEYS)]
    for f in range(6):
        if f<3:
            fr=fit_frame(key); w,h,j=meas[key]['fitted_width'],None,meas[key]['jaw_drop']
            tl2.append(dict(frame=len(frames2), viseme=key, phase='hold', jaw=meas[key]['jaw_drop']))
        else:
            t=smooth((f-3)/3); w=meas[key]['fitted_width']+(meas[nxt]['fitted_width']-meas[key]['fitted_width'])*t
            jd=meas[key]['jaw_drop']+(meas[nxt]['jaw_drop']-meas[key]['jaw_drop'])*t
            fr=fit_frame(key, w=w, jaw=jd)
            tl2.append(dict(frame=len(frames2), viseme=f'{key}->{nxt}', phase='transition', jaw=round(jd,2), width=round(w,1)))
        frames2.append(fr); fr.save(f'{OUT}/frames_phrase/phrase-f{len(frames2)-1:02d}.png')
frames2[0].save(f'{OUT}/phrase-movement-20261031.gif', save_all=True, append_images=frames2[1:], duration=1000//24, loop=0)
print('phrase movement', len(frames2), 'frames', flush=True)
# phrase key contact
def contact(frames_list, idxs, labels, path):
    tw,th=238,344; cols=len(idxs)
    sheet=Image.new('RGB',(cols*tw, th+26),'white'); d=ImageDraw.Draw(sheet)
    for i,(fi,lab) in enumerate(zip(idxs,labels)):
        im=frames_list[fi].copy(); im.thumbnail((tw,th))
        bg=Image.new('RGBA',(tw,th),(255,255,255,255)); bg.alpha_composite(im,((tw-im.width)//2,(th-im.height)//2))
        sheet.paste(bg.convert('RGB'),(i*tw,0)); d.text((i*tw+4,th+4),lab,fill=(0,0,0))
    sheet.save(path); print('contact', path, sheet.size, flush=True)
contact(frames, [3,9,15,21,27,33,39,45,51,57,63,69,75,81], ORDER, f'{OUT}/chart-cycle-contact-20261031.png')
contact(frames2, [1,7,13,19,25,31,37,43], KEYS, f'{OUT}/phrase-movement-contact-20261031.png')
# ---- 3. DEMO audio: uneven bursts, RMS detection ----
SR=24000; DUR=2.0; N=int(SR*DUR)
# bursts: (start_s, syllable, consonant_viseme, vowel_viseme) — uneven on purpose
BURSTS=[(0.10,'PAH','mbp','ah'),(0.62,'GO','gk','oh'),(1.05,'SEE','sz','ee'),(1.58,'PAH','mbp','ah')]
sig=np.zeros(N)
for start,syl,cv,vv in BURSTS:
    s0=int(start*SR); dur=int(0.38*SR)
    # consonant noise 0.05s, then vowel tone 220Hz + 440Hz, envelope up/down
    for i in range(dur):
        t=i/SR
        if i<int(0.05*SR): v=np.random.default_rng(7+i).normal(0,0.25)
        else:
            env=min(1.0,(i-0.05*SR)/(0.05*SR))*max(0.0,1.0-(i-0.05*SR)/(0.33*SR))
            v=env*(0.5*math.sin(2*math.pi*220*t)+0.25*math.sin(2*math.pi*440*t))
        sig[s0+i]+=v
sig=np.clip(sig,-0.95,0.95)
with wave.open(f'{OUT}/demo-dialogue-placeholder-20261031.wav','wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes(struct.pack('<'+'h'*N, *(np.round(sig*32767).astype(int))))
# RMS per 24fps frame (1000 samples)
FRAMES_N=48; rms=[]
for fi in range(FRAMES_N):
    seg=sig[fi*1000:(fi+1)*1000]; rms.append(float(np.sqrt(np.mean(seg**2))) if len(seg) else 0.0)
thr=0.08
onsets=[]
for fi in range(1,FRAMES_N):
    if rms[fi]>=thr and rms[fi-1]<thr: onsets.append(fi)
print('RMS onsets detected (frames):', onsets, 'expected starts (frames):', [round(s*24) for s,_,_,_ in BURSTS], flush=True)
# timeline FROM detected onsets: onset frame + next frame = consonant, rest of burst (up to 9 frames or next onset) = vowel, else rest
tl_audio=[]; frames3=[]
for fi in range(FRAMES_N):
    vis='rest'
    for oi,(start,syl,cv,vv) in zip(onsets, BURSTS):
        if fi==oi or fi==oi+1: vis=cv
        elif oi+2<=fi<oi+9: vis=vv
    tl_audio.append(dict(frame=fi, viseme=vis, rms=round(rms[fi],4)))
    fr=fit_frame(vis); frames3.append(fr); fr.save(f'{OUT}/frames_audio_demo/audio-f{fi:02d}-{vis}.png')
frames3[0].save(f'{OUT}/audio-demo-timing-20261031.gif', save_all=True, append_images=frames3[1:], duration=1000//24, loop=0)
print('audio demo', len(frames3), 'frames; onsets', onsets, flush=True)
# RMS plot
W,H=960,300; plot=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(plot)
mx=max(rms) if max(rms)>0 else 1
for fi,v in enumerate(rms):
    x=10+fi*19; h=int(240*v/mx); d.rectangle([x,H-30-h,x+14,H-30], fill=(90,39,114) if v>=thr else (180,180,180))
    d.text((x,H-24), str(fi), fill=(0,0,0))
d.line([(10,H-30-240*thr/mx),(W-10,H-30-240*thr/mx)], fill=(200,0,0))
d.text((10,8),'DEMO audio RMS per frame @24fps (purple = above threshold) — onsets: '+str(onsets), fill=(0,0,0))
plot.save(f'{OUT}/audio-demo-rms-20261031.png'); print('rms plot saved', flush=True)
json.dump(dict(bursts=BURSTS, rms=rms, onsets_detected=onsets, expected_onset_frames=[round(s*24) for s,_,_,_ in BURSTS], timeline=tl_audio, note='DEMO/PLACEHOLDER synthesised bursts, NOT Mars dialogue. Dialogue-driven Rhubarb pass = POST-EPISODE.'), open(f'{OUT}/audio-demo-timeline-20261031.json','w'), indent=1)
json.dump(timeline, open(f'{OUT}/chart-cycle-timeline-20261031.json','w'), indent=1)
json.dump(tl2, open(f'{OUT}/phrase-movement-timeline-20261031.json','w'), indent=1)
print('GIFS+AUDIO DONE')
