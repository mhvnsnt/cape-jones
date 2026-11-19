import bpy, bmesh, json, time, math
from collections import defaultdict

R = {}
D = math.radians

def union_find(n):
    p = list(range(n))
    def find(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: p[ra] = rb
    return find, union

body = bpy.data.objects["CapeJones_Body"]
cape = bpy.data.objects["CapeJones_Cape"]
rig = bpy.data.objects["CapeJones_Rig"]

# ---- modifier vgroup details
def modinfo(ob):
    out = []
    for md in ob.modifiers:
        d = {"name": md.name, "type": md.type}
        if md.type == "CORRECTIVE_SMOOTH":
            d["vertex_group"] = md.vertex_group
            d["invert"] = md.invert_vertex_group
        if md.type == "ARMATURE":
            d["vertex_group"] = md.vertex_group
        out.append(d)
    return out
R["body_mods"] = modinfo(body)
R["cape_mods"] = modinfo(cape)

# ---- vgroup weight stats
def vg_stats(ob, gname):
    if gname not in ob.vertex_groups:
        return None
    gi = ob.vertex_groups[gname].index
    n = 0; pts = []
    for v in ob.data.vertices:
        for g in v.groups:
            if g.group == gi and g.weight > 0.01:
                n += 1; pts.append(v.co)
                break
    if not pts:
        return {"count": 0}
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    return {"count": n, "bbox_min": [round(min(xs),3), round(min(ys),3), round(min(zs),3)],
            "bbox_max": [round(max(xs),3), round(max(ys),3), round(max(zs),3)]}
R["body_cape_mask"] = vg_stats(body, "cape_mask")
R["cape_cape_mask"] = vg_stats(cape, "cape_mask")
R["body_bbox"] = {"min": [round(min(v.co.x for v in body.data.vertices),3), round(min(v.co.y for v in body.data.vertices),3), round(min(v.co.z for v in body.data.vertices),3)],
                  "max": [round(max(v.co.x for v in body.data.vertices),3), round(max(v.co.y for v in body.data.vertices),3), round(max(v.co.z for v in body.data.vertices),3)]}
R["cape_bbox"] = {"min": [round(min(v.co.x for v in cape.data.vertices),3), round(min(v.co.y for v in cape.data.vertices),3), round(min(v.co.z for v in cape.data.vertices),3)],
                  "max": [round(max(v.co.x for v in cape.data.vertices),3), round(max(v.co.y for v in cape.data.vertices),3), round(max(v.co.z for v in cape.data.vertices),3)]}

# ---- body boundary components (count only)
bm = bmesh.new(); bm.from_mesh(body.data)
be = [e for e in bm.edges if len(e.link_faces) == 1]
R["body_boundary_edges"] = len(be)
bm.free()

# ---- cape islands + boundary loop classification
bm = bmesh.new(); bm.from_mesh(cape.data)
bm.faces.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.verts.ensure_lookup_table()
find, union = union_find(len(bm.faces))
for e in bm.edges:
    lf = e.link_faces
    if len(lf) == 2:
        union(lf[0].index, lf[1].index)
islands = defaultdict(int)
for f in bm.faces:
    islands[find(f.index)] += 1
R["cape_islands"] = {"count": len(islands), "sizes": sorted(islands.values(), reverse=True)[:12]}
boundary = [e for e in bm.edges if len(e.link_faces) == 1]
find2, union2 = union_find(len(bm.verts))
for e in boundary:
    union2(e.verts[0].index, e.verts[1].index)
loops = defaultdict(list)
for e in boundary:
    loops[find2(e.verts[0].index)].append(e)
loop_info = []
for root, es in loops.items():
    vs = set()
    for e in es:
        vs.add(e.verts[0].index); vs.add(e.verts[1].index)
    pts = [bm.verts[i].co for i in vs]
    cx = sum(p.x for p in pts)/len(pts); cy = sum(p.y for p in pts)/len(pts); cz = sum(p.z for p in pts)/len(pts)
    dx = max(p.x for p in pts)-min(p.x for p in pts); dy = max(p.y for p in pts)-min(p.y for p in pts); dz = max(p.z for p in pts)-min(p.z for p in pts)
    loop_info.append({"verts": len(vs), "centroid": [round(cx,3), round(cy,3), round(cz,3)],
                      "dims": [round(dx,3), round(dy,3), round(dz,3)]})
loop_info.sort(key=lambda d: -d["verts"])
R["cape_loops"] = loop_info
bm.free()

# ---- bone positions
bones = {}
for bn in ("root", "pelvis", "spine_1", "spine_2", "chest", "neck_1", "neck_2", "head",
           "thigh_fk_L", "foot_ik_L", "foot_ik_R", "upperarm_fk_L", "upperarm_fk_R"):
    b = rig.data.bones.get(bn)
    if b:
        bones[bn] = {"head": [round(v,3) for v in b.head_local], "tail": [round(v,3) for v in b.tail_local]}
R["bones"] = bones
# pose bone constraints summary for ik/fk switching insight
pb = {}
for bn in ("thigh_L", "thigh_ik_L", "upperarm_L", "upperarm_fk_L"):
    p = rig.pose.bones.get(bn)
    if p:
        pb[bn] = [{"type": c.type, "name": c.name} for c in p.constraints]
R["constraints"] = pb

# ---- timing: pose the rig, force eval
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="POSE")
pelv = rig.pose.bones["pelvis"]; pelv.rotation_mode = "XYZ"
pelv.location = (0.06, 0, -0.03); pelv.keyframe_insert("location", frame=1)
chst = rig.pose.bones["chest"]; chst.rotation_mode = "XYZ"
chst.rotation_euler = (0, D(12), 0); chst.keyframe_insert("rotation_euler", frame=1)
bpy.ops.object.mode_set(mode="OBJECT")
sc = bpy.context.scene
sc.frame_set(1)
t0 = time.time()
dg = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(dg); me = bpy.data.meshes.new_from_object(ev)
R["time_full_body_eval"] = round(time.time() - t0, 2)
R["full_body_eval_verts"] = len(me.vertices)
bpy.data.meshes.remove(me)
t0 = time.time()
dg = bpy.context.evaluated_depsgraph_get()
ev = cape.evaluated_get(dg); me = bpy.data.meshes.new_from_object(ev)
R["time_full_cape_eval"] = round(time.time() - t0, 2)
bpy.data.meshes.remove(me)

