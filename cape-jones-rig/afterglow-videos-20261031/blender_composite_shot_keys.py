"""Blender 5.2.3 compositor: one key frame per shot (30/30).
bg -> AlphaOver trail -> AlphaOver plate, Standard view, CPU, real render."""
import bpy, os, glob
R='/home/hatch/workspace/cape-jones-rig/afterglow-videos-20261031'
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.use_nodes=True; scene.render.use_compositing=True
scene.render.engine='CYCLES'; scene.render.compositor_device='CPU'
scene.cycles.device='CPU'; scene.cycles.samples=1
scene.render.resolution_x=640; scene.render.resolution_y=360; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'
tree=bpy.data.node_groups.new("ShotKeys","CompositorNodeTree"); scene.compositing_node_group=tree
nodes=tree.nodes; links=tree.links
tree.interface.new_socket(name="Image",in_out="OUTPUT",socket_type="NodeSocketColor")
def img(p,x,y):
    n=nodes.new("CompositorNodeImage"); n.location=(x,y); n.image=bpy.data.images.load(p); return n
def over(a,b,x,y):
    n=nodes.new("CompositorNodeAlphaOver"); n.location=(x,y)
    links.new(a.outputs['Image'],n.inputs['Background']); links.new(b.outputs['Image'],n.inputs['Foreground']); return n
bg=img('/tmp/afterglow_bg.png',-600,300)
tr=img(f'{R}/blender_keys_shots/CJ-01-trail.png',-600,0)
pl=img(f'{R}/blender_keys_shots/CJ-01-plate.png',-600,-300)
c=over(over(bg,tr,-300,300),pl,0,300)
out=nodes.new("NodeGroupOutput"); out.location=(300,300); links.new(c.outputs['Image'],out.inputs['Image'])
os.makedirs(f'{R}/blender_keys_out',exist_ok=True)
import re
ids=sorted(set(re.match(r'(CJ-\d+)-',os.path.basename(p)).group(1) for p in glob.glob(f'{R}/blender_keys_shots/*-trail.png')))
for sid in ids:
    tr.image=bpy.data.images.load(f'{R}/blender_keys_shots/{sid}-trail.png')
    pl.image=bpy.data.images.load(f'{R}/blender_keys_shots/{sid}-plate.png')
    scene.render.filepath=f'{R}/blender_keys_out/{sid}-blender-key.png'
    bpy.ops.render.render(write_still=True); print("KEY",sid,flush=True)
print("KEYS_DONE",len(ids))
