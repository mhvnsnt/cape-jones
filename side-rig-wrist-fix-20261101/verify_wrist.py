import bpy, math
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cape-jones-rig/side-rig-wrist-fix-20261101/side-rig-wrist-fix-20261101.blend')
arm = bpy.data.objects['SideRigArmature_WristFix']
print('ARMATURE', arm.name)
for bn in arm.pose.bones:
    print(' BONE', bn.name, 'parent', bn.parent.name if bn.parent else None, 'rotZ', round(bn.rotation_euler.z,4) if bn.rotation_mode=='XYZ' else bn.rotation_mode, 'head', tuple(round(v,3) for v in bn.head), 'tail', tuple(round(v,3) for v in bn.tail))
for ob in bpy.data.objects:
    if ob.type=='MESH':
        print(' PLANE', ob.name, 'parent_bone', ob.parent_bone, 'parent_type', ob.parent_type, 'world', tuple(round(v,3) for v in ob.matrix_world.translation), 'rotZ', round(ob.matrix_world.to_euler().z,3))
# wrist gate in bone space
for f,h in [('forearm_near','hand_near'),('forearm_far','hand_far')]:
    fb=arm.pose.bones[f]; hb=arm.pose.bones[h]
    d=(fb.tail-hb.head).length
    vec=fb.tail-fb.head
    print(' WRISTBONE', f, 'tail==hand head dist', round(d,6), 'elbow->wrist vec', tuple(round(v,3) for v in vec), 'facing +x?', vec.x>0)
