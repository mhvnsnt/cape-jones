import bpy,numpy as np
p=bpy.data.objects["CapeClothProxy"]; sc=bpy.context.scene
for o in bpy.data.objects:
    if o.name in("CapeJones_Body","CapeJones_CapeHi","CapeJones_Cape"): o.hide_viewport=True
for f in [1,10,20,30,40,60,90,130,170,210,250,268]:
    sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get(); m=p.evaluated_get(dg).data
    c=np.array([v.co[:] for v in m.vertices]); e=np.array([[ed.vertices[0],ed.vertices[1]] for ed in p.data.edges])
    L=np.linalg.norm(c[e[:,0]]-c[e[:,1]],axis=1)
    print("F",f,"min",c.min(0).round(3),"max",c.max(0).round(3),"edge med %.4f max %.4f"%(np.median(L),L.max()))
