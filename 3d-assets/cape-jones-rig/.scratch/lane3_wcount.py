"""Lane 3: check which finger bones have verts after v4."""
import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
vg_names = [v.name for v in mesh.vertex_groups]
for bn in sorted([b.name for b in bpy.data.objects["CapeJones_Rig"].pose.bones if b.name.startswith("finger_")]):
    gid = vg_names.index(bn)
    cnt = 0
    for v in me.vertices:
        for g in v.groups:
            if g.group == gid and g.weight >= 0.5:
                cnt += 1
                break
    print(f"{bn}: {cnt} verts w>=0.5")
