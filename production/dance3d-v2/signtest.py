import bpy, math, os
D = math.radians
for name in ("MPFB_ReferenceBody", "MPFB_FullSkeleton", "BlenRigMdefCage"):
    ob = bpy.data.objects.get(name)
    if ob: ob.hide_render = True
bpy.data.objects["CapeJones_Cape"].hide_render = True
sc = bpy.context.scene
sc.world = bpy.data.worlds.new("W"); sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.6, 0.8, 1)
bpy.ops.object.light_add(type="SUN", location=(1, -1, 3))
sun = bpy.context.active_object; sun.data.energy = 3.0; sun.rotation_euler = (D(40), 0, D(20))
bpy.ops.object.light_add(type="AREA", location=(0, -2, 1))
fl = bpy.context.active_object; fl.data.energy = 200; fl.data.size = 2.0; fl.rotation_euler = (D(90), 0, 0)
bpy.ops.object.camera_add(location=(0, -1.7, 0.5), rotation=(D(90), 0, 0))
cam = bpy.context.active_object; cam.data.lens = 50; sc.camera = cam
sc.render.engine = "BLENDER_EEVEE"; sc.eevee.taa_render_samples = 1
sc.render.resolution_x = 480; sc.render.resolution_y = 270
OUT = "/home/hatch/workspace/_cj-dance3d-v2/check"
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.objects.active = rig

def snap(tag, mods):
    bpy.ops.object.mode_set(mode="POSE")
    for pb in rig.pose.bones:
        pb.rotation_euler = (0, 0, 0); pb.location = (0, 0, 0)
    for bn, (loc, rot) in mods.items():
        pb = rig.pose.bones[bn]; pb.rotation_mode = "XYZ"
        if loc: pb.location = loc
        if rot: pb.rotation_euler = tuple(D(a) for a in rot)
    bpy.ops.object.mode_set(mode="OBJECT")
    sc.render.filepath = os.path.join(OUT, tag + ".png")
    bpy.ops.render.render(write_still=True)
    print("SNAP", tag, flush=True)

snap("sign_thighR_zplus", {"thigh_fk_R": (None, (0, 0, 20))})
snap("sign_thighR_zminus", {"thigh_fk_R": (None, (0, 0, -20))})
snap("sign_thighR_xminus", {"thigh_fk_R": (None, (0, 0, 0)), "thigh_fk_L": (None, (-25, 0, 0))})
snap("sign_chestx_heady", {"chest": (None, (12, 0, 0)), "head": (None, (0, 20, 0))})
snap("sign_pelvisloc", {"pelvis": ((0.08, 0, -0.04), (0, 0, 0))})
print("SIGN_DONE")
