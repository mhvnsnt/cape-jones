"""LANE 1 — merge baked cape into the full file.
Loads STEP1 (full: rig+body+unbaked cape), deletes unbaked cape,
appends baked cape (48 shape keys) from cape_sim_light_baked.blend,
mutes its Armature (motion is baked into shape keys — avoids double-deform),
saves FINAL cape_jones_rigged_w5r_idle_cape.blend."""
import bpy, os

# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# The raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
# The FINAL file saved below therefore carries the fixed arm chain + cj_arm_fix mark.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
cj_arm_guard.ensure_arm_fix()

STEP1 = os.path.join(os.getcwd(), 'cape_jones_rigged_w5r_idle_cape_STEP1.blend')
BAKED = os.path.join(os.getcwd(), 'cape_sim_light_baked.blend')
FINAL = os.path.join(os.getcwd(), 'cape_jones_rigged_w5r_idle_cape.blend')

# STEP1 is already loaded (run with -b STEP1)
cape_old = bpy.data.objects.get('CapeJones_Cape')
if cape_old:
    bpy.data.objects.remove(cape_old, do_unlink=True)
    print("removed unbaked cape", flush=True)

# append baked cape
with bpy.data.libraries.load(BAKED, link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n == 'CapeJones_Cape']
baked = dst.objects[0]
bpy.context.scene.collection.objects.link(baked)
print(f"appended {baked.name}, shape keys: {len(baked.data.shape_keys.key_blocks)}", flush=True)

# mute Armature (baked motion in shape keys) — keep Cloth muted for re-bake ref
for m in baked.modifiers:
    if m.type == 'ARMATURE':
        m.show_viewport = False
        m.show_render = False
        print("muted Armature (shape keys carry the bake)", flush=True)
    if m.type == 'CLOTH':
        m.show_viewport = False
        m.show_render = False

# sanity: shape key animation present?
sk = baked.data.shape_keys
print(f"keyframed shape keys: {sum(1 for kb in sk.key_blocks if kb.name.startswith('frame_'))}", flush=True)

bpy.ops.wm.save_as_mainfile(filepath=FINAL)
print(f"SAVED {FINAL}", flush=True)
