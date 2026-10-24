import bpy

body = bpy.data.objects.get("CapeJones_Body")
if body:
    print(f"=== VERTEX GROUPS ({len(body.vertex_groups)}) ===")
    for vg in body.vertex_groups:
        print(f"  {vg.name}")
    
    print(f"\n=== VERTEX COLORS ===")
    if body.data.color_attributes:
        for ca in body.data.color_attributes:
            print(f"  {ca.name} ({ca.domain}, {ca.data_type})")
    else:
        print("  None")
    
    print(f"\n=== UV LAYERS ===")
    for uv in body.data.uv_layers:
        print(f"  {uv.name}")
    
    print(f"\n=== SHAPE KEYS ===")
    if body.data.shape_keys:
        for kb in body.data.shape_keys.key_blocks:
            print(f"  {kb.name}")
    else:
        print("  None")
