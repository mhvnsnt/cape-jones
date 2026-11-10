import bpy, os
INP='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/shafts-only-cycles-v2-20261031.png'
OUT='/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/shafts-glare-blender-20261031.png'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.use_nodes=True
nt=bpy.data.node_groups.new('Comp','CompositorNodeTree'); sc.compositing_node_group=nt
img=nt.nodes.new('CompositorNodeImage'); img.image=bpy.data.images.load(INP)
gl=nt.nodes.new('CompositorNodeGlare')
for name,val in [('Type','Fog Glow'),('Quality','High'),('Threshold',0.6),('Strength',0.5),('Size',6.0)]:
    try: gl.inputs[name].default_value=val; print(name, "set", val)
    except Exception as e: print(name, "FAIL", e)
vw=nt.nodes.new('CompositorNodeViewer')
nt.links.new(img.outputs[0], gl.inputs[0])
nt.links.new(gl.outputs[0], vw.inputs[0])
sc.render.resolution_x=1100; sc.render.resolution_y=1500
sc.render.filepath='/tmp/_glare_scene_tmp.png'
bpy.ops.render.render(write_still=True)
print("render done, images:", [i.name for i in bpy.data.images])
vn=bpy.data.images.get('Viewer Node')
print("viewer node image:", vn, vn.size[:] if vn else None)
if vn:
    vn.save_render(OUT)
    print("SAVED_VIEWER", OUT, os.path.getsize(OUT))
else:
    print("NO_VIEWER_IMAGE")
