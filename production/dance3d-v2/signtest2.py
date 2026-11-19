import bpy, math, os, sys
D = math.radians
argv = sys.argv[sys.argv.index("--") + 1:]
TAG = argv[0]
for name in ("MPFB_ReferenceBody", "MPFB_FullSkeleton", "BlenRigMdefCage"):
    ob = bpy.data.objects.get(name)
    if ob: ob.hide_render = True
bpy.data.objects["CapeJones_Cape"].hide_render = True
body = bpy.data.objects["CapeJones_Body"]
for md in body.modifiers:
    if md.type == "CORRECTIVE_SMOOTH":
        md.show_render = False; md.show_viewport = False
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
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="POSE")
if TAG == "sign_thighR_zminus":
    pb = rig.pose.bones["thigh_fk_R"]; pb.rotation_mode = "XYZ"; pb.rotation_euler = (0, 0, D(-20))
elif TAG == "sign_chestx_heady":
    pb = rig.pose.bones["chest"]; pb.rotation_mode = "XYZ"; pb.rotation_euler = (D(12), 0, 0)
    pb = rig.pose.bones["head"]; pb.rotation_mode = "XYZ"; pb.rotation_euler = (0, D(20), 0)
bpy.ops.object.mode_set(mode="OBJECT")
sc.render.filepath = "/home/hatch/workspace/_cj-dance3d-v2/check/" + TAG + ".png"
bpy.ops.render.render(write_still=True)
print("SNAP_DONE", TAG, flush=True)
