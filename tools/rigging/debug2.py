"""Check drivers on guide-bone constraints + matrix_local sanity."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
arm = bpy.data.objects['biped_blenrig']
for d in arm.animation_data.drivers:
    if 'pelvis_str_L' in d.data_path or 'knee_pole_str_L' in d.data_path:
        print('DRV:', d.data_path)
# matrix_local sanity on one bone
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
pb = arm.pose.bones['master_torso_str']
print('matrix_basis == identity:', all(abs(a - b) < 1e-6 for a, b in zip((pb.matrix_basis.transposed() @ __import__('mathutils').Matrix.Identity(4).transposed()).row[0], (1,0,0))))
import mathutils
I = mathutils.Matrix.Identity(4)
diff = pb.matrix_basis - I
print('matrix_basis max deviation from identity:', max(abs(v) for row in diff for v in row))
print('bone.matrix_local head col:', tuple(round(v,3) for v in pb.bone.matrix_local.col[3][:3]))
print('rest head_local:', tuple(round(v,3) for v in pb.bone.head_local))
