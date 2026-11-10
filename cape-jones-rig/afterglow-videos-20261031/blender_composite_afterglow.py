"""Blender 5.2.3 compositor pass for afterglow videos.
Per frame: dark bg image -> AlphaOver trail layer -> AlphaOver plate layer.
Standard view transform (NOT AgX, so the cyan/gold trail colour is preserved),
CPU compositor, GroupOutput, real render with write_still=True.
Usage: blender -b --python blender_composite_afterglow.py -- PUNCH|SHOT <id>
PUNCH composites all 18 punch frames. SHOT composites the 12 frames of one
shot's frames_shots/<id> folder — but shot frames are already composited in
PIL, so for shots the Blender pass is run on ONE key motion frame per shot
(see blender_keyframes.py) and the full shot GIFs are PIL trail renders
using the identical layers; that distinction is stated in the report.
"""
import bpy, sys, os
R='/home/hatch/workspace/cape-jones-rig/afterglow-videos-20261031'
mode=sys.argv[-2] if len(sys.argv)>2 else 'PUNCH'
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.use_nodes=True; scene.render.use_compositing=True
scene.render.engine='CYCLES'; scene.render.compositor_device='CPU'
scene.cycles.device='CPU'; scene.cycles.samples=1
scene.render.resolution_x=640; scene.render.resolution_y=360; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
tree=bpy.data.node_groups.new("AfterglowComp","CompositorNodeTree")
scene.compositing_node_group=tree
nodes=tree.nodes; links=tree.links
tree.interface.new_socket(name="Image",in_out="OUTPUT",socket_type="NodeSocketColor")
def img(path,x,y):
    n=nodes.new("CompositorNodeImage"); n.location=(x,y); n.image=bpy.data.images.load(path); return n
def over(bg_n,fg_n,x,y):
    n=nodes.new("CompositorNodeAlphaOver"); n.location=(x,y)
    links.new(bg_n.outputs['Image'],n.inputs['Background']); links.new(fg_n.outputs['Image'],n.inputs['Foreground']); return n
bg_n=img('/tmp/afterglow_bg.png',-600,300)
trail_n=img(f'{R}/blender_layers_punch/trail-00.png',-600,0)
plate_n=img(f'{R}/blender_layers_punch/plate-00.png',-600,-300)
c1=over(bg_n,trail_n,-300,300); c2=over(c1,plate_n,0,300)
out=nodes.new("NodeGroupOutput"); out.location=(300,300)
links.new(c2.outputs['Image'],out.inputs['Image'])
os.makedirs(f'{R}/blender_punch',exist_ok=True)
for i in range(18):
    trail_n.image=bpy.data.images.load(f'{R}/blender_layers_punch/trail-{i:02d}.png')
    plate_n.image=bpy.data.images.load(f'{R}/blender_layers_punch/plate-{i:02d}.png')
    scene.render.filepath=f'{R}/blender_punch/punch-blender-{i:02d}.png'
    bpy.ops.render.render(write_still=True)
    print("BLENDER_FRAME",i,flush=True)
print("BLENDER_PUNCH_DONE")
