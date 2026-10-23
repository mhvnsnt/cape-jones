#!/usr/bin/env python3
"""Cape Jones weight bake-off driver (Blender 4.0.2 headless, xvfb-run).

Usage:
  blender -b --python bakeoff.py -- --entry W1 --poses all
  blender -b --python bakeoff.py -- --entry W5 --poses P3 --from-blend /path/W1.blend

Entries:
  W1 boneheat        Blender automatic weights (Bone Heat) on CJ-TEST skeleton
  W1p boneheat-proxy Bone Heat on decimated proxy, Data-Transfer to full mesh
  W2 envelope        Blender envelope weights on CJ-TEST skeleton
  W3 surfaceheat     Surface Heat Diffuse Skinning (meshonline, MIT) headless
  W4 brutalfist      brutalfist-fix auto_rig_humanoid.py end-to-end (own skeleton)
  W5 preservevol     W1 weights + Preserve Volume (DQ) + Corrective Smooth
  W6 twistbones      W1 weights + twist-bone chain (Copy Rotation Y, 0.5)
  W7 mdefcage        BlenRig-6-style mesh-deform cage skinning
  W7b mdefcage-dense  W7 with denser relaxed cage (~hundreds of verts)

Poses: P1 rest, P2 arms_raised, P3 elbow_90, P4 knee_deep, P5 shoulder_raise,
       P6 head_turn, P7 crouch
"""
import bpy, math, os, sys, time, subprocess
from mathutils import Vector

MODEL = '/home/hatch/workspace/cj-rev2-scratch/cape_jones_plain.glb'
SCRATCH = os.path.expanduser('~/workspace/weight-bakeoff-scratch')
BLEND_DIR = os.path.join(SCRATCH, 'blends')
PNG_DIR = os.path.join(SCRATCH, 'renders')
SHD_ADDON = os.path.expanduser('~/workspace/cape-jones-bakeoff/tools/weights/surface-heat-diffuse/addon/surface_heat_diffuse_skinning')
SHD_BIN = os.path.join(SHD_ADDON, 'bin', 'Linux', 'shd')

BONES = [
    ('root',       (0.0, 0.0, -0.05),  (0.0, 0.0, 0.05),   None),
    ('Hips',       (-0.03, 0.0, 0.03), (-0.03, 0.0, 0.12), 'root'),
    ('Spine',      (-0.015, 0.0, 0.12),(0.0, 0.0, 0.21),   'Hips'),
    ('Chest',      (0.0, 0.0, 0.21),   (0.015, 0.0, 0.30), 'Spine'),
    ('Neck',       (0.02, 0.0, 0.30),  (0.024, 0.0, 0.35), 'Chest'),
    ('Head',       (0.024, 0.0, 0.35), (0.036, 0.0, 0.47), 'Neck'),
    ('Shoulder.L', (0.015, 0.04, 0.28),(0.02, 0.11, 0.265),'Chest'),
    ('UpperArm.L', (0.02, 0.11, 0.265),(0.02, 0.27, 0.26), 'Shoulder.L'),
    ('ForeArm.L',  (0.02, 0.27, 0.26), (0.02, 0.40, 0.255),'UpperArm.L'),
    ('Hand.L',     (0.02, 0.40, 0.255),(0.02, 0.49, 0.255),'ForeArm.L'),
    ('Shoulder.R', (0.015, -0.04, 0.28),(0.02, -0.11, 0.265),'Chest'),
    ('UpperArm.R', (0.02, -0.11, 0.265),(0.02, -0.27, 0.26),'Shoulder.R'),
    ('ForeArm.R',  (0.02, -0.27, 0.26),(0.02, -0.40, 0.255),'UpperArm.R'),
    ('Hand.R',     (0.02, -0.40, 0.255),(0.02, -0.49, 0.255),'ForeArm.R'),
    ('Thigh.L',    (-0.03, 0.095, -0.02),(-0.035, 0.092, -0.185),'Hips'),
    ('Shin.L',     (-0.035, 0.092, -0.185),(-0.02, 0.091, -0.37),'Thigh.L'),
    ('Foot.L',     (-0.02, 0.091, -0.37),(0.10, 0.091, -0.44),'Shin.L'),
    ('Thigh.R',    (-0.03, -0.095, -0.02),(-0.035, -0.092, -0.185),'Hips'),
    ('Shin.R',     (-0.035, -0.092, -0.185),(-0.02, -0.091, -0.37),'Thigh.R'),
    ('Foot.R',     (-0.02, -0.091, -0.37),(0.10, -0.091, -0.44),'Shin.R'),
]

