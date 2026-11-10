import json, csv
from pathlib import Path
from PIL import Image, ImageDraw
OUT=Path.home()/"workspace/cape-jones-rig/duplicates-organize-20261031"
data=json.load(open(OUT/"measurements-duplicates-20261031.json"))
feat={r["path"]:r for r in json.load(open(OUT/"features.json"))}
org=data["organized"]
def thumb(p, size=(240,240)):
    try:
        im=Image.open(p).convert("RGBA")
        im.thumbnail(size)
        bg=Image.new("RGBA", size, (200,200,200,255))
        bg.alpha_composite(im, ((size[0]-im.width)//2,(size[1]-im.height)//2))
        return bg.convert("RGB")
    except Exception:
        return Image.new("RGB", size, (255,0,0))
def contact(groups, fname, cols=4, cell=260):
    rows=(max(len(g["members"]) for g in groups)+cols-1)//cols if groups else 1
    # simpler: one row per group, up to 4 members, label above
    W=cols*cell; H=len(groups)*(cell+28)
    img=Image.new("RGB",(W,H),(255,255,255)); d=ImageDraw.Draw(img)
    for gi,g in enumerate(groups):
        y=gi*(cell+28)
        d.text((8,y+6), f"{g['group_id']} size={g['size']} cats={','.join(g['categories'])} keep={Path(g['keep_candidate']).name[:40]}", fill=(0,0,0))
        for mi,m in enumerate(g["members"][:cols]):
            img.paste(thumb(m["path"],(cell-8,cell-8)), (mi*cell+4, y+28))
    img.save(OUT/f"contacts/{fname}")
    print(fname, img.size)
# top 8 largest, and first 8 cross-category (2+ cats)
contact(org[:8], "duplicate-groups-largest-20261031.png")
cross=[g for g in org if len(g["categories"])>=2][:8]
contact(cross, "duplicate-groups-cross-category-20261031.png")
pieces=[g for g in org if all(m["cat"]=="pieces" for m in g["members"])][:8]
contact(pieces, "duplicate-groups-pieces-20261031.png")
# faceted CSV O2 + O3 tags
with open(OUT/"organized/FACETED-INDEX-20261031.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["path","cat","duplicate_group","duplicate_status","keep_or_delete_suggestion","canonical_name","w","h","bytes","alpha_frac","aspect","dominant_colours","tag_orientation","tag_type"])
    grp_of={}
    for g in org:
        for m in g["members"]:
            grp_of[m["path"]]=(g["group_id"], "KEEP_CANDIDATE" if m["path"]==g["keep_candidate"] else "DELETE_CANDIDATE", g["canonical_name"])
    for r in feat.values():
        gid,sugg,canon=grp_of.get(r["path"], ("","UNIQUE_KEEP",""))
        orient="portrait" if r["h"]>r["w"] else ("landscape" if r["w"]>r["h"] else "square")
        ttype="full_figure" if r["alpha_frac"]>0.2 else "part_or_sparse"
        w.writerow([r["path"],r["cat"],gid,"DUPLICATE" if gid else "UNIQUE",sugg,canon,r["w"],r["h"],r["bytes"],r["alpha_frac"],r["aspect"],";".join(f"{c}:{n}" for c,n in r["dom"]),orient,ttype])
print("csv done")
