import bpy
s=bpy.context.scene
s.render.engine='CYCLES'
s.cycles.samples=24
s.cycles.device='CPU'
s.render.resolution_x=480; s.render.resolution_y=270; s.render.resolution_percentage=100
s.render.filepath='/home/hatch/workspace/cape-jones-rig/canonical-room-3d-2d-20261101/work/blender-render-maincam.png'
s.render.image_settings.file_format='PNG'
bpy.ops.render.render(write_still=True)
print("RENDERED")
