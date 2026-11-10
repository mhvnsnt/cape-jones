import os, json, hashlib, re, math
from pathlib import Path
from PIL import Image
import numpy as np

HOME=Path.home(); RIG=HOME/"workspace/cape-jones-rig"
OUT=RIG/"duplicates-organize-20261031"
IMG_EXT={".png",".jpg",".jpeg"}

def collect():
    cats={}
    fly=HOME/"workspace/cape-jones-flying/characters/sheets"
    sheets=[p for p in fly.rglob("*") if p.is_file() and p.suffix.lower() in IMG_EXT]
    cats["sheets"]=sorted(sheets, key=lambda p: str(p.relative_to(fly)))
    grok=list((RIG/"transparent-plates-grok-full-sweep-20261031/plates").rglob("*.png"))
    old=list((RIG/"transparent-plates-sweep-20261031/plates").rglob("*.png"))
    cats["plates"]=sorted(grok+old)
    oldpieces=list((RIG/"sliced-clean-20261031").rglob("*.png"))
    newpieces=list((RIG/"sliced-68-unsliced-20261031/sheets").rglob("*.png"))
    cats["pieces"]=sorted(oldpieces+newpieces)
    return cats

def dhash(im, n=16):
    g=im.convert("L").resize((n+1,n), Image.LANCZOS)
    a=np.asarray(g, dtype=int)
    bits=(a[:,1:]>a[:,:-1]).flatten()
    h=0
    for b in bits: h=(h<<1)|int(b)
    return h
def ahash(im, n=16):
    g=im.convert("L").resize((n,n), Image.LANCZOS)
    a=np.asarray(g, dtype=float)
    bits=(a>a.mean()).flatten()
    h=0
    for b in bits: h=(h<<1)|int(b)
    return h
def hist(im):
    rgb=im.convert("RGB").resize((64,64), Image.LANCZOS)
    a=np.asarray(rgb).reshape(-1,3)
    h=[]
    for c in range(3):
        hh,_=np.histogram(a[:,c], bins=8, range=(0,256))
        h.extend(hh/len(a))
    return np.array(h)
def thumb_gray(im):
    return np.asarray(im.convert("L").resize((32,32), Image.LANCZOS), dtype=float)
def layout(im):
    rgb=im.convert("RGB").resize((4,4), Image.LANCZOS)
    return np.asarray(rgb, dtype=float).flatten()/255.0
def alpha_mask(im):
    if im.mode=="RGBA":
        a=np.asarray(im.split()[3].resize((32,32), Image.LANCZOS), dtype=float)/255.0
        return (a>0.5).astype(float), float((np.asarray(im.split()[3])>10).mean())
    return np.ones((32,32)), 1.0

def norm_name(p):
    s=p.stem.lower()
    s=re.sub(r"[^a-z0-9]+"," ",s)
    s=re.sub(r"\b(20\d{6}|20261031|final|copy|v\d+)\b"," ",s)
    return re.sub(r"\s+"," ",s).strip()