# pose: bone -> euler XYZ radians (best guesses; verified visually, see POSE_NOTES)
POSES = {
    'P1_rest': {},
    'P2_arms_raised': {
        'UpperArm.L': (1.50, 0, 0), 'UpperArm.R': (-1.50, 0, 0),
        'ForeArm.L': (0.20, 0, 0), 'ForeArm.R': (-0.20, 0, 0)},
    'P3_elbow_90': {
        'ForeArm.L': (0, 0, -1.65), 'ForeArm.R': (0, 0, -1.65)},
    'P4_knee_deep': {
        'Thigh.L': (0, 0, -1.90), 'Thigh.R': (0, 0, -1.90),
        'Shin.L': (0, 0, 0.50), 'Shin.R': (0, 0, 0.50),
        'root:loc': (0, 0, -0.18)},
    'P5_shoulder_raise': {
        'UpperArm.L': (0, 0, -1.50), 'UpperArm.R': (0, 0, -1.50)},
    'P6_head_turn': {
        'Head': (0, 1.00, 0)},
    'P7_crouch': {
        'root:loc': (0, 0, -0.22),
        'Thigh.L': (0, 0, -1.20), 'Thigh.R': (0, 0, -1.20),
        'Shin.L': (0, 0, 0.30), 'Shin.R': (0, 0, 0.30),
        'Spine': (0, 0, -0.35)},
}
POSE_ORDER = ['P1_rest', 'P2_arms_raised', 'P3_elbow_90', 'P4_knee_deep',
              'P5_shoulder_raise', 'P6_head_turn', 'P7_crouch']

# W4 bone-name map: brutalfist names -> our pose keys (best effort)
W4_MAP = {'LowerArm.L': 'ForeArm.L', 'LowerArm.R': 'ForeArm.R'}


def args_after_dd():
    argv = sys.argv
    return argv[argv.index('--') + 1:] if '--' in argv else []


def load_model():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=MODEL)
    mesh = max((o for o in bpy.data.objects if o.type == 'MESH'),
               key=lambda o: len(o.data.vertices))
    for o in list(bpy.data.objects):
        if o.type == 'MESH' and o != mesh:
            bpy.data.objects.remove(o)
    return mesh


def build_skeleton(name='CJ_TestRig'):
    arm = bpy.data.armatures.new(name)
    rig = bpy.data.objects.new(name, arm)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')
    ebs = {}
    for bname, head, tail, parent in BONES:
        eb = arm.edit_bones.new(bname)
        eb.head = Vector(head)
        eb.tail = Vector(tail)
        eb.use_deform = True
        ebs[bname] = eb
    for bname, head, tail, parent in BONES:
        if parent:
            ebs[bname].parent = ebs[parent]
    bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
    bpy.ops.object.mode_set(mode='OBJECT')
    return rig


def clay_material(mesh):
    mat = bpy.data.materials.new('clay')
    mat.use_nodes = True
    mesh.data.materials.clear()
    mesh.data.materials.append(mat)


def select_for_parent(mesh, rig):
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig


def weights_boneheat(mesh, rig):
    t = time.time()
    select_for_parent(mesh, rig)
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    print('W1 boneheat done in %.0fs' % (time.time() - t))


def weights_envelope(mesh, rig):
    t = time.time()
    select_for_parent(mesh, rig)
    bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
    print('W2 envelope done in %.0fs' % (time.time() - t))


