"""Weld the cape's coincident shell boundaries into one continuous sheet.
Removes the independent-sliver ejection mode. Operates on a copy."""
import bpy
import bmesh

SRC = "/home/hatch/workspace/capebake-work/stage1_separated.blend"
OUT = "/home/hatch/workspace/capebake-work/stage1_welded.blend"
bpy.ops.wm.open_mainfile(filepath=SRC)
cape = bpy.data.objects["CapeJones_Cape"]
mesh = cape.data
print(f"cape verts before weld: {len(mesh.vertices)}", flush=True)

bm = bmesh.new()
bm.from_mesh(mesh)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0002)
print(f"bmesh verts after remove_doubles: {len(bm.verts)}", flush=True)
bm.to_mesh(mesh)
bm.free()
print(f"cape verts after weld: {len(mesh.vertices)}", flush=True)
assert len(mesh.vertices) < 282518, "no verts merged - unexpected"
assert len(mesh.vertices) > 150000, "merged away too much - abort"
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print(f"SAVED {OUT}", flush=True)
print("WELD DONE", flush=True)
