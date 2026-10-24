import bpy
import os

print("=== FILE ===", bpy.data.filepath)
print("\n=== LIBRARIES ===")
for lib in bpy.data.libraries:
    print(f"  {lib.name} -> {lib.filepath} exists={os.path.exists(bpy.path.abspath(lib.filepath))}")

print("\n=== COLLECTIONS ===")
for col in bpy.data.collections:
    lib = col.library.name if col.library else "local"
    print(f"  {col.name} (lib={lib}) objects={[o.name for o in col.objects]}")

print("\n=== OBJECTS ===")
for ob in bpy.data.objects:
    mw = ob.matrix_world
    loc = tuple(round(v, 3) for v in mw.translation)
    extra = ""
    if ob.type == 'MESH':
        extra = f" verts={len(ob.data.vertices)} mats={[m.name if m else None for m in ob.data.materials]}"
    if ob.type == 'ARMATURE':
        extra = f" bones={len(ob.data.bones)}"
    print(f"  {ob.name} [{ob.type}] parent={ob.parent.name if ob.parent else None} loc={loc}{extra}")
    if ob.get("recline") is not None or len(ob.keys()) > 1:
        print(f"      custom props: { {k: ob[k] for k in ob.keys() if k != '_RNA_UI'} }")

print("\n=== SCENE CUSTOM PROPS ===")
sc = bpy.context.scene
print(" ", {k: sc[k] for k in sc.keys() if k != '_RNA_UI'})
print("  frame range:", sc.frame_start, sc.frame_end, "current:", sc.frame_current)
print("  render:", sc.render.engine, sc.cycles.samples if sc.render.engine=='CYCLES' else '-', sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage)

chair = bpy.data.objects.get('loungeChairRelax(Clone)')
if chair:
    print("\n=== CHAIR ===")
    print("  matrix_world:")
    for row in chair.matrix_world:
        print("   ", tuple(round(v, 4) for v in row))
    xs = [ (chair.matrix_world @ v.co).x for v in chair.data.vertices ]
    ys = [ (chair.matrix_world @ v.co).y for v in chair.data.vertices ]
    zs = [ (chair.matrix_world @ v.co).z for v in chair.data.vertices ]
    print(f"  world bbox x {min(xs):.3f}..{max(xs):.3f}  y {min(ys):.3f}..{max(ys):.3f}  z {min(zs):.3f}..{max(zs):.3f}")
    print("  modifiers:", [(m.name, m.type) for m in chair.modifiers])
    print("  vertex groups:", [g.name for g in chair.vertex_groups])
    print("  shape keys:", list(chair.data.shape_keys.key_blocks.keys()) if chair.data.shape_keys else None)
    print("  parent:", chair.parent.name if chair.parent else None, " parent_type:", chair.parent_type)
    print("  constraints:", [(c.name, c.type) for c in chair.constraints])

rig = bpy.data.objects.get('CapeJones_Rig')
if rig:
    print("\n=== RIG ===")
    print("  action:", rig.animation_data.action.name if rig.animation_data and rig.animation_data.action else None)
    act = rig.animation_data.action
    if act:
        print("  action frame range:", tuple(round(v,1) for v in act.frame_range), " fcurves:", len(act.fcurves))
    print("  bones:", [b.name for b in rig.data.bones])
    print("\n  pose bone constraints:")
    for pb in rig.pose.bones:
        if pb.constraints:
            for c in pb.constraints:
                print(f"    {pb.name}: {c.name} [{c.type}] influence={c.influence:.3f} target={getattr(c,'target',None)} subtarget={getattr(c,'subtarget','')}")
    print("\n  leg/foot bone chain:")
    for name in ('thigh_L','shin_L','foot_L','toe_L','thigh_R','shin_R','foot_R','toe_R','root','pelvis'):
        b = rig.data.bones.get(name)
        if b:
            print(f"    {name}: parent={b.parent.name if b.parent else None} head={tuple(round(v,3) for v in b.head_local)} tail={tuple(round(v,3) for v in b.tail_local)}")
        else:
            print(f"    {name}: MISSING")

body = bpy.data.objects.get('CapeJones_Body')
if body:
    print("\n=== BODY ===")
    print("  modifiers:", [(m.name, m.type) for m in body.modifiers])
    for m in body.modifiers:
        if m.type == 'ARMATURE':
            print("    armature mod object:", m.object.name if m.object else None, " preserve_volume:", m.use_deform_preserve_volume)
    print("  shape keys:", list(body.data.shape_keys.key_blocks.keys()) if body.data.shape_keys else None)
    print("  parent:", body.parent.name if body.parent else None)

print("\n=== DRIVERS (all id blocks) ===")
def scan_drivers(idblock, label):
    ad = getattr(idblock, 'animation_data', None)
    if ad and ad.drivers:
        for d in ad.drivers:
            print(f"  {label}: {d.data_path} expr='{d.driver.expression}'")
for ob in bpy.data.objects:
    scan_drivers(ob, f"obj {ob.name}")
    if ob.type == 'ARMATURE':
        scan_drivers(ob.data, f"armature {ob.name}")
scan_drivers(bpy.context.scene, "scene")
print("\n=== DONE ===")
