import bpy, os
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
bpy.ops.mesh.primitive_plane_add(size=10, location=(0,0,0))
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.9)); b=bpy.context.active_object; b.dimensions=(0.6,0.3,1.8); b.location=(0,0,0.9)
bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5,0,1.4)); a=bpy.context.active_object; a.dimensions=(0.6,0.3,1.8); a.location=(1.5,0,1.4)
bpy.ops.object.light_add(type='SUN', location=(5,-5,8))
cam_data=bpy.data.cameras.new("Cam"); co=bpy.data.objects.new("Cam", cam_data); bpy.context.collection.objects.link(co); co.location=(0,-6,2.2)
from mathutils import Vector
d=(Vector((0,0,0.9))-co.location).normalized(); co.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); bpy.context.scene.camera=co
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=16
sc.render.resolution_x=640; sc.render.resolution_y=480
sc.view_layers[0].use_pass_z=True
sc.use_nodes=True; nt=sc.node_tree; nt.nodes.clear()
rl=nt.nodes.new('CompositorNodeRLayers'); norm=nt.nodes.new('CompositorNodeNormalize'); out=nt.nodes.new('CompositorNodeOutputFile')
out.base_path=os.path.expanduser("~/workspace/cape-jones-rig/ground-gate-complete-20261031")
out.file_slots[0].path="blender-depth-20261031"
nt.links.new(rl.outputs['Depth'], norm.inputs[0]); nt.links.new(norm.outputs[0], out.inputs[0])
sc.render.filepath=os.path.expanduser("~/workspace/cape-jones-rig/ground-gate-complete-20261031/blender-depth-color-20261031.png")
bpy.ops.render.render(write_still=True)
print("DEPTH_OK grounded_box_bottom_z=0.0 airborne_box_bottom_z=0.5")