def weights_boneheat_proxy(mesh, rig, ratio=0.08):
    """Bone Heat on a decimated proxy, weights transferred to the full mesh.
    Rescue variant for meshes where heat fails directly (W1)."""
    t = time.time()
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.duplicate()
    proxy = bpy.context.view_layer.objects.active
    proxy.name = 'CJ_Proxy'
    dec = proxy.modifiers.new('Decimate', 'DECIMATE')
    dec.ratio = ratio
    bpy.ops.object.modifier_apply(modifier=dec.name)
    print('W1p proxy verts: %d (%.0fs)' % (len(proxy.data.vertices), time.time() - t))
    t = time.time()
    select_for_parent(proxy, rig)
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    nw = sum(1 for v in proxy.data.vertices if v.groups)
    print('W1p proxy weighted verts: %d/%d (%.0fs)' % (nw, len(proxy.data.vertices), time.time() - t))
    # transfer vertex groups proxy -> full mesh
    t = time.time()
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select_set(True)
    proxy.select_set(True)
    bpy.context.view_layer.objects.active = mesh
    dt = mesh.modifiers.new('DataTransfer', 'DATA_TRANSFER')
    dt.object = proxy
    dt.use_vert_data = True
    dt.data_types_verts = {'VGROUP_WEIGHTS'}
    dt.vert_mapping = 'POLYINTERP_NEAREST'
    dt.mix_mode = 'REPLACE'
    bpy.ops.object.modifier_apply(modifier=dt.name)
    nw = sum(1 for v in mesh.data.vertices if v.groups)
    print('W1p full-mesh weighted verts: %d/%d (%.0fs)' % (nw, len(mesh.data.vertices), time.time() - t))
    bpy.data.objects.remove(proxy)
    mod = mesh.modifiers.new('Armature', 'ARMATURE')
    mod.object = rig


def weights_surface_heat(mesh, rig, resolution=128):
    t = time.time()
    data_dir = os.path.join(SCRATCH, 'shd')
    os.makedirs(data_dir, exist_ok=True)
    # mesh txt (world coords)
    with open(os.path.join(data_dir, 'untitled-mesh.txt'), 'w') as f:
        f.write('# surface heat diffuse mesh export.\n')
        for v in mesh.data.vertices:
            c = mesh.matrix_world @ v.co
            f.write('v,%f,%f,%f\n' % (c[0], c[1], c[2]))
        for poly in mesh.data.polygons:
            f.write('f' + ''.join(',%d' % mesh.data.loops[li].vertex_index
                                  for li in poly.loop_indices) + '\n')
    # bone txt (world coords, deform bones)
    with open(os.path.join(data_dir, 'untitled-bone.txt'), 'w') as f:
        f.write('# surface heat diffuse bone export.\n')
        for b in rig.data.bones:
            if b.use_deform:
                h = rig.matrix_world @ b.head_local
                t_ = rig.matrix_world @ b.tail_local
                f.write('b,%s,%f,%f,%f,%f,%f,%f\n' % (
                    b.name.replace(',', '\\;'), h[0], h[1], h[2], t_[0], t_[1], t_[2]))
    print('W3 txt written in %.0fs, running shd...' % (time.time() - t))
    t = time.time()
    # resolution, loops, samples, influence, falloff, sharpness, solidify
    r = subprocess.run([SHD_BIN, 'untitled-mesh.txt', 'untitled-bone.txt',
                        'untitled-weight.txt', str(resolution), '5', '64',
                        '8', '0.2', '3', 'n'],
                       cwd=data_dir, capture_output=True, text=True, timeout=3600)
    print('W3 shd rc=%d in %.0fs' % (r.returncode, time.time() - t))
    print('W3 shd tail:', (r.stdout or '')[-500:])
    if r.returncode != 0:
        raise RuntimeError('shd failed: ' + (r.stderr or '')[-500:])
    # read weights
    t = time.time()
    bones = []
    with open(os.path.join(data_dir, 'untitled-weight.txt')) as f:
        for line in f:
            tok = line.strip().split(',')
            if not tok or not tok[0]:
                continue
            if tok[0] == 'b':
                gname = tok[1].replace('\\;', ',')
                bones.append(gname)
                if mesh.vertex_groups.get(gname):
                    mesh.vertex_groups.remove(mesh.vertex_groups[gname])
                mesh.vertex_groups.new(name=gname)
            elif tok[0] == 'w':
                mesh.vertex_groups[bones[int(tok[2])]].add([int(tok[1])],
                                                           float(tok[3]), 'REPLACE')
    mod = mesh.modifiers.new('Armature', 'ARMATURE')
    mod.object = rig
    print('W3 weights applied in %.0fs, %d groups' % (time.time() - t, len(bones)))


def add_preserve_volume_and_smooth(mesh):
    arm_mod = next(m for m in mesh.modifiers if m.type == 'ARMATURE')
    arm_mod.use_deform_preserve_volume = True
    cs = mesh.modifiers.new('CorrectiveSmooth', 'CORRECTIVE_SMOOTH')
    cs.factor = 0.5
    cs.iterations = 3
    print('W5 modifiers added: preserve_volume + corrective_smooth')