# decimated copies timing
def dec_copy(src, ratio, name):
    cp = src.copy(); cp.data = src.data.copy(); cp.name = name
    sc.collection.objects.link(cp)
    # strip corrective smooth for speed test purity, keep only decimate+armature
    for md in list(cp.modifiers):
        cp.modifiers.remove(md)
    dm = cp.modifiers.new("Dec", "DECIMATE"); dm.ratio = ratio; dm.use_collapse_triangulate = True
    if src == body:
        am = cp.modifiers.new("Arm", "ARMATURE"); am.object = rig
    return cp
t0 = time.time()
db = dec_copy(body, 0.10, "ProbeBodyDec")
dg = bpy.context.evaluated_depsgraph_get()
ev = db.evaluated_get(dg); me = bpy.data.meshes.new_from_object(ev)
R["time_dec_body_eval"] = round(time.time() - t0, 2)
R["dec_body_verts"] = len(me.vertices); R["dec_body_faces"] = len(me.polygons)
bpy.data.meshes.remove(me)
t0 = time.time()
dc = dec_copy(cape, 0.30, "ProbeCapeDec")
dg = bpy.context.evaluated_depsgraph_get()
ev = dc.evaluated_get(dg); me = bpy.data.meshes.new_from_object(ev)
R["time_dec_cape_eval_norig"] = round(time.time() - t0, 2)
R["dec_cape_verts"] = len(me.vertices); R["dec_cape_faces"] = len(me.polygons)
bpy.data.meshes.remove(me)

with open("/home/hatch/workspace/_cj-dance-v2/probe2.json", "w") as f:
    json.dump(R, f, indent=1)
print("PROBE2_DONE")
