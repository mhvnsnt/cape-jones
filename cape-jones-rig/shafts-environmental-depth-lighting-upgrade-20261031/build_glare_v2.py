import bpy, os
INP='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/shafts-only-cycles-v2-20261031.png'
OUTDIR='/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/'
os.makedirs(OUTDIR, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.use_nodes=True
nt=bpy.data.node_groups.new('Comp','CompositorNodeTree'); sc.compositing_node_group=nt
img=nt.nodes.new('CompositorNodeImage'); img.image=bpy.data.images.load(INP)
gl=nt.nodes.new('CompositorNodeGlare')
# set by name where possible
try: gl.inputs['Type'].default_value='Fog Glow'
except Exception as e: print("Type set fail", e)
try: gl.inputs['Quality'].default_value='High'
except Exception as e: print("Quality set fail", e)
for name, val in [('Threshold',0.6),('Strength',0.5),('Size',6.0)]:
    try: gl.inputs[name].default_value=val
    except Exception as e: print(name, "fail", e)
fo=nt.nodes.new('CompositorNodeOutputFile')
print("fo items:", list(fo.file_output_items) if hasattr(fo,'file_output_items') else None)
try: fo.directory=OUTDIR
except Exception as e: print("directory fail", e)
try: fo.file_name='shafts-glare-blender'
except Exception as e: print("file_name fail", e)
try: fo.format.file_format='PNG'
except Exception as e: print("format fail", e)
print("fo directory/file:", getattr(fo,'directory',None), getattr(fo,'file_name',None))
nt.links.new(img.outputs[0], gl.inputs[0])
nt.links.new(gl.outputs[0], fo.inputs[0])
sc.render.resolution_x=1100; sc.render.resolution_y=1500
sc.render.filepath=OUTDIR+'_glare_render_tmp.png'
bpy.ops.render.render(write_still=True)
print("GLARE_V2_DONE")
