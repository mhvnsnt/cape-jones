"""Reusable direction-matching retarget: glTF guard stance (Alisa-named skeleton carrying CMU 13_17 boxing,
Cyborg X fight stance) -> CapeJones_Rig deform bones. Same math as v1 (guard_stance_retarget_render.py)
so the v1 defect can be reproduced on the v1 rig; the arm fix lives in the rig (build_rig_v2.py)."""
import bpy
from mathutils import Matrix, Vector
M=[("Hips","pelvis"),("Spine","spine_1"),("Spine1","spine_2"),("Spine2","chest"),("Neck","neck_1"),("Head","head"),
 ("LeftShoulder","clavicle_L"),("LeftArm","upperarm_L"),("LeftForeArm","forearm_L"),("LeftHand","hand_L"),
 ("RightShoulder","clavicle_R"),("RightArm","upperarm_R"),("RightForeArm","forearm_R"),("RightHand","hand_R"),
 ("LeftUpLeg","thigh_L"),("LeftLeg","shin_L"),("LeftFoot","foot_L"),("RightUpLeg","thigh_R"),("RightLeg","shin_R"),("RightFoot","foot_R")]
CH={"LeftShoulder":"LeftArm","LeftArm":"LeftForeArm","LeftForeArm":"LeftHand","RightShoulder":"RightArm","RightArm":"RightForeArm",
 "RightForeArm":"RightHand","LeftUpLeg":"LeftLeg","LeftLeg":"LeftFoot","LeftFoot":"LeftToeBase","RightUpLeg":"RightLeg","RightLeg":"RightFoot","RightFoot":"RightToeBase"}
def import_src(path):
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=path)
    new=[o for o in bpy.data.objects if o not in before]
    src=[o for o in new if o.type=='ARMATURE'][0]
    for o in new:
        if o.type=='MESH': o.hide_render=True; o.hide_viewport=True
    return src
def prep_target(tgt):
    for pb in tgt.pose.bones:
        for c in pb.constraints: c.mute=True
        pb.rotation_mode='QUATERNION'
def bake(tgt,src,src_frames,dst_frames,widen=0.22):
    sc=bpy.context.scene; sw=src.matrix_world; tw=tgt.matrix_world
    hs=(sw@src.data.bones["Head"].head_local).z; ht=(tw@tgt.data.bones["head"].head_local).z; ratio=ht/hs
    src_h0=sw@src.data.bones["Hips"].head_local; tgt_h0=tw@tgt.data.bones["pelvis"].head_local
    meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.hide_viewport]
    for o in meshes: o.hide_viewport=True   # armature-only evaluation while baking
    for sf,df in zip(src_frames,dst_frames):
        sc.frame_set(int(sf)); bpy.context.view_layer.update()
        for s,t in M:
            spb=src.pose.bones[s]; tpb=tgt.pose.bones[t]; rest_w=tw@tpb.bone.matrix_local
            if s in CH:
                c=src.pose.bones[CH[s]]; sd=((sw@c.head)-(sw@spb.head)).normalized()
                if s in('LeftUpLeg','RightUpLeg'): sd.x+=widen*(1 if s[0]=='L' else -1); sd=sd.normalized()
                trest=(tw.to_3x3()@(tpb.bone.tail_local-tpb.bone.head_local)).normalized()
                R=trest.rotation_difference(sd).to_matrix()@rest_w.to_3x3()
            else:
                sr=(sw@spb.bone.matrix_local).to_3x3(); sp=(sw@spb.matrix).to_3x3(); R=(sp@sr.inverted())@rest_w.to_3x3()
            pos=tw@tpb.head
            if t=="pelvis": pos=tgt_h0+((sw@spb.head)-src_h0)*ratio
            tpb.matrix=tw.inverted()@(Matrix.Translation(pos)@R.to_4x4()); bpy.context.view_layer.update()
            tpb.keyframe_insert("rotation_quaternion",frame=df)
            if t=="pelvis": tpb.keyframe_insert("location",frame=df)
    for o in meshes: o.hide_viewport=False
    src.hide_viewport=True; src.hide_render=True
    return ratio
