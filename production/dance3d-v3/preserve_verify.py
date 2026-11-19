import bpy, sys

def log(*a):
    print(*a); sys.stdout.flush()

log("SCENE frames:", bpy.context.scene.frame_start, bpy.context.scene.frame_end)
for name in ("CJ_Dance_3D_V3", "CJ_Dance_3D_V3_BAKED"):
    act = bpy.data.actions.get(name)
    if act:
        log("ACTION:", name, "| fcurves:", len(act.fcurves), "| range:", tuple(act.frame_range))
    else:
        log("ACTION MISSING:", name)
for obname in ("CapeJones_Rig", "CapeJones_Rig_BAKED"):
    ob = bpy.data.objects.get(obname)
    if ob:
        log("OBJECT:", obname, "| bones:", len(ob.data.bones),
            "| constraints:", sum(len(pb.constraints) for pb in ob.pose.bones),
            "| action:", ob.animation_data.action.name if ob.animation_data and ob.animation_data.action else None)
    else:
        log("OBJECT MISSING:", obname)
# pose spot-check on baked rig at frame 900: hand_L world position should be a real danced pose, not rest
sc = bpy.context.scene
sc.frame_set(900)
rig = bpy.data.objects["CapeJones_Rig"]
dup = bpy.data.objects["CapeJones_Rig_BAKED"]
for bn in ("hand_L", "foot_R", "head", "cape_3"):
    p1 = (rig.matrix_world @ rig.pose.bones[bn].matrix).translation
    p2 = (dup.matrix_world @ dup.pose.bones[bn].matrix).translation
    log("POSE f900", bn, "orig:", tuple(round(v, 3) for v in p1), "baked:", tuple(round(v, 3) for v in p2))
log("REOPEN CHECK DONE")
