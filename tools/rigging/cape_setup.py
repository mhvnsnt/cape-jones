"""Cape separation (memory-efficient): y>0.10 verts -> separate object."""
import bpy, os
import numpy as np
from mathutils import Vector

TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_bound.blend'))
scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
for o in (char,):
    if o.name not in scn.collection.objects:
        scn.collection.objects.link(o)
bpy.context.view_layer.update()

bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.objects.active = char

# get verts as numpy (world space)
n = len(char.data.vertices)
verts = np.empty(n*3, dtype=np.float64)
char.data.vertices.foreach_get('co', verts)
verts = verts.reshape(-1, 3)
# to world
mw = np.array(char.matrix_world)
verts_w = (mw[:3,:3] @ verts.T).T + mw[:3,3]
# cape mask
mask = verts_w[:,1] > 0.10
print('cape verts:', mask.sum(), '/', n)

# create vertex group for cape
vg = char.vertex_groups.new(name='cape_mask')
# add in chunks to avoid huge list
idx = np.where(mask)[0]
for i in range(0, len(idx), 10000):
    chunk = idx[i:i+10000].tolist()
    vg.add(chunk, 1.0, 'REPLACE')
print('vg created')

# select cape verts via vertex group, then separate
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
# select by vertex group
bpy.context.object.vertex_groups.active = vg
bpy.ops.object.vertex_group_select()
bpy.ops.mesh.separate(type='SELECTED')
bpy.ops.object.mode_set(mode='OBJECT')

# find separated cape
cape = None
for o in bpy.data.objects:
    if o.type == 'MESH' and o != char and 'Body' in o.name:
        cape = o
        break
if cape:
    cape.name = 'CapeJones_Cape'
    print('CAPE:', cape.name, len(cape.data.vertices))
    mat = bpy.data.materials.new('Cape_Black')
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0, 0, 0, 1)
    cape.data.materials.clear()
    cape.data.materials.append(mat)
    # remove cape verts from char's MeshDeform? No, char keeps its bind (cape verts were part of it)
    # The cape object needs its own deform: it was part of char, so it has the MeshDeform bind data?
    # Actually, separated object is a new mesh; it needs modifiers. We'll add cloth + armature.
else:
    print('CAPE NOT FOUND')
    raise SystemExit

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_cape_sep.blend'))
print('CAPE SEPARATED')
