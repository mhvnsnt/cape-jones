import bpy
from mathutils import Vector
def setup(view="front3q",res=(1920,1080),pct=100,samples=8,floor_z=None):
    sc=bpy.context.scene; tw=bpy.data.objects["CapeJones_Rig"].matrix_world
    if "BlenRigMdefCage" in bpy.data.objects: bpy.data.objects["BlenRigMdefCage"].hide_render=True
    bpy.ops.mesh.primitive_plane_add(size=30); fl=bpy.context.object; fl.name="SetFloor"
    m=bpy.data.materials.new("floor"); m.use_nodes=True; m.node_tree.nodes["Principled BSDF"].inputs[0].default_value=(0.12,0.12,0.14,1); fl.data.materials.append(m)
    fl.location.z=floor_z if floor_z is not None else -0.013
    wd=bpy.data.worlds.new("w"); sc.world=wd; wd.use_nodes=True; wd.node_tree.nodes["Background"].inputs[0].default_value=(0.05,0.05,0.08,1)
    for n,loc,e in (("key",(3,-4,5),900),("fill",(-4,-3,3),300),("rim",(0,5,4),700)):
        L=bpy.data.lights.new(n,'AREA'); L.energy=e; L.size=3; o=bpy.data.objects.new(n,L); sc.collection.objects.link(o); o.location=loc
        o.rotation_euler=(Vector((0,0,1))-Vector(loc)).to_track_quat('-Z','Y').to_euler()
    H=0.9121; cz=0.456
    cd=bpy.data.cameras.new("cam"); cam=bpy.data.objects.new("cam",cd); sc.collection.objects.link(cam); sc.camera=cam; cd.lens=50
    pos={"front3q":(H*0.9,-H*3.0,cz+H*0.1),"front":(0,-H*3.2,cz+H*0.1),"side":(H*3.2,0,cz+H*0.1)}[view]
    cam.location=pos; cam.rotation_euler=(Vector((0,0,cz))-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.render.resolution_x,sc.render.resolution_y=res; sc.render.resolution_percentage=pct; sc.render.fps=24
    sc.render.engine='BLENDER_EEVEE'; sc.eevee.taa_render_samples=samples; sc.render.use_persistent_data=True
    return cam
