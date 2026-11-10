"""Lane 3: compare body textures across the 4 rig blends + test material nuke decisively."""
import bpy, sys
from mathutils import Vector, Matrix

BLENDS = [
    "cape_jones_rigged.blend",
    "cape_jones_rigged_w5r.blend",
    "cape_jones_rigged_w5r_clean.blend",
    "cape_jones_rigged_w5r_idle.blend",
]
BASE = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/"
for b in BLENDS:
    bpy.ops.wm.open_mainfile(filepath=BASE + b)
    mesh = bpy.data.objects.get("CapeJones_Body")
    if not mesh:
        print(b, "NO CapeJones_Body"); continue
    mats = [s.material.name if s.material else None for s in mesh.material_slots]
    imgs = []
    for img in bpy.data.images:
        if img.size[0] > 100:
            imgs.append(f"{img.name} {img.size[0]}x{img.size[1]} packed={img.packed_file is not None}")
    print(b, "| slots:", mats)
    for i in imgs[:6]:
        print("   ", i)

# decisive nuke test on idle blend
bpy.ops.wm.open_mainfile(filepath=BASE + "cape_jones_rigged_w5r_idle.blend")
for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nt = mat.node_tree
    outs = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL']
    for out in outs:
        for link in list(nt.links):
            if link.to_node == out:
                nt.links.remove(link)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = 1.0
        em.inputs["Color"].default_value = (1.0, 0.0, 0.0, 1.0)  # PURE RED: unmistakable
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
# verify
mat = bpy.data.objects["CapeJones_Body"].material_slots[0].material
nt = mat.node_tree
for link in nt.links:
    if link.to_node.type == 'OUTPUT_MATERIAL':
        print("POST-NUKE LINK:", link.from_node.name, "->", link.to_node.name, link.to_socket.name,
              "color:", tuple(round(v,2) for v in link.from_node.inputs['Color'].default_value))
