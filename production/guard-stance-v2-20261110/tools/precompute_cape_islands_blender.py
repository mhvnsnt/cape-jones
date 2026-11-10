import bpy,numpy as np
b=bpy.data.objects["CapeJones_Body"]; me=b.data
co=np.zeros(len(me.vertices)*3); me.vertices.foreach_get("co",co)
e=np.zeros(len(me.edges)*2,np.int32); me.edges.foreach_get("vertices",e)
np.save("/workspace/cj3d/diag/bco.npy",co.reshape(-1,3).astype(np.float32)); np.save("/workspace/cj3d/diag/bedges.npy",e.reshape(-1,2))
# per-vertex texture colour sample: get image
mat=me.materials[0]; imgs=[n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
print("IMGS",[(i.name,i.size[:]) for i in imgs])
uv=me.uv_layers.active.data; cv=np.zeros(len(me.loops),np.int32); me.loops.foreach_get("vertex_index",cv)
u=np.zeros(len(me.loops)*2,np.float32); uv.foreach_get("uv",u); u=u.reshape(-1,2)
vu=np.zeros((len(me.vertices),2),np.float32); vu[cv]=u
im=imgs[0]; W,H=im.size; px=np.array(im.pixels[:],np.float32).reshape(H,W,-1)
xi=np.clip((vu[:,0]%1*W).astype(int),0,W-1); yi=np.clip((vu[:,1]%1*H).astype(int),0,H-1)
np.save("/workspace/cj3d/diag/bcol.npy",px[yi,xi,:3])
