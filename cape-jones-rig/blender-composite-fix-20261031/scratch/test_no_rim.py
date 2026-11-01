"""Final Blender-only composite, Blender 5.2.3 LTS.
DUAL-LIGHT COMBINED CASE ONLY (Mars 15:48 CDT correction):
cyan backlight / cyan god rays apply ONLY when cyan rim is combined
with the gold LUT/overlay. Gold rim alone gets NO cyan backlight.
This frame IS that combined case: gold grade on background only,
cyan volumetric backlight, cyan back rim as a separate layer.
Base art is never recoloured: plate goes in untouched; gold tint is
on the background only; cyan rim is an Add layer from plate alpha.

Industry-standard output path in Blender 5.2 (verified by probe):
- CompositorNodeComposite is UNDEFINED in 5.2. Do NOT use it.
- Scene tree = new CompositorNodeTree assigned to
  scene.compositing_node_group, with an interface OUTPUT socket
  named "Image", linked from a NodeGroupOutput node. That IS the
  Composite output in 5.2.
- Render with scene.render.use_compositing=True and
  bpy.ops.render.render(write_still=True) with filepath set.
  Building the tree and saving the .blend alone produces NO image.
  Reading 'Render Result' before a render also produces NO plate.
- AlphaOver inputs: [0]=Background, [1]=Foreground, Factor=1.0.
  Swapping them hides the plate behind an opaque background.
- Image nodes: load RGBA PNGs; alpha comes from the image file.
  AlphaOver 'Straight Alpha' left at default (premultiplied path)
  worked for this straight-alpha PNG in the minimal test.
"""
import bpy
print("FINAL COMPOSITE START")
BASE = '/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/scratch/volumetric-base-20261031.png'
PLATE = '/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png'
OUT = '/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/test-no-rim-20261031.png'
BLEND = '/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/test-no-rim-20261031.blend'

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.use_nodes = True
scene.render.use_compositing = True
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = OUT

tree = bpy.data.node_groups.new("CapeJonesDualLightComposite", "CompositorNodeTree")
scene.compositing_node_group = tree
tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
nodes = tree.nodes
links = tree.links

bg = nodes.new("CompositorNodeImage"); bg.name = "VolumetricBase"; bg.location = (-800, 300)
bg.image = bpy.data.images.load(BASE)

# Gold LUT/overlay on BACKGROUND ONLY: MixRGB MULTIPLY (1.10, 0.95, 0.70)
gold = nodes.new("ShaderNodeMixRGB"); gold.name = "GoldGrade_BG_Only"; gold.location = (-550, 300)
gold.blend_type = 'MULTIPLY'
gold.inputs['Factor'].default_value = 1.0
gold.inputs['Color2'].default_value = (1.0, 0.86, 0.64, 1.0)  # 1.10/0.95/0.70 normalised to Blender 0-1 socket range
links.new(bg.outputs['Image'], gold.inputs['Color1'])

fg = nodes.new("CompositorNodeImage"); fg.name = "CharacterPlate_Untouched"; fg.location = (-800, -300)
fg.image = bpy.data.images.load(PLATE)
print("Plate size", list(fg.image.size))

scale = nodes.new("CompositorNodeScale"); scale.name = "Plate_Scale"; scale.location = (-550, -300)
scale.inputs['Type'].default_value = 'Relative'
scale.inputs['X'].default_value = 0.213
scale.inputs['Y'].default_value = 0.213
links.new(fg.outputs['Image'], scale.inputs['Image'])

trans = nodes.new("CompositorNodeTransform"); trans.name = "Plate_Translate"; trans.location = (-300, -300)
trans.inputs['X'].default_value = 0
trans.inputs['Y'].default_value = 10
links.new(scale.outputs['Image'], trans.inputs['Image'])

over = nodes.new("CompositorNodeAlphaOver"); over.name = "AlphaOver_BG_Plate"; over.location = (0, 0)
links.new(gold.outputs['Color'], over.inputs['Background'])
links.new(trans.outputs['Image'], over.inputs['Foreground'])

# Cyan back rim, separate layer: transformed plate alpha -> Dilate(3) - alpha
sep = nodes.new("CompositorNodeSeparateColor"); sep.name = "Plate_Alpha_Extract"; sep.location = (-300, -550)
links.new(trans.outputs['Image'], sep.inputs['Image'])
dil = nodes.new("CompositorNodeDilateErode"); dil.name = "Rim_Dilate3"; dil.location = (0, -550)
dil.inputs['Size'].default_value = 3
links.new(sep.outputs['Alpha'], dil.inputs['Mask'])
sub = nodes.new("ShaderNodeMath"); sub.name = "Rim_Subtract"; sub.location = (250, -550)
sub.operation = 'SUBTRACT'
links.new(dil.outputs['Mask'], sub.inputs[0])
links.new(sep.outputs['Alpha'], sub.inputs[1])
rim = nodes.new("ShaderNodeMixRGB"); rim.name = "CyanBackRim_Add"; rim.location = (500, -200)
rim.blend_type = 'ADD'
links.new(sub.outputs['Value'], rim.inputs['Factor'])
links.new(over.outputs['Image'], rim.inputs['Color1'])
rim.inputs['Color2'].default_value = (0.0, 0.784, 1.0, 1.0)  # cyan (0,200,255)

out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (800, 0)
links.new(over.outputs['Image'], out.inputs['Image'])

print("nodes:", [n.name for n in nodes])
print("links:", [(l.from_node.name, l.from_socket.name, l.to_node.name, l.to_socket.name) for l in links])
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("saved blend, rendering compositor...")
bpy.ops.render.render(write_still=True)
print("FINAL COMPOSITE DONE")