cats=collect()
records=[]
for cat, files in cats.items():
    for p in files:
        try:
            data=p.read_bytes()
            md5=hashlib.md5(data).hexdigest()
            with Image.open(p) as im:
                w,h=im.size; mode=im.mode
                dh=dhash(im); ah=ahash(im); hg=hist(im); tg=thumb_gray(im); lo=layout(im); mask,afrac=alpha_mask(im)
                # dominant colours: quantize resized rgb
                rgb=np.asarray(im.convert("RGB").resize((32,32))).reshape(-1,3)
                # simple dominant: most common quantized colour
                q=(rgb//64)*64
                from collections import Counter
                dom=Counter(map(tuple,q)).most_common(3)
        except Exception as e:
            print("SKIP",p,e); continue
        records.append(dict(cat=cat, path=str(p), rel=str(p.relative_to(HOME)) if str(p).startswith(str(HOME)) else str(p),
            name=p.name, stem=p.stem, norm=norm_name(p), md5=md5, bytes=len(data), w=w, h=h, mode=mode,
            dhash=dh, ahash=ah, alpha_frac=round(afrac,4), aspect=round(w/h,3) if h else 0,
            dom=[[[int(x) for x in c],int(n)] for c,n in dom],
            _hist=hg.tolist(), _thumb=tg.tolist(), _layout=lo.tolist(), _mask=mask.tolist()))
    print(cat, len(files), "->", sum(1 for r in records if r["cat"]==cat), flush=True)

# save features without big arrays for index, keep arrays in separate file
feat=Path(OUT/"features.json")
with open(feat,"w") as f: json.dump(records,f)
print("total records", len(records))

def groups_by(keyfn):
    g={}
    for i,r in enumerate(records):
        g.setdefault(keyfn(r),[]).append(i)
    return {k:v for k,v in g.items() if len(v)>1}

def rep_cluster(indices, simfn, thresh_desc):
    # representative clustering, in order
    clusters=[]  # list of (rep_idx, [members])
    for i in indices:
        placed=False
        for rep,members in clusters:
            if simfn(records[rep], records[i]):
                members.append(i); placed=True; break
        if not placed: clusters.append((i,[i]))
    return [m for _,m in clusters if len(m)>1]

# D1 exact md5 (all)
D1=groups_by(lambda r: r["md5"])
# D2 size+dimensions
D2=groups_by(lambda r: (r["bytes"], r["w"], r["h"]))
# D7 normalized name
D7=groups_by(lambda r: r["norm"]) if True else {}
D7={k:v for k,v in D7.items() if k}
# D8 metadata bucket: dims + aspect bucket + alpha bucket + size bucket (log)
def meta_bucket(r):
    return (r["w"], r["h"], r["aspect"], round(r["alpha_frac"],1), int(math.log10(max(r["bytes"],1))))
D8=groups_by(meta_bucket)

def ham(a,b): return bin(a^b).count("1")
# per-category representative clusters (fast enough, categories separate)
def per_cat(simfn):
    out=[]
    for cat in ["sheets","plates","pieces"]:
        idx=[i for i,r in enumerate(records) if r["cat"]==cat]
        out.extend(rep_cluster(idx, simfn, ""))
    return out

D3=per_cat(lambda a,b: ham(a["dhash"],b["dhash"])<=5)
D4=per_cat(lambda a,b: ham(a["ahash"],b["ahash"])<=10)
def hist_sim(a,b):
    x=np.array(a["_hist"]); y=np.array(b["_hist"])
    return float(x@y/(np.linalg.norm(x)*np.linalg.norm(y)+1e-9))>0.985
D5=per_cat(hist_sim)
def mask_iou(a,b):
    x=np.array(a["_mask"]); y=np.array(b["_mask"])
    inter=(x*y).sum(); union=((x+y)>0).sum()
    return inter/max(union,1)>0.92
D6=per_cat(lambda a,b: a["mode"]=="RGBA" and b["mode"]=="RGBA" and mask_iou(a,b))
def mse_sim(a,b):
    x=np.array(a["_thumb"]); y=np.array(b["_thumb"])
    return float(((x-y)**2).mean())<150
D9=per_cat(mse_sim)
def layout_sim(a,b):
    x=np.array(a["_layout"]); y=np.array(b["_layout"])
    return float(np.sqrt(((x-y)**2).mean()))<0.12
D10=per_cat(layout_sim)

# cross sheets<->plates for D3/D5/D9 (representative, small)
cross_idx=[i for i,r in enumerate(records) if r["cat"] in ("sheets","plates")]
D3x=rep_cluster(cross_idx, lambda a,b: ham(a["dhash"],b["dhash"])<=5)
D5x=rep_cluster(cross_idx, hist_sim)

methods={
 "D1_exact_md5": [v for v in D1.values()],
 "D2_size_dimensions": [v for v in D2.values()],
 "D3_perceptual_dhash_le5": D3,
 "D4_average_hash_le10": D4,
 "D5_colour_histogram_cos_gt0985": D5,
 "D6_alpha_silhouette_iou_gt092": D6,
 "D7_normalized_name": [v for v in D7.values()],
 "D8_metadata_bucket": [v for v in D8.values()],
 "D9_downscaled_pixel_mse_lt150": D9,
 "D10_colour_layout_4x4": D10,
 "D3_cross_sheets_plates": D3x,
 "D5_cross_sheets_plates": D5x,
}
summary={}
for k,v in methods.items():
    members=sum(len(g) for g in v)
    summary[k]=dict(groups=len(v), members=members, extra_copies=members-len(v))
    print(k, summary[k], flush=True)

# Union duplicate groups: union-find over all method groups (per category + cross)
parent=list(range(len(records)))
def find(x):
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
def union(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: parent[rb]=ra
for v in methods.values():
    for g in v:
        for m in g[1:]: union(g[0],m)
ug={}
for i in range(len(records)): ug.setdefault(find(i),[]).append(i)
union_groups=[v for v in ug.values() if len(v)>1]
print("union groups", len(union_groups), "members", sum(len(g) for g in union_groups))

# Organization O1-O5
def canon_name(group):
    # most common group folder, first repo-order file, type guess
    recs=[records[i] for i in group]
    # keep candidate: highest resolution, then largest bytes, then earliest path
    keep=max(range(len(recs)), key=lambda j: (recs[j]["w"]*recs[j]["h"], recs[j]["bytes"]))
    base=recs[keep]
    grp=base["cat"]
    # type guess from dominant? use stem words
    stem=re.sub(r"[^a-z0-9]+","-",base["stem"].lower()).strip("-")[:40]
    return f"CJ-{grp}-{stem}", recs[keep]["path"], [r["path"] for j,r in enumerate(recs) if j!=keep]

organized=[]
for gi,g in enumerate(sorted(union_groups, key=lambda g: -len(g))):
    recs=[records[i] for i in g]
    canon,keep,others=canon_name(g)
    cats_in=sorted(set(r["cat"] for r in recs))
    organized.append(dict(group_id=f"DUP-{gi+1:04d}", size=len(g), categories=cats_in,
        canonical_name=canon, keep_candidate=keep, delete_candidates=others,
        members=[dict(path=r["path"], cat=r["cat"], name=r["name"], w=r["w"], h=r["h"], bytes=r["bytes"], md5=r["md5"][:12]) for r in recs]))

out_data=dict(summary=summary, union_groups=len(union_groups), union_members=sum(len(g) for g in union_groups),
    total_records=len(records), by_cat={c: sum(1 for r in records if r["cat"]==c) for c in ["sheets","plates","pieces"]},
    methods={k: [[records[i]["path"] for i in g] for g in v] for k,v in methods.items()},
    organized=organized)
with open(OUT/"measurements-duplicates-20261031.json","w") as f: json.dump(out_data,f,indent=1)
# public index without method member paths duplication? keep it, it's the index
with open(OUT/"organized/ORGANIZED-INDEX-20261031.json","w") as f: json.dump(organized,f,indent=1)
print("done")
