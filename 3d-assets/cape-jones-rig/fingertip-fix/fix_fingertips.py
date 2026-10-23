# Fix fingertip weight bleed: re-weight finger regions by rest-pose bone proximity.
# Two passes: (1) assign every vert to its globally-nearest finger chain,
# (2) per chain, set articulation-correct weights (100% distal at tips,
# smooth joint blends, knuckle blend to hand bone, zero forearm influence).
# Fully procedural - no hand-painting.
import bpy, sys
import numpy as np

blend, outpath = sys.argv[-2], sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=blend)
arm = max((o for o in bpy.data.objects if o.type=='ARMATURE'), key=lambda o: len(o.data.bones))
mesh = max((o for o in bpy.data.objects if o.type=='MESH'), key=lambda o: len(o.data.vertices))
print("ARMATURE:", arm.name, len(arm.data.bones), "MESH:", mesh.name, len(mesh.data.vertices), flush=True)

bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
for pb in arm.pose.bones:
    pb.location.zero(); pb.rotation_euler.zero(); pb.rotation_quaternion.identity(); pb.scale = (1,1,1,)
bpy.context.view_layer.update()

mesh_inv = mesh.matrix_world.inverted()
def seg_local(bone):
    h = (mesh_inv @ arm.matrix_world @ bone.head_local).to_3d()
    t = (mesh_inv @ arm.matrix_world @ bone.tail_local).to_3d()
    return np.array(h[:], dtype=np.float64), np.array(t[:], dtype=np.float64)

chains = {}
for side in ('L','R'):
    for f in ('index','middle','ring','pinky'):
        chains[(f,side)] = ['finger_%s_%d_%s' % (f,i,side) for i in (1,2,3)]
    chains[('thumb',side)] = ['finger_thumb_1_%s' % side, 'finger_thumb_2_%s' % side]
hand_bone = {'L':'hand_L', 'R':'hand_R'}

chain_segs = {}   # key -> (segs[(name,h,t,c0,c1)], total_len)
chain_keys = []
for key, names in chains.items():
    segs = []; cum = 0.0; ok = True
    for nm in names:
        b = arm.data.bones.get(nm)
        if b is None: print("MISSING BONE", nm, flush=True); ok = False; break
        h, t = seg_local(b)
        L = float(np.linalg.norm(t-h)); segs.append((nm,h,t,cum,cum+L)); cum += L
    if ok: chain_segs[key] = (segs, cum); chain_keys.append(key)

n = len(mesh.data.vertices)
cos = np.empty(n*3, dtype=np.float32); mesh.data.vertices.foreach_get('co', cos)
P_all = cos.reshape(n,3).astype(np.float64)

R_FINGER = 0.022
R_BLEND  = 0.005
R_BASE   = 0.008
CHUNK = 40000

# Precompute segment arrays per chain for vectorized distance
chain_arr = {}
for key,(segs,total) in chain_segs.items():
    H = np.stack([s[1] for s in segs]); T = np.stack([s[2] for s in segs])
    AB = T-H; DEN = np.einsum('ij,ij->i',AB,AB)
    chain_arr[key] = (segs,total,H,T,AB,DEN)

# PASS 1: global nearest chain per vert (chunked)
assign_chain = np.full(n, -1, dtype=np.int64)   # index into chain_keys
assign_dist  = np.full(n, 1e9)
assign_si    = np.zeros(n, dtype=np.int64)
assign_t     = np.zeros(n)
for c0 in range(0, n, CHUNK):
    c1 = min(n, c0+CHUNK); P = P_all[c0:c1]
    for ki,key in enumerate(chain_keys):
        segs,total,H,T,AB,DEN = chain_arr[key]
        for si in range(len(segs)):
            tt = np.clip(((P-H[si]) @ AB[si]) / DEN[si], 0, 1)
            q = H[si] + tt[:,None]*AB[si]
            d = np.linalg.norm(P-q, axis=1)
            upd = d < assign_dist[c0:c1]
            assign_dist[c0:c1][upd] = d[upd]
            assign_chain[c0:c1][upd] = ki
            assign_si[c0:c1][upd] = si
            assign_t[c0:c1][upd] = tt[upd]
    if c0 % 200000 == 0: print("pass1 chunk", c0, flush=True)
in_finger = assign_dist < R_FINGER
print("verts in finger regions:", int(in_finger.sum()), flush=True)

# PASS 2: set weights per chain
vg_cache = {}
def get_vg(name):
    vg = vg_cache.get(name)
    if vg is None:
        vg = mesh.vertex_groups.get(name)
        if vg is None: vg = mesh.vertex_groups.new(name=name)
        vg_cache[name] = vg
    return vg

fixed = 0
for ki,key in enumerate(chain_keys):
    segs,total,H,T,AB,DEN = chain_arr[key]
    side = key[1]; hb = hand_bone[side]
    sel = np.where(in_finger & (assign_chain == ki))[0]
    if len(sel) == 0: continue
    joints = [s[4] for s in segs[:-1]]
    for vi in sel:
        vi = int(vi)
        si = int(assign_si[vi]); tt = float(assign_t[vi])
        nm,h,t,c_start,c_end = segs[si]
        cpos = c_start + tt*(c_end-c_start)
        weights = {}
        main = None; nxt = None; w_main, w_next = 1.0, 0.0
        for ji,jp in enumerate(joints):
            if abs(cpos - jp) < R_BLEND:
                f = (cpos-(jp-R_BLEND))/(2*R_BLEND); f = max(0.0,min(1.0,f)); f = f*f*(3-2*f)
                main = segs[ji][0]; nxt = segs[ji+1][0]; w_main, w_next = 1.0-f, f
                break
        if main is None:
            for nm2,h2,t2,cs,ce in segs:
                if cs-1e-9 <= cpos <= ce+1e-9: main = nm2; break
            if main is None: continue
        weights[main] = w_main
        if nxt: weights[nxt] = w_next
        if cpos < R_BASE:
            f = 1.0 - cpos/R_BASE; f = f*f*(3-2*f)
            for k in list(weights): weights[k] *= (1.0-0.7*f)
            weights[hb] = weights.get(hb,0.0) + 0.7*f
        v = mesh.data.vertices[vi]
        for g in list(v.groups):
            mesh.vertex_groups[g.group].remove([vi])
        tot = sum(weights.values())
        for gname,w in weights.items():
            if w > 1e-4: get_vg(gname).add([vi], w/tot, 'REPLACE')
        fixed += 1
    print("chain %s_%s: %d verts" % (key[0], key[1], len(sel)), flush=True)

print("FIXED VERTS:", fixed, flush=True)
bpy.ops.wm.save_as_mainfile(filepath=outpath)
print("SAVED", outpath, flush=True)
