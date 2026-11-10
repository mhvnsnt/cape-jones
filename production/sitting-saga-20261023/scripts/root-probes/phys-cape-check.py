import bpy
import numpy as np

cape = bpy.data.objects.get("CapeJones_Cape_Cloth")
if cape:
    verts = np.array([cape.matrix_world @ v.co for v in cape.data.vertices])
    print(f"Cape verts: {len(verts)}")
    print(f"World bbox min: {verts.min(0).round(3)}")
    print(f"World bbox max: {verts.max(0).round(3)}")
    print(f"Size: {(verts.max(0) - verts.min(0)).round(3)}")
    
    # Where's the character? Get body bounds
    body = bpy.data.objects.get("CapeJones_Body")
    if body:
        # Sample verts (too many for all)
        import random
        sample_idx = random.sample(range(len(body.data.vertices)), min(10000, len(body.data.vertices)))
        bverts = np.array([body.matrix_world @ body.data.vertices[i].co for i in sample_idx])
        print(f"\nBody (sampled) bbox min: {bverts.min(0).round(3)}")
        print(f"Body (sampled) bbox max: {bverts.max(0).round(3)}")
