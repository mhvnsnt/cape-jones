"""Moving proof: a WH cast GLB playing a SHOW clip (anims/show/<char>/<clip>.glb) in Cape's living room.
blender -b 3d-assets/living_room.blend -P shared/cast/render_show_clip_in_room.py -- <model.glb> <clip.glb> <rotate_y_deg> <out_dir> '[x,y,z]' [frames] [engine] [frame_step]
Show clips only (ANIM-GATE: SHOW context). Never saves the .blend. Renders PNG frames; assemble with ffmpeg."""
import bpy, sys, math, json, mathutils
a = sys.argv[sys.argv.index("--")+1:]
model, clip, rot, out = a[0], a[1], float(a[2]), a[3]
target = mathutils.Vector(json.loads(a[4])) if len(a) > 4 else mathutils.Vector((1.2, 0.9, 0))
nframes = int(a[5]) if len(a) > 5 else 60
engine = a[6] if len(a) > 6 else 'BLENDER_EEVEE_NEXT'
step = int(a[7]) if len(a) > 7 else 1
def imp(p):
    b = set(bpy.data.objects); acts = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=p)
    return [o for o in bpy.data.objects if o not in b], [x for x in bpy.data.actions if x not in acts]
new, _ = imp(model)
arm = next(o for o in new if o.type == 'ARMATURE')
for o in new:
    if o.type == 'MESH' and not (o.parent and o.parent.type == 'ARMATURE'): o.hide_render = True
cnew, cacts = imp(clip)
act = cacts[0]
bones = {b.name for b in arm.data.bones}
paths = [fc.data_path for fc in act.fcurves]
bound = sum(1 for p in paths if p.startswith('pose.bones["') and p.split('"')[1] in bones)
for o in cnew: bpy.data.objects.remove(o, do_unlink=True)
print("BINDING", json.dumps({"clip": clip, "action": act.name, "bound_fcurves": bound, "total_fcurves": len(paths)}))
if bound < 8: raise SystemExit("binding gate: <8 bound tracks")
arm.animation_data_create(); arm.animation_data.action = act
sc = bpy.context.scene
f0, f1 = map(int, act.frame_range); sc.frame_start = f0; sc.frame_end = min(f1, f0 + nframes*step - 1); sc.frame_step = step; sc.render.fps = 30
sc.frame_set(f0)
roots = [o for o in new if o.parent is None]
dg = bpy.context.evaluated_depsgraph_get()
def bbox():
    dg.update(); mn = mathutils.Vector((1e9,)*3); mx = -mn
    for o in new:
        if o.type != 'MESH' or o.hide_render: continue
        e = o.evaluated_get(dg); me = e.to_mesh()
        for v in me.vertices:
            w = e.matrix_world @ v.co; mn = mathutils.Vector(map(min, mn, w)); mx = mathutils.Vector(map(max, mx, w))
        e.to_mesh_clear()
    return mn, mx
mn, mx = bbox(); s = 1.8 / (mx.z - mn.z)
for r in roots: r.scale = [v*s for v in r.scale]; r.rotation_mode = 'XYZ'; r.rotation_euler.z += math.radians(rot)
bpy.context.view_layer.update(); mn, mx = bbox(); c = (mn + mx) / 2
for r in roots: r.location += mathutils.Vector((target.x - c.x, target.y - c.y, target.z - mn.z))
cam = bpy.data.objects.new("showProofCam", bpy.data.cameras.new("showProofCam")); sc.collection.objects.link(cam)
look = target + mathutils.Vector((0, 0, 0.95)); cam.location = look + mathutils.Vector((-0.6, -4.6, 0.25)); cam.data.lens = 35
cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Y').to_euler(); sc.camera = cam
sc.render.engine = engine
if engine == 'CYCLES': sc.cycles.device = 'CPU'; sc.cycles.samples = 12; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 640, 360; sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = out.rstrip('/') + '/f_'
bpy.ops.render.render(animation=True)
