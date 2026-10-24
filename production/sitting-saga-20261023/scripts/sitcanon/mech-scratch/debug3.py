import bpy
from mathutils import Euler

def pad_bbox(tag, pad):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = pad.evaluated_get(dg)
    ws = [ev.matrix_world @ v.co for v in ev.data.vertices]
    print(f"  {tag}: pad x {min(v.x for v in ws):.3f}..{max(v.x for v in ws):.3f} z {min(v.z for v in ws):.3f}..{max(v.z for v in ws):.3f}")

def bone_mat(tag, rrig):
    dg = bpy.context.evaluated_depsgraph_get()
    evr = rrig.evaluated_get(dg)
    m = evr.pose.bones['footrest'].matrix
    print(f"  {tag}: footrest evaluated matrix loc={tuple(round(v,3) for v in m.translation)} rotY={m.to_euler().y:.3f}")

print("=== STANDALONE: whole-euler assignment ===")
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/mech-scratch/repo/3d-assets/living-room/recliner/recliner_rigged.blend")
rrig = bpy.data.objects['recliner_rig']
pad = bpy.data.objects['recliner_footrest_pad']
pb = rrig.pose.bones['footrest']
print("  before:", tuple(round(v, 3) for v in pb.rotation_euler))
pb.rotation_euler = Euler((0.0, -0.873, 0.0))
print("  after set:", tuple(round(v, 3) for v in pb.rotation_euler))
bpy.context.view_layer.update()
bone_mat("manual euler", rrig)
pad_bbox("manual euler", pad)
pb.rotation_euler = Euler((0.0, 0.0, 0.0))
bpy.context.view_layer.update()

print("\n=== STANDALONE: recline + update_tag + frame change ===")
rrig['recline'] = 1.0
rrig.update_tag(refresh={'DATA'})
bpy.context.scene.frame_set(2)
bone_mat("recline=1", rrig)
pad_bbox("recline=1", pad)
print("  prop value readback:", rrig['recline'])
print("  raw pb euler:", tuple(round(v, 3) for v in pb.rotation_euler))

print("\n=== MY SCENE: canonical-rig driver probe (ik_leg_L) ===")
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend")
rig = bpy.data.objects.get("CapeJones_Rig")
scene = bpy.context.scene
scene.frame_set(40)
root = rig.pose.bones['root']
print("  ik_leg_L before:", root.get('ik_leg_L'))
thigh = rig.pose.bones['thigh_L']
ik_c = [c for c in thigh.constraints if c.name == 'IK'][0]
print("  thigh_L IK influence (raw):", round(ik_c.influence, 3))
root['ik_leg_L'] = 1.0
scene.frame_set(41)
scene.frame_set(40)
dg = bpy.context.evaluated_depsgraph_get()
evr = rig.evaluated_get(dg)
ethigh = evr.pose.bones['thigh_L']
eik = [c for c in ethigh.constraints if c.name == 'IK'][0]
print("  thigh_L IK influence (evaluated):", round(eik.influence, 3))
print("=== DEBUG3 DONE ===")
