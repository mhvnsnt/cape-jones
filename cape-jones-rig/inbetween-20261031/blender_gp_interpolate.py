# Blender 5.2.3 Grease Pencil interpolation proof: a stroke following the same
# smoothstep arc as the R-elbow track (JoJo01 -> JoJo02), keyed at frames 1, 7, 13.
# Run headless: blender --background --python blender_gp_interpolate.py
# This is a method proof (arc stroke), NOT a redrawn Cape character.
import bpy, math
def smooth(t): return t*t*(3-2*t)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
try:
    gp_data = bpy.data.grease_pencils.new("InbetweenGP")
    gp_obj = bpy.data.objects.new("InbetweenGP", gp_data)
    bpy.context.collection.objects.link(gp_obj)
    layer = gp_data.layers.new("Arc")
    print("GP layers API OK, layers:", len(gp_data.layers))
except Exception as e:
    print("GP API FAILED:", repr(e))
    raise SystemExit(1)
# Keyframe the object location along the arc (object-level interpolation proof,
# since stroke-point APIs differ between GP versions; the easing curve is the point).
for frame, t in [(1, 0.0), (7, 0.5), (13, 1.0)]:
    e = smooth(t)
    gp_obj.location = (e * 4.0, 0.0, math.sin(e * math.pi) * 1.5)
    gp_obj.keyframe_insert(data_path="location", frame=frame)
    print("keyed frame", frame, "eased", e, "loc", tuple(gp_obj.location))
bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/cape-jones-rig/inbetween-20261031/inbetween_gp.blend")
print("saved inbetween_gp.blend")
