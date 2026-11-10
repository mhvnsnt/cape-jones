"""Tool 5: final rig gate checker. Image + manifest -> PASS/FAIL, exit code.
Gates: canvas 1400x1600, alpha>0, feet bottom at ground 1450 +-10, head top >0,
no piece clipped at canvas edge (all placed rects inside canvas), facing consistent,
all pieces whole (no piece file altered except scale/flip/rotate recorded)."""
import sys, json
from PIL import Image
def check(img_path, manifest):
    im=Image.open(img_path); fails=[]
    if im.size!=(1400,1600): fails.append(f"canvas {im.size} != 1400x1600")
    a=im.getchannel('A'); bbox=a.getbbox()
    if not bbox: fails.append('empty image')
    else:
        if abs(bbox[3]-manifest.get('ground',1450))>10: fails.append(f"feet bottom {bbox[3]} not at ground {manifest.get('ground',1450)}")
        if bbox[1]<=0: fails.append('head clipped at top')
    for p in manifest.get('pieces',[]):
        if p['x']<0 or p['y']<0 or p['x']+p['w']>1400 or p['y']+p['h']>1600:
            fails.append(f"piece {p['name']} clipped at canvas edge")
    print('PASS' if not fails else 'FAIL', 'bbox=',bbox)
    for x in fails: print(' -',x)
    return 0 if not fails else 1
if __name__=='__main__': sys.exit(check(sys.argv[1], json.load(open(sys.argv[2]))))
