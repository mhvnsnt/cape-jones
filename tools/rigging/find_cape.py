"""Find cape as disconnected island (~82k verts, behind)."""
import bpy, os
import bmesh
from mathutils import Vector

TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
# reload from bound (before bad separation)
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_bound.blend'))
char = bpy.data.objects['CapeJones_Body']
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.objects.active = char
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(char.data)
bm.verts.ensure_lookup_table()
# find islands via BFS on linked verts
visited = set()
islands = []
for v in bm.verts:
    if v.index in visited:
        continue
    # BFS
    stack = [v]
    island = set()
    while stack:
        cur = stack.pop()
        if cur.index in visited:
            continue
        visited.add(cur.index)
        island.add(cur.index)
        for e in cur.link_edges:
            for ov in e.verts:
                if ov.index not in visited:
                    stack.append(ov)
    islands.append(island)
print('islands:', len(islands))
for i, isl in enumerate(islands):
    print(f'  island {i}: {len(isl)} verts')
# the cape should be ~82k. Find it.
# (Don't separate yet, just identify)
bpy.ops.object.mode_set(mode='OBJECT')
