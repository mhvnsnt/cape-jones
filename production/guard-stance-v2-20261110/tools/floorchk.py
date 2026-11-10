import bpy,sys,numpy as np; sys.path.insert(0,"/workspace/cape-jones-show-deliver/guard-stance-v2-20261110/tools"); import cj_scene as S
sc=bpy.context.scene; S.setup("front3q",pct=25)
fl=bpy.data.objects["SetFloor"]; print("FLOOR z",fl.location.z,"prop",sc.get("cj_floor_z"), "objs named floor", [o.name for o in bpy.data.objects if 'loor' in o.name or o.type=='MESH' and o.dimensions.x>5])
b=bpy.data.objects["CapeJones_Body"]
for f in (100,150,200):
    sc.frame_set(f); m=b.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    a=np.zeros(len(m.vertices)*3); m.vertices.foreach_get("co",a); a=a.reshape(-1,3); W=np.array(b.matrix_world); a=(W[:3,:3]@a.T).T+W[:3,3]
    lo=a[:,2].min(); i=a[:,2].argmin(); near=(a[:,2]<lo+0.004)
    print("F",f,"min z %.4f at x%.3f y%.3f"%(lo,a[i,0],a[i,1]),"verts within 4mm",int(near.sum()),"bbox near",a[near].min(0).round(3),a[near].max(0).round(3),"total verts",len(a))
