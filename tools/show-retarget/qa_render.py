"""QA render: Cape Jones show model, T-pose (rest), front + side, neutral studio.
Usage: blender -b <living_room.blend> --python qa_render.py -- <outdir>
Hides the room; shows only CapeJones_Rig + Body + Cape. Never saves the .blend."""
import bpy, sys, math
from mathutils import Vector

out = sys.argv[sys.argv.index("--") + 1:][0]

rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
cape = bpy.data.objects.get("CapeJones_Cape")
assert rig and body, "character objects missing"
keep = {rig.name, body.name, cape.name if cape else ""}

# reset to rest pose
if rig.animation_data:
    rig.animation_data.action = None
for b in rig.pose.bones:
    b.rotation_mode = 'QUATERNION'
    b.rotation_quaternion = (1, 0, 0, 0)
    b.location = (0, 0, 0)
bpy.context.view_layer.update()

# hide everything except the character
for o in bpy.data.objects:
    if o.name not in keep:
        o.hide_viewport = True
        o.hide_render = True

sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE_NEXT'
sc.render.resolution_x, sc.render.resolution_y = 960, 1280
sc.render.image_settings.file_format = 'PNG'
sc.eevee.taa_render_samples = 64
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.12, 0.12, 0.14, 1)

# key light
bpy.ops.object.light_add(type='SUN', location=(2, -3, 4))
sun = bpy.context.active_object
sun.data.energy = 3.0
bpy.ops.object.light_add(type='SUN', location=(-2, 3, 2))
fill = bpy.context.active_object
fill.data.energy = 0.8

def render_view(name, campos):
    camd = bpy.data.cameras.new(name)
    cam = bpy.data.objects.new(name, camd)
    sc.collection.objects.link(cam)
    cam.location = Vector(campos)
    look = Vector((0, 0, 0.48))
    cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Y').to_euler()
    camd.lens = 50
    sc.camera = cam
    sc.render.filepath = out.rstrip("/") + "/" + name
    bpy.ops.render.render(write_still=True)
    print("wrote", sc.render.filepath + ".png")

render_view("cape_tpose_front", (0.0, -2.6, 0.55))
render_view("cape_tpose_side", (2.6, 0.0, 0.55))
print("QA RENDER DONE")