def add_twist_bones(mesh, rig):
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')
    arm = rig.data
    twists = []
    for side in ('L', 'R'):
        for src, tgt, inf in (('UpperArm', 'ForeArm', 0.5), ('ForeArm', 'Hand', 0.5)):
            sb = arm.edit_bones[f'{src}.{side}']
            tb = arm.edit_bones.new(f'{src}Twist.{side}')
            tb.head = sb.head.lerp(sb.tail, 0.25)
            tb.tail = sb.head.lerp(sb.tail, 0.75)
            tb.parent = sb.parent
            tb.use_deform = True
            twists.append((f'{src}Twist.{side}', f'{tgt}.{side}', inf))
    bpy.ops.object.mode_set(mode='OBJECT')
    for tname, target, inf in twists:
        pb = rig.pose.bones[tname]
        c = pb.constraints.new('COPY_ROTATION')
        c.target = rig
        c.subtarget = target
        c.use_x = False
        c.use_y = True
        c.use_z = False
        c.influence = inf
        c.target_space = 'LOCAL'
        c.owner_space = 'LOCAL'
    # redistribute: distal half of limb -> 50% to twist bone
    for side, sgn in (('L', 1), ('R', -1)):
        for src in ('UpperArm', 'ForeArm'):
            gsrc = mesh.vertex_groups.get(f'{src}.{side}')
            if not gsrc:
                continue
            gtw = mesh.vertex_groups.new(name=f'{src}Twist.{side}')
            jz = {'UpperArm': 0.19, 'ForeArm': 0.335}[src]  # distal-half split
            for v in mesh.data.vertices:
                if (v.co.y * sgn) > jz:
                    for g in v.groups:
                        if g.group == gsrc.index and g.weight > 0.001:
                            w = g.weight * 0.5
                            gsrc.add([v.index], g.weight - w, 'REPLACE')
                            gtw.add([v.index], w, 'REPLACE')
                            break
    print('W6 twist bones added')


def weights_mdef_cage(mesh, rig, decimate_ratio=0.002, tag='W7'):
    t = time.time()
    # cage = convex hull of mesh, decimated
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.duplicate()
    cage = bpy.context.view_layer.objects.active
    cage.name = 'CJ_Cage'
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.convex_hull()
    bpy.ops.object.mode_set(mode='OBJECT')
    dec = cage.modifiers.new('Decimate', 'DECIMATE')
    dec.ratio = decimate_ratio
    bpy.ops.object.modifier_apply(modifier=dec.name)
    # relax the hull lightly so it hugs the body instead of bridging concavities
    bpy.context.view_layer.objects.active = cage
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=3)
    bpy.ops.object.mode_set(mode='OBJECT')
    cage.scale = Vector((1.06, 1.06, 1.06))
    bpy.context.view_layer.update()
    print('%s cage verts: %d (%.0fs)' % (tag, len(cage.data.vertices), time.time() - t))
    # deform the CAGE with bone heat (fast, low poly)
    select_for_parent(cage, rig)
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    # bind full mesh to cage
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = mesh
    md = mesh.modifiers.new('MeshDeform', 'MESH_DEFORM')
    md.object = cage
    md.precision = 5
    t = time.time()
    bpy.ops.object.meshdeform_bind(modifier=md.name)
    print('%s meshdeform bind done in %.0fs, bound=%s' % (tag, time.time() - t, md.is_bound))
    cage.hide_render = True


def apply_pose(rig, pose, name_map=None):
    bpy.context.view_layer.objects.active = rig
    for pb in rig.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
    for key, val in pose.items():
        if key == 'root:loc':
            rig.pose.bones['root'].location = val
            continue
        bname = key
        if name_map and key in name_map:
            bname = name_map[key]
        # also try mapped lookup the other way
        if bname not in rig.pose.bones:
            continue
        rig.pose.bones[bname].rotation_euler = val
    bpy.context.view_layer.update()


def setup_render():
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 6
    sc.cycles.max_bounces = 1
    sc.render.resolution_x = 480
    sc.render.resolution_y = 270
    sc.render.film_transparent = True
    for loc, e in [((2, -2, 3), 600), ((-2, 2, 2), 250)]:
        bpy.ops.object.light_add(type='POINT', location=loc)
        bpy.context.object.data.energy = e
    cam = bpy.data.cameras.new('bake_cam')
    co = bpy.data.objects.new('bake_cam', cam)
    sc.collection.objects.link(co)
    sc.camera = co
    co.location = (1.9, -2.1, 0.55)
    d = Vector((0, 0, 0.0)) - co.location
    co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return co


