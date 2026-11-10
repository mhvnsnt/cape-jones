"""Check body collection and material for Cycles."""
import bpy
body = bpy.data.objects.get("CapeJones_Body")
print(f"users_collection: {[c.name for c in body.users_collection]}", flush=True)
# check view layer
vl = bpy.context.view_layer
print(f"body in view layer: {body.name in vl.objects}", flush=True)
# material
if body.data.materials:
    mat = body.data.materials[0]
    print(f"material: {mat.name}, use_nodes={mat.use_nodes}", flush=True)
    if mat.use_nodes:
        out = [n for n in mat.node_tree.nodes if n.type=='OUTPUT_MATERIAL']
        print(f"  material outputs: {len(out)}", flush=True)
else:
    print("no materials", flush=True)
print("DONE", flush=True)
