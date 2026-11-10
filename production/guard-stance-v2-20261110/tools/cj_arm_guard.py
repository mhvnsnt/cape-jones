"""Shared guarded loader for Cape Jones w5r rigs (owner pt98u permanent arm fix).
Every Cape show/fight/dance consumer calls ensure_arm_fix() right after the rig blend is open.
- rig already fixed (rig.data['cj_arm_fix']) -> no-op
- rig shows the known w5r defect signature (clavicle tail / upperarm head at x~0.243 = elbow crease)
  -> repair IN MEMORY (bones to mesh joints + arm-weight redistribution, totals preserved); file on disk untouched
- anything else -> REFUSE (unknown arm chain; inspect before animating), unless allow_unknown=True
Sitting-rig lanes are deliberately NOT routed here (owner: don't touch the sitting rig)."""
import bpy, numpy as np
J={"shoulder":0.130,"elbow":0.243,"wrist":0.376,"handtip":0.440}
OLD=[(0.0,-0.01,0.80),(0.243,-0.031,0.745),(0.376,-0.034,0.723),(0.484,-0.045,0.718)]
MARK="v2 20261110: arm joints moved to mesh joints (shoulder x0.130, elbow 0.243, wrist 0.376); arm weights redistributed, totals preserved"
def _zy(x):
    xs=[p[0] for p in OLD]; return np.interp(x,xs,[p[1] for p in OLD]),np.interp(x,xs,[p[2] for p in OLD])
def has_defect_signature(rig):
    b=rig.data.bones
    try: return all(abs(abs(b[f"upperarm_{s}"].head_local.x)-0.243)<0.012 and abs(abs(b[f"forearm_{s}"].head_local.x)-0.376)<0.012 for s in "LR")
    except KeyError: return False
def apply_arm_fix(rig, body):
    def P(x,s):
        y,z=_zy(x); return (x if s=="L" else -x, float(y), float(z))
    prev=bpy.context.view_layer.objects.active; bpy.context.view_layer.objects.active=rig
    mode=rig.mode; bpy.ops.object.mode_set(mode='EDIT'); eb=rig.data.edit_bones
    for s in "LR":
        sh,el,wr,ht=P(J["shoulder"],s),P(J["elbow"],s),P(J["wrist"],s),P(J["handtip"],s)
        eb[f"clavicle_{s}"].tail=sh
        for k in ("","_fk","_ik"):
            if f"upperarm{k}_{s}" not in eb: continue
            u=eb[f"upperarm{k}_{s}"]; u.head=sh; u.tail=el
            f=eb[f"forearm{k}_{s}"]; f.head=el; f.tail=wr
            h=eb[f"hand{k}_{s}"]; h.head=wr; h.tail=ht
        if f"elbow_pole_{s}" in eb: eb[f"elbow_pole_{s}"].head=(el[0],0.216,el[2]); eb[f"elbow_pole_{s}"].tail=(el[0],0.266,el[2])
    bpy.ops.object.mode_set(mode='OBJECT'); bpy.context.view_layer.objects.active=prev
    me=body.data; n=len(me.vertices); co=np.zeros(n*3); me.vertices.foreach_get("co",co); co=co.reshape(-1,3)
    def ss(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
    stats={}
    for s in "LR":
        names=[f"clavicle_{s}",f"upperarm_{s}",f"forearm_{s}",f"hand_{s}"]
        G=[body.vertex_groups[nm] for nm in names]; gi=[g.index for g in G]; W=np.zeros((n,4))
        for v in me.vertices:
            for g in v.groups:
                if g.group in gi: W[v.index,gi.index(g.group)]=g.weight
        tot=W.sum(1); m=tot>0; ax=co[:,0]*(1 if s=="L" else -1); axc=np.clip(ax,0,0.5)
        yc=np.interp(axc,[0,0.243,0.376,0.484],[-0.01,-0.031,-0.034,-0.045]); zc=np.interp(axc,[0,0.243,0.376,0.484],[0.80,0.745,0.723,0.718])
        r=np.hypot(co[:,1]-yc,co[:,2]-zc)
        a_up=ss(0.105,0.155,ax)*(1-ss(0.06,0.09,r)); a_fo=ss(0.232,0.256,ax); a_ha=ss(0.366,0.386,ax)
        nw=np.stack([1-a_up,a_up*(1-a_fo),a_up*a_fo*(1-a_ha),a_up*a_fo*a_ha],1)*tot[:,None]; idx=np.where(m)[0]
        for k,g in enumerate(G):
            g.remove(idx.tolist()); vals=np.round(nw[idx,k],3)
            for val in np.unique(vals):
                if val>0: g.add(idx[vals==val].tolist(),float(val),'REPLACE')
        stats[s]=float(np.abs(np.round(nw[idx],3).sum(1)-tot[idx]).max())
    rig.data["cj_arm_fix"]=MARK
    return stats
def ensure_arm_fix(rig_name="CapeJones_Rig", body_name="CapeJones_Body", allow_unknown=False):
    rig=bpy.data.objects.get(rig_name); body=bpy.data.objects.get(body_name)
    if rig is None or body is None: raise SystemExit(f"cj_arm_guard: {rig_name}/{body_name} not in file")
    if "cj_arm_fix" in rig.data.keys(): print("cj_arm_guard: already fixed"); return "already"
    if has_defect_signature(rig):
        st=apply_arm_fix(rig,body); print("cj_arm_guard: raw w5r arm chain repaired in memory; weight-sum err",st); return "repaired"
    if allow_unknown: print("cj_arm_guard: WARNING unknown arm chain, allowed by caller"); return "unknown-allowed"
    raise SystemExit("cj_arm_guard: REFUSED - unmarked rig without the known w5r signature; inspect arm chain first")
