"""Save pelvis vert indices to file."""
import bpy
body = bpy.data.objects.get("CapeJones_Body")
gi = body.vertex_groups["pelvis"].index
idx = [v.index for v in body.data.vertices for g in v.groups if g.group == gi and g.weight > 0.6]
with open("/tmp/pelvis_idx.txt", "w") as f:
    f.write(",".join(map(str, idx)))
print(f"saved {len(idx)} indices", flush=True)
