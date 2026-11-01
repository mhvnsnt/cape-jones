"""Workstream A production sweep 2026-10-31.
MBP-clean: mouth-only component from 09_RBN01_CAMS_DCTTAS, NOT the old
patch (old patch included a jaw-diagonal fragment at the right edge, which
read as a second slanted segment). Component analysis in box
(180,680,321,711): 3 dark components; jaw L 122px touches edge, jaw R
109px touches edge, MOUTH 71px x213-246 y690-694 touches NO edge,
1 component = continuous. That component alone, verbatim pixels, is the
new patch. Jaw fragments are EXCLUDED, documented, not redrawn.
Placement: pahgo target (231.5,504.5), alpha-bbox centre anchor,
alpha width normalised to 178px (old fitted MBP alpha width) for every
viseme, so mouths do not jump. Scale for MBP = 178/34 = 5.24x upscale
of a simple stroke - disclosed as resolution caveat, not hidden.
Phrase: 'PAH GO, SEE PAH' fixed 6f/viseme @24fps, NOT audio-driven.
GAP slots (OH, SZ) = clean head, no patch, no duplication.
"""
from PIL import Image, ImageDraw
import numpy as np, json, os
from scipy import ndimage
RIG='/home/hatch/workspace/cape-jones-rig'
OUT=f'{RIG}/eyes-mouths-production-20261031'
RENDER=f'{RIG}/robin-eyes-100-20261031/render/09_RBN01_CAMS_DCTTAS.png'
BASE=Image.open(f'{RIG}/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')
TARGET=(231.5,504.5); ALPHA_W=178.0

# --- MBP mouth-only extraction ---
src=Image.open(RENDER).convert('RGBA')
box=(180,680,321,711)
a=np.array(src.crop(box))
dark=(a[:,:,3]>100)&(a[:,:,0]<100)&(a[:,:,1]<100)&(a[:,:,2]<100)
lab,n=ndimage.label(dark)
mouth=None
for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    if xs.min()>0 and xs.max()<a.shape[1]-1 and ys.min()>0 and ys.max()<a.shape[0]-1:
        # interior component = mouth (jaw pieces touch edges)
        mouth=(i,xs,ys)
assert mouth, 'no interior component'
i,xs,ys=mouth
mx0,my0=xs.min()+box[0], ys.min()+box[1]
mx1,my1=xs.max()+box[0], ys.max()+box[1]
patch_arr=np.zeros((my1-my0+1, mx1-mx0+1, 4), dtype=np.uint8)
full=np.array(src.crop((mx0,my0,mx1+1,my1+1)))
mask=(lab[ys.min():ys.max()+1, xs.min():xs.max()+1]==i)
patch_arr[mask]=full[mask]
patch=Image.fromarray(patch_arr)
patch.save(f'{OUT}/mbp-clean-front-09_patch.png')
print(f"MBP-clean: component px={int(mask.sum())} bbox_orig=({mx0},{my0},{mx1},{my1}) size={patch.size} components=1")

def alpha_bbox(im):
    a=np.array(im); ys,xs=np.where(a[:,:,3]>0)
    if len(xs)==0: return None
    return (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),int(len(xs)))

def place(patch, label):
    bb=alpha_bbox(patch)
    w=bb[2]-bb[0]+1
    sc=ALPHA_W/w
    nw=max(1,int(round(patch.width*sc))); nh=max(1,int(round(patch.height*sc)))
    rs=patch.resize((nw,nh), Image.LANCZOS)
    bb2=alpha_bbox(rs)
    cx=(bb2[0]+bb2[2])/2; cy=(bb2[1]+bb2[3])/2
    head=BASE.copy()
    head.alpha_composite(rs,(int(round(TARGET[0]-cx)),int(round(TARGET[1]-cy))))
    return head, dict(label=label, scale=round(sc,4), resized=[nw,nh],
                      alpha_bbox=bb2, alpha_px=bb2[4], target=list(TARGET))

PATCHES={
 'MBP': (patch, 'mbp-clean-front-09'),
 'AH': (Image.open(f'{RIG}/pahgo-mouth-fix-20261031/mouths-tight/ah-front-03_tight_patch.png'), 'ah-front-03 open smile, NOT shout'),
 'GK': (Image.open(f'{RIG}/pahgo-mouth-fix-20261031/mouths-tight/gk-front-05_tight_patch.png'), 'gk-front-05 teeth band'),
 'EE': (Image.open(f'{RIG}/superhero-mouths-20261031/mouths/04_smile-ee_patch.png'), 'ee-front-04 smile, small upper mark defect carried'),
}
fitted={}; meas=[]
for k,(p,lab) in PATCHES.items():
    h,m=place(p,lab); fitted[k]=h; meas.append(m)
    h.save(f'{OUT}/fitted/{k.lower()}-on-cape-head.png')
    print(k, m)

