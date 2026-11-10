import bpy
import os

SRC_BLEND = "/home/hatch/workspace/sitcanon-work/mech-scratch/repo/3d-assets/living-room/recliner/recliner_rigged.blend"
OUT = "/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend"

print("=== STAGE A: integrate rigged recliner ===")
print("opened:", bpy.data.filepath)

# --- 1. append recliner objects locally ---
names = ['recliner_rig', 'recliner_base', 'recliner_backrest', 'recliner_footrest_link',
         'recliner_footrest_pad', 'recliner_armrest_L', 'recliner_armrest_R', 'recliner_legs']
with bpy.data.libraries.load(SRC_BLEND, link=False) as (data_from, data_to):
    data_to.objects = names
objs = [o for o in data_to.objects if o is not None]
print("appended:", [o.name for o in objs])
assert len(objs) == 8, f"expected 8 objects, got {len(objs)}"

coll = bpy.data.collections.new("ReclinerMech")
bpy.context.scene.collection.children.link(coll)
for o in objs:
    if o.name not in coll.objects:
        coll.objects.link(o)

# --- 2. materials: reuse scene's existing datablocks by base name ---
def base_name(n):
    return n.split('.')[0] if n.rsplit('.', 1)[-1].isdigit() else n
scene_mats = {}
for m in bpy.data.materials:
    scene_mats.setdefault(base_name(m.name), m)
for o in objs:
    if o.type != 'MESH':
        continue
    for i, m in enumerate(o.data.materials):
        if m and m.name not in ('metal', 'carpet', 'wood'):
            bn = base_name(m.name)
            if bn in scene_mats:
                o.data.materials[i] = scene_mats[bn]
                print(f"  {o.name}: material {m.name} -> {scene_mats[bn].name}")

rrig = bpy.data.objects['recliner_rig']
print("recliner_rig loc:", tuple(round(v, 3) for v in rrig.location), "rotZ:", round(rrig.rotation_euler.z, 4))
print("recline prop:", rrig.get('recline'))

# --- 3. clear the ReclinerOpen action assignment (keep drivers); manual prop control ---
if rrig.animation_data:
    rrig.animation_data.action = None
    print("cleared recliner action assignment; drivers kept:", len(rrig.animation_data.drivers))
# clamp UI range 0..1
try:
    ui = rrig.id_properties_ui("recline")
    ui.update(min=0.0, max=1.0, soft_min=0.0, soft_max=1.0)
except Exception as e:
    print("ui clamp note:", e)
rrig['recline'] = 0.0

# --- 4. canonical retraction slide on rigged parts (chair-local: y<0.217 & z<0.20 -> y+=0.21) ---
# mirrors the canonical scene edit (world x<2.87 & z<0.20 -> world x+=0.21; world x = local y + 2.653)
total_slid = 0
for o in objs:
    if o.type != 'MESH':
        continue
    slid = 0
    for v in o.data.vertices:
        if v.co.y < 0.217 and v.co.z < 0.20:
            v.co.y += 0.21
            slid += 1
    if slid:
        o.data.update()
    print(f"  {o.name}: slid {slid} verts")
    total_slid += slid
print("total verts slid:", total_slid, "(canonical static-chair edit slid 66)")

# --- 5. remove the static chair (replaced 1:1 by rigged parts) ---
old = bpy.data.objects.get('loungeChairRelax(Clone)')
if old:
    bpy.data.objects.remove(old, do_unlink=True)
    print("removed static chair loungeChairRelax(Clone)")

bpy.context.view_layer.update()

# --- 6. verify closed-state union bbox vs canonical chair bbox (x 2.858..3.328, y 1.822..2.312, z 0..0.63) ---
import mathutils
allw = []
for o in objs:
    if o.type == 'MESH':
        allw += [o.matrix_world @ v.co for v in o.data.vertices]
print(f"rigged chair union bbox: x {min(v.x for v in allw):.3f}..{max(v.x for v in allw):.3f}  "
      f"y {min(v.y for v in allw):.3f}..{max(v.y for v in allw):.3f}  z {min(v.z for v in allw):.3f}..{max(v.z for v in allw):.3f}")
print("canonical chair bbox  : x 2.858..3.328  y 1.822..2.312  z 0.000..0.630")

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
print("=== STAGE A DONE ===")
