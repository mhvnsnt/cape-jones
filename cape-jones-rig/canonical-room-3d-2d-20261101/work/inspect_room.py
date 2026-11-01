import bpy, json
print("BLENDER", bpy.app.version_string)
print("SCENE", bpy.context.scene.name)
print("FRAME", bpy.context.scene.frame_start, bpy.context.scene.frame_end, bpy.context.scene.frame_current)
cams=[o.name for o in bpy.data.objects if o.type=='CAMERA']
lights=[(o.name,o.type,o.data.energy if hasattr(o.data,'energy') else None, tuple(o.data.color) if hasattr(o.data,'color') else None) for o in bpy.data.objects if o.type=='LIGHT']
print("CAMERAS", cams)
print("ACTIVE_CAM", bpy.context.scene.camera.name if bpy.context.scene.camera else None)
print("LIGHTS", lights)
print("RENDER_ENGINE", bpy.context.scene.render.engine)
objs=[]
for o in bpy.data.objects:
    objs.append({"name":o.name,"type":o.type,"loc":[round(v,3) for v in o.location],"hide_render":o.hide_render})
print("N_OBJECTS", len(objs))
for o in objs: print(o)
print("MATERIALS", sorted(set(m.name for m in bpy.data.materials)))
print("COLLECTIONS", [c.name for c in bpy.data.collections])
