import bpy, bmesh, json, time, sys

out = {"objects": [], "meshes": {}, "armatures": {}, "cape_diag": {}, "timing": {}}

for ob in bpy.data.objects:
    out["objects"].append({"name": ob.name, "type": ob.type,
                            "parent": ob.parent.name if ob.parent else None,
                            "hide_render": ob.hide_render})
    if ob.type == "ARMATURE":
        out["armatures"][ob.name] = [b.name for b in ob.data.bones]

for name in ("CapeJones_Body", "CapeJones_Cape"):
    ob = bpy.data.objects.get(name)
    if not ob:
        out["meshes"][name] = "MISSING"
        continue
    me = ob.data
    d = {"verts": len(me.vertices), "edges": len(me.edges), "polys": len(me.polygons),
         "materials": [m.name if m else None for m in me.materials],
         "vgroups": [g.name for g in ob.vertex_groups],
         "modifiers": [], "parent": ob.parent.name if ob.parent else None,
         "parent_bone": ob.parent_bone if hasattr(ob, "parent_bone") else ""}
    for md in ob.modifiers:
        md_info = {"name": md.name, "type": md.type, "show_render": md.show_render}
        if md.type == "SUBSURF":
            md_info["levels"] = md.levels; md_info["render_levels"] = md.render_levels
        if md.type == "ARMATURE":
            md_info["object"] = md.object.name if md.object else None
        if md.type == "MESH_DEFORM":
            md_info["object"] = md.object.name if md.object else None
            md_info["precision"] = md.precision
        if md.type == "CORRECTIVE_SMOOTH":
            md_info["iterations"] = md.iterations; md_info["factor"] = md.factor
        d["modifiers"].append(md_info)
    out["meshes"][name] = d

# cape geometry diagnostics
cape = bpy.data.objects.get("CapeJones_Cape")
if cape:
    bm = bmesh.new(); bm.from_mesh(cape.data)
    bm.edges.ensure_lookup_table(); bm.verts.ensure_lookup_table()
    boundary = [e for e in bm.edges if len(e.link_faces) == 1]
    nonman = [e for e in bm.edges if len(e.link_faces) > 2]
    zero_faces = [f for f in bm.faces if f.calc_area() < 1e-10]
    # connected components of boundary edges (by shared verts)
    from collections import defaultdict
    adj = defaultdict(set)
    for e in boundary:
        a, b = e.verts[0].index, e.verts[1].index
        adj[a].add(b); adj[b].add(a)
    seen = set(); comps = 0; comp_sizes = []
    for v in list(adj.keys()):
        if v in seen: continue
        comps += 1; stack = [v]; seen.add(v); n = 0
        while stack:
            x = stack.pop(); n += 1
            for y in adj[x]:
                if y not in seen:
                    seen.add(y); stack.append(y)
        comp_sizes.append(n)
    out["cape_diag"] = {"boundary_edges": len(boundary), "boundary_components": comps,
                        "boundary_comp_vert_counts": sorted(comp_sizes, reverse=True)[:10],
                        "nonmanifold_edges": len(nonman), "zero_area_faces": len(zero_faces),
                        "total_faces": len(bm.faces), "total_verts": len(bm.verts)}
    bm.free()
    # material node summary for cape
    mats = []
    for m in cape.data.materials:
        if not m: continue
        md = {"name": m.name, "blend_method": getattr(m, "blend_method", "?"),
              "use_nodes": m.use_nodes, "nodes": []}
        if m.use_nodes:
            for n in m.node_tree.nodes:
                nd = {"type": n.type, "name": n.name}
                if n.type == "TEX_IMAGE":
                    nd["image"] = n.image.name if n.image else None
                md["nodes"].append(nd)
            # alpha links into principled
            for n in m.node_tree.nodes:
                if n.type == "BSDF_PRINCIPLED":
                    al = n.inputs["Alpha"]
                    md["alpha_linked"] = bool(al.links)
                    md["alpha_default"] = al.default_value
        mats.append(md)
    out["cape_diag"]["materials"] = mats

# timing: full eval of body+cape at two frames
sc = bpy.context.scene
t0 = time.time()
sc.frame_set(1)
dg = bpy.context.evaluated_depsgraph_get()
ev = bpy.data.objects["CapeJones_Body"].evaluated_get(dg)
me1 = bpy.data.meshes.new_from_object(ev)
out["timing"]["eval_frame1_s"] = round(time.time() - t0, 2)
out["timing"]["eval_body_verts"] = len(me1.vertices)
bpy.data.meshes.remove(me1)
t0 = time.time()
sc.frame_set(7)
dg = bpy.context.evaluated_depsgraph_get()
ev = bpy.data.objects["CapeJones_Body"].evaluated_get(dg)
me2 = bpy.data.meshes.new_from_object(ev)
out["timing"]["eval_frame7_s"] = round(time.time() - t0, 2)
bpy.data.meshes.remove(me2)

with open("/home/hatch/workspace/_cj-dance-v2/probe.json", "w") as f:
    json.dump(out, f, indent=1)
print("PROBE_DONE")
