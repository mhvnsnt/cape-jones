"""LANE 1 CAPE REBUILD — fast Workbench proof render.
Usage: blender -b <blend> --python cape_wb_render.py -- <outdir> <prefix> [frame]
Renders back + side + front at 480x360 Workbench (fast). Uses TRACK_TO aim."""
import bpy, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
outdir, prefix = argv[0], argv[1]
frame = int(argv[2]) if len(argv) > 2 else 1
os.makedirs(outdir, exist_ok=True)

sc = bpy.context.scene
sc.frame_set(frame)
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.resolution_x = 480
sc.render.resolution_y = 360
sc.render.film_transparent = False
sc.render.image_settings.file_format = 'PNG'
sc.display.shading.light = 'FLAT'
sc.display.shading.color_type = 'OBJECT'

cage = bpy.data.objects.get('BlenRigMdefCage')
if cage:
    cage.hide_render = True

body = bpy.data.objects.get('CapeJones_Body')
tx, ty, tz = 0, 0, 0.45
if body:
    ws = [body.matrix_world @ v.co for v in body.data.vertices]
    xs = [c.x for c in ws]; ys = [c.y for c in ws]; zs = [c.z for c in ws]
    tx, ty, tz = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2, (min(zs)+max(zs))/2

views = {'back': (0, 2.0, 0.55), 'side': (2.0, 0, 0.55), 'front': (0, -2.0, 0.55)}
aim = bpy.data.objects.new('wb_aim', None)
sc.collection.objects.link(aim)
aim.location = (tx, ty, tz)
for vname, vloc in views.items():
    cd = bpy.data.cameras.new(f'wb_{vname}')
    cam = bpy.data.objects.new(f'wb_{vname}', cd)
    sc.collection.objects.link(cam)
    cam.location = vloc
    con = cam.constraints.new('TRACK_TO')
    con.target = aim
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    cd.lens = 45
    sc.camera = cam
    bpy.context.view_layer.update()
    sc.render.filepath = os.path.join(outdir, f'{prefix}_{vname}.png')
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {sc.render.filepath}", flush=True)
print("DONE", flush=True)
