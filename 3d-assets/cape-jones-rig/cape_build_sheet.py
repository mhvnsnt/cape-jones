"""LANE 1 CAPE REBUILD — Step 1: build the single-sheet cape.
Reads CapeJones_Cape fragments -> extracts width profile per z ->
builds ONE clean quad sheet in the exact same space:
  - z 0.10..0.433 : fragment (xmin,xmax) per z-band, y = frag plane + hang
  - z 0.433..0.78 : taper to shoulder width (+-0.24), y follows back + clearance
Pin group 'cape_pin' for z > 0.68. Black #000000 material.
Old fragments -> hidden collection 'CapeFragments_OLD' (provenance, not deleted).
Saves to cape_jones_rigged_w5r_idle_cape_STEP1.blend (original untouched)."""
import bpy, os
from mathutils import Vector

BLEND = 'cape_jones_rigged_w5r_idle.blend'
OUT = os.path.join(os.getcwd(), 'cape_jones_rigged_w5r_idle_cape_STEP1.blend')

old = bpy.data.objects['CapeJones_Cape']
me = old.data
mw = old.matrix_world  # identity, but be safe

# ---- 1. fragment width profile per z-band ----
NB = 40
zmin, zmax = 0.10, 0.435
bands = [[] for _ in range(NB)]
for v in me.vertices:
    w = mw @ v.co
    b = int((w.z - zmin) / (zmax - zmin) * NB)
    b = max(0, min(NB - 1, b))
    bands[b].append((w.x, w.y))
prof = []  # (zmid, xmin, xmax, ymid)
for i, b in enumerate(bands):
    zmid = zmin + (i + 0.5) / NB * (zmax - zmin)
    if b:
        xs = [p[0] for p in b]; ys = [p[1] for p in b]
        prof.append((zmid, min(xs), max(xs), sum(ys) / len(ys)))
    else:
        prof.append((zmid, None, None, None))
# fill gaps by interpolation
for i in range(NB):
    if prof[i][1] is None:
        lo = next((prof[j] for j in range(i - 1, -1, -1) if prof[j][1] is not None), None)
        hi = next((prof[j] for j in range(i + 1, NB) if prof[j][1] is not None), None)
        if lo and hi:
            t = (prof[i][0] - lo[0]) / (hi[0] - lo[0])
            prof[i] = (prof[i][0], lo[1] + t * (hi[1] - lo[1]),
                       lo[2] + t * (hi[2] - lo[2]), lo[3] + t * (hi[3] - lo[3]))
        elif lo:
            prof[i] = (prof[i][0], lo[1], lo[2], lo[3])
        elif hi:
            prof[i] = (prof[i][0], hi[1], hi[2], hi[3])
print("FRAGMENT PROFILE (z, xmin, xmax, ymid):")
for z, xn, xx, ym in prof[::5]:
    print(f"  z={z:.3f} x[{xn:.3f},{xx:.3f}] ymid={ym:.3f}")

# body back surface function (measured 2026-10-17, idle pose)
BACK = [(0.10, 0.052), (0.15, 0.101), (0.20, 0.101), (0.25, 0.101), (0.30, 0.102),
        (0.35, 0.102), (0.40, 0.101), (0.45, 0.100), (0.50, 0.097), (0.60, 0.089),
        (0.70, 0.089), (0.75, 0.080), (0.80, 0.064)]
