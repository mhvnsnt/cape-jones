"""LANE 1 CAPE REBUILD — inspection of cape_jones_rigged_w5r_idle.blend.
Reports: all objects, cape-fragment candidates (name + verts + world bbox),
character body bounds, armature summary. Run headless via xvfb-run."""
import bpy
from mathutils import Vector

# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# The raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
# Presence-checked: this is an inspection script and may be run on files without a CJ rig.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
if bpy.data.objects.get("CapeJones_Rig") is not None and bpy.data.objects.get("CapeJones_Body") is not None:
    cj_arm_guard.ensure_arm_fix()

print("=" * 70)
print("OBJECTS IN FILE")
print("=" * 70)
for ob in bpy.data.objects:
    print(f"{ob.type:10s} {ob.name}  verts={len(ob.data.vertices) if ob.type=='MESH' else '-'}")
    if ob.type == 'ARMATURE':
        print(f"    bones: {len(ob.data.bones)}")
        deforms = [b.name for b in ob.data.bones if b.use_deform]
        print(f"    deform bones: {len(deforms)}")

print()
print("=" * 70)
print("CAPE-CANDIDATE OBJECTS (name match)")
print("=" * 70)
cands = [ob for ob in bpy.data.objects if ob.type == 'MESH' and
         any(k in ob.name.lower() for k in ('cape', 'cloth', 'fragment', 'frag'))]
total_v = 0
for ob in cands:
    ws = [ob.matrix_world @ v.co for v in ob.data.vertices]
    xs = [c.x for c in ws]; ys = [c.y for c in ws]; zs = [c.z for c in ws]
    total_v += len(ws)
    print(f"{ob.name:40s} verts={len(ws):5d} "
          f"x[{min(xs):.3f},{max(xs):.3f}] y[{min(ys):.3f},{max(ys):.3f}] z[{min(zs):.3f},{max(zs):.3f}]")
print(f"TOTAL cape verts: {total_v}, count: {len(cands)}")

print()
print("=" * 70)
print("SCENE / RENDER / ANIM INFO")
print("=" * 70)
sc = bpy.context.scene
print(f"scene={sc.name} fps={sc.render.fps} start={sc.frame_start} end={sc.frame_end}")
print(f"render engine={sc.render.engine} res={sc.render.resolution_x}x{sc.render.resolution_y}")
for ob in bpy.data.objects:
    if ob.type == 'ARMATURE':
        act = ob.animation_data.action if ob.animation_data else None
        print(f"armature {ob.name}: action={act.name if act else None} "
              f"fcurves={len(act.fcurves) if act else 0}")
