"""Cape-through-body measure. For sampled frames: fraction of cape verts lying >10% deep inside the per-bone body
ellipsoids (legs/pelvis/torso), for (a) the OLD skin-bound cape (body verts in cape_hi_sel, mask off; = v1/v2 look)
and (b) the v3 cloth-driven hi-res cape. Writes JSON. Gate: v3 median deep-inside fraction <= 0.5% and below old."""
import bpy,numpy as np,json,sys
out=sys.argv[-1]; THR=float(sys.argv[-2]); sc=bpy.context.scene
body=bpy.data.objects["CapeJones_Body"]; hi=bpy.data.objects["CapeJones_CapeHi"]; mk=body.modifiers["HideCapeHi"]
sel=np.zeros(len(body.data.vertices),bool); gi=body.vertex_groups["cape_hi_sel"].index
for v in body.data.vertices:
    for g in v.groups:
        if g.group==gi and g.weight>0.5: sel[v.index]=True
caps=[o for o in bpy.data.objects if o.name.startswith("ColCap_") and any(k in o.name for k in("thigh","shin"))]
def deep(P):
    ins=np.zeros(len(P),bool); per={}
    for o in caps:
        M=np.linalg.inv(np.array(o.matrix_world)); L=(M[:3,:3]@P.T).T+M[:3,3]; r=np.linalg.norm(L,axis=1)<THR; ins|=r; per[o.name]=int(r.sum())
    return float(ins.mean()),per
def ev(o):
    m=o.evaluated_get(bpy.context.evaluated_depsgraph_get()).data; a=np.zeros(len(m.vertices)*3); m.vertices.foreach_get("co",a)
    a=a.reshape(-1,3); W=np.array(o.matrix_world); return (W[:3,:3]@a.T).T+W[:3,3]
rows=[]
for f in [60,90,120,150,180,210,240,270]:
    mk.show_viewport=False; sc.frame_set(f); old=ev(body)[sel]; mk.show_viewport=True
    sc.frame_set(f); new=ev(hi)
    fo,po=deep(old); fn,pn=deep(new); rows.append({"frame":f,"old_skin_cape_deep_frac":fo,"v3_cloth_cape_deep_frac":fn,"old_per":po,"v3_per":pn})
    print("PEN",f,"old %.4f v3 %.4f"%(fo,fn)); sys.stdout.flush()
mo=float(np.median([r["old_skin_cape_deep_frac"] for r in rows])); mn=float(np.median([r["v3_cloth_cape_deep_frac"] for r in rows])); mx=float(max(r["v3_cloth_cape_deep_frac"] for r in rows))
res={"rows":rows,"median_old":mo,"median_v3":mn,"max_v3":mx,"PASS":bool(mn<=0.005 and mn<mo),"note":"ellipsoids = tools/capsules.py proxies shrunk to 0.9; deep-inside only"}
json.dump(res,open(out,"w"),indent=1); print("RESULT",res["PASS"],mo,mn,mx)
