"""Non-destructive arm-joint + arm-weight repair for cape_jones_rigged_w5r_clean.blend.
Diagnosis (diag/arm_weights_rest.png, rest_front_grid2.png): the arm chain is shifted one joint outward.
 rig 'shoulder' (clavicle tail/upperarm head) x=0.243 = the ELBOW crease on the mesh;
 rig 'elbow' x=0.376 = the WRIST; rig 'wrist' x=0.484 = fingertips.
 => clavicle_L carries deltoid+bicep (shoulder->bicep) and barely rotates: the owner's H-shape.
Fix: move deform+FK+IK arm bones to the mesh's anatomical joints, then redistribute each vertex's
existing TOTAL arm weight (clavicle+upperarm+forearm+hand) along the arm axis. Bind/rest shape is
unchanged (weights per vertex still sum the same, rest pose = identity). Saves to a NEW file."""
import bpy, numpy as np, sys
OUT=sys.argv[-1]
rig=bpy.data.objects["CapeJones_Rig"]; body=bpy.data.objects["CapeJones_Body"]
J={"shoulder":0.130,"elbow":0.243,"wrist":0.376,"handtip":0.440}
def zy(x,side):  # interpolate y,z of the old chain at |x|
    pts=[(0.0,-0.01,0.80),(0.243,-0.031,0.745),(0.376,-0.034,0.723),(0.484,-0.045,0.718)]
    xs=[p[0] for p in pts]; return np.interp(x,xs,[p[1] for p in pts]),np.interp(x,xs,[p[2] for p in pts])
def P(x,s):
    y,z=zy(x,s); return (x if s=="L" else -x, y, z)
bpy.context.view_layer.objects.active=rig; bpy.ops.object.mode_set(mode='EDIT'); eb=rig.data.edit_bones
for s in "LR":
    sh,el,wr,ht=P(J["shoulder"],s),P(J["elbow"],s),P(J["wrist"],s),P(J["handtip"],s)
    eb[f"clavicle_{s}"].tail=sh
    for k in ("","_fk","_ik"):
        u=eb[f"upperarm{k}_{s}"]; u.head=sh; u.tail=el
        f=eb[f"forearm{k}_{s}"]; f.head=el; f.tail=wr
        h=eb[f"hand{k}_{s}"]; h.head=wr; h.tail=ht
    eb[f"elbow_pole_{s}"].head=(el[0],0.216,el[2]); eb[f"elbow_pole_{s}"].tail=(el[0],0.266,el[2])
bpy.ops.object.mode_set(mode='OBJECT')
# --- weights
me=body.data; n=len(me.vertices)
co=np.zeros(n*3); me.vertices.foreach_get("co",co); co=co.reshape(-1,3)
def ss(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
stats={}
for s in "LR":
    names=[f"clavicle_{s}",f"upperarm_{s}",f"forearm_{s}",f"hand_{s}"]
    G=[body.vertex_groups[nm] for nm in names]; gi=[g.index for g in G]
    W=np.zeros((n,4))
    for v in me.vertices:
        for g in v.groups:
            if g.group in gi: W[v.index,gi.index(g.group)]=g.weight
    tot=W.sum(1); m=tot>0
    ax=co[:,0]*(1 if s=="L" else -1)
    yz=np.array([zy(abs(a),s) for a in np.clip(ax,0,0.5)]) if False else None
    yc=np.interp(np.clip(ax,0,0.5),[0,0.243,0.376,0.484],[-0.01,-0.031,-0.034,-0.045])
    zc=np.interp(np.clip(ax,0,0.5),[0,0.243,0.376,0.484],[0.80,0.745,0.723,0.718])
    r=np.hypot(co[:,1]-yc,co[:,2]-zc)
    a_up=ss(0.105,0.155,ax)*(1-ss(0.06,0.09,r))   # clavicle->upperarm, only near the arm axis (not torso side)
    a_fo=ss(0.232,0.256,ax); a_ha=ss(0.366,0.386,ax)
    nw=np.stack([1-a_up, a_up*(1-a_fo), a_up*a_fo*(1-a_ha), a_up*a_fo*a_ha],1)
    # verts past the shoulder but far from axis (armpit seam) keep clavicle, already handled by r term
    nw=nw*tot[:,None]
    idx=np.where(m)[0]
    for k,g in enumerate(G):
        g.remove(idx.tolist())
        for val in np.unique(np.round(nw[idx,k],3)):
            if val<=0: continue
            sel=idx[np.round(nw[idx,k],3)==val]; g.add(sel.tolist(),float(val),'REPLACE')
    dom=np.argmax(np.where(m[:,None],nw,-1),1)
    stats[s]={nm:int(((dom==k)&m).sum()) for k,nm in enumerate(names)}
    stats[s]["sum_err_max"]=float(np.abs(np.round(nw[idx],3).sum(1)-tot[idx]).max())
print("V2STATS",stats)
rig.data["cj_arm_fix"]="v2 20261110: arm joints moved to mesh joints (shoulder x0.130, elbow 0.243, wrist 0.376); arm weights redistributed, totals preserved"
bpy.ops.wm.save_as_mainfile(filepath=OUT,compress=True)
print("SAVED",OUT)