def back_y(z):
    if z <= BACK[0][0]:
        return BACK[0][1]
    for (z0, y0), (z1, y1) in zip(BACK, BACK[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return y0 + t * (y1 - y0)
    return BACK[-1][1]

# ---- 2. sheet grid (rows follow sloped top edge; width from W(z)) ----
# Body-back x-extent measured 2026-10-17: z0.68:+-0.192, z0.72:+-0.201,
# z0.74-0.76:+-0.204, z0.78:+-0.150, z0.80:+-0.135
NZ, NX = 48, 36
X_TOP_HALF = 0.205
BOT_W = None  # set after prof_at defined

def prof_at(z):
    for i in range(NB - 1):
        if prof[i][0] <= z <= prof[i + 1][0]:
            t = (z - prof[i][0]) / (prof[i + 1][0] - prof[i][0] + 1e-9)
            _, xn0, xx0, _ = prof[i]; _, xn1, xx1, _ = prof[i + 1]
            return (xn0 + t * (xn1 - xn0), xx0 + t * (xx1 - xx0))
    return (prof[0][1], prof[0][2]) if z < prof[0][0] else (prof[-1][1], prof[-1][2])

BOT_W = prof_at(0.146)  # hold full fragment width at bottom (ignore debris taper)

def width_at(z):
    """Cape half-width at height z: fragment profile -> measured body back."""
    if z <= 0.435:
        if z < 0.14:
            xn, xx = BOT_W
        else:
            xn, xx = prof_at(z)
            xn -= 0.004; xx += 0.004
        return (xx - xn) / 2.0
    pts = [(0.435, 0.149), (0.60, 0.170), (0.68, 0.193), (0.72, 0.202),
           (0.76, 0.205), (0.78, 0.151)]
    if z >= pts[-1][0]:
        return pts[-1][1]
    for (z0, w0), (z1, w1) in zip(pts, pts[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return w0 + t * (w1 - w0)
    return pts[0][1]

def z_top_at(x):
    ax = abs(x)
    if ax <= 0.15:
        return 0.78
    return 0.78 - ((ax - 0.15) / 0.055) * 0.045  # 0.78 -> 0.735 at |x|=0.205

verts, faces = [], []
for r in range(NZ):
    f = r / (NZ - 1)  # 0 top -> 1 bottom
    for c in range(NX):
        xf = c / (NX - 1)
        x_top = -X_TOP_HALF + xf * 2 * X_TOP_HALF
        zt = z_top_at(x_top)
        z = zt * (1 - f) + 0.10 * f
        W = width_at(z)
        x = -W + xf * 2 * W
        if z > 0.68:
            y = back_y(z) + 0.008  # pinned: sits on the body
        elif z < 0.16:
            y = back_y(0.16) + 0.018  # hang straight below buttocks curve
        else:
            y = back_y(z) + 0.018
        verts.append((x, y, z))
for r in range(NZ - 1):
    for c in range(NX - 1):
        a = r * NX + c; b = a + 1; d = a + NX; e = d + 1
        faces.append((a, d, e, b))

mesh = bpy.data.meshes.new('CapeJones_Cape_Sheet_Mesh')
mesh.from_pydata(verts, [], faces)
mesh.update()
new = bpy.data.objects.new('CapeJones_Cape_NEW', mesh)
bpy.context.scene.collection.objects.link(new)
print(f"BUILT sheet: {len(verts)} verts, {len(faces)} quads")

# ---- 3. pin vertex group (shoulders, z > 0.68) ----
vg = new.vertex_groups.new(name='cape_pin')
for i, (x, y, z) in enumerate(verts):
    if z > 0.68:
        vg.add([i], 1.0, 'REPLACE')
print(f"pin group verts: z>0.68")

# ---- 4. black material #000000 ----
mat = bpy.data.materials.get('Cape_Black')
if mat is None:
    mat = bpy.data.materials.new('Cape_Black')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.85
if new.data.materials:
    new.data.materials[0] = mat
else:
    new.data.materials.append(mat)

# ---- 5. retire old fragments (hidden collection, NOT deleted) ----
coll = bpy.data.collections.get('CapeFragments_OLD')
if coll is None:
    coll = bpy.data.collections.new('CapeFragments_OLD')
    coll.hide_viewport = True
    coll.hide_render = True
    bpy.context.scene.collection.children.link(coll)
for c in old.users_collection:
    c.objects.unlink(old)
coll.objects.link(old)
old.name = 'CapeJones_Cape_FRAGMENTS_OLD'
old.hide_viewport = True
old.hide_render = True
new.name = 'CapeJones_Cape'
print("old fragments retired to hidden collection CapeFragments_OLD")

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print(f"SAVED {OUT}")