def main():
    a = args_after_dd()
    entry = a[a.index('--entry') + 1] if '--entry' in a else 'W1'
    poses_arg = a[a.index('--poses') + 1] if '--poses' in a else 'all'
    from_blend = a[a.index('--from-blend') + 1] if '--from-blend' in a else None
    if poses_arg == 'all':
        poses = POSE_ORDER
    else:
        poses = []
        for token in poses_arg.split(','):
            token = token.strip()
            match = [p for p in POSE_ORDER if p == token or p.startswith(token + '_')]
            if not match:
                raise SystemExit('unknown pose ' + token)
            poses.extend(match)
    os.makedirs(BLEND_DIR, exist_ok=True)
    os.makedirs(PNG_DIR, exist_ok=True)

    if entry == 'W4':
        run_w4(poses)
        return

    if from_blend:
        bpy.ops.wm.open_mainfile(filepath=from_blend)
        mesh = next(o for o in bpy.data.objects if o.type == 'MESH'
                    and 'Cage' not in o.name and len(o.data.vertices) > 100000)
        rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
        if entry == 'W5':
            add_preserve_volume_and_smooth(mesh)
            entry = 'W5r'
        elif entry == 'W6':
            add_twist_bones(mesh, rig)
            entry = 'W6r'
    else:
        mesh = load_model()
        rig = build_skeleton()
        clay_material(mesh)
        if entry == 'W1':
            weights_boneheat(mesh, rig)
        elif entry == 'W1p':
            weights_boneheat_proxy(mesh, rig)
        elif entry == 'W2':
            weights_envelope(mesh, rig)
        elif entry == 'W3':
            weights_surface_heat(mesh, rig)
        elif entry == 'W5':
            weights_boneheat(mesh, rig)
            add_preserve_volume_and_smooth(mesh)
        elif entry == 'W6':
            weights_boneheat(mesh, rig)
            add_twist_bones(mesh, rig)
        elif entry == 'W7':
            weights_mdef_cage(mesh, rig)
        elif entry == 'W7b':
            weights_mdef_cage(mesh, rig, decimate_ratio=0.15, tag='W7b')
        else:
            raise SystemExit('unknown entry ' + entry)
        blend_path = os.path.join(BLEND_DIR, entry + '.blend')
        bpy.ops.wm.save_mainfile(filepath=blend_path)
        print('saved', blend_path)

    setup_render()
    for p in poses:
        apply_pose(rig, POSES[p])
        out = os.path.join(PNG_DIR, '%s_%s.png' % (entry, p))
        bpy.context.scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print('rendered', out)
    print('ENTRY %s DONE' % entry)


def run_w4(poses):
    """BrutalFist auto_rig_humanoid.py end-to-end, then pose renders."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'bf_auto', os.path.expanduser('~/workspace/brutalfist-fix/tools/animation/auto_rig_humanoid.py'))
    bf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bf)
    t = time.time()
    bf.clear_scene()
    objects = bf.import_glb(MODEL)
    print('W4 skinned already?', bf.has_skin(objects))
    rig = bf.build_humanoid(objects)
    bf.bind_automatic_weights(objects, rig)
    print('W4 rig+weights done in %.0fs, bones=%d' % (time.time() - t, len(rig.data.bones)))
    mesh = max((o for o in objects if o.type == 'MESH'), key=lambda o: len(o.data.vertices))
    clay_material(mesh)
    bpy.ops.wm.save_mainfile(filepath=os.path.join(BLEND_DIR, 'W4.blend'))
    setup_render()
    # map our pose dict onto BF bone names
    inv_map = {v: k for k, v in W4_MAP.items()}
    for p in poses:
        pose = {}
        for k, v in POSES[p].items():
            bk = inv_map.get(k, k)
            pose[bk] = v
        apply_pose(rig, pose)
        out = os.path.join(PNG_DIR, 'W4_%s.png' % p)
        bpy.context.scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print('rendered', out)
    print('ENTRY W4 DONE')


if __name__ == '__main__':
    main()
