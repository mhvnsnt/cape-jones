"""Check evaluated mesh."""
import bpy
scn = bpy.context.scene
scn.frame_set(41)
bpy.context.view_layer.update()
body = bpy.data.objects.get("CapeJones_Body")
print(f"original verts: {len(body.data.vertices)}", flush=True)
deps = bpy.context.evaluated_depsgraph_get()
pm = body.evaluated_get(deps)
mesh = pm.to_mesh()
print(f"evaluated verts: {len(mesh.vertices)}", flush=True)
zs = [v.co.z for v in mesh.vertices]
print(f"eval Z range: {min(zs):.3f} to {max(zs):.3f}", flush=True)
pm.to_mesh_clear()
print("DONE", flush=True)
