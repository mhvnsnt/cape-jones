import bpy, sys, json

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[0] if argv else "/tmp/inspect_out.json"

info = {"objects": [], "armatures": {}, "actions": [], "materials": 0,
        "scene_frames": [bpy.context.scene.frame_start, bpy.context.scene.frame_end],
        "render_engine": bpy.context.scene.render.engine}
for ob in bpy.data.objects:
    info["objects"].append({"name": ob.name, "type": ob.type,
                            "parent": ob.parent.name if ob.parent else None})
    if ob.type == "ARMATURE":
        info["armatures"][ob.name] = [b.name for b in ob.data.bones]
for a in bpy.data.actions:
    info["actions"].append({"name": a.name, "range": list(a.frame_range)})
info["materials"] = len(bpy.data.materials)
with open(out, "w") as f:
    json.dump(info, f, indent=1)
print("INSPECT_DONE", out)
