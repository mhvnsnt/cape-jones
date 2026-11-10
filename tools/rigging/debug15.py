"""Test: bake one control's ON-mode final as pose, then OFF. Measure error."""
import bpy
from mathutils import Matrix
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_raw.blend')
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

# quick fit of just the arm guides (reuse warp? no -- do minimal: scale rest + set 3 guides)
# Actually simpler: use the already-fitted ON state from blenrig_fit logic is complex.
# Instead: manually move wrist_str_L in ON mode and see if baking the control works.
def set_repro(on):
    arm.data['reproportion'] = 1 if on else 0
    for pb in arm.pose.bones:
        for C in pb.constraints:
            if 'REPROP' in C.name:
                C.mute = not on
            elif 'NOREP' in C.name:
                C.mute = on
    bpy.context.view_layer.update()

set_repro(True)
# move wrist_str_L +0.1 x (simulate fitting)
ws = arm.pose.bones['wrist_str_L']
ws.location.x += 0.1
bpy.context.view_layer.update()
hm = arm.pose.bones['hand_ik_mstr_L']
M_on = hm.matrix.copy()
print('ON: hand_ik_mstr_L head', tuple(round(v,3) for v in hm.head))
# bake as pose: mb = rest.inverted() @ M_on
rb = arm.data.bones['hand_ik_mstr_L']
mb = rb.matrix_local.inverted() @ M_on
# now turn OFF and apply mb
set_repro(False)
hm.rotation_mode = 'QUATERNION'
hm.matrix_basis = mb
bpy.context.view_layer.update()
print('OFF baked: hand_ik_mstr_L head', tuple(round(v,3) for v in hm.head))
print('target was:', tuple(round(v,3) for v in (M_on.col[3][:3])))
err = (hm.head - M_on.col[3][:3]).length
print('err =', round(err, 4))
