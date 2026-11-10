"""Mathematical pose verification: check cage verts move correctly."""
import bpy, math
from mathutils import Vector
print('START', flush=True)
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_clean.blend')
print('LOADED', flush=True)
arm = bpy.data.objects['CapeJones_Rig']
cage = bpy.data.objects['BlenRigMdefCage']
scn = bpy.context.scene
for o in (arm, cage):
    if o.name not in scn.collection.objects:
        scn.collection.objects.link(o)
bpy.context.view_layer.update()

def get_cage_vert(i):
    deps = bpy.context.evaluated_depsgraph_get()
    ce = deps.objects.get(cage.name)
    return Vector(ce.data.vertices[i].co)

def reset_pose():
    for pb in arm.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
    bpy.context.view_layer.update()

D = math.radians
# Test: arms raised - check a cage vert near the left arm
# Find cage vert near elbow (0.376, -0.034, 0.722)
reset_pose()
deps = bpy.context.evaluated_depsgraph_get()
ce = deps.objects.get(cage.name)
best_i, best_d = -1, 1e9
for i, v in enumerate(ce.data.vertices):
    d = (v.co - Vector((0.376, -0.034, 0.722))).length
    if d < best_d:
        best_d, best_i = d, i
v_rest = get_cage_vert(best_i)
print(f'cage vert {best_i} rest: {tuple(round(v,3) for v in v_rest)}', flush=True)
# raise arm
arm.pose.bones['upperarm_fk_L'].rotation_mode = 'XYZ'
arm.pose.bones['upperarm_fk_L'].rotation_euler = (D(80), 0, 0)
bpy.context.view_layer.update()
v_pos = get_cage_vert(best_i)
print(f'cage vert {best_i} raised: {tuple(round(v,3) for v in v_pos)}', flush=True)
moved = (v_pos - v_rest).length
print(f'moved: {moved:.3f}m', 'PASS' if moved > 0.05 else 'FAIL', flush=True)
# Test: elbow bend
reset_pose()
# find vert near wrist
best_i, best_d = -1, 1e9
for i, v in enumerate(ce.data.vertices):
    d = (v.co - Vector((0.484, -0.045, 0.718))).length
    if d < best_d:
        best_d, best_i = d, i
v_rest = get_cage_vert(best_i)
arm.pose.bones['forearm_fk_L'].rotation_mode = 'XYZ'
arm.pose.bones['forearm_fk_L'].rotation_euler = (0, 0, D(-90))
bpy.context.view_layer.update()
v_pos = get_cage_vert(best_i)
moved = (v_pos - v_rest).length
print(f'elbow bend: moved {moved:.3f}m', 'PASS' if moved > 0.05 else 'FAIL', flush=True)
print('VERIFY DONE', flush=True)
