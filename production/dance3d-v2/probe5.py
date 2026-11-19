import bpy, json, math, os, time
import numpy as np
D = math.radians
OUT = "/home/hatch/workspace/_cj-dance3d-v2/check"
os.makedirs(OUT, exist_ok=True)

# ---------- part 1: hem zoom renders
for name in ("MPFB_ReferenceBody", "MPFB_FullSkeleton", "BlenRigMdefCage"):
    ob = bpy.data.objects.get(name)
    if ob: ob.hide_render = True
sc = bpy.context.scene
if not sc.world:
    sc.world = bpy.data.worlds.new("W"); sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.6, 0.8, 1)
bpy.ops.object.light_add(type="SUN", location=(1, -1, 3))
sun = bpy.context.active_object; sun.data.energy = 3.0; sun.rotation_euler = (D(40), 0, D(20))
bpy.ops.object.light_add(type="AREA", location=(0, -2, 1))
fl = bpy.context.active_object; fl.data.energy = 200; fl.data.size = 2.0; fl.rotation_euler = (D(90), 0, 0)
sc.render.engine = "BLENDER_EEVEE"; sc.eevee.taa_render_samples = 1
sc.render.resolution_x = 960; sc.render.resolution_y = 540

def shot(loc, rot, lens, tag, show_body, show_cape):
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    cam = bpy.context.active_object; cam.data.lens = lens; sc.camera = cam
    bpy.data.objects["CapeJones_Body"].hide_render = not show_body
    bpy.data.objects["CapeJones_Cape"].hide_render = not show_cape
    sc.render.filepath = os.path.join(OUT, tag + ".png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    print("SHOT", tag, flush=True)

shot((0, 1.0, 0.30), (D(85), 0, D(180)), 55, "hem_back_both", True, True)
shot((0, 1.0, 0.30), (D(85), 0, D(180)), 55, "hem_back_bodyonly", True, False)
bpy.data.objects["CapeJones_Body"].hide_render = False
bpy.data.objects["CapeJones_Cape"].hide_render = False

# ---------- part 2: island analysis (data-space union-find)
def islands(mesh):
    nv = len(mesh.vertices)
    nl = len(mesh.loops)
    lv = np.empty(nl, dtype=np.int64)
    mesh.loops.foreach_get("vertex_index", lv)
    npol = len(mesh.polygons)
    ls = np.empty(npol, dtype=np.int64); lt = np.empty(npol, dtype=np.int64)
    mesh.polygons.foreach_get("loop_start", ls)
    mesh.polygons.foreach_get("loop_total", lt)
    parent = np.arange(nv, dtype=np.int64)
    def find(x):
        r = x
        while parent[r] != r:
            r = parent[r]
        while parent[x] != r:
            parent[x], x = r, parent[x]
        return r
    t0 = time.time()
    for p in range(npol):
        s = ls[p]; t = lt[p]
        if t < 2: continue
        a = lv[s]
        ra = find(a)
        for j in range(s + 1, s + t):
            rb = find(lv[j])
            if rb != ra:
                parent[rb] = ra
    roots = np.empty(nv, dtype=np.int64)
    for i in range(nv):
        roots[i] = find(i)
    uniq, counts = np.unique(roots, return_counts=True)
    order = np.argsort(-counts)
    co = np.empty(nv * 3, dtype=np.float32)
    mesh.vertices.foreach_get("co", co)
    co = co.reshape(nv, 3)
    top = []
    for k in order[:25]:
        r = uniq[k]
        mask = roots == r
        pts = co[mask]
        top.append({"verts": int(counts[k]),
                    "min": [round(float(pts[:, i].min()), 3) for i in range(3)],
                    "max": [round(float(pts[:, i].max()), 3) for i in range(3)]})
    return {"island_count": int(len(uniq)), "top": top, "union_s": round(time.time() - t0, 1)}

R = {}
R["body"] = islands(bpy.data.objects["CapeJones_Body"].data)
R["cape"] = islands(bpy.data.objects["CapeJones_Cape"].data)
with open("/home/hatch/workspace/_cj-dance3d-v2/probe5.json", "w") as f:
    json.dump(R, f, indent=1)
print("PROBE5_DONE")
