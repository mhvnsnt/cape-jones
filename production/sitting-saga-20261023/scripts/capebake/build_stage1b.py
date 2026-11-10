"""Stage 1B: load cape vert indices, separate into CapeJones_Cape, save stage1 file."""
import bpy
import numpy as np
import gc

SRC = "/home/hatch/workspace/sitcanon-work/scene_anim_placed3.blend"
NPZ = "/home/hatch/workspace/capebake-work/cape_verts.npz"
OUT = "/home/hatch/workspace/capebake-work/stage1_separated.blend"

cape_idx = np.load(NPZ)["cape_idx"]
expected = len(cape_idx)
print(f"loaded {expected} cape vert indices", flush=True)

bpy.ops.wm.open_mainfile(filepath=SRC)
body = bpy.data.objects["CapeJones_Body"]
mesh = body.data
assert len(mesh.vertices) - len(cape_idx) > 0

bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
bpy.context.view_layer.objects.active = body
sel = np.zeros(len(mesh.vertices), dtype=bool)
sel[cape_idx] = True
for i in np.nonzero(sel)[0]:
    mesh.vertices[int(i)].select = True
del sel, cape_idx
gc.collect()
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='SELECTED')
bpy.ops.object.mode_set(mode='OBJECT')
cape = None
for o in bpy.data.objects:
    if o.type == 'MESH' and o != body and len(o.data.vertices) == expected:
        cape = o
        break
assert cape, "separated cape object not found"
cape.name = "CapeJones_Cape"
print(f"cape object: {cape.name} verts={len(cape.data.vertices)} body now {len(body.data.vertices)}", flush=True)
if cape.data.shape_keys:
    for kb in list(cape.data.shape_keys.key_blocks)[1:]:
        cape.shape_key_remove(kb)
    cape.shape_key_remove(cape.data.shape_keys.key_blocks[0])
for m in list(cape.modifiers):
    if m.type == 'CORRECTIVE_SMOOTH':
        cape.modifiers.remove(m)
print("cape modifiers:", [(m.name, m.type) for m in cape.modifiers], flush=True)
gc.collect()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print(f"SAVED {OUT}", flush=True)
print("STAGE1B DONE", flush=True)
