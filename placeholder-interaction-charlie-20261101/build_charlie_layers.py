"""Render Charlie XFL into separate transparent layer PNGs, same canvas.
Method: schematic XFL vector re-render (render_xfl2.py logic), NOT an Animate render.
Top-level groups = Charlie's own XFL layers. Assembly gaps from the XFL re-render carry over."""
import os, re, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
NS="{http://ns.adobe.com/xfl/2008/}"
SRC=os.path.expanduser('~/workspace/cape-jones-rig/actual-donor-placeholders-20261101/work/charlie_xfl')
OUT=os.path.expanduser('~/workspace/cape-jones-rig/placeholder-interaction-charlie-20261101/charlie_layers')
os.makedirs(OUT, exist_ok=True)
def num(s):
    if s.startswith("#"):
        if "." in s:
            a,b=s[1:].split(".",1); return int(a,16)+(int(b,16)/(16**len(b)) if b else 0)
        return int(s[1:],16)
    return float(s)
def parse_edges(s):
    toks=re.findall(r'[!|\[]|#?[0-9A-Fa-f]+\.[0-9A-Fa-f]+|#?[0-9A-Fa-f]+|-?\d+\.?\d*', s)
    paths=[]; cur=None; curpt=None; i=0
    while i < len(toks):
        t=toks[i]
        if t=="!":
            x,y=num(toks[i+1]),num(toks[i+2]); i+=3; cur=[(x/20,y/20)]; paths.append(cur); curpt=(x/20,y/20)
        elif t=="|":
            x,y=num(toks[i+1]),num(toks[i+2]); i+=3
            if cur is None: cur=[(x/20,y/20)]; paths.append(cur)
            else: cur.append((x/20,y/20))
            curpt=(x/20,y/20)
        elif t=="[":
            cx,cy,ax,ay=num(toks[i+1]),num(toks[i+2]),num(toks[i+3]),num(toks[i+4]); i+=5
            if cur is None or curpt is None: continue
            x0,y0=curpt
            for k in range(1,9):
                tt=k/8; cur.append(((1-tt)**2*x0+2*(1-tt)*tt*cx/20+tt*tt*ax/20, (1-tt)**2*y0+2*(1-tt)*tt*cy/20+tt*tt*ay/20))
            curpt=(ax/20,ay/20)
        else: i+=1
    return paths
def chain(paths):
    segs=[list(p) for p in paths if len(p)>=2]; out=[]
    while segs:
        cur=segs.pop(0); changed=True
        while changed:
            changed=False
            for j,s in enumerate(segs):
                if abs(s[0][0]-cur[-1][0])<2 and abs(s[0][1]-cur[-1][0])<2:
                    cur.extend(s[1:]); segs.pop(j); changed=True; break
                if abs(s[-1][0]-cur[-1][0])<2 and abs(s[-1][1]-cur[-1][0])<2:
                    cur.extend(reversed(s[:-1])); segs.pop(j); changed=True; break
        out.append(cur)
    return out
def load_symbols(d):
    syms={}
    for root,dirs,files in os.walk(os.path.join(d,"LIBRARY")):
        for f in files:
            if f.endswith(".xml"):
                p=os.path.join(root,f); syms[os.path.relpath(p,d)[len("LIBRARY/"):-4]]=ET.fromstring(open(p,'rb').read())
    return syms
