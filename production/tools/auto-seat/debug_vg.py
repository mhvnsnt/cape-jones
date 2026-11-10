"""Check pelvis vertex group on full body."""
import bpy
body = bpy.data.objects.get("CapeJones_Body")
gi = body.vertex_groups["pelvis"].index
count = 0
maxw = 0
for v in body.data.vertices:
    for g in v.groups:
        if g.group == gi:
            maxw = max(maxw, g.weight)
            if g.weight > 0.6:
                count += 1
            break
print(f"pelvis verts weight>0.6: {count}, max weight: {maxw:.3f}", flush=True)
print("DONE", flush=True)
