import bpy, os, math
# Clean scene, Blender 5.2.3
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
# Ground plane at z=0 (the world ground line, feet anchor)
bpy.ops.mesh.primitive_plane_add(size=10, location=(0,0,0))
plane=bpy.context.active_object; plane.name="GroundPlane_z0"
# Proxy figure: box 0.6 wide, 1.8 tall, bottom exactly on plane (centre z=0.9)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.9))
box=bpy.context.active_object; box.name="ProxyFigure"; box.dimensions=(0.6,0.3,1.8); box.location=(0,0,0.9)
# Raised proxy: second box, bottom 0.5 above plane (airborne height analogue)
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5,0,1.4))
air=bpy.context.active_object; air.name="ProxyAirborne"; air.dimensions=(0.6,0.3,1.8); air.location=(1.5,0,1.4)
# Sun + camera looking at ground line
bpy.ops.object.light_add(type='SUN', location=(5,-5,8))
cam_data=bpy.data.cameras.new("Cam"); cam_obj=bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam_obj); cam_obj.location=(0,-6,2.2)
from mathutils import Vector
def look_at(o, t):
    d=(Vector(t)-o.location).normalized(); o.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
look_at(cam_obj,(0,0,0.9)); bpy.context.scene.camera=cam_obj
bpy.context.scene.render.engine='CYCLES'
bpy.context.scene.cycles.device='CPU'
bpy.context.scene.cycles.samples=16
bpy.context.scene.render.resolution_x=640; bpy.context.scene.render.resolution_y=480
bpy.ops.wm.save_as_mainfile(filepath=os.path.expanduser('~/workspace/cape-jones-rig/ground-gate-complete-20261031/blender-ground-plane-20261031.blend'))
print('BLENDER_SCENE_OK plane_z=',plane.location.z,'proxy_bottom=',box.location.z-box.dimensions.z/2,'airborne_bottom=',air.location.z-air.dimensions.z/2)
out=os.path.expanduser("~/workspace/cape-jones-rig/ground-gate-complete-20261031/blender-ground-plane-20261031.png")
bpy.context.scene.render.filepath=out; bpy.ops.render.render(write_still=True)
print("BLENDER_GROUND_OK plane_z=",plane.location.z,"proxy_bottom=",box.location.z-box.dimensions.z/2,"airborne_bottom=",air.location.z-air.dimensions.z/2,"render=",out)
