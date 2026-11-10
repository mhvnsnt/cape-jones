import bpy
import math

rrig = bpy.data.objects['recliner_rig']
pad = bpy.data.objects['recliner_footrest_pad']
pb_shank = rrig.pose.bones['footrest']
pb_pad = rrig.pose.bones['footrest_pad']
for d in rrig.animation_data.drivers:
    d.mute = True

def pad_bbox():
    bpy.context.view_layer.update()
    ws = [pad.matrix_world @ v.co for v in pad.data.vertices]
    return (min(v.x for v in ws), max(v.x for v in ws), min(v.z for v in ws), max(v.z for v in ws))

print("scan (pad world bbox under shank rotation phi, pad bone at 0):", flush=True)
best = None
for sign in (1, -1):
    for deg in range(15, 85, 5):
        phi = sign * math.radians(deg)
        pb_shank.rotation_euler.y = phi
        pb_pad.rotation_euler.y = 0.0
        x0, x1, z0, z1 = pad_bbox()
        ok = x0 >= 2.85 and z1 <= 0.26 and z0 >= 0.004
        print(f"  phi={phi:+.3f}: x {x0:.3f}..{x1:.3f} z {z0:.3f}..{z1:.3f} {'OK' if ok else ''}", flush=True)
        if ok and best is None:
            best = phi
    if best is not None:
        break
print("STOW =", best, flush=True)