def collect(syms,name,tr,out,group=None,depth=0):
    if depth>12 or name not in syms: return
    root=syms[name]; layers=[]
    for layer in root.iter(NS+"DOMLayer"):
        if layer.attrib.get("layerType") in ("mask","folder"): continue
        frames=list(layer.iter(NS+"DOMFrame"))
        if frames: layers.append(frames[0])
    for fr in reversed(layers):
        for el in fr.iter():
            tag=el.tag.split('}')[-1]
            if tag=="DOMSymbolInstance":
                m=el.find(NS+"matrix/"+NS+"Matrix")
                a=float(m.attrib.get("a",1)) if m is not None else 1; b=float(m.attrib.get("b",0)) if m is not None else 0
                c=float(m.attrib.get("c",0)) if m is not None else 0; d=float(m.attrib.get("d",1)) if m is not None else 1
                tx=float(m.attrib.get("tx",0)) if m is not None else 0; ty=float(m.attrib.get("ty",0)) if m is not None else 0
                A,B,C,D,TX,TY=tr; nt=(A*a+C*b, B*a+D*b, A*c+C*d, B*c+D*d, A*tx+C*ty+TX, B*tx+D*ty+TY)
                g=group if group is not None else el.attrib.get("libraryItemName")
                collect(syms, el.attrib.get("libraryItemName"), nt, out, g, depth+1)
            elif tag=="DOMShape":
                if el.attrib.get("isFloating")=="true": continue
                if any((sc.attrib.get("alpha")=="0") for fs in el.iter(NS+"FillStyle") for sc in [fs.find(NS+"SolidColor")] if sc is not None): continue
                fills={}
                for fs in el.iter(NS+"FillStyle"):
                    sc=fs.find(NS+"SolidColor"); fills[fs.attrib.get("index")]=sc.attrib.get("color","#000000") if sc is not None else "#000000"
                groups={}; lines=[]
                for edge in el.iter(NS+"Edge"):
                    paths=parse_edges(edge.attrib.get("edges",""))
                    f1=edge.attrib.get("fillStyle1")
                    if f1 and f1 in fills: groups.setdefault(f1,[]).extend(paths)
                    else: lines.extend(paths)
                sm=el.find(NS+"matrix/"+NS+"Matrix"); tr2=tr
                if sm is not None:
                    sa=float(sm.attrib.get("a",1)); sb=float(sm.attrib.get("b",0)); sc=float(sm.attrib.get("c",0)); sd=float(sm.attrib.get("d",1)); stx=float(sm.attrib.get("tx",0)); sty=float(sm.attrib.get("ty",0))
                    A,B,C,D,TX,TY=tr; tr2=(A*sa+C*sb, B*sa+D*sb, A*sc+C*sd, B*sc+D*sd, A*stx+C*sty+TX, B*stx+D*sty+TY)
                for f1,paths in groups.items():
                    for poly in chain(paths):
                        if len(poly)>=3: out.append((group or "Charlie_direct", fills[f1], poly, tr2, True))
                for path in lines: out.append((group or "Charlie_direct", None, path, tr2, False))
syms=load_symbols(SRC); shapes=[]; collect(syms,"Charlie",(1,0,0,1,0,0),shapes)
pts=[]
for g,col,path,tr,fill in shapes:
    A,B,C,D,TX,TY=tr
    for x,y in path: pts.append((A*x+C*y+TX, B*x+D*y+TY))
minx,miny=min(p[0] for p in pts),min(p[1] for p in pts); maxx,maxy=max(p[0] for p in pts),max(p[1] for p in pts)
print("bounds",minx,maxx,miny,maxy,"shapes",len(shapes))
W=int(maxx-minx)+80; H=int(maxy-miny)+80
groups={}
for s in shapes: groups.setdefault(s[0],[]).append(s)
for g,items in groups.items():
    img=Image.new("RGBA",(W,H),(0,0,0,0)); dr=ImageDraw.Draw(img)
    for _,col,path,tr,fill in items:
        A,B,C,D,TX,TY=tr; poly=[(A*x+C*y+TX-minx+40, B*x+D*y+TY-miny+40) for x,y in path]
        if fill and col: dr.polygon(poly, fill=col)
        dr.line(poly, fill=(0,0,0), width=2)
    fn=re.sub(r'[^A-Za-z0-9]+','_',g)+".png"; img.save(os.path.join(OUT,fn))
    print(g, "->", fn, "bbox", img.getbbox(), "opaque", sum(1 for px in img.getdata() if px[3]>10))
print("canvas",W,H)
