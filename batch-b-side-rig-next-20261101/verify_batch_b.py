"""Re-open saved Batch B .blends and verify gates (no build claims from logs).
Usage: blender -b --python verify_batch_b.py -- <blendfile>
Prints: bones + parents + local rotations, plane parent bones, wrist
distances (forearm tail == hand head), FK keyframes on side rig.
"""
import bpy, sys, math
from mathutils import Vector

path = sys.argv[sys.argv.index('--') + 1]
bpy.ops.wm.open_mainfile(filepath=path)
print('FILE', path)
for ob in bpy.data.objects:
    if ob.type == 'ARMATURE':
        print('ARMATURE', ob.name)
        for bn in ob.pose.bones:
            print(' BONE', bn.name, 'parent', bn.parent.name if bn.parent else None,
                  'rotXYZ', tuple(round(v, 4) for v in bn.rotation_euler),
                  'head', tuple(round(v, 3) for v in bn.head),
                  'tail', tuple(round(v, 3) for v in bn.tail))
        for f, h in [('forearm_near', 'hand_near'), ('forearm_far', 'hand_far'),
                     ('forearm_ArmBack', 'hand_ArmBack'), ('forearm_ArmFront', 'hand_ArmFront'),
                     ('forearm_R', 'hand_R'), ('forearm_L', 'hand_L')]:
            if f in ob.pose.bones and h in ob.pose.bones:
                fb, hb = ob.pose.bones[f], ob.pose.bones[h]
                print(' WRISTBONE', f, 'tail==hand head dist', round((fb.tail - hb.head).length, 6))
        if ob.animation_data and ob.animation_data.action:
            print(' ACTION', ob.animation_data.action.name)
            try:
                cb = ob.animation_data.action.layers[0].strips[0].channelbag
                fcs = cb().fcurves if callable(cb) else cb.fcurves
            except Exception as e:
                print('  FCURVE-ERR', e)
                fcs = []
            for fc in fcs:
                print('  FCURVE', fc.data_path, 'keys', len(fc.keyframe_points),
                      [round(k.co.x, 1) for k in fc.keyframe_points])
for ob in bpy.data.objects:
    if ob.type == 'MESH' and not ob.name.startswith('Marker'):
        print(' PLANE', ob.name, 'parent_bone', ob.parent_bone, 'parent_type', ob.parent_type,
              'world', tuple(round(v, 3) for v in ob.matrix_world.translation),
              'rotZ', round(ob.matrix_world.to_euler().z, 3))
