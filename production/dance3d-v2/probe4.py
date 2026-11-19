import bpy, json

R = {}
sc = bpy.context.scene

def island_stats(src_name):
    src = bpy.data.objects[src_name]
    cp = src.copy(); cp.data = src.data.copy(); cp.name = "TmpIslands"
    sc.collection.objects.link(cp)
    # strip modifiers so separate works on raw mesh
    for md in list(cp.modifiers):
        cp.modifiers.remove(md)
    bpy.context.view_layer.objects.active = cp
    cp.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="LOOSE")
    bpy.ops.object.mode_set(mode="OBJECT")
    parts = [o for o in bpy.context.selected_objects if o.type == "MESH"]
    infos = []
    for o in parts:
        vs = o.data.vertices
        if not vs: continue
        xs = [v.co.x for v in vs]; ys = [v.co.y for v in vs]; zs = [v.co.z for v in vs]
        infos.append({"verts": len(vs),
                      "min": [round(min(xs),3), round(min(ys),3), round(min(zs),3)],
                      "max": [round(max(xs),3), round(max(ys),3), round(max(zs),3)]})
    infos.sort(key=lambda d: -d["verts"])
    for o in parts:
        bpy.data.objects.remove(o, do_unlink=True)
    return {"count": len(infos), "top": infos[:20]}

R["body"] = island_stats("CapeJones_Body")
R["cape"] = island_stats("CapeJones_Cape")
with open("/home/hatch/workspace/_cj-dance-v2/probe4.json", "w") as f:
    json.dump(R, f, indent=1)
print("PROBE4_DONE")
