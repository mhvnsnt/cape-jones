"""Lane 3: inspect materials on CapeJones_Body."""
import bpy, sys
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
mesh = bpy.data.objects["CapeJones_Body"]
print("OBJECT:", mesh.name, "material slots:", len(mesh.material_slots))
for i, s in enumerate(mesh.material_slots):
    m = s.material
    print(f"  slot {i}: {m.name if m else None} library={m.library.filepath if m and m.library else None}")
print("num materials total:", len(bpy.data.materials))
for m in bpy.data.materials:
    lib = m.library.filepath if m.library else None
    uses = sum(1 for o in bpy.data.objects if o.type == 'MESH' and any(s.material == m for s in o.material_slots))
    print(f"  {m.name} lib={lib} users_on_meshes={uses} use_nodes={m.use_nodes}")
    if m.use_nodes:
        outs = [n for n in m.node_tree.nodes if n.type == 'OUTPUT_MATERIAL']
        print("    outputs:", [(n.name, [l.from_node.name for l in n.inputs['Surface'].links]) for n in outs])
        print("    node types:", sorted(set(n.type for n in m.node_tree.nodes)))
        # color attribute usage?
        for n in m.node_tree.nodes:
            if n.type in ('ATTRIBUTE', 'VERTEX_COLOR', 'TEX_IMAGE', 'TEX_COORD', 'UVMAP'):
                print("    special node:", n.type, n.name, getattr(n, 'attribute_name', getattr(n, 'image', '')))
