import bpy,sys
from mathutils import Vector
exec(open('/workspace/cj3d/v2/clothdiag.py').read().split('print("GRAV"')[0])
for k in ("CapeJones_CapeHi","CapeJones_Cape"): bpy.data.objects[k].hide_viewport=True; bpy.data.objects[k].hide_render=True
bpy.data.objects["CapeJones_Body"].hide_viewport=False
body=bpy.data.objects["CapeJones_Body"]; body.modifiers["HideCapeHi"].show_render=True
p.hide_render=False; col.hide_render=True; bpy.data.objects["BlenRigMdefCage"].hide_render=True
mat=bpy.data.materials.new("red"); mat.diffuse_color=(1,0.1,0.1,1); p.data.materials.append(mat)
sc.render.engine='BLENDER_WORKBENCH'; sc.display.shading.color_type='MATERIAL'; sc.render.resolution_x=480; sc.render.resolution_y=540
cd=bpy.data.cameras.new("c"); cam=bpy.data.objects.new("c",cd); sc.collection.objects.link(cam); sc.camera=cam
cam.location=(2.6,0.3,0.5); cam.rotation_euler=(Vector((0,0,0.45))-cam.location).to_track_quat('-Z','Y').to_euler()
for f in range(1,111):
    sc.frame_set(f)
    if f in (1,30,50,80,110): sc.render.filepath=f"/workspace/cj3d/v2/probe/cl4_{f:03d}.png"; bpy.ops.render.render(write_still=True)
