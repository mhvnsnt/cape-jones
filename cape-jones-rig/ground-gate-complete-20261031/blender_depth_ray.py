import bpy, os, math
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
bpy.ops.mesh.primitive_plane_add(size=20, location=(0,0,0))
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.9)); b=bpy.context.active_object; b.dimensions=(0.6,0.3,1.8); b.location=(0,0,0.9)
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5,0,1.4)); a=bpy.context.active_object; a.dimensions=(0.6,0.3,1.8); a.location=(1.5,0,1.4)
bpy.context.view_layer.update()
cam_data=bpy.data.cameras.new("Cam"); co=bpy.data.objects.new("Cam", cam_data); bpy.context.collection.objects.link(co); co.location=(0,-6,2.2)
d=(Vector((0,0,0.9))-co.location).normalized(); co.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
bpy.context.scene.camera=co; bpy.context.view_layer.update()
W,H=160,120; deps=bpy.context.scene.view_layers[0].depsgraph
img=[[0.0]*W for _ in range(H)]; hitmask=[[False]*W for _ in range(H)]
for j in range(H):
    for i in range(W):
        # camera ray through pixel (simple pinhole, fov 50deg, aspect W/H)
        x=(i/W-0.5)*2*math.tan(math.radians(25))*W/H; y=(0.5-j/H)*2*math.tan(math.radians(25))
        local=Vector((x,y,-1)).normalized()
        direction=co.matrix_world.to_3x3()@local
        hit,loc,normal,idx,obj,mat=bpy.context.scene.ray_cast(deps, co.location, direction)
        if hit:
            img[j][i]=(loc-co.location).length; hitmask[j][i]=True
flat=[v for row in img for v in row]; hm=[hitmask[j][i] for j in range(H) for i in range(W)]; print("RAYCAST hits", sum(hm), "/", W*H)
# sample centres: ground plane far left, grounded box centre, airborne box centre (approx pixel positions by projecting)
def project(p):
    v=co.matrix_world.inverted()@Vector(p); x=-v.x/v.z/math.tan(math.radians(25))*H/W; y=-v.y/v.z/math.tan(math.radians(25))
    return int((x/2+0.5)*W), int((0.5-y/2)*H)
for name,p in [("ground_plane",(-3,0,0)),("grounded_box_centre",(0,0,0.9)),("airborne_box_centre",(1.5,0,1.4))]:
    px,py=project(p); print(name,"pixel",px,py,"depth",round(float(img[py][px]),3) if hitmask[py][px] else "no-hit")
vals=[img[j][i] for j in range(H) for i in range(W) if hitmask[j][i] and img[j][i]>0]
lo,hi=min(vals),max(vals)
pixels=[]
for j in range(H):
    for i in range(W):
        v=(img[j][i]-lo)/(hi-lo) if hitmask[j][i] and img[j][i]>0 else 0.0
        pixels.extend([v,v,v,1.0])
im=bpy.data.images.new("depth",W,H); im.pixels=pixels; im.filepath_raw=os.path.expanduser("~/workspace/cape-jones-rig/ground-gate-complete-20261031/blender-depth-20261031.png"); im.file_format='PNG'; im.save()
print("DEPTH_RAY_OK saved blender-depth-20261031.png")
