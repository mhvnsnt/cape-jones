import bpy, math, os, time
D = math.radians
t00 = time.time()
for name in ("MPFB_ReferenceBody", "MPFB_FullSkeleton", "BlenRigMdefCage", "CapeJones_Cape"):
    ob = bpy.data.objects.get(name)
    if ob: ob.hide_render = True
sc = bpy.context.scene
body = bpy.data.objects["CapeJones_Body"]
rig = bpy.data.objects["CapeJones_Rig"]
# decimated render copy (decimate first, then armature; no corrective smooth)
cp = body.copy(); cp.data = body.data.copy(); cp.name = "BodyDec"
sc.collection.objects.link(cp)
for md in list(cp.modifiers):
    cp.modifiers.remove(md)
dm = cp.modifiers.new("Dec", "DECIMATE"); dm.ratio = 0.10; dm.use_collapse_triangulate = True
am = cp.modifiers.new("Arm", "ARMATURE"); am.object = rig
body.hide_render = True
print("COPY_BUILT", round(time.time() - t00, 1), flush=True)

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
bpy.context.view_layer.objects.active = rig

def snap(tag, mods):
    bpy.ops.object.mode_set(mode="POSE")
    for pb in rig.pose.bones:
        pb.rotation_euler = (0, 0, 0); pb.location = (0, 0, 0)
    for bn, rot in mods.items():
        pb = rig.pose.bones[bn]; pb.rotation_mode = "XYZ"
        pb.rotation_euler = tuple(D(a) for a in rot)
    bpy.ops.object.mode_set(mode="OBJECT")
    t0 = time.time()
    sc.render.filepath = os.path.join(OUT, tag + ".png")
    bpy.ops.render.render(write_still=True)
    print("SNAP", tag, round(time.time() - t0, 1), flush=True)

snap("sign3_thighR_zminus", {"thigh_fk_R": (0, 0, -20)})
snap("sign3_chestx_heady", {"chest": (12, 0, 0), "head": (0, 20, 0)})
print("SIGN3_DONE", round(time.time() - t00, 1))
