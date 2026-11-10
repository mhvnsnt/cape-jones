"""Guard-arm gate. Usage: blender -b RIG.blend --python test_guard_arms.py -- STANCE.glb OUT.json
Measures, on sampled guard frames, the UPPER-ARM direction (shoulder->elbow) in CHEST coordinates for
 (a) source skeleton, (b) target bones, (c) the actual EVALUATED Cape body mesh (landmark rings picked on the
 rest mesh from its anatomy, independent of where the rig puts its joints). Exits 1 on failure."""
import bpy, sys, json, os, numpy as np
os.environ["CJ_ALLOW_RAW_RIG"]="1"  # the gate must be able to measure (and fail) the raw rig
from mathutils import Vector
sys.path.insert(0,__import__("os").environ.get("CJ_TOOLS","/workspace/cj3d/v2")); import cj_retarget as R
glb,out=sys.argv[-2],sys.argv[-1]
tgt=bpy.data.objects["CapeJones_Rig"]; body=bpy.data.objects["CapeJones_Body"]
src=R.import_src(glb); R.prep_target(tgt)
f0,f1=src.animation_data.action.frame_range; SF=[int(f0)+k for k in range(0,int(f1-f0),10)]
R.bake(tgt,src,SF,list(range(1,len(SF)+1)))
me=body.data; n=len(me.vertices); co=np.zeros(n*3); me.vertices.foreach_get("co",co); co=co.reshape(-1,3)
def ring(s,x0,x1,rmax):
    ax=co[:,0]*(1 if s=="L" else -1); yc=np.interp(ax,[0,.243,.376],[-.01,-.031,-.034]); zc=np.interp(ax,[0,.243,.376],[.80,.745,.723])
    return np.where((ax>x0)&(ax<x1)&(np.hypot(co[:,1]-yc,co[:,2]-zc)<rmax))[0]
RING={s:(ring(s,0.122,0.140,0.05),ring(s,0.236,0.250,0.04)) for s in "LR"}
tw=tgt.matrix_world; sw=src.matrix_world
def chestR(arm,bone,w):
    pb=arm.pose.bones[bone]; return ((w@pb.matrix).to_3x3()@(w@pb.bone.matrix_local).to_3x3().inverted())
ang=lambda a,b: float(np.degrees(np.arccos(np.clip(np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b),-1,1))))
rows=[]
dg=bpy.context.evaluated_depsgraph_get()
for i,sf in enumerate(SF):
    src.hide_viewport=False; bpy.context.scene.frame_set(int(sf)); bpy.context.view_layer.update()
    Rs=chestR(src,"Spine2",sw).inverted(); 
    sdir={s:np.array(Rs@((sw@src.pose.bones[("Left" if s=="L" else "Right")+"ForeArm"].head)-(sw@src.pose.bones[("Left" if s=="L" else "Right")+"Arm"].head)).normalized()) for s in "LR"}
    src.hide_viewport=True; bpy.context.scene.frame_set(i+1); bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get()
    Rt=chestR(tgt,"chest",tw).inverted()
    ev=body.evaluated_get(dg).data; ec=np.zeros(len(ev.vertices)*3); ev.vertices.foreach_get("co",ec); ec=ec.reshape(-1,3)
    wm=np.array(body.matrix_world)
    row={"src_frame":sf}
    for s in "LR":
        a,b=RING[s]; d=ec[b].mean(0)-ec[a].mean(0); d=np.array(Rt@Vector(d)); d/=np.linalg.norm(d)
        bd=np.array(Rt@((tw@tgt.pose.bones[f"forearm_{s}"].head)-(tw@tgt.pose.bones[f"upperarm_{s}"].head)).normalized())
        sign=1 if s=="L" else -1
        row[s]={"src":sdir[s].round(3).tolist(),"mesh":d.round(3).tolist(),"bone":bd.round(3).tolist(),
            "src_vs_mesh_deg":ang(sdir[s],d),"bone_vs_mesh_deg":ang(bd,d),"mesh_lateral":float(d[0]*sign),"src_lateral":float(sdir[s][0]*sign)}
    rows.append(row)
res={"frames":rows}; ok=True; checks={}
for s in "LR":
    sm=np.median([r[s]["src_vs_mesh_deg"] for r in rows]); lat=np.median([r[s]["mesh_lateral"] for r in rows])
    bm=np.median([r[s]["bone_vs_mesh_deg"] for r in rows]); mx=max(r[s]["src_vs_mesh_deg"] for r in rows)
    M_=np.array([r[s]["mesh"] for r in rows]); S_=np.array([r[s]["src"] for r in rows])
    mr=max(ang(a,b) for a in M_ for b in M_); sr=max(ang(a,b) for a in S_ for b in S_)
    c={"median_src_vs_mesh_deg<=30":(sm,sm<=30),"median_mesh_lateral<=0.6":(lat,lat<=0.6),
       "median_bone_vs_mesh_deg<=15":(bm,bm<=15),"max_src_vs_mesh_deg<=45":(mx,mx<=45),"mesh_range_deg>=max(3,0.5*src_range)":((mr,sr),mr>=max(3,0.5*sr))}
    checks[s]={k:{"value":v[0],"pass":bool(v[1])} for k,v in c.items()}; ok&=all(v[1] for v in c.values())
res["checks"]=checks; res["PASS"]=bool(ok); res["rig_file"]=bpy.data.filepath
json.dump(res,open(out,"w"),indent=1,default=float)
print("GATE",json.dumps(checks,default=float)); print("RESULT","PASS" if ok else "FAIL")
sys.stdout.flush(); import os; os._exit(0 if ok else 1)
