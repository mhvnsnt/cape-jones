import bpy, sys
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cape-jones-parking-lot-2d/brotheman/brotheman-rig.blend")
scene = bpy.context.scene
scene.render.filepath = "/home/hatch/workspace/_cape-jones-parking-lot-2d/brotheman/rest-f0001.png"
scene.frame_set(1)
bpy.ops.render.render(write_still=True)
print("RENDERED rest frame")
