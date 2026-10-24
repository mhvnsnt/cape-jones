import bpy

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend")
scene = bpy.context.scene
rrig = bpy.data.objects['recliner_rig']
rig = bpy.data.objects['CapeJones_Rig']
pad = bpy.data.objects['recliner_footrest_pad']

print("=== recliner_rig animation state ===")
ad = rrig.animation_data
print("  action:", ad.action.name if ad and ad.action else None)
if ad and ad.action:
    for fc in ad.action.fcurves:
        print(f"    fcurve {fc.data_path} idx={fc.array_index} keys={[(round(k.co.x,1), round(k.co.y,4)) for k in fc.keyframe_points]}")
print("  NLA tracks:", len(ad.nla_tracks) if ad else 0)
if ad:
    for t in ad.nla_tracks:
        for s in t.strips:
            print(f"    strip {s.name} action={s.action.name if s.action else None} frame {s.frame_start}..{s.frame_end}")

def pad_bbox(tag):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = pad.evaluated_get(dg)
    ws = [ev.matrix_world @ v.co for v in ev.data.vertices]
    print(f"  {tag}: pad x {min(v.x for v in ws):.3f}..{max(v.x for v in ws):.3f} z {min(v.z for v in ws):.3f}..{max(v.z for v in ws):.3f}")

scene.frame_set(40)
print("\n=== test: recline=1 with frame changes ===")
print("  recline before:", rrig['recline'])
rrig['recline'] = 1.0
scene.frame_set(41)
scene.frame_set(40)
print("  recline readback:", rrig['recline'])
pad_bbox("after recline=1")

print("\n=== leg probe: ik_leg_L 0 -> 1 (geometry truth) ===")
def foot_world(tag):
    dg = bpy.context.evaluated_depsgraph_get()
    evr = rig.evaluated_get(dg)
    f = evr.matrix_world @ evr.pose.bones['foot_L'].head
    fik = evr.matrix_world @ evr.pose.bones['foot_ik_L'].head
    print(f"  {tag}: deform foot_L {tuple(round(v,3) for v in f)}  foot_ik_L {tuple(round(v,3) for v in fik)}")
foot_world("baseline (ik_leg_L=0)")
rig.pose.bones['root']['ik_leg_L'] = 1.0
scene.frame_set(41)
scene.frame_set(40)
foot_world("ik_leg_L=1")
rig.pose.bones['root']['ik_leg_L'] = 0.0
rrig['recline'] = 0.0
scene.frame_set(41)
scene.frame_set(40)
print("=== DEBUG4 DONE ===")
