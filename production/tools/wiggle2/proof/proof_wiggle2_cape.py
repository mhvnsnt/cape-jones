"""Wiggle 2 headless proof (v2): sequential play, rigid-vs-wiggle A/B, bake verify, renders."""
import bpy, math, os
from mathutils import Vector

OUT = '/tmp/rigpull/proof'
os.makedirs(OUT, exist_ok=True)
ADDON = '/tmp/rigpull/wiggle2/wiggle_2.py'

bpy.ops.preferences.addon_install(filepath=ADDON, overwrite=True)
bpy.ops.preferences.addon_enable(module='wiggle_2')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# armature: root + 8-bone chain hanging down -Z
bpy.ops.object.armature_add(enter_editmode=True)
arm = bpy.context.object
arm.name = 'CapeChain'
eb = arm.data.edit_bones
eb[0].name = 'cape_root'
eb[0].head = (0, 0, 1.35); eb[0].tail = (0, 0, 1.2)
parent = 'cape_root'
for i in range(1, 9):
    b = eb.new('cape_%d' % i)
    b.head = (0, 0, 1.2 - 0.15 * (i - 1))
    b.tail = (0, 0, 1.2 - 0.15 * i)
    b.parent = eb[parent]
    b.use_connect = (i > 1)
    parent = 'cape_%d' % i
bpy.ops.object.mode_set(mode='OBJECT')

# proxy cape: grid plane, rows bound to bones
mesh = bpy.data.meshes.new('CapeMesh')
cape = bpy.data.objects.new('CapeMesh', mesh)
bpy.context.collection.objects.link(cape)
cols, rows = 5, 9
verts, faces = [], []
for r in range(rows):
    z = 1.2 - 0.15 * r
    for c in range(cols):
        verts.append((-0.2 + 0.1 * c, 0, z))
for r in range(rows - 1):
    for c in range(cols - 1):
        a = r * cols + c
        faces.append((a, a + 1, a + 1 + cols, a + cols))
mesh.from_pydata(verts, [], faces)
mesh.update()
bone_for_row = ['cape_root'] + ['cape_%d' % i for i in range(1, 9)]
for r in range(rows):
    g = cape.vertex_groups.new(name=bone_for_row[r])
    g.add([r * cols + c for c in range(cols)], 1.0, 'REPLACE')
mod = cape.modifiers.new('Armature', 'ARMATURE')
mod.object = arm
cape.parent = arm
mat = bpy.data.materials.new('CapeMat')
mat.use_nodes = True
mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.55, 0.08, 0.1, 1)
cape.data.materials.append(mat)

# camera + light
bpy.ops.object.camera_add(location=(0, -3.4, 0.7), rotation=(math.radians(80), 0, 0))
bpy.context.scene.camera = bpy.context.object
bpy.ops.object.light_add(type='SUN', location=(2, -2, 4))

# swing on cape_root (bone-local Z == armature Y): -25 .. +25 .. -25 deg
scn = bpy.context.scene
scn.frame_start = 1; scn.frame_end = 40
pb = arm.pose.bones['cape_root']
pb.rotation_mode = 'XYZ'
for f, deg in ((1, -25), (20, 25), (40, -25)):
    pb.rotation_euler = (0, 0, math.radians(deg))
    pb.keyframe_insert(data_path='rotation_euler', frame=f)

def tip_x():
    """World x of cape_4's tail via evaluated pose matrix (reflects sim)."""
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    ob = arm.evaluated_get(dg)
    b = ob.pose.bones['cape_4']
    return (ob.matrix_world @ (b.matrix @ Vector((0, b.length, 0)))).x

def play(wiggle_on):
    scn.wiggle_enable = True
    bpy.ops.wiggle.reset()
    scn.wiggle_enable = wiggle_on
    out = {}
    for f in range(1, 41):
        scn.frame_set(f)
        if f in (10, 20, 30):
            out[f] = round(tip_x(), 4)
    return out

# wiggle params (POSE mode + selection: addon update-callback needs it)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.select_all(action='DESELECT')
for i in range(1, 9):
    arm.data.bones['cape_%d' % i].select = True
for i in range(1, 9):
    b = arm.pose.bones['cape_%d' % i]
    b.wiggle_tail = True
    b.wiggle_enable = True
    b.wiggle_stiff = 60.0
    b.wiggle_damp = 0.5
    b.wiggle_gravity = 1.0
bpy.ops.object.mode_set(mode='OBJECT')

rigid = play(False)
print('RIGID tip x:', rigid, flush=True)
wig = play(True)
print('WIGGLE tip x:', wig, flush=True)
lag = {f: round(rigid[f] - wig[f], 4) for f in rigid}
print('LAG (rigid - wiggle):', lag, flush=True)
print('WIGGLE LAG CONFIRMED:', 'YES' if any(abs(v) > 0.03 for v in lag.values()) else 'NO', flush=True)

# --- bake ---
bpy.context.view_layer.objects.active = arm
arm.select_set(True)
bpy.ops.object.mode_set(mode='POSE')
scn.wiggle.preroll = 5
scn.wiggle.bake_overwrite = True  # bake wiggle INTO the current action (keeps root swing)
scn.wiggle_enable = True
try:
    bpy.ops.wiggle.bake()
    print('BAKE: OK', flush=True)
except Exception as e:
    print('BAKE FAIL:', e, flush=True)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.wiggle.reset()
scn.wiggle_enable = False
baked = {}
for f in range(1, 41):
    scn.frame_set(f)
    if f in (10, 20, 30):
        baked[f] = round(tip_x(), 4)
print('BAKED tip x:', baked, flush=True)
print('BAKE MATCHES SIM:', 'YES' if all(abs(baked[f] - wig[f]) < 0.03 for f in baked) else 'NO', flush=True)

# --- renders (Cycles CPU) ---
scn.render.engine = 'CYCLES'
scn.cycles.device = 'CPU'
scn.cycles.samples = 8
scn.render.resolution_x = 320; scn.render.resolution_y = 240
for f in (10, 20, 30):
    scn.frame_set(f)
    scn.render.filepath = os.path.join(OUT, 'wiggle_cape_f%02d.png' % f)
    bpy.ops.render.render(write_still=True)
    print('RENDERED', scn.render.filepath, flush=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'wiggle2_cape_proof.blend'))
print('PROOF DONE', flush=True)
