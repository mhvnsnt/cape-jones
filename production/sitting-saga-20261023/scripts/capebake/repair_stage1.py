"""Repair stage1 file: find the REAL separated cape (249971 verts), restore antenna name."""
import bpy

PATH = "/home/hatch/workspace/capebake-work/stage1_separated.blend"
bpy.ops.wm.open_mainfile(filepath=PATH)

real = None
for o in bpy.data.objects:
    if o.type == 'MESH' and len(o.data.vertices) == 249971:
        real = o
        break
print("real cape candidate:", real.name if real else None)
assert real, "real cape object (249971 verts) not found"

fake = bpy.data.objects.get("CapeJones_Cape")
print("current CapeJones_Cape:", fake.name if fake else None, "verts:", len(fake.data.vertices) if fake else None)
if fake and fake is not real:
    fake.name = "antenna_0"
    print("renamed fake back to antenna_0")
real.name = "CapeJones_Cape"
print("cape modifiers before:", [(m.name, m.type) for m in real.modifiers])
print("cape shape keys before:", [kb.name for kb in real.data.shape_keys.key_blocks] if real.data.shape_keys else None)
if real.data.shape_keys:
    for kb in list(real.data.shape_keys.key_blocks)[1:]:
        real.shape_key_remove(kb)
    real.shape_key_remove(real.data.shape_keys.key_blocks[0])
for m in list(real.modifiers):
    if m.type == 'CORRECTIVE_SMOOTH':
        real.modifiers.remove(m)
print("cape modifiers after:", [(m.name, m.type) for m in real.modifiers])
body = bpy.data.objects["CapeJones_Body"]
print(f"body verts {len(body.data.vertices)}, cape verts {len(real.data.vertices)}, sum {len(body.data.vertices)+len(real.data.vertices)}")
bpy.ops.wm.save_as_mainfile(filepath=PATH)
print("REPAIR SAVED")
