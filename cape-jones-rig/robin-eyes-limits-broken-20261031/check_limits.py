"""Gate for robin-eyes-limits-broken. PASS/FAIL per limit, measured from files."""
import json, sys
from PIL import Image
import numpy as np
OUT='/home/hatch/workspace/cape-jones-rig/robin-eyes-limits-broken-20261031'
m=json.load(open(f'{OUT}/measurements-20261031.json'))
checks=[]
def chk(name, ok, detail): checks.append((name, bool(ok), detail)); print(('PASS' if ok else 'FAIL'), name, '-', detail)
# L1: all 10 expression sides differ from neutral
sd=[r['symdiff_vs_neutral_pct'] for r in m['expression']]
chk('L1 expression masks differ from neutral', all(v>0 for v in sd) and len(sd)==10, f'10/10 sides, symdiff {min(sd)}-{max(sd)}% (mean {sum(sd)/len(sd):.1f}%)')
# L1 coverage: each expression proof file exists and contains Cape white
for e in ['11-expres01-angry','12-expres02-determined','13-expres03-angry-point','14-expres04-strain','15-expres05-grit']:
    a=np.array(Image.open(f'{OUT}/expression/{e}-expression.png').convert('RGBA'))
    cw=((a[:,:,0]==248)&(a[:,:,1]==250)&(a[:,:,2]==248)).sum()
    chk(f'L1 proof {e} contains Cape white', cw>0, f'{cw} Cape-white px at 4x')
# L2 profile: mask 110px, proof fills it at 4x
a=np.array(Image.open(f'{OUT}/profile/profile-04-robin-profile-on-cape-profile.png').convert('RGBA'))
# profile mask bbox x74-96 y80-87 at 4x
crop=a[80*4:88*4, 74*4:97*4]
cw=((crop[:,:,0]==248)&(crop[:,:,1]==250)&(crop[:,:,2]==248)).sum()
chk('L2 profile near eye filled 100%', cw==110*16, f'{cw} Cape-white px in profile bbox at 4x, expected {110*16}')
# clean proofs: 0 red
reds=0
for f in ['expression/11-expres01-angry-expression.png','profile/profile-04-robin-profile-on-cape-profile.png','detail/02-night-front-neutral-detail-variant.png']:
    aa=np.array(Image.open(f'{OUT}/{f}').convert('RGBA')); reds+=int(((aa[:,:,0]>200)&(aa[:,:,1]<80)&(aa[:,:,2]<80)).sum())
chk('Clean proofs 0 red pixels', reds==0, f'{reds} red px across 3 sampled clean proofs')
# L3 detail: night gradient stronger than day control
n=m['detail_night']; d=m['detail_day_control']
chk('L3 night detail gradient preserved', n['left']['tone_std']>d['left']['tone_std'] and n['left']['pixels_darker_than_flat']>0 and d['left']['pixels_darker_than_flat']==0,
    f"night L std {n['left']['tone_std']} darker {n['left']['pixels_darker_than_flat']}px vs day L std {d['left']['tone_std']} darker 0px")
print('GATE', 'PASS' if all(c[1] for c in checks) else 'FAIL', f"{sum(c[1] for c in checks)}/{len(checks)}")
sys.exit(0 if all(c[1] for c in checks) else 1)
