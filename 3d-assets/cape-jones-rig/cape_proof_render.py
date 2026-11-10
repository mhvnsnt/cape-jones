"""LANE 1 CAPE REBUILD — proof render script.
Renders front/side/back stills of the cape in the CURRENT state.
Call: blender -b <blend> --python cape_proof_render.py -- <outdir> <prefix> [frame]
Small res, EEVEE, simple 3-point light rig added to scene."""
import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
outdir = argv[0]
prefix = argv[1]
frame = int(argv[2]) if len(argv) > 2 else 1
os.makedirs(outdir, exist_ok=True)

sc = bpy.context.scene
sc.frame_set(frame)
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x = 640
sc.render.resolution_y = 480
sc.render.resolution_percentage = 100
sc.render.film_transparent = True
sc.render.image_settings.file_format = 'PNG'

# Hide the MDEF cage if present (clutter)
cage = bpy.data.objects.get('BlenRigMdefCage')
if cage:
    cage.hide_render = True
    cage.hide_viewport = True

body = bpy.data.objects.get('CapeJones_Body')
cape = bpy.data.objects.get('CapeJones_Cape')
target = (0, 0, 0.45)
if body:
    ws = [body.matrix_world @ v.co for v in body.data.vertices]
    xs = [c.x for c in ws]; ys = [c.y for c in ws]; zs = [c.z for c in ws]
    target = ((min(xs)+max(xs))/2, (min(ys)+max(ys))/2, (min(zs)+max(zs))/2)

# Simple camera views: (name, location offset direction)
views = {
    'front': (0, -2.2, 0.45),
    'side':  (2.2, 0, 0.45),
    'back':  (0, 2.2, 0.45),
    'threequarter': (1.6, -1.6, 0.9),
}

def aim(cam, loc, tgt):
    import math
    from mathutils import Vector
    d = Vector(tgt) - Vector(loc)
    # point -Z at target, Y up
    rot = d.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot.to_euler()

for vname, vloc in views.items():
    cam_data = bpy.data.cameras.new(f'proof_{vname}')
    cam = bpy.data.objects.new(f'proof_{vname}', cam_data)
    sc.collection.objects.link(cam)
    cam.location = vloc
    aim(cam, vloc, target)
    cam_data.lens = 50
    sc.camera = cam
    sc.render.filepath = os.path.join(outdir, f'{prefix}_{vname}.png')
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {sc.render.filepath}")

print("DONE")
