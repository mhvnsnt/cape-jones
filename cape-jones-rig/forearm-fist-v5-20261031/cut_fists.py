from PIL import Image, ImageFilter
import collections
src = Image.open('/home/hatch/workspace/user/files/1000179204_34_scne.jpg').convert('RGB')
W,H = src.size
bg = (243,230,213)
def dist2(p):
    return (p[0]-bg[0])**2+(p[1]-bg[1])**2+(p[2]-bg[2])**2
px = src.load()
def flood_crop(box, name):
    x0,y0,x1,y1 = box
    cw, ch = x1-x0, y1-y0
    crop = src.crop(box)
    cp = crop.load()
    flooded = [[False]*cw for _ in range(ch)]
    dq = collections.deque()
    # seed all border pixels that are bg-like
    for x in range(cw):
        for y in (0, ch-1):
            if dist2(cp[x,y]) < 40**2 and not flooded[y][x]:
                flooded[y][x]=True; dq.append((x,y))
    for y in range(ch):
        for x in (0, cw-1):
            if dist2(cp[x,y]) < 40**2 and not flooded[y][x]:
                flooded[y][x]=True; dq.append((x,y))
    while dq:
        x,y = dq.popleft()
        for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=nx<cw and 0<=ny<ch and not flooded[ny][nx] and dist2(cp[nx,ny]) < 40**2:
                flooded[ny][nx]=True; dq.append((nx,ny))
    mask = Image.new('L',(cw,ch),0)
    mp = mask.load()
    for y in range(ch):
        for x in range(cw):
            if not flooded[y][x]:
                mp[x,y]=255
    # largest component only
    visited=[[False]*cw for _ in range(ch)]
    best=[]
    for y in range(ch):
        for x in range(cw):
            if mp[x,y]==255 and not visited[y][x]:
                comp=[]; dq=collections.deque([(x,y)]); visited[y][x]=True
                while dq:
                    cx,cy=dq.popleft(); comp.append((cx,cy))
                    for nx,ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
                        if 0<=nx<cw and 0<=ny<ch and not visited[ny][nx] and mp[nx,ny]==255:
                            visited[ny][nx]=True; dq.append((nx,ny))
                if len(comp)>len(best): best=comp
    mask2=Image.new('L',(cw,ch),0); mp2=mask2.load()
    for x,y in best: mp2[x,y]=255
    # bbox crop
    xs=[x for x,y in best]; ys=[y for x,y in best]
    bx0,bx1,by0,by1=min(xs),max(xs)+1,min(ys),max(ys)+1
    print(name, 'crop', box, 'bbox', (bx0,by0,bx1,by1), 'size', bx1-bx0, by1-by0, 'px', len(best))
    out_crop=crop.crop((bx0,by0,bx1,by1))
    m_crop=mask2.crop((bx0,by0,bx1,by1))
    # 1px feather on alpha
    alpha=m_crop.filter(ImageFilter.GaussianBlur(0.8))
    out=out_crop.convert('RGBA')
    # desaturate chroma to 15% (near-white, black stays black)
    rp=out.load(); ap=alpha.load()
    for y in range(out.size[1]):
        for x in range(out.size[0]):
            r,g,b,a=rp[x,y]
            lum=int(0.299*r+0.587*g+0.114*b)
            r2=int(lum+(r-lum)*0.15); g2=int(lum+(g-lum)*0.15); b2=int(lum+(b-lum)*0.15)
            rp[x,y]=(r2,g2,b2,ap[x,y])
    out.save(f'/home/hatch/workspace/cape-jones-rig/forearm-fist-v5-20261031/{name}.png')
    return out
left=flood_crop((0,0,254,339),'fist-left-v5-20261031')
right=flood_crop((255,0,509,339),'fist-right-v5-20261031')
print('left',left.size,'right',right.size)
