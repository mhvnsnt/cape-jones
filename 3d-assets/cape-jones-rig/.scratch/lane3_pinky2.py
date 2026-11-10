import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
vg_names = [v.name for v in mesh.vertex_groups]
for bn in ["finger_pinky_1_R","finger_pinky_2_R","finger_pinky_3_R","finger_ring_3_R","finger_thumb_2_R","finger_thumb_2_L","finger_index_1_L","finger_index_2_L","finger_index_3_L"]:
    gid = vg_names.index(bn)
    cnt = sum(1 for v in me.vertices for g in v.groups if g.group==gid and g.weight>=0.5)
    print(f"{bn}: {cnt}")