# old fragmented MBP for comparison (pahgo tight patch, jaw fragment included)
old=Image.open(f'{RIG}/pahgo-mouth-fix-20261031/mouths-tight/mbp-front-09_tight_patch.png')
oldh,oldm=place(old,'OLD mbp-front-09 (jaw fragment included)')
oldh.save(f'{OUT}/fitted/mbp-OLD-fragmented-on-cape-head.png')
print('OLD', oldm)

# --- longer phrase, fixed timing ---
SLOTS=[('MBP','P'),('AH','AH'),('GK','G'),('OH','OH - GAP'),('SZ','S - GAP'),
       ('EE','EE'),('MBP','P'),('AH','AH')]
frames=[]; timeline=[]
for slot_idx,(vis,phon) in enumerate(SLOTS):
    for f in range(6):
        if vis in fitted: head=fitted[vis].copy()
        else: head=BASE.copy()
        frames.append(head)
        timeline.append(dict(frame=len(frames)-1, slot=slot_idx, viseme=vis,
                             phoneme=phon, gap=(vis not in fitted)))
for idx,fr in enumerate(frames):
    fr.save(f'{OUT}/frames/phrase-f{idx:02d}.png')
frames[0].save(f'{OUT}/phrase-pah-go-see-pah-20261031.gif', save_all=True,
               append_images=frames[1:], duration=1000//24, loop=0)
print('phrase frames', len(frames), 'duration s', len(frames)/24)

# --- contacts ---
def contact(imgs, labels, path, thumb=(476,688), scale=0.5):
    tw,th=int(thumb[0]*scale),int(thumb[1]*scale)
    cols=4; rows=(len(imgs)+cols-1)//cols
    sheet=Image.new('RGB',(cols*tw, rows*(th+24)),'white'); d=ImageDraw.Draw(sheet)
    for i,(im,lab) in enumerate(zip(imgs,labels)):
        t=im.resize((tw,th), Image.LANCZOS)
        x=(i%cols)*tw; y=(i//cols)*(th+24)
        sheet.paste(t.convert('RGB'),(x,y)); d.text((x+4,y+th+4),lab,fill='black')
    sheet.save(path); print('contact',path,sheet.size)

# mouth-zone zoom contact: crop mouth zone from fitted heads, 3x
def zone(im):
    return im.crop((110,400,393,565)).resize((283*3,165*3), Image.NEAREST)
contact([zone(oldh), zone(fitted['MBP']), zone(fitted['AH']), zone(fitted['GK'])],
        ['OLD MBP (jaw frag = 2nd seg)','NEW MBP-clean (1 comp)','AH-front 03 (smile, no teeth)','GK-front 05 (teeth)'],
        f'{OUT}/mbp-old-vs-new-contact-20261031.png', thumb=(849,495), scale=0.5)
# phrase contact: key frame per slot (frame 2 of each 6-frame block)
keys=[frames[s*6+2] for s in range(len(SLOTS))]
contact(keys, [f"{s}: {v} {p}" for s,(v,p) in enumerate(SLOTS)],
        f'{OUT}/phrase-contact-20261031.png')
# phrase mouth-zone contact
contact([zone(f) for f in keys], [f"{s}: {v} {p}" for s,(v,p) in enumerate(SLOTS)],
        f'{OUT}/phrase-mouthzone-contact-20261031.png', thumb=(849,495), scale=0.45)

# archive re-count
tt=json.load(open(f'{RIG}/robin-eyes-100-20261031/tt-entries.json'))
def cnt(k): return sum(1 for e in tt if k in e['name'].lower())
counts=dict(total=len(tt), robin_name=cnt('robin'), batman=cnt('batman'),
            superman=cnt('superman'), cyborg=cnt('cyborg'), starfire=cnt('starfire'),
            raven=cnt('raven'), beast=cnt('beast'), slade=cnt('slade'))
print(counts)
json.dump(dict(mbp_patch=dict(px=int(mask.sum()), bbox=[int(mx0),int(my0),int(mx1),int(my1)],
                              size=list(patch.size), components=1),
               fitted=meas, old_mbp=oldm, phrase_timeline=timeline,
               phrase=dict(slots=SLOTS, frames=len(frames), fps=24,
                           pulled_slots=6, gap_slots=2),
               archive_counts=counts,
               audio_driven=False, rhubarb_available=False),
          open(f'{OUT}/measurements-20261031.json','w'), indent=1)
print('DONE')
