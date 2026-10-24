import bpy

body = bpy.data.objects.get("CapeJones_Body")
if body:
    print(f"Body verts: {len(body.data.vertices)}")
    print(f"\n=== MATERIALS ({len(body.data.materials)}) ===")
    for i, mat in enumerate(body.data.materials):
        if mat:
            # Get base color
            bsdf = None
            if mat.use_nodes:
                for n in mat.node_tree.nodes:
                    if n.type == 'BSDF_PRINCIPLED':
                        bsdf = n
                        break
            color = "?"
            if bsdf and 'Base Color' in bsdf.inputs:
                c = bsdf.inputs['Base Color'].default_value
                color = f"({c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f})"
            print(f"  [{i}] {mat.name} color={color}")
        else:
            print(f"  [{i}] None")
    
    # Count faces per material
    from collections import Counter
    mat_counts = Counter()
    for p in body.data.polygons:
        mat_counts[p.material_index] += 1
    print(f"\n=== FACES PER MATERIAL ===")
    for mi, count in sorted(mat_counts.items()):
        mat = body.data.materials[mi] if mi < len(body.data.materials) else None
        print(f"  [{mi}] {mat.name if mat else 'None'}: {count} faces")
