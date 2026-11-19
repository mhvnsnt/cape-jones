import bpy, os, sys

STAGE = "/home/hatch/workspace/_cj-dance3d-v3/preserve"
OUT_BLEND = STAGE + "/cj-dance-3d-v3.blend"
OUT_BVH = STAGE + "/cj-dance-3d-v3.bvh"
F0, F1 = 1, 1824

def log(*a):
    print(*a); sys.stdout.flush()

os.makedirs(STAGE, exist_ok=True)
sc = bpy.context.scene
sc.frame_start, sc.frame_end = F0, F1

# ---------- 1. Name the original dance action unambiguously ----------
act = bpy.data.actions.get("DanceV3")
assert act, "DanceV3 action missing!"
bones_keyed = sorted({fc.data_path.split('"')[1] for fc in act.fcurves if '"' in fc.data_path})
props_keyed = sorted({fc.data_path for fc in act.fcurves if '"' not in fc.data_path})
log("KEYED BONES (%d):" % len(bones_keyed), bones_keyed)
log("KEYED NON-BONE PATHS:", props_keyed)
act.name = "CJ_Dance_3D_V3"
act.use_fake_user = True

rig = bpy.data.objects["CapeJones_Rig"]

# ---------- 2. Duplicate the armature as the baked carrier ----------
bpy.ops.object.select_all(action='DESELECT')
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.duplicate()
dup = bpy.context.view_layer.objects.active
dup.name = "CapeJones_Rig_BAKED"
dup.data.name = "CapeJones_Rig_BAKED_Data"
coll = bpy.data.collections.new("SAVED_ANIMATION_BAKED")
sc.collection.children.link(coll)
for c in list(dup.users_collection):
    c.objects.unlink(dup)
coll.objects.link(dup)
log("DUP:", dup.name, "| constraints:", sum(len(pb.constraints) for pb in dup.pose.bones))

# ---------- 3. Visual bake onto the duplicate, constraints cleared ----------
bpy.ops.object.select_all(action='DESELECT')
dup.select_set(True)
bpy.context.view_layer.objects.active = dup
bpy.ops.nla.bake(frame_start=F0, frame_end=F1, only_selected=False,
                 visual_keying=True, clear_constraints=True,
                 use_current_action=False, bake_types={'POSE'})
baked = dup.animation_data.action
baked.name = "CJ_Dance_3D_V3_BAKED"
baked.use_fake_user = True
log("BAKED ACTION:", baked.name, "| fcurves:", len(baked.fcurves), "| range:", tuple(baked.frame_range),
    "| constraints left:", sum(len(pb.constraints) for pb in dup.pose.bones))

# ---------- 4. Verify: deform-bone world matrices, original vs baked ----------
CHECK_BONES = ['root', 'pelvis', 'spine_1', 'chest', 'neck_1', 'head',
               'upperarm_L', 'forearm_L', 'hand_L', 'upperarm_R', 'forearm_R', 'hand_R',
               'thigh_L', 'shin_L', 'foot_L', 'thigh_R', 'shin_R', 'foot_R',
               'cape_1', 'cape_2', 'cape_3']
worst = 0.0
for f in (1, 100, 240, 500, 768, 1000, 1200, 1537, 1819, 1824):
    sc.frame_set(f)
    for bn in CHECK_BONES:
        m1 = rig.matrix_world @ rig.pose.bones[bn].matrix
        m2 = dup.matrix_world @ dup.pose.bones[bn].matrix
        d = max(abs(m1[i][j] - m2[i][j]) for i in range(4) for j in range(4))
        worst = max(worst, d)
log("VERIFY worst matrix element diff (orig vs baked):", worst)
assert worst < 1e-3, "BAKE MISMATCH too large: %f" % worst

# ---------- 5. Save the .blend ----------
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
log("SAVED BLEND:", OUT_BLEND, os.path.getsize(OUT_BLEND))

# ---------- 6. Export BVH from the baked armature ----------
try:
    bpy.ops.preferences.addon_enable(module='io_anim_bvh')
except Exception as e:
    log("addon enable note:", e)
bpy.ops.object.select_all(action='DESELECT')
dup.select_set(True)
bpy.context.view_layer.objects.active = dup
sc.frame_set(F0)
bpy.ops.export_anim.bvh(filepath=OUT_BVH, frame_start=F0, frame_end=F1,
                        global_scale=1.0, root_transform_only=False)
log("SAVED BVH:", OUT_BVH, os.path.getsize(OUT_BVH))
log("ALL DONE")
