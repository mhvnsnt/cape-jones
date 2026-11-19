import bpy, json, math
D = math.radians
R = {}
for name in ("CapeJones_Body", "CapeJones_Cape", "CapeJones_Rig", "BlenRigMdefCage"):
    ob = bpy.data.objects[name]
    R[name] = {"loc": [round(v,3) for v in ob.location],
               "rot_deg": [round(math.degrees(v),1) for v in ob.rotation_euler],
               "scale": [round(v,3) for v in ob.scale]}
    if ob.type == "MESH":
        import mathutils
        ws = [ob.matrix_world @ mathutils.Vector(c) for c in ob.bound_box]
        R[name]["world_bbox"] = {"min": [round(min(w[i] for w in ws),3) for i in range(3)],
                                 "max": [round(max(w[i] for w in ws),3) for i in range(3)]}
with open("/home/hatch/workspace/_cj-dance-v2/probe3.json", "w") as f:
    json.dump(R, f, indent=1)

# --- minimal scene for cape inspection renders
for name in ("MPFB_ReferenceBody", "MPFB_FullSkeleton", "BlenRigMdefCage"):
    ob = bpy.data.objects.get(name)
    if ob: ob.hide_render = True
sc = bpy.context.scene
sc.world = bpy.data.worlds.new("W"); sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.6, 0.8, 1)
bpy.ops.object.light_add(type="SUN", location=(1, -1, 3))
sun = bpy.context.active_object; sun.data.energy = 3.0; sun.rotation_euler = (D(40), 0, D(20))
bpy.ops.object.light_add(type="AREA", location=(0, -2, 1))
fl = bpy.context.active_object; fl.data.energy = 200; fl.data.size = 2.0; fl.rotation_euler = (D(90), 0, 0)
sc.render.engine = "BLENDER_EEVEE"; sc.eevee.taa_render_samples = 1
sc.render.resolution_x = 480; sc.render.resolution_y = 270
sc.render.film_transparent = False
import os
OUT = "/home/hatch/workspace/_cj-dance-v2/check"
os.makedirs(OUT, exist_ok=True)

def shot(cam_loc, cam_rot, tag, show_body, show_cape):
    bpy.ops.object.camera_add(location=cam_loc, rotation=cam_rot)
    cam = bpy.context.active_object; cam.data.lens = 50; sc.camera = cam
    bpy.data.objects["CapeJones_Body"].hide_render = not show_body
    bpy.data.objects["CapeJones_Cape"].hide_render = not show_cape
    sc.render.filepath = os.path.join(OUT, tag + ".png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)
    print("SHOT", tag, flush=True)

shot((0, 1.7, 0.5), (D(90), 0, D(180)), "back_both", True, True)
shot((0, 1.7, 0.5), (D(90), 0, D(180)), "back_capeonly", False, True)
shot((0, 1.7, 0.5), (D(90), 0, D(180)), "back_bodyonly", True, False)
shot((0, -1.7, 0.5), (D(90), 0, 0), "front_both", True, True)
print("PROBE3_DONE")
