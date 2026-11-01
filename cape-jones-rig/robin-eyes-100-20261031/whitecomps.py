import sys
from PIL import Image
import numpy as np
from scipy import ndimage
def comps(path, thr=235, minpx=80):
    im=np.array(Image.open(path).convert('RGBA'))
    rgb=im[:,:,:3].astype(int); a=im[:,:,3]
    white=(rgb[:,:,0]>thr)&(rgb[:,:,1]>thr)&(rgb[:,:,2]>thr)&(a>200)
    lab,n=ndimage.label(white)
    ys,xs=np.where(a>10); fb=(int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()))
    out=[]
    for i in range(1,n+1):
        yy,xx=np.where(lab==i)
        if len(yy)>=minpx: out.append((len(yy), int(xx.min()),int(xx.max()),int(yy.min()),int(yy.max())))
    print(path.split('/')[-1], 'figbbox', fb, 'ncomps', len(out))
    for c in sorted(out, reverse=True)[:20]: print('  ', c)
    return fb, out
if __name__=='__main__':
    for p in sys.argv[1:]: comps(p)
