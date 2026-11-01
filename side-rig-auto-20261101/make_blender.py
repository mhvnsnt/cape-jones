# Blender armature from AUTO-MANIFEST joints (computed by build_auto.py, not hand-typed coords in the rig builder).
# Units: x=(px-660)/100, y=(1450-py)/100, so ground=0, head top ~13.3, facing +x.
import bpy, json, os
man = json.load(open(os.path.expanduser('~/workspace/cape-jones-rig/side-rig-auto-20261101/AUTO-MANIFEST.json')))
J = man['joints_px']
def P(px, py): return ((px-660)/100.0, (1450-py)/100.0, 0.0)
# joints not in manifest, derived from segments in build_auto (thigh/knee, ankle=ground start)
shoulder = J['shoulder']; elbow = J['elbow_near_idle']; wrist = J['wrist_near_idle']
neck_top = J['neck_top']; pelvis_top = J['pelvis_top']; hip = J['thigh_near_top']
# knee: hip + thigh segment (243 native * S) in y, +14 native x offset * S
S = man['global_scale_S']; knee = (hip[0]+14*S, hip[1]+243*S); ankle = (700.0, 1450.0)
neck_bottom = (neck_top[0], neck_top[1]+186*S); head_top = (neck_top[0], 120.0)
bones = [
    ('hip', P(*hip), P(*pelvis_top), None),
    ('chest', P(*pelvis_top), P(*shoulder), 'hip'),
    ('neck', P(*neck_bottom), P(*neck_top), 'chest'),
    ('head', P(*neck_top), P(*head_top), 'neck'),
    ('upper_arm', P(*shoulder), P(*elbow), 'chest'),
    ('forearm', P(*elbow), P(*wrist), 'upper_arm'),
    ('thigh', P(*hip), P(*knee), 'hip'),
    ('shin', P(*knee), P(*ankle), 'thigh'),
]
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
bpy.ops.object.armature_add(enter_editmode=True)
arm = bpy.context.object; arm.name = 'SideRigArmature_Auto'
eb = arm.data.edit_bones
eb[0].name = 'hip'; eb[0].head = bones[0][1]; eb[0].tail = bones[0][2]
for name, head, tail, parent in bones[1:]:
    b = eb.new(name); b.head = head; b.tail = tail
    if parent: b.parent = eb[parent]
bpy.ops.object.mode_set(mode='OBJECT')
out = os.path.expanduser('~/workspace/cape-jones-rig/side-rig-auto-20261101/side-rig-auto-20261101.blend')
bpy.ops.wm.save_as_mainfile(filepath=out)
print('SAVED', out)
for b in bpy.context.object.data.bones:
    print(b.name, tuple(round(v,2) for v in b.head_local), tuple(round(v,2) for v in b.tail_local))
