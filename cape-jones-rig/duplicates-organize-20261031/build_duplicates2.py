import json, math, re
from pathlib import Path
import numpy as np
OUT=Path.home()/"workspace/cape-jones-rig/duplicates-organize-20261031"
records=json.load(open(OUT/"features.json"))
print("records", len(records))
# candidate pairs via LSH buckets: dhash/ahash 32-bit chunks, size bucket, norm name, md5
from collections import defaultdict
buckets=defaultdict(list)
for i,r in enumerate(records):
    for name,val,bits in (("d",r["dhash"],256),("a",r["ahash"],256)):
        for c in range(8):
            chunk=(val >> (c*32)) & 0xFFFFFFFF
            buckets[(name,c,chunk)].append(i)
    buckets[("size",r["w"],r["h"])].append(i)
    if r["norm"]: buckets[("norm",r["norm"])].append(i)
    buckets[("md5",r["md5"])].append(i)
cand=set()
for v in buckets.values():
    if 1<len(v)<=60:
        for a in range(len(v)):
            for b in range(a+1,len(v)):
                cand.add((v[a],v[b]))
print("candidate pairs", len(cand))
def ham(a,b): return bin(a^b).count("1")
def hist_sim(a,b):
    x=np.array(a["_hist"]); y=np.array(b["_hist"])
    return float(x@y/(np.linalg.norm(x)*np.linalg.norm(y)+1e-9))>0.985
def mask_iou(a,b):
    x=np.array(a["_mask"]); y=np.array(b["_mask"])
    inter=(x*y).sum(); union=((x+y)>0).sum()
    return inter/max(union,1)>0.92
def mse_sim(a,b):
    x=np.array(a["_thumb"]); y=np.array(b["_thumb"])
    return float(((x-y)**2).mean())<150
def layout_sim(a,b):
    x=np.array(a["_layout"]); y=np.array(b["_layout"])
    return float(np.sqrt(((x-y)**2).mean()))<0.12

# union-find per method
def uf_groups(pairs):
    parent={}
    def find(x):
        parent.setdefault(x,x)
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    for a,b in pairs: union(a,b)
    g=defaultdict(list)
    for x in list(parent): g[find(x)].append(x)
    return [sorted(v) for v in g.values() if len(v)>1]

def groups_by(keyfn):
    g=defaultdict(list)
    for i,r in enumerate(records): g[keyfn(r)].append(i)
    return [v for v in g.values() if len(v)>1]

methods={}
methods["D1_exact_md5"]=groups_by(lambda r: r["md5"])
methods["D2_size_dimensions"]=groups_by(lambda r: (r["bytes"],r["w"],r["h"]))
methods["D7_normalized_name"]=[v for v in groups_by(lambda r: r["norm"]) if v]
methods["D8_metadata_bucket"]=groups_by(lambda r: (r["w"],r["h"],r["aspect"],round(r["alpha_frac"],1),int(math.log10(max(r["bytes"],1)))))
methods["D3_perceptual_dhash_le5"]=uf_groups([(a,b) for a,b in cand if ham(records[a]["dhash"],records[b]["dhash"])<=5])
methods["D4_average_hash_le10"]=uf_groups([(a,b) for a,b in cand if ham(records[a]["ahash"],records[b]["ahash"])<=10])
methods["D5_colour_histogram_cos_gt0985"]=uf_groups([(a,b) for a,b in cand if hist_sim(records[a],records[b])])
methods["D6_alpha_silhouette_iou_gt092"]=uf_groups([(a,b) for a,b in cand if records[a]["mode"]=="RGBA" and records[b]["mode"]=="RGBA" and mask_iou(records[a],records[b])])
methods["D9_downscaled_pixel_mse_lt150"]=uf_groups([(a,b) for a,b in cand if mse_sim(records[a],records[b])])
methods["D10_colour_layout_4x4"]=uf_groups([(a,b) for a,b in cand if layout_sim(records[a],records[b])])

summary={}
for k,v in methods.items():
    m=sum(len(g) for g in v); summary[k]=dict(groups=len(v), members=m, extra_copies=m-len(v)); print(k, summary[k], flush=True)

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
ug=defaultdict(list)
for i in range(len(records)): ug[find(i)].append(i)
union_groups=[v for v in ug.values() if len(v)>1]
print("union", len(union_groups), sum(len(g) for g in union_groups))

def canon_name(group):
    recs=[records[i] for i in group]
    keep=max(range(len(recs)), key=lambda j: (recs[j]["w"]*recs[j]["h"], recs[j]["bytes"]))
    base=recs[keep]
    stem=re.sub(r"[^a-z0-9]+","-",base["stem"].lower()).strip("-")[:40]
    return f"CJ-{base['cat']}-{stem}", base["path"], [r["path"] for j,r in enumerate(recs) if j!=keep]
organized=[]
for gi,g in enumerate(sorted(union_groups, key=lambda g: -len(g))):
    canon,keep,others=canon_name(g)
    recs=[records[i] for i in g]
    organized.append(dict(group_id=f"DUP-{gi+1:04d}", size=len(g), categories=sorted(set(r["cat"] for r in recs)),
        canonical_name=canon, keep_candidate=keep, delete_candidates=others,
        members=[dict(path=r["path"], cat=r["cat"], name=r["name"], w=r["w"], h=r["h"], bytes=r["bytes"], md5=r["md5"][:12]) for r in recs]))
out=dict(summary=summary, union_groups=len(union_groups), union_members=sum(len(g) for g in union_groups),
    total_records=len(records), by_cat={c: sum(1 for r in records if r["cat"]==c) for c in ["sheets","plates","pieces"]},
    candidate_pairs=len(cand),
    methods={k: [[records[i]["path"] for i in g] for g in v] for k,v in methods.items()},
    organized=organized)
json.dump(out, open(OUT/"measurements-duplicates-20261031.json","w"), indent=1)
json.dump(organized, open(OUT/"organized/ORGANIZED-INDEX-20261031.json","w"), indent=1)
print("done")
